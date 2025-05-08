from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet, country_list, country_detail

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='country')

# API endpoints
urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]

# Move HTML views to a different namespace to avoid path conflicts
urlpatterns += [
    path('web/', country_list, name='country-list'),
    path('web/countries/<str:cca2>/', country_detail, name='country-detail'),
]
