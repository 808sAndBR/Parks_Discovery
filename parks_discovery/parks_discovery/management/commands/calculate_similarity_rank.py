from numpy import dot
from math import sqrt
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from parks_discovery.models import Park, ParkAttribute, ParkSimilarityRanking


class Command(BaseCommand):
    help = 'Calculate the similarity.'

    def cosine_similarity(self, v,w):
        return dot(v,w) / sqrt(dot(v,v) * dot(w,w))

    def make_park_att(self, attributes, possible):
        vec =[]
        for attribute in possible:
            if attribute in attributes:
                vec.append(1)
            else:
                vec.append(0)
        return vec

    def most_similar_parks(self, park_row, park_similarities):
        pairs = []
        for other_park_row, similarity in \
            enumerate(park_similarities[park_row]):
                if similarity > 0 and other_park_row != park_row:
                    pairs.append((other_park_row, similarity))
        return sorted(pairs, key = lambda similar:similar[1], reverse = True)

    def handle(self, *args, **options):
        possible_attributes = ParkAttribute.objects.all().values_list("attribute", flat=True).distinct()

        attribute_matrix =[]
        for park in Park.objects.all():
            attributes = ParkAttribute.objects.filter(park=park).values_list("attribute", flat=True)
            attribute_matrix.append(self.make_park_att(attributes, possible_attributes))


        park_similarities = []

        for x in attribute_matrix:
            sim_row = []
            for y in attribute_matrix:
                sim_row.append(self.cosine_similarity(x,y))
            park_similarities.append(sim_row)


        for num, park in enumerate(Park.objects.all()):
            for sim in self.most_similar_parks(num, park_similarities):
                similar_park = Park.objects.all()[sim[0]]
                similarity_value = sim[1]
                similarity, created = ParkSimilarityRanking.objects.get_or_create(
                    park = park,
                    similar_park = similar_park,
                    similarity_value = similarity_value)

                if created:
                    self.stdout.write(self.style.SUCCESS(
                        'Sim created: park: "%s" similar_park: %s sim value: %s' % (park.name, similar_park.name, similarity_value)))

                else:
                    self.stdout.write(self.style.SUCCESS(
                        'Sim already exists: park: "%s" similar_park: %s sim value: %s' % (park.name, similar_park.name, similarity_value)))








