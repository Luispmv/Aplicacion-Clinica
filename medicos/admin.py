from django.contrib import admin
from medicos.models import Especialidad, Medico, Agenda

class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ['nombre']  

class MedicoAdmin(admin.ModelAdmin):
    list_display = [
        'nombre', 'crm', 'telefono', 
    ]
    search_fields = ['nombre', 'crm']  # Permitir búsqueda por nombre y CRM.

class AgendaAdmin(admin.ModelAdmin):
    list_display = [
        'dia', 'medico', 'horario'  
    ]
    list_filter = ['dia', 'medico']  # Filtrar por día y médico.
    ordering = ['dia']  # Ordenar las agendas por fecha.

admin.site.register(Especialidad, EspecialidadAdmin)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(Agenda, AgendaAdmin)
