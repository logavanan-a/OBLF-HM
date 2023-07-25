from django.core.management.base import BaseCommand
from health_management.response_mail import *
# from OBLH_HM.settings import TEMPLATE_DIRS,BASE_DIR
# from health_management.management.commands.materialized_view_refresh import refresh_materialized_view


class Command(BaseCommand):

    help = 'Runs cron for sending mail on survey reponses'

    # C def add_arguments(self, parser):
    # C    parser.add_argument('poll_id', nargs='+', type=int)

    @staticmethod
    def handle(*args, **options):
        survey_responses()
        # refresh_materialized_view()
        # attachment_email()
