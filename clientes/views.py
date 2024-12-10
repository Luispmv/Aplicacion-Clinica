from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cliente, Consulta


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    template_name = 'clientes/cadastro.html'
    fields = ['sexo', 'telefono', 'nif']
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        # Asegúrate de usar el campo correcto del modelo
        form.instance.usuario = self.request.user  # Cambiado de user a usuario
        return super().form_valid(form)


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    login_url = reverse_lazy('accounts:login')
    template_name = 'accounts/update_user.html'
    fields = ['sexo', 'telefono', 'nif']
    success_url = reverse_lazy('accounts:index')

    def get_object(self):
        user = self.request.user
        try:
            return Cliente.objects.get(usuario=user)
        except Cliente.DoesNotExist:
            messages.error(self.request, "No se encontró un cliente asociado al usuario actual.")
            return None

    def form_valid(self, form):
        form.instance.usuario = self.request.user  # Cambiado de user a usuario
        return super().form_valid(form)


class ConsultaCreateView(LoginRequiredMixin, CreateView):
    model = Consulta
    login_url = 'accounts:login'
    template_name = 'clientes/cadastro.html'
    fields = ['agenda']
    success_url = reverse_lazy('clientes:consulta_list')
    
    def form_valid(self, form):
        try:
            # Asegúrate de usar el campo correcto del modelo
            form.instance.cliente = Cliente.objects.get(usuario=self.request.user)
            form.save()
        except IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                messages.warning(self.request, 'No puedes marcar esta consulta.')
                return HttpResponseRedirect(reverse_lazy('clientes:consulta_create'))
        except Cliente.DoesNotExist:
            messages.warning(self.request, 'Complete su registro.')
            return HttpResponseRedirect(reverse_lazy('clientes:cliente_cadastro'))
        messages.success(self.request, 'Consulta marcada con éxito.')
        return HttpResponseRedirect(reverse_lazy('clientes:consulta_list'))


class ConsultaUpdateView(LoginRequiredMixin, UpdateView):
    model = Consulta
    login_url = 'accounts:login'
    template_name = 'clientes/cadastro.html'
    fields = ['agenda']
    success_url = reverse_lazy('clientes:consulta_list')
    
    def form_valid(self, form):
        try:
            # Asegúrate de usar el campo correcto del modelo
            form.instance.cliente = Cliente.objects.get(usuario=self.request.user)
        except Cliente.DoesNotExist:
            messages.error(self.request, "Complete su registro antes de actualizar consultas.")
            return HttpResponseRedirect(reverse_lazy('clientes:consulta_list'))
        return super().form_valid(form)


class ConsultaDeleteView(LoginRequiredMixin, DeleteView):
    model = Consulta
    success_url = reverse_lazy('clientes:consulta_list')
    template_name = 'form_delete.html'

    def get_success_url(self):
        messages.success(self.request, "Consulta eliminada con éxito.")
        return reverse_lazy('clientes:consulta_list')


class ConsultaListView(LoginRequiredMixin, ListView):
    login_url = 'accounts:login'
    template_name = 'clientes/consulta_list.html'
    context_object_name = 'consultas'

    def get_queryset(self):
        user = self.request.user
        try:
            cliente = Cliente.objects.get(usuario=user)
        except Cliente.DoesNotExist:
            messages.warning(self.request, 'Complete su registro para acceder a las consultas.')
            return Consulta.objects.none()
        return Consulta.objects.filter(cliente=cliente).order_by('-pk')


# Configuración de vistas
cliente_cadastro = ClienteCreateView.as_view()
cliente_atualizar = ClienteUpdateView.as_view()
consulta_lista = ConsultaListView.as_view()
consulta_cadastro = ConsultaCreateView.as_view()
consulta_atualizar = ConsultaUpdateView.as_view()
consulta_excluir = ConsultaDeleteView.as_view()
