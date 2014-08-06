from django.db.models import Manager, BooleanField, NullBooleanField, FieldDoesNotExist
from .exceptions import ConvertError
from django.core.exceptions import ObjectDoesNotExist
import logging
from fastbill import FastbillWrapper
from django.conf import settings
from django.utils import timezone
from datetime import datetime

logger = logging.getLogger(__name__)


def convert_to_aware_datetime(timestamp):
    """

    :param timestamp:
    :return:
    """
    if timestamp in ["0000-00-00 00:00:00", "", "0000-00-00"]:
        return None

    try:
        # fastbill uses UTC in timestamps
        date = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    except ValueError, e:
        date = datetime.strptime(timestamp, '%Y-%m-%d')

    utc = timezone.pytz.timezone("UTC")

    return utc.localize(date)


class FastBillApiManager(Manager):
    """

    """
    def update_or_create(self, api_item):
        """

        :param api_item:
        :return:
        """
        pk = self.model._meta.pk.name

        try:
            pk_value = api_item[pk.upper()]
        except KeyError:
            raise ConvertError("Error during conversion of %s: Could not find %s in API item" % (self.model.__name__,
                                                                                                 pk))

        # try to load this thing by identifier from DB
        created = False
        try:
            obj = self.get(pk=pk_value)
        except ObjectDoesNotExist:
            # does not exist, create a new object
            obj = self.model(pk=pk_value)
            created = True

        # loop the api_item and set the values
        for key, value in api_item.iteritems():
            # lower the key, because fastbills responses are SHOUTED :)
            key = key.lower()

            # get the field type if we need to do some casting
            try:
                field_class = self.model._meta.get_field(key)
                field_nullable = field_class.null
                field_type = field_class.get_internal_type()
            except FieldDoesNotExist:
                #logger.debug("%s has no mapping field on %s, skipping" % (key, self.model.__name__))
                continue

            # we might need to do some basic type casting. If we fail raise a ConvertError
            try:
                # FastBill gives us boolean values as strings. That leads to problems for BooleanFields because
                # bool("0") = True. Workaround cast the string to int to convert it to a bool.
                if field_type in ["BooleanField", "NullBooleanField"]:
                    value = bool(int(value))
                # integer and floats get casted by django itself. We cast them "by hand" nonetheless because that
                # makes it easier to handle the returned object later on
                elif field_type == "IntegerField":
                    value = None if field_nullable and value == "" else int(value)
                elif field_type == "FloatField":
                    value = None if field_nullable and value == "" else float(value)
                elif field_type == "DateTimeField":
                    # convert to local time
                    value = convert_to_aware_datetime(value)
                    if not field_nullable and value is None:
                        raise ConvertError("Failed to extract datetime for not nullable field %s" % key)

            except (ValueError,) as e:
                raise ConvertError("Could not convert %s on %s, value: %s. Error: %s" % (key, self.model.__name__,
                                   value, e))

            # finally set the attr
            obj.__setattr__(key, value)

        obj.save()

        return created, obj