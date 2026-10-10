from django.core.management.base import BaseCommand
from mapa.models import Dzielnica

# Dane demograficzne: dzielnica -> (kobiety: [mlodzi, dorosli, seniorzy], mezczyzni: [mlodzi, dorosli, seniorzy])
DEMOGRAFIA_DATA = {
    "Aniołki": {"kobiety": [288, 1128, 153], "mezczyzni": [323, 1083, 133]},
    "Brętowo": {"kobiety": [481, 1893, 171], "mezczyzni": [577, 1835, 152]},
    "Brzeźno": {"kobiety": [658, 2760, 415], "mezczyzni": [673, 2602, 336]},
    "Chełm": {"kobiety": [2501, 8319, 673], "mezczyzni": [2587, 7687, 474]},
    "Jasień": {"kobiety": [3312, 7993, 454], "mezczyzni": [3471, 7242, 369]},
    "Kokoszki": {"kobiety": [1218, 2998, 279], "mezczyzni": [1289, 2950, 224]},
    "Krakowiec–Górki Zachodnie": {"kobiety": [138, 441, 48], "mezczyzni": [161, 431, 35]},
    "Letnica": {"kobiety": [347, 1030, 49], "mezczyzni": [369, 916, 46]},
    "Matarnia": {"kobiety": [519, 1721, 259], "mezczyzni": [614, 1505, 187]},
    "Młyniska": {"kobiety": [102, 572, 77], "mezczyzni": [124, 583, 91]},
    "Nowy Port": {"kobiety": [532, 2193, 197], "mezczyzni": [631, 2152, 208]},
    "Oliwa": {"kobiety": [1025, 3707, 445], "mezczyzni": [998, 3583, 376]},
    "Olszynka": {"kobiety": [227, 755, 86], "mezczyzni": [240, 736, 71]},
    "Orunia Górna–Gdańsk Południe": {"kobiety": [2526, 7740, 522], "mezczyzni": [2639, 6693, 418]},
    "Orunia–Św. Wojciech–Lipce": {"kobiety": [892, 3370, 429], "mezczyzni": [991, 3366, 374]},
    "Osowa": {"kobiety": [1572, 4813, 412], "mezczyzni": [1744, 4294, 346]},
    "Piecki–Migowo": {"kobiety": [2942, 8155, 487], "mezczyzni": [3128, 7534, 368]},
    "Przeróbka": {"kobiety": [207, 862, 115], "mezczyzni": [227, 943, 105]},
    "Przymorze Małe": {"kobiety": [1079, 3900, 495], "mezczyzni": [1085, 3584, 406]},
    "Przymorze Wielkie": {"kobiety": [1297, 6074, 792], "mezczyzni": [1392, 5710, 769]},
    "Rudniki": {"kobiety": [68, 243, 37], "mezczyzni": [76, 240, 30]},
    "Siedlce": {"kobiety": [861, 3325, 330], "mezczyzni": [1000, 3050, 262]},
    "Stogi": {"kobiety": [515, 2449, 390], "mezczyzni": [591, 2289, 354]},
    "Strzyża": {"kobiety": [412, 1262, 141], "mezczyzni": [414, 1213, 125]},
    "Suchanino": {"kobiety": [611, 2393, 253], "mezczyzni": [652, 2375, 224]},
    "Śródmieście": {"kobiety": [1460, 6257, 739], "mezczyzni": [1557, 5908, 652]},
    "Ujeścisko–Łostowice": {"kobiety": [3034, 9241, 607], "mezczyzni": [3276, 8278, 460]},
    "VII Dwór": {"kobiety": [176, 1133, 116], "mezczyzni": [194, 930, 100]},
    "Wrzeszcz Dolny": {"kobiety": [1538, 5789, 679], "mezczyzni": [1585, 5367, 551]},
    "Wrzeszcz Górny": {"kobiety": [1446, 5467, 602], "mezczyzni": [1545, 5329, 489]},
    "Wyspa Sobieszewska": {"kobiety": [247, 865, 113], "mezczyzni": [285, 814, 98]},
    "Wzgórze Mickiewicza": {"kobiety": [156, 592, 76], "mezczyzni": [179, 518, 65]},
    "Zaspa Młyniec": {"kobiety": [754, 3087, 227], "mezczyzni": [823, 2929, 200]},
    "Zaspa Rozstaje": {"kobiety": [854, 3179, 256], "mezczyzni": [948, 2953, 237]},
    "Żabianka–Wejhera–Jelitkowo–Tysiąclecia": {"kobiety": [732, 3566, 427], "mezczyzni": [754, 3306, 412]},
}

# Mapowanie nazw z różnymi formatami
NAME_MAPPING = {
    "Krakowiec- Górki Zachodnie": "Krakowiec–Górki Zachodnie",
    "Krakowiec-Górki Zachodnie": "Krakowiec–Górki Zachodnie",
    "Orunia Górna-Gdańsk Południe": "Orunia Górna–Gdańsk Południe",
    "Orunia-Św. Wojciech-Lipce": "Orunia–Św. Wojciech–Lipce",
    "Piecki- Migowo": "Piecki–Migowo",
    "Piecki-Migowo": "Piecki–Migowo",
    "Ujeścisko": "Ujeścisko–Łostowice",
    "Ujeścisko-Łostowice": "Ujeścisko–Łostowice",
    "Wrzeszcz-Dolny": "Wrzeszcz Dolny",
    "Wrzeszcz-Górny": "Wrzeszcz Górny",
    "Żabianka-Wejhera-Jelit.Tysiąc.": "Żabianka–Wejhera–Jelitkowo–Tysiąclecia",
}


class Command(BaseCommand):
    help = 'Ładuje dane demograficzne (podział na kobiety/mężczyzn) do bazy danych'

    def handle(self, *args, **options):
        self.stdout.write('Ładowanie danych demograficznych...')
        
        updated_count = 0
        not_found = []
        
        for nazwa, dane in DEMOGRAFIA_DATA.items():
            try:
                dzielnica = Dzielnica.objects.get(dzielnica=nazwa)
            except Dzielnica.DoesNotExist:
                # Spróbuj znaleźć z mapowaniem
                mapped_name = NAME_MAPPING.get(nazwa, nazwa)
                try:
                    dzielnica = Dzielnica.objects.get(dzielnica=mapped_name)
                except Dzielnica.DoesNotExist:
                    not_found.append(nazwa)
                    continue
            
            dzielnica.kobiety_mlodzi = dane["kobiety"][0]
            dzielnica.kobiety_dorosli = dane["kobiety"][1]
            dzielnica.kobiety_seniorzy = dane["kobiety"][2]
            dzielnica.mezczyzni_mlodzi = dane["mezczyzni"][0]
            dzielnica.mezczyzni_dorosli = dane["mezczyzni"][1]
            dzielnica.mezczyzni_seniorzy = dane["mezczyzni"][2]
            dzielnica.save()
            
            updated_count += 1
            razem = dzielnica.liczba_mieszkancow
            self.stdout.write(f'  ~ {dzielnica.dzielnica}: K={dzielnica.liczba_kobiet}, M={dzielnica.liczba_mezczyzn}, Razem={razem}')
        
        if not_found:
            self.stdout.write('')
            self.stdout.write(self.style.WARNING(f'Nie znaleziono dzielnic: {not_found}'))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Zakończono! Zaktualizowano: {updated_count} dzielnic'))




