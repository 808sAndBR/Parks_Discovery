from django.http import HttpResponse
from django.template import loader

from .models import Park


def index(request):
    template = loader.get_template('index.html')
    parks = Park.objects.all().values('name', 'latitude', 'longitude')
    context = {
        'parks': parks,
    }
    return HttpResponse(template.render(context, request))