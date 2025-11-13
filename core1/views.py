from django.shortcuts import render, redirect
from .forms import PersonaForm, SolicitudForm
from .models import Categoria, Persona

def inicio(request):
    categorias = Categoria.objects.all()
    
    persona_form = PersonaForm()
    solicitud_form = SolicitudForm()
    
    persona_estado = None
    solicitudes = None
    error_estado = None
    
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
    
    return render(request, 'index.html', context)


def aplicar(request):
    if request.method == 'POST':
        persona_form = PersonaForm(request.POST)
        solicitud_form = SolicitudForm(request.POST)
        categoria_id = request.POST.get('categoria')

        if persona_form.is_valid() and solicitud_form.is_valid() and categoria_id:
            correo = persona_form.cleaned_data['correo']
            cedula = persona_form.cleaned_data['cedula']

            persona = Persona.objects.filter(correo=correo, cedula=cedula).first()
            if not persona:
                persona = persona_form.save()

            solicitud = solicitud_form.save(commit=False)
            solicitud.persona = persona
            solicitud.categoria_id = categoria_id
            solicitud.save()

            return redirect('index')

        categorias = Categoria.objects.all()
        context = {
            'categorias': categorias,
            'persona_form': persona_form, 
            'solicitud_form': solicitud_form, 
            'mostrar_resultado_busqueda': False
        }
        return render(request, 'index.html', context)

    return redirect('index')



def estado(request):
    if request.method == "POST":
        correo = request.POST.get("email")
        cedula = request.POST.get("cedula")

        try:
            persona = Persona.objects.get(correo=correo, cedula=cedula)

            solicitudes = persona.solicitudes.all().select_related('estado')

            categorias = Categoria.objects.all()
            context = {
                'categorias': categorias,
                'persona_form': PersonaForm(),
                'solicitud_form': SolicitudForm(),
                'persona_estado': persona,
                'solicitudes': solicitudes,
                'mostrar_resultado_busqueda': True,
            }
            
            return render(request, 'index.html', context)

        except Persona.DoesNotExist:
            categorias = Categoria.objects.all()
            context = {
                'categorias': categorias,
                'persona_form': PersonaForm(),
                'solicitud_form': SolicitudForm(),
                'error_estado': "No se encontró una persona con esos datos.",
                'mostrar_resultado_busqueda': True,
            }
            return render(request, 'index.html', context)
    
    return redirect('index')


def categorias(request):
    return redirect('index')

def gracias(request):
    return redirect('index')