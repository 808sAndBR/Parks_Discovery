from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import simplejson

from .forms import ParkSearchForm
from .models import Park, ParkSimilarityRanking


def index(request):
    # if request.method == 'POST':
    #     form = ParkSearchForm(request.POST)
    #     if form.is_valid():
    #         park_name = form.cleaned_data['park_name']
    #         park = Park.objects.filter(name=park_name).first()
    #         if park is not None:
    #             park_id = park.id
    #             return HttpResponseRedirect('/park/%d' % park_id)
    # else:
    #     form = ParkSearchForm()
    template = loader.get_template('index.html')
    parks = Park.objects.all().values('name', 'latitude', 'longitude')
    context = {
        'parks': parks,
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


def search_similar_parks(request):
    if request.method == 'POST':
        name = request.POST.get("park_name")
        if name == "" or name is None:
            all_parks = Park.objects.all()
            parks = [{'name': park.name, 'latitude': park.latitude, 'longitude': park.longitude}
                for park in all_parks]
            results = {
                'park': None,
                'similar_parks': parks
            }
        else:
            park = Park.objects.get(name=name)
            park_dict = {
                'name': park.name, 'latitude': park.latitude,
                'longitude': park.longitude}
            similar_parks = ParkSimilarityRanking.objects.filter(park=park).order_by('similarity_value').values(
                'similar_park', 'similar_park__name', 'similar_park__latitude', 'similar_park__longitude')[:5]
            parks = [{'name': park['similar_park__name'], 'latitude': park[
                'similar_park__latitude'], 'longitude': park['similar_park__longitude']}
                for park in similar_parks]
            results = {
                'park': park_dict,
                'similar_parks': parks
            }
        data = simplejson.dumps(results)
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)
    else:
        return None


def autofill_parks(request):
    if request.is_ajax():
        query = request.GET.get('term', '')
        parks = Park.objects.filter(name__icontains=query)[:10]
        results = []
        for park in parks:
            park_json = {}
            park_json['id'] = park.id
            park_json['label'] = park.name
            park_json['value'] = park.name
            results.append(park_json)
        data = simplejson.dumps(results)
    else:
        raise Exception("Error making parks autofill request.")
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
