from django.shortcuts import render, get_object_or_404, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Country, Language
from .serializers import CountrySerializer
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.db.models import Q

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = AuthenticationForm

@login_required
def get_auth_token(request):
    token, created = Token.objects.get_or_create(user=request.user)
    return JsonResponse({'token': token.key})

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 
    lookup_field = 'cca2'
    

    @action(detail=True, methods=['get'], url_path='regional')
    def regional(self, request, cca2=None):
        """List same regional countries of a specific country"""
        country = self.get_object()
        regional_countries = Country.objects.filter(
            region=country.region
        ).exclude(cca2=cca2)
        serializer = self.get_serializer(regional_countries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_language(self, request):
        """List countries that speak the same language"""
        language_code = request.query_params.get('language')
        if not language_code:
            return Response(
                {"error": "Language code parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        countries = Country.objects.filter(languages__code=language_code)
        serializer = self.get_serializer(countries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search for a country by name (supports partial search)"""
        query = request.query_params.get('q')
        if not query:
            return Response(
                {"error": "Search query parameter 'q' is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        countries = Country.objects.filter(
            Q(common_name__icontains=query) |
            Q(official_name__icontains=query) |
            Q(alt_spellings__icontains=query)
        )
        serializer = self.get_serializer(countries, many=True)
        return Response(serializer.data)

@login_required
def country_list(request):
    query = request.GET.get('q', '').strip()
    countries = Country.objects.filter(common_name__icontains=query) if query else Country.objects.all()
    return render(request, 'countries/country_list.html', {'countries': countries})

@login_required
def country_detail(request, cca2):
    country = get_object_or_404(Country, cca2=cca2)
    regional_countries = Country.objects.filter(region=country.region).exclude(cca2=cca2)
    languages = Language.objects.filter(country=country)
    return render(request, 'countries/country_detail.html', {
        'country': country,
        'regional_countries': regional_countries,
        'languages': languages
    })
    
