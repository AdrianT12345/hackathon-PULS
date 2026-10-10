import json
from django.core.management.base import BaseCommand
from mapa.models import Dzielnica


class Command(BaseCommand):
    help = 'Ładuje dane dzielnic z pliku Dzielnice.geojson do bazy danych'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='Dzielnice.geojson',
            help='Ścieżka do pliku GeoJSON (domyślnie: Dzielnice.geojson)'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        
        self.stdout.write(f'Ładowanie danych z pliku: {file_path}')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'Plik {file_path} nie został znaleziony!'))
            return
        except json.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f'Błąd parsowania JSON: {e}'))
            return
        
        features = data.get('features', [])
        self.stdout.write(f'Znaleziono {len(features)} dzielnic')
        
        created_count = 0
        updated_count = 0
        
        for feature in features:
            properties = feature.get('properties', {})
            geometry = feature.get('geometry', {})
            
            nazwa = properties.get('NAZWA', '')
            if not nazwa:
                self.stderr.write(self.style.WARNING('Pominięto feature bez nazwy'))
                continue
            
            dzielnica_data = {
                'geometry': geometry,
                'powierzchnia': properties.get('POWIERZCHN', 0.0),
                'obwod': properties.get('OBWOD', 0.0),
                'id_jednostki': properties.get('ID_JEDNOST', 0),
                'id_okregu': properties.get('ID_OKREGU_', 0),
            }
            
            dzielnica, created = Dzielnica.objects.update_or_create(
                dzielnica=nazwa,
                defaults=dzielnica_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  + Utworzono: {nazwa}'))
            else:
                updated_count += 1
                self.stdout.write(f'  ~ Zaktualizowano: {nazwa}')
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Zakończono! Utworzono: {created_count}, Zaktualizowano: {updated_count}'
        ))

