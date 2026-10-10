from rest_framework import serializers
from .models import Note, Dzielnica, ZdarzenieSpoleczne, Komentarz


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'


class DzielnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dzielnica
        fields = '__all__'


class ZdarzenieSpoleczneSerializer(serializers.ModelSerializer):
    dzielnica_nazwa = serializers.CharField(write_only=True, required=False, allow_blank=True)
    dzielnica = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = ZdarzenieSpoleczne
        fields = '__all__'
        read_only_fields = ['id', 'data_utworzenia', 'like', 'dislike', 'kategoria', 'dzielnica']
    
    def create(self, validated_data):
        dzielnica_nazwa = validated_data.pop('dzielnica_nazwa', None)
        if dzielnica_nazwa:
            try:
                dzielnica = Dzielnica.objects.get(dzielnica=dzielnica_nazwa)
                validated_data['dzielnica'] = dzielnica
            except Dzielnica.DoesNotExist:
                pass
        return super().create(validated_data)


class KomentarzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Komentarz
        fields = ['id', 'zdarzenie', 'autor', 'tresc', 'data_utworzenia']
        read_only_fields = ['id', 'data_utworzenia']