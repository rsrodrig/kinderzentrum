# -*- encoding: utf-8 -*-
from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.forms import formset_factory, modelformset_factory
from django.views.generic.edit import UpdateView
from django import template
#from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Usuario','autofocus':'autofocus'}))
    password = forms.CharField(label="",widget=forms.PasswordInput(render_value=False, attrs={'placeholder': 'Contraseña'}))


class UserCreateForm(UserCreationForm):
	password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(render_value=False, attrs={'placeholder': 'Contraseña','class':'form-control'}))
	password2 = forms.CharField(label="Repita contraseña", widget=forms.PasswordInput(render_value=False, attrs={'placeholder': 'Contraseña','class':'form-control'}))
	grupos = forms.ModelMultipleChoiceField(queryset=None,widget=forms.CheckboxSelectMultiple())

	def __init__(self, *args, **kw):
	    super(UserCreateForm, self).__init__(*args, **kw)
	    self.fields['grupos'].queryset=Group.objects.all()

	class Meta:
		model = User
		fields = ('username', 'first_name' , 'last_name','email', 'password1', 'password2','grupos')
		widgets = {
				   'email': forms.EmailInput(attrs={'placeholder': 'email@email.com','class':'form-control'})
					}

	def save(self, commit=True):
		user = super(UserCreateForm, self).save(commit=False)
		user.mail = self.cleaned_data['email']

		print self.cleaned_data['grupos']
		if commit:
			user.save()
			user.groups = self.cleaned_data['grupos']
			user.save()
		return user

	def get_mensaje(self):
		return self.cleaned_data['first_name'] + ' ' + self.cleaned_data['last_name']

	def get_permisos(self):
		return self.cleaned_data['grupos']


class UserForm(ModelForm):
	#required=False para que al evaluar la función clean retorne True así tenga campos vacíos (lo cuál es correcto)
	grupos = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple(), required=False)

	def __init__(self, *args, **kw):
	    super(UserForm, self).__init__(*args, **kw)
	    self.fields['grupos'].queryset = Group.objects.all()
	    self.fields['grupos'].initial = Group.objects.filter(user=self.instance.id)
	    self.fields['username'].widget.attrs['readonly'] = True

	class Meta:
		model = User
		fields = ('username', 'first_name' ,)

	def save(self, commit=False):
		user = self.instance
		user.groups = self.cleaned_data['grupos']
		return user

	def clean(self):
		cleaned_data = super(UserForm, self).clean()


UsuariosFormset = modelformset_factory(User, form=UserForm, extra=0)

class ChangePasswordForm(forms.Form):
    newpassword = forms.CharField(label="Nueva Contraseña", widget=forms.PasswordInput(attrs={'placeholder': 'Contrasenia'}))
    renewpasssword = forms.CharField(label="Repita nueva contraseña", widget=forms.PasswordInput(attrs={'placeholder': 'Repita nueva contrasenia'}))

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        newpassword = cleaned_data.get('newpassword')
        renewpasssword = cleaned_data.get('renewpasssword')
        if newpassword != renewpasssword:
            raise forms.ValidationError("Las contraseñas deben ser iguales")
            #self.add_error('renewpasssword', 'Las contraseñas deben ser iguales')



'''
class RegistroUsuario(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nombres','autofocus':'autofocus'}))
    apellido = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Apellidos'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'placeholder': 'Contraseña','class':'form-control'}))
    repeat_password = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'placeholder': 'Contraseña','class':'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'email@email.com','class':'form-control'}))
'''
