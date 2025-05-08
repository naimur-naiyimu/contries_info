from django.contrib import admin
from .models import Country, NativeName, Currency, Language, Translation, Demonym, IDD, CapitalInfo

class CurrencyInline(admin.TabularInline):
    model = Currency
    extra = 0

class LanguageInline(admin.TabularInline):
    model = Language
    extra = 0

class CountryAdmin(admin.ModelAdmin):
    list_display = ('common_name', 'cca2', 'cca3', 'region', 'subregion', 'population')
    search_fields = ('common_name', 'official_name', 'cca2', 'cca3')
    list_filter = ('region', 'subregion', 'continent')  # Changed from 'continents' to 'continent'
    inlines = [CurrencyInline, LanguageInline]

admin.site.register(Country, CountryAdmin)
admin.site.register(NativeName)
admin.site.register(Translation)
admin.site.register(Demonym)
admin.site.register(IDD)
admin.site.register(CapitalInfo)