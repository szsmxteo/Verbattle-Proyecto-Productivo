from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from .models import PerfilJugador


class RegistroForm(forms.Form):
    gamer_tag = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField()
    nivel_dominio = forms.ChoiceField(choices=PerfilJugador.NIVELES)

    def clean_gamer_tag(self):
        tag = self.cleaned_data["gamer_tag"].strip()
        if len(tag) < 3:
            raise forms.ValidationError("El GamerTag debe tener al menos 3 caracteres.")
        if User.objects.filter(username__iexact=tag).exists():
            raise forms.ValidationError("Ese GamerTag ya está en uso.")
        return tag

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ese correo ya está registrado.")
        return email

    def clean(self):
        datos = super().clean()
        password = datos.get("password")
        if password:
            usuario_temporal = User(
                username=datos.get("gamer_tag", ""), email=datos.get("email", "")
            )
            try:
                validate_password(password, user=usuario_temporal)
            except forms.ValidationError as error:
                self.add_error("password", error)
        return datos
