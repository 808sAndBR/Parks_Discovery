import csv

from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError

from parks_discovery.models import Park, ParkAttribute

class Command(BaseCommand):
    help = 'Ingests features CSV content to Park Attribute DB.'

    def add_arguments(self, parser):
        parser.add_argument('--filepath')

    def handle(self, *args, **options):
        filepath = options['filepath']

        with open(filepath, 'r') as park_file:
            reader = csv.DictReader(park_file)
            for row in reader:
                park_ob = Park.objects.filter(name =row['ParkName'].title())[0]
                attribute, created = ParkAttribute.objects.get_or_create(
                    park=park_ob,
                    attribute=row['Feature'])
                if created:
                    self.stdout.write(self.style.SUCCESS('Successfully created park: "%s" attribute:%s' % (
                        attribute.park.name, attribute.attribute)))
                else:
                    self.stdout.write(self.style.SUCCESS('Park: "%s" attribute:%s, already exists' % (
                        attribute.park.name, attribute.attribute)))
