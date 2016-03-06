from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .forms import ParkSearchForm
from .models import Park, ParkSimilarityRanking


def index(request):
    if request.method == 'POST':
        form = ParkSearchForm(request.POST)
        if form.is_valid():
            park_name = form.cleaned_data['park_name']
            park_id = Park.objects.get(name=park_name).id
            return HttpResponseRedirect('/park/%d' % park_id)
    else:
        form = ParkSearchForm()

    template = loader.get_template('index.html')
    parks = Park.objects.all().values('name', 'latitude', 'longitude')
    context = {
        'parks': parks,
        'form': form
    }
    return HttpResponse(template.render(context, request))


def similar_parks(request, pid):
    template = loader.get_template('similar_parks.html')
    park = Park.objects.get(id=pid)
    park_dict = {
        'name': park.name, 'latitude': park.latitude,
        'longitude': park.longitude}
    similar_parks = ParkSimilarityRanking.objects.filter(park=park).order_by('similarity_value').values(
        'similar_park', 'similar_park__name', 'similar_park__latitude', 'similar_park__longitude')[:5]
    parks = [{'name': park['similar_park__name'], 'latitude': park[
        'similar_park__latitude'], 'longitude': park['similar_park__longitude']}
        for park in similar_parks]
    context = {
        'park': park_dict,
        'similar_parks': parks
    }
    return HttpResponse(template.render(context, request))
