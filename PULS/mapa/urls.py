from django.urls import include, path
from rest_framework import routers
from .views import (
    NotesViewSet, DzielnicaViewSet, DzielnicaGeoJSONView,
    ZdarzenieSpoleczneViewSet, ZdarzeniaGeoJSONView, KomentarzViewSet,
    AdminLoginView
)

router = routers.DefaultRouter()
router.register(r'mapa', NotesViewSet)
router.register(r'dzielnice', DzielnicaViewSet)
router.register(r'zdarzenia', ZdarzenieSpoleczneViewSet)
router.register(r'komentarze', KomentarzViewSet)

urlpatterns = [
    path('dzielnice-geojson/', DzielnicaGeoJSONView.as_view(), name='dzielnice-geojson'),
    path('zdarzenia-geojson/', ZdarzeniaGeoJSONView.as_view(), name='zdarzenia-geojson'),
    path('admin-login/', AdminLoginView.as_view(), name='admin-login'),
    path('', include(router.urls)),
]