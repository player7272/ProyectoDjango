from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Empleado, Permiso, Nomina, PeriodoNomina
from .forms import EmpleadoForm, PermisoForm
from datetime import date

def index(request):
    """Vista de inicio del core2"""
    return render(request, 'core2/index.html')

def home_core2(request):
    """Vista home del core2"""
    return redirect('completar_datos')

@login_required
def dashboard_empleado(request):
    """Vista principal del dashboard del empleado"""
    try:
        empleado = request.user.empleado
        
        # Si no ha completado sus datos, redirigir al formulario
        if not empleado.datos_completados:
            return redirect('completar_datos')
        
        # Obtener datos para el dashboard
        permisos_pendientes = empleado.permisos.filter(estado='PENDIENTE').count()
        permisos_aprobados = empleado.permisos.filter(estado='APROBADO').count()
        dias_empresa = empleado.dias_en_empresa()
        anos_empresa = empleado.anos_en_empresa()
        
        # Obtener últimas nóminas
        ultimas_nominas = empleado.nominas.all()[:5]
        
        # Obtener últimos permisos
        ultimos_permisos = empleado.permisos.all().order_by('-fecha_solicitud')[:5]
        
        context = {
            'empleado': empleado,
            'permisos_pendientes': permisos_pendientes,
            'permisos_aprobados': permisos_aprobados,
            'dias_empresa': dias_empresa,
            'anos_empresa': anos_empresa,
            'ultimas_nominas': ultimas_nominas,
            'ultimos_permisos': ultimos_permisos,
        }
        
        return render(request, 'core2/dashboard.html', context)
        
    except Empleado.DoesNotExist:
        # Si no existe el empleado, crear uno y redirigir a completar datos
        empleado = Empleado.objects.create(
            user=request.user,
            nombre=request.user.first_name or '',
            apellido=request.user.last_name or '',
            correo=request.user.email or '',
            datos_completados=False
        )
        return redirect('completar_datos')


@login_required
def completar_datos(request):
    """Vista para completar los datos del empleado por primera vez"""
    empleado, created = Empleado.objects.get_or_create(
        user=request.user,
        defaults={
            'nombre': request.user.first_name or '',
            'apellido': request.user.last_name or '',
            'correo': request.user.email or '',
            'datos_completados': False
        }
    )
    
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            empleado = form.save(commit=False)
            empleado.datos_completados = True
            empleado.save()
            messages.success(request, '¡Datos actualizados correctamente!')
            return redirect('dashboard_empleado')
    else:
        form = EmpleadoForm(instance=empleado)
    
    context = {
        'form': form,
        'empleado': empleado,
    }
    
    return render(request, 'core2/completar_datos.html', context)


@login_required
def mis_nominas(request):
    """Vista para ver todas las nóminas del empleado"""
    try:
        empleado = request.user.empleado
        
        if not empleado.datos_completados:
            return redirect('completar_datos')
        
        nominas = empleado.nominas.all()
        
        context = {
            'empleado': empleado,
            'nominas': nominas,
        }
        
        return render(request, 'core2/mis_nominas.html', context)
    except Empleado.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil primero')
        return redirect('completar_datos')


@login_required
def detalle_nomina(request, nomina_id):
    """Vista para ver el detalle de una nómina específica"""
    try:
        empleado = request.user.empleado
        nomina = get_object_or_404(Nomina, id=nomina_id, empleado=empleado)
        
        context = {
            'empleado': empleado,
            'nomina': nomina,
        }
        
        return render(request, 'core2/detalle_nomina.html', context)
    except Empleado.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil primero')
        return redirect('completar_datos')


@login_required
def mis_permisos(request):
    """Vista para ver y gestionar permisos"""
    try:
        empleado = request.user.empleado
        
        if not empleado.datos_completados:
            return redirect('completar_datos')
        
        permisos = empleado.permisos.all().order_by('-fecha_solicitud')
        
        context = {
            'empleado': empleado,
            'permisos': permisos,
        }
        
        return render(request, 'core2/mis_permisos.html', context)
    except Empleado.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil primero')
        return redirect('completar_datos')


@login_required
def solicitar_permiso(request):
    """Vista para solicitar un nuevo permiso"""
    try:
        empleado = request.user.empleado
        
        if not empleado.datos_completados:
            return redirect('completar_datos')
        
        if request.method == 'POST':
            form = PermisoForm(request.POST)
            if form.is_valid():
                permiso = form.save(commit=False)
                permiso.empleado = empleado
                permiso.save()
                messages.success(request, '¡Permiso solicitado correctamente! Está pendiente de aprobación.')
                return redirect('mis_permisos')
        else:
            form = PermisoForm()
        
        context = {
            'empleado': empleado,
            'form': form,
        }
        
        return render(request, 'core2/solicitar_permiso.html', context)
    except Empleado.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil primero')
        return redirect('completar_datos')


@login_required
def perfil_empleado(request):
    """Vista para ver y editar el perfil del empleado"""
    try:
        empleado = request.user.empleado
        
        if not empleado.datos_completados:
            return redirect('completar_datos')
        
        if request.method == 'POST':
            form = EmpleadoForm(request.POST, instance=empleado)
            if form.is_valid():
                form.save()
                messages.success(request, '¡Perfil actualizado correctamente!')
                return redirect('perfil_empleado')
        else:
            form = EmpleadoForm(instance=empleado)
        
        context = {
            'empleado': empleado,
            'form': form,
        }
        
        return render(request, 'core2/perfil_empleado.html', context)
    except Empleado.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil primero')
        return redirect('completar_datos')