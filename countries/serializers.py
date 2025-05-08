from rest_framework import serializers
from .models import Country, Currency, Language, Translation, Demonym

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = '__all__'

class DemonymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demonym
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    currencies = CurrencySerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    translations = TranslationSerializer(many=True, read_only=True)
    demonyms = DemonymSerializer(many=True, read_only=True)
    
    class Meta:
        model = Country
        fields = '__all__'
        depth = 1