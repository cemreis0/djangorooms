from django.forms import CharField, ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['topic', 'name', 'description']