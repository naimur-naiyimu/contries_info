from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Country, Language
from .serializers import CountrySerializer
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.db.models import Q


def country_list(request):
    query = request.GET.get('q', '').strip()
    countries = Country.objects.filter(common_name__icontains=query) if query else Country.objects.all()
    return render(request, 'countries/country_list.html', {'countries': countries})


def country_detail(request, cca2):
    country = get_object_or_404(Country, cca2=cca2)
    regional_countries = Country.objects.filter(region=country.region).exclude(cca2=cca2)
    languages = Language.objects.filter(country=country)
    return render(request, 'countries/country_detail.html', {
        'country': country,
        'regional_countries': regional_countries,
        'languages': languages
    })
    
