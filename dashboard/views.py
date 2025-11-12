from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Avg, Q
from proyectos.models import Proyecto
from actividades.models import Actividad
from noc.models import NoConformidad


def dashboard(request):
    proyectos = Proyecto.objects.all().select_related('control')
    total_proyectos = proyectos.count()
    proyectos_finalizados = proyectos.filter(estado='finalizado').count()
    proyectos_activos = proyectos.filter(estado='en_ejecucion').count()

    actividades = Actividad.objects.all()
    total_actividades = actividades.count()
    completadas = actividades.filter(estado='completada').count()
    avance_promedio = actividades.aggregate(Avg('avance'))['avance__avg'] or 0

    noc_abiertas = NoConformidad.objects.filter(estado='abierta').count()
    noc_proceso = NoConformidad.objects.filter(estado='en_proceso').count()
    noc_cerradas = NoConformidad.objects.filter(estado='cerrada').count()

    data_chart = {
        "labels": [p.codigo for p in proyectos],
        "values": [float(p.control.avance_global) if hasattr(p, 'control') else 0 for p in proyectos],
    }

    context = {
        "total_proyectos": total_proyectos,
        "proyectos_activos": proyectos_activos,
        "proyectos_finalizados": proyectos_finalizados,
        "total_actividades": total_actividades,
        "completadas": completadas,
        "avance_promedio": round(avance_promedio, 2),
        "noc_abiertas": noc_abiertas,
        "noc_proceso": noc_proceso,
        "noc_cerradas": noc_cerradas,
        "chart": data_chart,
    }
    return render(request, "dashboard/dashboard.html", context)


def proyectos_lista(request):
    """Lista de todos los proyectos con filtros"""
    estado_filter = request.GET.get('estado', '')
    search = request.GET.get('search', '')
    
    proyectos = Proyecto.objects.all().select_related('cliente', 'responsable', 'control')
    
    # Filtros
    if estado_filter:
        proyectos = proyectos.filter(estado=estado_filter)
    
    if search:
        proyectos = proyectos.filter(
            Q(codigo__icontains=search) | 
            Q(nombre__icontains=search) |
            Q(cliente__nombre__icontains=search)
        )
    
    # Agregar estadísticas por proyecto
    proyectos_data = []
    for proyecto in proyectos:
        total_act = proyecto.actividades.count()
        completadas = proyecto.actividades.filter(estado='completada').count()
        total_noc = proyecto.noc.count()
        noc_abiertas = proyecto.noc.filter(estado='abierta').count()
        avance = proyecto.control.avance_global if hasattr(proyecto, 'control') else 0
        
        proyectos_data.append({
            'proyecto': proyecto,
            'total_actividades': total_act,
            'actividades_completadas': completadas,
            'total_noc': total_noc,
            'noc_abiertas': noc_abiertas,
            'avance_global': avance,
        })
    
    context = {
        'proyectos_data': proyectos_data,
        'estado_filter': estado_filter,
        'search': search,
        'estados': Proyecto.ESTADO_CHOICES,
    }
    return render(request, "dashboard/proyectos_lista.html", context)


