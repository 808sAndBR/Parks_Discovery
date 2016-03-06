from django.http import HttpResponse
from django.template import loader

from .models import Park, ParkSimilarityRanking


def index(request):
    template = loader.get_template('index.html')
    parks = Park.objects.all().values('name', 'latitude', 'longitude')
    context = {
        'parks': parks,
    }
    return HttpResponse(template.render(context, request))

def similar_parks(request, pid):
    template = loader.get_template('similar_parks.html')
    park = Park.objects.get(id=pid)
    park_dict = {'name': park.name, 'latitude': park.latitude, 'longitude': park.longitude}
    similar_parks = ParkSimilarityRanking.objects.filter(park=park).order_by('similarity_value').values('similar_park','similar_park__name', 'similar_park__latitude', 'similar_park__longitude')[:5]
    parks = [{'name': park['similar_park__name'], 'latitude': park['similar_park__latitude'], 'longitude': park['similar_park__longitude']} for park in similar_parks]
    context = {
        'park': park_dict,
        'similar_parks': parks
    }
    return HttpResponse(template.render(context, request))
