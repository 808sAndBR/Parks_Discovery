from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from parks_discovery.models import Park, ParkAttribute


class Command(BaseCommand):
    help = 'Ingests Park CSV content to create Park models.'

    def handle(self, *args, **options):
        for park in Park.objects.all():
            park_type = park.park_type
            neighborhood = park.neighborhood
            size = park.size
            attribute, created = ParkAttribute.objects.get_or_create(
                park = park,
                attribute = park_type)
            if created:
                self.stdout.write(self.style.SUCCESS('Successfully created park: "%s" attribute:%s' % (attribute.park.name, attribute.attribute)))
            else:
                self.stdout.write(self.style.SUCCESS('Park: "%s" attribute:%s, already exists' % (attribute.park.name, attribute.attribute)))

            attribute, created = ParkAttribute.objects.get_or_create(
                park = park,
                attribute = neighborhood)
            if created:
                self.stdout.write(self.style.SUCCESS('Successfully created park: "%s" attribute:%s' % (attribute.park.name, attribute.attribute)))
            else:
                self.stdout.write(self.style.SUCCESS('Park: "%s" attribute:%s, already exists' % (attribute.park.name, attribute.attribute)))

            attribute, created = ParkAttribute.objects.get_or_create(
                park = park,
                attribute = size)
            if created:
                self.stdout.write(self.style.SUCCESS('Successfully created park: "%s" attribute:%s' % (attribute.park.name, attribute.attribute)))
            else:
                self.stdout.write(self.style.SUCCESS('Park: "%s" attribute:%s, already exists' % (attribute.park.name, attribute.attribute)))
