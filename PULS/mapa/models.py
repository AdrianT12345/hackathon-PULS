from django.db import models
from django.utils import timezone


class Note(models.Model):
    content = models.TextField()


class ZdarzenieSpoleczne(models.Model):
    KATEGORIA2_CHOICES = [
        ('zgloszenie', 'Zgłoszenie'),
        ('wydarzenie', 'Wydarzenie'),
    ]
    
    # Kategorie dla zgłoszeń
    ZGLOSZENIE_CHOICES = [
        ('roboty_drogowe', 'Roboty drogowe'),
        ('wypadek_drogowy', 'Wypadek na drodze'),
        ('wypadek_ludzki', 'Wypadek ludzki'),
        ('korek', 'Korek'),
        ('pozar', 'Pożar'),
        ('zagrozenie', 'Zagrożenie'),
        ('zle_parkowanie', 'Złe parkowanie'),
        ('bezdomny', 'Bezdomny'),
        ('wandalizm', 'Wandalizm'),
    ]
    
    # Kategorie dla wydarzeń
    WYDARZENIE_CHOICES = [
        ('sportowe', 'Wydarzenie sportowe'),
        ('hobbystyczne', 'Wydarzenie hobbystyczne'),
        ('dla_dzieci', 'Wydarzenie dla dzieci'),
        ('akcja_spoleczna', 'Akcja społeczna'),
        ('kulturowe', 'Wydarzenie kulturowe'),
        ('religijne', 'Wydarzenie religijne'),
        ('muzyczne', 'Wydarzenie muzyczne'),
    ]
    
    KATEGORIA3_CHOICES = ZGLOSZENIE_CHOICES + WYDARZENIE_CHOICES
    
    lokalizacja_lat = models.FloatField(verbose_name="Szerokość geograficzna")
    lokalizacja_lng = models.FloatField(verbose_name="Długość geograficzna")
    dzielnica = models.ForeignKey(
        'Dzielnica', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Dzielnica",
        related_name="zdarzenia"
    )
    kategoria = models.CharField(max_length=50, default='spolecznosc', verbose_name="Kategoria")
    kategoria2 = models.CharField(max_length=50, choices=KATEGORIA2_CHOICES, verbose_name="Typ zdarzenia")
    kategoria3 = models.CharField(max_length=100, choices=KATEGORIA3_CHOICES, blank=True, default='', verbose_name="Podkategoria")
    tytul = models.CharField(max_length=200, verbose_name="Tytuł")
    opis = models.TextField(verbose_name="Opis")
    like = models.IntegerField(default=0, verbose_name="Polubienia")
    dislike = models.IntegerField(default=0, verbose_name="Nie lubię")
    data_utworzenia = models.DateTimeField(default=timezone.now, verbose_name="Data utworzenia")
    termin_od = models.DateTimeField(null=True, blank=True, verbose_name="Termin od")
    termin_do = models.DateTimeField(null=True, blank=True, verbose_name="Termin do")
    min_wiek = models.PositiveIntegerField(default=0, verbose_name="Minimalny wiek")
    dla_niepelnosprawnych = models.BooleanField(default=False, verbose_name="Dostosowane dla niepełnosprawnych")
    
    class Meta:
        verbose_name = "Zdarzenie społeczne"
        verbose_name_plural = "Zdarzenia społeczne"
        ordering = ['-data_utworzenia']
    
    def __str__(self):
        return f"{self.tytul} ({self.get_kategoria2_display()})"


class Komentarz(models.Model):
    zdarzenie = models.ForeignKey(
        ZdarzenieSpoleczne,
        on_delete=models.CASCADE,
        related_name='komentarze',
        verbose_name="Zdarzenie"
    )
    autor = models.CharField(max_length=100, default='Anonim', verbose_name="Autor")
    tresc = models.TextField(verbose_name="Treść")
    data_utworzenia = models.DateTimeField(default=timezone.now, verbose_name="Data utworzenia")
    
    class Meta:
        verbose_name = "Komentarz"
        verbose_name_plural = "Komentarze"
        ordering = ['-data_utworzenia']
    
    def __str__(self):
        return f"Komentarz do {self.zdarzenie.tytul} - {self.autor}"



class Dzielnica(models.Model):
    
    dzielnica = models.CharField(max_length=100, primary_key=True, verbose_name="Nazwa dzielnicy")
    geometry = models.JSONField(verbose_name="Geometria (współrzędne)")
    powierzchnia = models.FloatField(default=0.0, verbose_name="Powierzchnia (km²)")
    obwod = models.FloatField(default=0.0, verbose_name="Obwód")
    id_jednostki = models.IntegerField(default=0, verbose_name="ID jednostki")
    id_okregu = models.IntegerField(default=0, verbose_name="ID okręgu")
    
    # Demografia - kobiety (3 grupy wiekowe)
    kobiety_mlodzi = models.IntegerField(default=0, verbose_name="Kobiety - młodzi")
    kobiety_dorosli = models.IntegerField(default=0, verbose_name="Kobiety - dorośli")
    kobiety_seniorzy = models.IntegerField(default=0, verbose_name="Kobiety - seniorzy")
    
    # Demografia - mężczyźni (3 grupy wiekowe)
    mezczyzni_mlodzi = models.IntegerField(default=0, verbose_name="Mężczyźni - młodzi")
    mezczyzni_dorosli = models.IntegerField(default=0, verbose_name="Mężczyźni - dorośli")
    mezczyzni_seniorzy = models.IntegerField(default=0, verbose_name="Mężczyźni - seniorzy")
    
    class Meta:
        verbose_name = "Dzielnica"
        verbose_name_plural = "Dzielnice"
        ordering = ['dzielnica']
    
    def __str__(self):
        return self.dzielnica
    
    @property
    def liczba_kobiet(self):
        return self.kobiety_mlodzi + self.kobiety_dorosli + self.kobiety_seniorzy
    
    @property
    def liczba_mezczyzn(self):
        return self.mezczyzni_mlodzi + self.mezczyzni_dorosli + self.mezczyzni_seniorzy
    
    @property
    def liczba_mieszkancow(self):
        return self.liczba_kobiet + self.liczba_mezczyzn
    
    def to_geojson_feature(self):
        return {
            "type": "Feature",
            "properties": {
                "nazwa": self.dzielnica,
                "liczba_mieszkancow": self.liczba_mieszkancow,
                "liczba_kobiet": self.liczba_kobiet,
                "liczba_mezczyzn": self.liczba_mezczyzn,
                "kobiety_mlodzi": self.kobiety_mlodzi,
                "kobiety_dorosli": self.kobiety_dorosli,
                "kobiety_seniorzy": self.kobiety_seniorzy,
                "mezczyzni_mlodzi": self.mezczyzni_mlodzi,
                "mezczyzni_dorosli": self.mezczyzni_dorosli,
                "mezczyzni_seniorzy": self.mezczyzni_seniorzy,
                "powierzchnia": self.powierzchnia,
                "obwod": self.obwod,
                "id_jednostki": self.id_jednostki,
                "id_okregu": self.id_okregu,
            },
            "geometry": self.geometry
        }