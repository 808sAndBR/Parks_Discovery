from django.db import models


class Park(models.Model):
    name = models.CharField(db_index=True, max_length=200)
    park_type = models.CharField(max_length=200)
    park_service_area = models.CharField(max_length=200)
    psa_manager = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    acreage = models.FloatField()
    district = models.IntegerField(null=True)
    park_id = models.IntegerField(db_index=True, unique=True)
    address = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    size = models.CharField(max_length=200)
    neighborhood = models.CharField(max_length=200)


class ParkSimilarityRanking(models.Model):
    park = models.ForeignKey(Park, db_index=True)
    similar_park = models.ForeignKey(Park, related_name="parks")
    similarity_value = models.IntegerField(default=0)


class ParkAttribute(models.Model):
    park = models.ForeignKey(Park, db_index=True)
    attribute = models.CharField(max_length=200)
