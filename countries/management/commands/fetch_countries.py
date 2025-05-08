from django.core.management.base import BaseCommand
import requests
from countries.models import (
    Country, NativeName, Currency, Language,
    Translation, Demonym, IDD, CapitalInfo
)

class Command(BaseCommand):
    help = 'Fetch country data from restcountries.com and store in database'
    
    def handle(self, *args, **options):
        url = 'https://restcountries.com/v3.1/all'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            self.stdout.write(f"Fetched {len(data)} countries")
            
            for country_data in data:
                self.process_country(country_data)
            
            self.stdout.write(self.style.SUCCESS('Successfully fetched and stored country data'))
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Error fetching data: {e}'))
    
    def process_country(self, country_data):
        # Handle array fields by converting to comma-separated strings
        def to_csv(array_data):
            return ",".join(array_data) if array_data else None
        
        # Get basic data
        name_data = country_data.get('name', {})
        capital_data = country_data.get('capital', [])
        capital = capital_data[0] if capital_data else None
        
        # Create or update country
        country, created = Country.objects.update_or_create(
            cca2=country_data.get('cca2'),
            defaults={
                'common_name': name_data.get('common', ''),
                'official_name': name_data.get('official', ''),
                'cca3': country_data.get('cca3'),
                'ccn3': country_data.get('ccn3'),
                'cioc': country_data.get('cioc'),
                'fifa': country_data.get('fifa'),
                'independent': country_data.get('independent', False),
                'un_member': country_data.get('unMember', False),
                'status': country_data.get('status', ''),
                'region': country_data.get('region', ''),
                'subregion': country_data.get('subregion'),
                'continent': country_data.get('continents', [''])[0],
                'lat': country_data.get('latlng', [None])[0],
                'lng': country_data.get('latlng', [None, None])[1],
                'landlocked': country_data.get('landlocked', False),
                'area': country_data.get('area'),
                'capital': capital,
                'capital_lat': country_data.get('capitalInfo', {}).get('latlng', [None])[0],
                'capital_lng': country_data.get('capitalInfo', {}).get('latlng', [None, None])[1],
                'timezone': country_data.get('timezones', [''])[0],
                'population': country_data.get('population', 0),
                'gini': country_data.get('gini'),
                'flag_emoji': country_data.get('flag', ''),
                'flag_png': country_data.get('flags', {}).get('png', ''),
                'flag_svg': country_data.get('flags', {}).get('svg', ''),
                'flag_alt': country_data.get('flags', {}).get('alt'),
                'coat_of_arms_png': country_data.get('coatOfArms', {}).get('png'),
                'coat_of_arms_svg': country_data.get('coatOfArms', {}).get('svg'),
                'car_signs': to_csv(country_data.get('car', {}).get('signs', [])),
                'car_side': country_data.get('car', {}).get('side', 'right'),
                'tld': to_csv(country_data.get('tld', [])),
                'postal_code_format': country_data.get('postalCode', {}).get('format'),
                'postal_code_regex': country_data.get('postalCode', {}).get('regex'),
                'google_maps': country_data.get('maps', {}).get('googleMaps'),
                'openstreet_maps': country_data.get('maps', {}).get('openStreetMaps'),
                'borders': to_csv(country_data.get('borders', [])),
                'alt_spellings': to_csv(country_data.get('altSpellings', [])),
            }
        )
        
        # Process native names
        native_names = name_data.get('nativeName', {})
        for lang_code, names in native_names.items():
            NativeName.objects.update_or_create(
                country=country,
                language_code=lang_code,
                defaults={
                    'official': names.get('official', ''),
                    'common': names.get('common', ''),
                }
            )
        
        # Process currencies
        currencies = country_data.get('currencies', {})
        for code, currency_data in currencies.items():
            Currency.objects.update_or_create(
                country=country,
                code=code,
                defaults={
                    'name': currency_data.get('name', ''),
                    'symbol': currency_data.get('symbol'),
                }
            )
        
        # Process languages
        languages = country_data.get('languages', {})
        for code, name in languages.items():
            Language.objects.update_or_create(
                country=country,
                code=code,
                defaults={'name': name}
            )
        
        # Process translations
        translations = country_data.get('translations', {})
        for lang_code, translation_data in translations.items():
            Translation.objects.update_or_create(
                country=country,
                language_code=lang_code,
                defaults={
                    'official': translation_data.get('official', ''),
                    'common': translation_data.get('common', ''),
                }
            )
        
        # Process demonyms
        demonyms = country_data.get('demonyms', {})
        for lang_code, demonym_data in demonyms.items():
            Demonym.objects.update_or_create(
                country=country,
                language_code=lang_code,
                defaults={
                    'masculine': demonym_data.get('m'),
                    'feminine': demonym_data.get('f'),
                }
            )
        
        # Process IDD information
        idd_data = country_data.get('idd', {})
        if idd_data:
            IDD.objects.update_or_create(
                country=country,
                defaults={
                    'root': idd_data.get('root', ''),
                    'suffixes': to_csv(idd_data.get('suffixes', [])),
                }
            )
        
        # Process capital info
        capital_info = country_data.get('capitalInfo', {})
        if capital_info.get('latlng'):
            CapitalInfo.objects.update_or_create(
                country=country,
                defaults={
                    'lat': capital_info.get('latlng', [None])[0],
                    'lng': capital_info.get('latlng', [None, None])[1],
                }
            )