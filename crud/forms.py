from django import forms

class BuscarMensaje(forms.Form):
    id_juego = forms.IntegerField(label='ID del juego')