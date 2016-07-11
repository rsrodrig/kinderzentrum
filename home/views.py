# -*- encoding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.template import RequestContext
from home.forms import *
from django.views.generic import View
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.decorators import login_required

# Create your views here.


def index_view(request):
    if request.user.is_authenticated():
        #grupos = request.user.groups.all()
        user = request.user
        '''
        Aqui vamos a colocar las condiciones para que se habiliten las condiciones que el usuario
        va a usar
        '''
        registro = user.has_module_perms('registro')
        #registro = grupos.filter(name='registro').count() == 1
        ctx = {'registro':registro,'pagina_actual':'inicio'}
        return render(request, 'base.html', ctx)
    else:
        return render(request, 'base.html')


def login_view(request):
    mensaje = ""
    print "hghjgfhjgj"
    if request.user.is_authenticated():
    	#si esta autenticado redirecciona al formulario
        print "redirect"
        return HttpResponseRedirect('/')
    else:
        if request.method == "POST":
            print "post"
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                #print "hghjgfhjgj"
                usuario = authenticate(username=username,password=password)
                if usuario is not None and usuario.is_active:
                    login(request,usuario)
                    return HttpResponseRedirect('/')
                else:
                    mensaje = "Usuario y/o contraseña incorrecto"
        form = LoginForm()
        ctx = {'form':form,'mensaje':mensaje}
        return render_to_response('home/login.html',ctx,context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def change_password(request):
    #newpassword = request.POST.get("newpassword")
    #renewpasssword = request.POST.get("renewpasssword")
    #
    if request.method == 'GET':
        form = ChangePasswordForm()
    else:
        username = request.user.username
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            newpassword = request.POST.get("newpassword")
            u = User.objects.get(username__exact=username)
            u.set_password(newpassword)
            u.save()
            return redirect('/')
    return render(request,'home/cambio_contrasenia.html', {'form': form})

class AdminUsuariosView(PermissionRequiredMixin, View):
    permission_required = ('auth.add_user')
    template_name = 'home/admin_usuarios.html'

    def get(self, request, *args, **kwargs):
        registro_usuario = UserCreateForm()
        ctx = {'registro_usuario':registro_usuario, 'pagina_actual':'manejo_usuarios'}
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        registro_usuario = UserCreateForm(request.POST)
        if registro_usuario.is_valid():
            user = registro_usuario.save()
            mensaje = registro_usuario.get_mensaje()
            grupos = registro_usuario.get_permisos()
            ctx = {'registro_usuario_correcto':True, 'mensaje':mensaje, 'permisos':grupos, 'pagina_actual':'manejo_usuarios'}
            return render(request, self.template_name, ctx)
        else:
            return render(request, self.template_name, {'registro_usuario':registro_usuario})


class AdminUsuariosPermisosView(PermissionRequiredMixin, View):
    permission_required = ('auth.add_user')
    template_name = 'home/admin_usuarios.html'

    def get(self, request, *args, **kwargs):
        #únicamente se pueden modificar usuarios que no sean superusuarios
        usuarios = UsuariosFormset(queryset=User.objects.exclude(is_superuser=1))
        ctx = {'usuarios':usuarios, 'pagina_actual':'manejo_usuarios'}
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        usuarios_formset = UsuariosFormset(request.POST)
        if usuarios_formset.is_valid():
            for user in usuarios_formset:
                user.save()
        ctx = {'usuarios':usuarios_formset, 'pagina_actual':'manejo_usuarios'}
        return render(request, self.template_name, ctx)
