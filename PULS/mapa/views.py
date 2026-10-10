import os
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Note, Dzielnica, ZdarzenieSpoleczne, Komentarz
from .serializers import NoteSerializer, DzielnicaSerializer, ZdarzenieSpoleczneSerializer, KomentarzSerializer

# Admin password - defaults to 'admin123' for demo purposes
# In production, set ADMIN_PASSWORD environment variable
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')


class NotesViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class DzielnicaViewSet(viewsets.ModelViewSet):
    queryset = Dzielnica.objects.all()
    serializer_class = DzielnicaSerializer


class ZdarzenieSpoleczneViewSet(viewsets.ModelViewSet):
    queryset = ZdarzenieSpoleczne.objects.all()
    serializer_class = ZdarzenieSpoleczneSerializer
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        zdarzenie = self.get_object()
        zdarzenie.like += 1
        zdarzenie.save()
        return Response({'like': zdarzenie.like})
    
    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        zdarzenie = self.get_object()
        zdarzenie.dislike += 1
        zdarzenie.save()
        return Response({'dislike': zdarzenie.dislike})
    
    @action(detail=True, methods=['get'])
    def komentarze(self, request, pk=None):
        zdarzenie = self.get_object()
        komentarze = zdarzenie.komentarze.all()
        serializer = KomentarzSerializer(komentarze, many=True)
        return Response(serializer.data)


class KomentarzViewSet(viewsets.ModelViewSet):
    queryset = Komentarz.objects.all()
    serializer_class = KomentarzSerializer


class DzielnicaGeoJSONView(APIView):
    """Widok zwracający dane dzielnic w formacie GeoJSON."""
    
    def get(self, request):
        dzielnice = Dzielnica.objects.all()
        features = [dzielnica.to_geojson_feature() for dzielnica in dzielnice]
        
        geojson = {
            "type": "FeatureCollection",
            "features": features
        }
        
        return Response(geojson)


class ZdarzeniaGeoJSONView(APIView):
    """Widok zwracający zdarzenia społeczne w formacie GeoJSON."""
    
    def get(self, request):
        zdarzenia = ZdarzenieSpoleczne.objects.all()
        features = []
        
        for z in zdarzenia:
            feature = {
                "type": "Feature",
                "properties": {
                    "id": z.id,
                    "tytul": z.tytul,
                    "opis": z.opis,
                    "kategoria": z.kategoria,
                    "kategoria2": z.kategoria2,
                    "kategoria3": z.kategoria3,
                    "dzielnica": z.dzielnica.dzielnica if z.dzielnica else None,
                    "like": z.like,
                    "dislike": z.dislike,
                    "data_utworzenia": z.data_utworzenia.isoformat() if z.data_utworzenia else None,
                    "termin_od": z.termin_od.isoformat() if z.termin_od else None,
                    "termin_do": z.termin_do.isoformat() if z.termin_do else None,
                    "min_wiek": z.min_wiek,
                    "dla_niepelnosprawnych": z.dla_niepelnosprawnych,
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [z.lokalizacja_lng, z.lokalizacja_lat]
                }
            }
            features.append(feature)
        
        geojson = {
            "type": "FeatureCollection",
            "features": features
        }
        
        return Response(geojson)


class AdminLoginView(APIView):
    """Widok do logowania admina."""
    
    def post(self, request):
        password = request.data.get('password', '')
        
        if password == ADMIN_PASSWORD:
            return Response({
                'success': True,
                'message': 'Zalogowano pomyślnie',
                'isAdmin': True
            })
        else:
            return Response({
                'success': False,
                'message': 'Nieprawidłowe hasło'
            }, status=status.HTTP_401_UNAUTHORIZED)