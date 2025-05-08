from django.db import models
from django.db.models import JSONField

class Country(models.Model):
    # Basic Identification
    cca2 = models.CharField(max_length=2, primary_key=True)
    cca3 = models.CharField(max_length=3, unique=True)
    ccn3 = models.CharField(max_length=3, null=True, blank=True)
    
    # Names
    common_name = models.CharField(max_length=100)
    official_name = models.CharField(max_length=200)
    
    # Status
    independent = models.BooleanField(default=False)
    status = models.CharField(max_length=50)
    un_member = models.BooleanField(default=False)
    
    # Codes
    cioc = models.CharField(max_length=3, null=True, blank=True)
    fifa = models.CharField(max_length=3, null=True, blank=True)
    
    # Geography
    region = models.CharField(max_length=50)
    subregion = models.CharField(max_length=50, null=True, blank=True)
    continent = models.CharField(max_length=20)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    landlocked = models.BooleanField(default=False)
    area = models.FloatField(null=True, blank=True)
    
    # Capital
    capital = models.CharField(max_length=100, null=True, blank=True)
    capital_lat = models.FloatField(null=True, blank=True)
    capital_lng = models.FloatField(null=True, blank=True)
    
    # Time
    timezone = models.CharField(max_length=20)
    start_of_week = models.CharField(max_length=10, default='monday')
    
    # Demographics
    population = models.PositiveIntegerField()
    gini = JSONField(null=True, blank=True)
    
    # Flags
    flag_emoji = models.CharField(max_length=10)
    flag_png = models.URLField()
    flag_svg = models.URLField()
    flag_alt = models.TextField(null=True, blank=True)
    
    # Coat of Arms
    coat_of_arms_png = models.URLField(null=True, blank=True)
    coat_of_arms_svg = models.URLField(null=True, blank=True)
    
    # Transportation
    car_signs = models.CharField(max_length=100, null=True, blank=True)  # Comma-separated values
    car_side = models.CharField(
        max_length=10, 
        choices=[('left', 'Left'), ('right', 'Right')], 
        default='right'
    )
    
    # Internet
    tld = models.CharField(max_length=200, null=True, blank=True)  # Comma-separated values
    
    # Postal
    postal_code_format = models.CharField(max_length=100, null=True, blank=True)
    postal_code_regex = models.CharField(max_length=200, null=True, blank=True)
    
    # Maps
    google_maps = models.URLField(null=True, blank=True)
    openstreet_maps = models.URLField(null=True, blank=True)
    
    # Borders (comma-separated values)
    borders = models.CharField(max_length=500, null=True, blank=True)
    
    # Alternative spellings (comma-separated values)
    alt_spellings = models.CharField(max_length=500, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "countries"
        ordering = ['common_name']
    
    def __str__(self):
        return f"{self.common_name} ({self.cca2})"
    
    # Helper methods to handle comma-separated fields
    def get_car_signs(self):
        return self.car_signs.split(',') if self.car_signs else []
    
    def get_tlds(self):
        return self.tld.split(',') if self.tld else []
    
    def get_borders(self):
        return self.borders.split(',') if self.borders else []
    
    def get_alt_spellings(self):
        return self.alt_spellings.split(',') if self.alt_spellings else []


class NativeName(models.Model):
    country = models.ForeignKey(Country, related_name='native_names', on_delete=models.CASCADE)
    language_code = models.CharField(max_length=10)
    official = models.TextField()
    common = models.TextField()
    
    class Meta:
        unique_together = ('country', 'language_code')
        verbose_name_plural = "native names"
    
    def __str__(self):
        return f"{self.language_code} names for {self.country.cca2}"


class Currency(models.Model):
    country = models.ForeignKey(Country, related_name='currencies', on_delete=models.CASCADE)
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "currencies"
        unique_together = ('country', 'code')
    
    def __str__(self):
        return f"{self.code} ({self.country.cca2})"


class Language(models.Model):
    country = models.ForeignKey(Country, related_name='languages', on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('country', 'code')
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class Translation(models.Model):
    country = models.ForeignKey(Country, related_name='translations', on_delete=models.CASCADE)
    language_code = models.CharField(max_length=10)
    official = models.TextField()
    common = models.TextField()
    
    class Meta:
        unique_together = ('country', 'language_code')
    
    def __str__(self):
        return f"{self.language_code} translation of {self.country.cca2}"


class Demonym(models.Model):
    country = models.ForeignKey(Country, related_name='demonyms', on_delete=models.CASCADE)
    language_code = models.CharField(max_length=10)
    masculine = models.CharField(max_length=50, null=True, blank=True)
    feminine = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        unique_together = ('country', 'language_code')
    
    def __str__(self):
        return f"{self.language_code} demonyms for {self.country.cca2}"


class IDD(models.Model):
    country = models.OneToOneField(Country, related_name='idd', on_delete=models.CASCADE)
    root = models.CharField(max_length=5)
    suffixes = models.CharField(max_length=200, null=True, blank=True)  # Comma-separated values
    
    class Meta:
        verbose_name = "International Direct Dialing"
        verbose_name_plural = "IDD information"
    
    def __str__(self):
        return f"IDD for {self.country.cca2}"
    
    def get_suffixes(self):
        return self.suffixes.split(',') if self.suffixes else []


class CapitalInfo(models.Model):
    country = models.OneToOneField(Country, related_name='capital_info', on_delete=models.CASCADE)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "capital info"
    
    def __str__(self):
        return f"Capital info for {self.country.cca2}"