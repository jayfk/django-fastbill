from django.core.management.base import BaseCommand, CommandError
from django_fastbill.helper import get_articles, get_article_by_number
from optparse import make_option


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--update-articles',
            action='store_true',
            dest='update-articles',
            default=False,
            help='Delete poll instead of closing it'),
        )

    def handle(self, *args, **options):
        if options["update-articles"]:
            print "updating all articles"
            get_articles()
            print "DONE"