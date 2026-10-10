from django.contrib import admin
from .models import Note, Dzielnica, ZdarzenieSpoleczne


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'content']


@admin.register(Dzielnica)
class DzielnicaAdmin(admin.ModelAdmin):
    list_display = ['dzielnica', 'liczba_kobiet_display', 'liczba_mezczyzn_display', 'liczba_mieszkancow_display', 'powierzchnia']
    search_fields = ['dzielnica']
    ordering = ['dzielnica']
    
    def liczba_kobiet_display(self, obj):
        return obj.liczba_kobiet
    liczba_kobiet_display.short_description = 'Kobiety'
    
    def liczba_mezczyzn_display(self, obj):
        return obj.liczba_mezczyzn
    liczba_mezczyzn_display.short_description = 'Mężczyźni'
    
    def liczba_mieszkancow_display(self, obj):
        return obj.liczba_mieszkancow
    liczba_mieszkancow_display.short_description = 'Razem'


@admin.register(ZdarzenieSpoleczne)
class ZdarzenieSpoleczneAdmin(admin.ModelAdmin):
    list_display = ['id', 'tytul', 'kategoria2', 'data_utworzenia', 'like', 'dislike']
    list_filter = ['kategoria2', 'data_utworzenia']
    search_fields = ['tytul', 'opis']
    ordering = ['-data_utworzenia']