def proyecto_detalle(request, proyecto_id):
    """Detalle completo de un proyecto"""
    proyecto = get_object_or_404(
        Proyecto.objects.select_related('cliente', 'responsable', 'control'),
        id=proyecto_id
    )
    
    # Actividades del proyecto
    actividades = proyecto.actividades.all().select_related('responsable').order_by('-fecha_programada')
    
    # Estadísticas de actividades
    total_actividades = actividades.count()
    act_completadas = actividades.filter(estado='completada').count()
    act_en_ejecucion = actividades.filter(estado='en_ejecucion').count()
    act_pendientes = actividades.filter(estado='pendiente').count()
    act_atrasadas = actividades.filter(estado='atrasada').count()
    
    # No conformidades
    nocs = proyecto.noc.all().select_related('responsable').order_by('-fecha_detectada')
    total_noc = nocs.count()
    noc_abiertas = nocs.filter(estado='abierta').count()
    noc_proceso = nocs.filter(estado='en_proceso').count()
    noc_cerradas = nocs.filter(estado='cerrada').count()
    
    # Gráfico de actividades por estado
    chart_actividades = {
        'labels': ['Completadas', 'En Ejecución', 'Pendientes', 'Atrasadas'],
        'values': [act_completadas, act_en_ejecucion, act_pendientes, act_atrasadas],
        'colors': ['#28a745', '#007bff', '#ffc107', '#dc3545']
    }
    
    # Gráfico de NOC por estado
    chart_noc = {
        'labels': ['Abiertas', 'En Proceso', 'Cerradas'],
        'values': [noc_abiertas, noc_proceso, noc_cerradas],
        'colors': ['#dc3545', '#ffc107', '#28a745']
    }
    
    context = {
        'proyecto': proyecto,
        'actividades': actividades[:20],  # Últimas 20 actividades
        'total_actividades': total_actividades,
        'act_completadas': act_completadas,
        'act_en_ejecucion': act_en_ejecucion,
        'act_pendientes': act_pendientes,
        'act_atrasadas': act_atrasadas,
        'nocs': nocs[:10],  # Últimas 10 NOC
        'total_noc': total_noc,
        'noc_abiertas': noc_abiertas,
        'noc_proceso': noc_proceso,
        'noc_cerradas': noc_cerradas,
        'chart_actividades': chart_actividades,
        'chart_noc': chart_noc,
    }
    return render(request, "dashboard/proyecto_detalle.html", context)


def actividades_lista(request):
    """Lista de todas las actividades con filtros y paginación"""
    from django.core.paginator import Paginator
    
    # Filtros
    estado_filter = request.GET.get('estado', '')
    proyecto_filter = request.GET.get('proyecto', '')
    search = request.GET.get('search', '')
    
    # Query base
    actividades = Actividad.objects.all().select_related('proyecto', 'responsable').order_by('-fecha_programada')
    
    # Aplicar filtros
    if estado_filter:
        actividades = actividades.filter(estado=estado_filter)
    
    if proyecto_filter:
        actividades = actividades.filter(proyecto_id=proyecto_filter)
    
    if search:
        actividades = actividades.filter(
            Q(item__icontains=search) | 
            Q(descripcion__icontains=search) |
            Q(proyecto__codigo__icontains=search)
        )
    
    # Estadísticas generales
    total_actividades = Actividad.objects.count()
    completadas = Actividad.objects.filter(estado='completada').count()
    en_ejecucion = Actividad.objects.filter(estado='en_ejecucion').count()
    pendientes = Actividad.objects.filter(estado='pendiente').count()
    atrasadas = Actividad.objects.filter(estado='atrasada').count()
    avance_promedio = Actividad.objects.aggregate(Avg('avance'))['avance__avg'] or 0
    
    # Estadísticas filtradas
    total_filtradas = actividades.count()
    
    # Paginación
    paginator = Paginator(actividades, 20)  # 20 actividades por página
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Proyectos para el filtro
    proyectos = Proyecto.objects.all().order_by('codigo')
    
    # Gráfico de actividades por estado
    chart_data = {
        'labels': ['Completadas', 'En Ejecución', 'Pendientes', 'Atrasadas'],
        'values': [completadas, en_ejecucion, pendientes, atrasadas],
        'colors': ['#28a745', '#007bff', '#ffc107', '#dc3545']
    }
    
    context = {
        'page_obj': page_obj,
        'total_actividades': total_actividades,
        'completadas': completadas,
        'en_ejecucion': en_ejecucion,
        'pendientes': pendientes,
        'atrasadas': atrasadas,
        'avance_promedio': round(avance_promedio, 2),
        'total_filtradas': total_filtradas,
        'estado_filter': estado_filter,
        'proyecto_filter': proyecto_filter,
        'search': search,
        'estados': Actividad.ESTADO_CHOICES,
        'proyectos': proyectos,
        'chart_data': chart_data,
    }
    return render(request, "dashboard/actividades_lista.html", context)
