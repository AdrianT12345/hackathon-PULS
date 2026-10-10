import random
from django.core.management.base import BaseCommand
from mapa.models import ZdarzenieSpoleczne, Dzielnica

class Command(BaseCommand):
    help = 'Generuje losowe zdarzenia społeczne w dzielnicach'

    def handle(self, *args, **options):
        # Pobierz wszystkie dzielnice
        dzielnice = list(Dzielnica.objects.all())
        
        if not dzielnice:
            self.stdout.write(self.style.ERROR('Brak dzielnic w bazie danych!'))
            return
        
        # Kategorie zgłoszeń
        zgloszenia = [
            ('roboty_drogowe', 'Roboty drogowe na ulicy', 'Trwają prace remontowe, możliwe utrudnienia w ruchu.'),
            ('wypadek_drogowy', 'Kolizja samochodowa', 'Doszło do kolizji dwóch pojazdów, służby na miejscu.'),
            ('korek', 'Duży korek', 'Znaczne utrudnienia w ruchu, zalecam objazd.'),
            ('pozar', 'Pożar kontenera', 'Straż pożarna interweniuje przy pożarze śmietnika.'),
            ('zagrozenie', 'Uszkodzone drzewo', 'Drzewo grozi przewróceniem, niebezpieczeństwo dla przechodniów.'),
            ('zle_parkowanie', 'Źle zaparkowany samochód', 'Auto blokuje chodnik i utrudnia przejście.'),
            ('wandalizm', 'Zniszczona ławka', 'Ktoś zniszczył ławkę w parku, wymaga naprawy.'),
            ('bezdomny', 'Osoba potrzebująca pomocy', 'Przy przystanku śpi osoba bezdomna, wymaga wsparcia.'),
        ]
        
        # Kategorie wydarzeń
        wydarzenia = [
            ('sportowe', 'Turniej piłki nożnej', 'Zapraszamy na lokalny turniej dla amatorów!'),
            ('sportowe', 'Poranny jogging', 'Wspólne bieganie w parku, start o 7:00.'),
            ('hobbystyczne', 'Spotkanie miłośników gier', 'Planszówki i gry karciane dla wszystkich.'),
            ('hobbystyczne', 'Wymiana książek', 'Przynieś książkę, zabierz inną!'),
            ('dla_dzieci', 'Festyn dla dzieci', 'Dmuchańce, konkursy i słodycze dla najmłodszych.'),
            ('dla_dzieci', 'Warsztaty plastyczne', 'Bezpłatne zajęcia dla dzieci 5-12 lat.'),
            ('akcja_spoleczna', 'Sprzątanie parku', 'Wspólna akcja sprzątania okolicy.'),
            ('akcja_spoleczna', 'Zbiórka darów', 'Zbieramy ubrania i żywność dla potrzebujących.'),
            ('kulturowe', 'Wystawa fotografii', 'Fotografie starego Gdańska w bibliotece.'),
            ('kulturowe', 'Spotkanie z pisarzem', 'Promocja nowej książki o historii miasta.'),
            ('religijne', 'Koncert chóru', 'Występ chóru parafialnego w kościele.'),
            ('muzyczne', 'Koncert w parku', 'Muzyka na żywo pod chmurką!'),
            ('muzyczne', 'Jam session', 'Otwarte spotkanie muzyków, instrumenty mile widziane.'),
        ]
        
        # Generuj losowe zdarzenia
        created_count = 0
        max_zdarzenia = 40
        
        for i in range(max_zdarzenia):
            dzielnica = random.choice(dzielnice)
            
            # Losowe współrzędne w obrębie dzielnicy (przybliżone)
            # Bazowe współrzędne Gdańska + losowe przesunięcie
            base_lat = 54.35 + random.uniform(-0.08, 0.08)
            base_lng = 18.60 + random.uniform(-0.15, 0.15)
            
            # Losuj czy zgłoszenie czy wydarzenie
            if random.random() < 0.5:
                # Zgłoszenie
                kat3, tytul, opis = random.choice(zgloszenia)
                kategoria2 = 'zgloszenie'
            else:
                # Wydarzenie
                kat3, tytul, opis = random.choice(wydarzenia)
                kategoria2 = 'wydarzenie'
            
            # Dodaj numer do tytułu żeby były unikalne
            tytul = f"{tytul} #{i+1}"
            
            # Losowe like'i 0-10
            likes = random.randint(0, 10)
            dislikes = random.randint(0, 3)
            
            zdarzenie = ZdarzenieSpoleczne.objects.create(
                lokalizacja_lat=base_lat,
                lokalizacja_lng=base_lng,
                dzielnica=dzielnica,
                kategoria='spolecznosc',
                kategoria2=kategoria2,
                kategoria3=kat3,
                tytul=tytul,
                opis=opis,
                like=likes,
                dislike=dislikes,
            )
            
            created_count += 1
            self.stdout.write(f"Utworzono: {zdarzenie.tytul} w {dzielnica.dzielnica} (👍 {likes})")
        
        self.stdout.write(self.style.SUCCESS(f'\nUtworzono {created_count} zdarzeń!'))


