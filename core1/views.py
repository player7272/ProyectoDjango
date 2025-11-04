from django.shortcuts import render, redirect
from .forms import PersonaForm, SolicitudForm
from .models import Categoria, Persona

def inicio(request):
    """Vista unificada que contiene todo el contenido en una sola página"""
    
    # Obtener todas las categorías para mostrarlas
    categorias = Categoria.objects.all()
    
    # Inicializar formularios
    persona_form = PersonaForm()
    solicitud_form = SolicitudForm()
    
    # Variables para el estado de solicitud
    persona_estado = None
    solicitudes = None
    error_estado = None
    
    # Variables de control
    mostrar_gracias = False
    mostrar_resultado_busqueda = False
    
    context = {
        'categorias': categorias,
        'persona_form': persona_form,
        'solicitud_form': solicitud_form,
        'persona_estado': persona_estado,
        'solicitudes': solicitudes,
        'error_estado': error_estado,
        'mostrar_gracias': mostrar_gracias,
        'mostrar_resultado_busqueda': mostrar_resultado_busqueda,
    }
    
    return render(request, 'inicio_unificado.html', context)


def aplicar(request):
    """Procesa el formulario de aplicación"""
    if request.method == 'POST':
        persona_form = PersonaForm(request.POST)
        solicitud_form = SolicitudForm(request.POST)

        if persona_form.is_valid() and solicitud_form.is_valid():
            correo = persona_form.cleaned_data['correo']
            cedula = persona_form.cleaned_data['cedula']

            # Buscar persona existente por correo o cédula
            persona = Persona.objects.filter(correo=correo, cedula=cedula).first()

            if not persona:
                # Si no existe, crearla
                persona = persona_form.save(commit=False)
                persona.save()

            # Crear solicitud asociada
            solicitud = solicitud_form.save(commit=False)
            solicitud.persona = persona
            solicitud.save()

            print("✅ Solicitud registrada correctamente")
            # Redirigir a la sección de gracias con un ancla
            return redirect('inicio_unificado')
    
    return redirect('inicio_unificado')


def estado(request):
    """Procesa la búsqueda de estado de solicitudes"""
    if request.method == "POST":
        correo = request.POST.get("email")
        cedula = request.POST.get("cedula")

        try:
            # Buscar persona con esos datos
            persona = Persona.objects.get(correo=correo, cedula=cedula)

            # Obtener todas sus solicitudes relacionadas
            solicitudes = persona.solicitudes.all().select_related('estado')

            # Renderizar con los resultados
            categorias = Categoria.objects.all()
            context = {
                'categorias': categorias,
                'persona_form': PersonaForm(),
                'solicitud_form': SolicitudForm(),
                'persona_estado': persona,
                'solicitudes': solicitudes,
                'mostrar_resultado_busqueda': True,
            }
            
            return render(request, 'inicio_unificado.html', context)

        except Persona.DoesNotExist:
            categorias = Categoria.objects.all()
            context = {
                'categorias': categorias,
                'persona_form': PersonaForm(),
                'solicitud_form': SolicitudForm(),
                'error_estado': "No se encontró una persona con esos datos.",
                'mostrar_resultado_busqueda': True,
            }
            return render(request, 'inicio_unificado.html', context)
    
    return redirect('inicio_unificado')


# Mantener vistas antiguas por compatibilidad (pueden eliminarse después)
def categorias(request):
    return redirect('inicio_unificado')

def gracias(request):
    return redirect('inicio_unificado')