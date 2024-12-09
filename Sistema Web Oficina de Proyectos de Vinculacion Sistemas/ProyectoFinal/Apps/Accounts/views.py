from django.shortcuts import render, redirect
from django.contrib.auth.models import Group

from django.db.models.query_utils import Q
from django.core.mail import send_mail, BadHeaderError
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_str

from django.contrib.auth import update_session_auth_hash
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Substr
from django.db.models import Count
from datetime import date, timedelta
from django.utils import timezone
from django.conf import settings
import re
import pytz
import string  
import random  
import math
from .models import *
from .forms import *
from .decorators import *
from .utils import enviar_email
# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@dashboard
def home(request):
    group = request.user.groups.all()[0].name
    all_estudiantes = Estudiante.objects.all()
    all_anteproyectos = Anteproyecto.objects.all()
    all_residencias = Residencia.objects.all()
    docentes = Docente.objects.all().count()
    totalAlumnos = all_estudiantes.count()                
    all_e_anteproyectos = Estudiante_Anteproyecto.objects.filter(estado = 'ACTIVO')           
    all_e_residencias = Estudiante_Residencia.objects.filter(estado = 'ACTIVO')       
    
    anteproyectosT = all_anteproyectos.count()
    residenciasT = all_residencias.count()
    
    anteproyectosE = all_anteproyectos.filter(estatus = 'ENVIADO').count()
    anteproyectosP = all_anteproyectos.filter(estatus = 'PENDIENTE').count()
    anteproyectosER = all_anteproyectos.filter(estatus = 'EN REVISION').count()
    anteproyectosRE = all_anteproyectos.filter(estatus = 'REVISADO').count()
    anteproyectosA = all_anteproyectos.filter(estatus = 'ACEPTADO').count()
    anteproyectosR = all_anteproyectos.filter(estatus = 'RECHAZADO').count()
    
    residenciasI = all_residencias.filter(estatus = 'INICIADA').count()
    residenciasEP = all_residencias.filter(estatus = 'EN PROCESO').count()
    residenciasP = all_residencias.filter(estatus = 'PROROGA').count()
    residenciasF = all_residencias.filter(estatus = 'FINALIZADA').count()
    
    epedientesC = Expediente.objects.filter(estatus = 'COMPLETO').count()                              
    
    context = {'group': group, 'totalAlumnos': totalAlumnos, 'anteproyectosE': anteproyectosE, 'anteproyectosT': anteproyectosT, 'anteproyectosP': anteproyectosP, 'anteproyectosER': anteproyectosER, 'anteproyectosRE': anteproyectosRE, 'anteproyectosA': anteproyectosA, 'anteproyectosR': anteproyectosR, 'residenciasI': residenciasI, 'residenciasEP': residenciasEP, 'residenciasP': residenciasP ,'residenciasF': residenciasF, 'docentes': docentes, 'title': 'Inicio', 'epedientesC': epedientesC}
    return render(request, 'Global/dashboard.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def studentPage(request):    
    group = request.user.groups.all()[0].name
    student = request.user.estudiante
    all_anteproyectos = Estudiante_Anteproyecto.objects.filter(estudiante = student, estado = 'ACTIVO')
    all_residencias = Estudiante_Residencia.objects.filter(estudiante = student, estado = 'ACTIVO')                                    
    
    try:
        invitacion = Invitacion.objects.get(estudiante_destinatario = student.estudiante_aut)
    except:
        invitacion = None
    
    if all_anteproyectos:        
        anteproyecto = all_anteproyectos[0].anteproyecto    
    else:
        anteproyecto = None      
    
    if all_residencias:        
        proyecto = all_residencias[0].residencia    
    else:
        proyecto = None      
            
    expediente = student.expediente      
    
    all_avisos = Avisos.objects.all().order_by('-fechaCreacion')  
    if all_avisos:
        for aviso in all_avisos:
            fin_aviso = aviso.fechaCreacion + timedelta(days=aviso.tiempoVida)
            fecha_actual = timezone.now()                        
            fin_aviso = convert_to_localtime(fin_aviso)
            fecha_actual = convert_to_localtime(fecha_actual)            
            if fecha_actual > fin_aviso:            
                aviso.delete()            
            
    avisosP = all_avisos.filter(estudiante = student)
    avisosT = all_avisos.filter(entidad = 'TODOS')
    avisosE = all_avisos.filter(entidad = 'ESTUDIANTES')
    avisos = avisosP | avisosT | avisosE    
    
    observacion = None
    observaciones = None
    fechaObservacion = None    
        
    try:
        observacion = anteproyecto.observacion
        observaciones = ObservacionDocente.objects.filter(observacion=observacion).order_by('-fechaElaboracion')       
        fechaObservacion = observacion.fechaCreacion            
        dias = 5 + observacion.incrementarDias
        fechaObservacion = fechaObservacion + timedelta(days=dias)                   
        fechaObservacion = fechaObservacion.strftime("%d/%b/%Y")                    
    except:
        pass
    context = {'group': group, 'anteproyecto': anteproyecto, 'proyecto': proyecto, 'expediente': expediente, 'fechaObservacion': fechaObservacion,'observaciones': observaciones, 'avisos':avisos, 'invitacion': invitacion, 'title': 'Inicio'}    
    return render(request, 'Student/dashboard.html', context)

@login_required(login_url='login')
def teacherPage(request):
    group = request.user.groups.all()[0].name
    docente = request.user.docente
    
    all_avisos = Avisos.objects.all().order_by('-fechaCreacion')  
    if all_avisos:
        for aviso in all_avisos:
            fin_aviso = aviso.fechaCreacion + timedelta(days=aviso.tiempoVida)
            fecha_actual = timezone.now()                        
            fin_aviso = convert_to_localtime(fin_aviso)
            fecha_actual = convert_to_localtime(fecha_actual)            
            if fecha_actual > fin_aviso:            
                aviso.delete()
                        
    avisosP = all_avisos.filter(docente = docente)
    avisosT = all_avisos.filter(entidad = 'TODOS')
    avisosD = all_avisos.filter(entidad = 'DOCENTES')
    avisos = avisosP | avisosT | avisosD
    
    all_anteproyectos = Anteproyecto.objects.all()
    all_residencias = Residencia.objects.all()    
    
    anteproyectos_activos_r1 = all_anteproyectos.filter(revisor1=docente).exclude(estatus__in=['ACEPTADO', 'RECHAZADO'])
    anteproyectos_activos_r2 = all_anteproyectos.filter(revisor2=docente).exclude(estatus__in=['ACEPTADO', 'RECHAZADO'])
    
    residencias_activas_a = all_residencias.filter(r_asesorInterno=docente).exclude(estatus__in=['FINALIZADA', 'RECHAZADA', 'NO FINALIZADA'])
    residencias_activas_r = all_residencias.filter(r_revisor=docente).exclude(estatus__in=['FINALIZADA', 'RECHAZADA', 'NO FINALIZADA'])
    
    anteproyectos_pasados_r1 = all_anteproyectos.filter(estatus='ACEPTADO', revisor1=docente)
    anteproyectos_pasados_r2 = all_anteproyectos.filter(estatus='ACEPTADO', revisor2=docente)
    
    residencias_pasadas_a = all_residencias.filter(estatus='FINALIZADA', r_asesorInterno=docente)
    residencias_pasadas_r = all_residencias.filter(estatus='FINALIZADA', r_revisor=docente)
    
    actividad_docente = [anteproyectos_activos_r1.count() + anteproyectos_activos_r2.count(),
                         residencias_activas_a.count() + residencias_activas_r.count(), 
                         residencias_activas_a.count(), 
                         anteproyectos_pasados_r1.count() + anteproyectos_pasados_r2.count(), 
                         residencias_pasadas_a.count() + residencias_pasadas_r.count(), 
                         residencias_activas_r.count()
                         ]

    all_anteproyectos_activos = anteproyectos_activos_r1 | anteproyectos_activos_r2
    actualizaciones = Actualizacion_anteproyecto.objects.filter(anteproyecto__in=all_anteproyectos_activos, tipo='ACTUALIZADO').exclude(estado='LEIDO').order_by('-fecha')
    
    context = {'group': group, 'docente': docente, 'actividad_docente': actividad_docente, 'actualizaciones': actualizaciones, 'avisos': avisos, 'title': 'Inicio'}
    return render(request, 'Teacher/dashboard.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@unauthenticated_user
def loginPage(request):    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return redirect('home')
        else:
            #messages.info(request, 'Número de control o contraseña incorrecta')    
            messages.info(request, 'Invalid username or password')    

    context = {}
    return render(request, 'Global/login.html', context)

def errorPage(request):
    return render(request, 'Global/404.html')

@unauthenticated_user
def email_verification(request, pk):    
    estudiante = Estudiante.objects.get(id = pk)
    email = estudiante.correoElectronico
    return render(request, 'Global/email_verify/email_verification.html', {'email': email})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@d_faqs
def faqs(request):
    group = request.user.groups.all()[0].name
    context = {'group': group, 'title': 'Preguntas Frecuentes'}
    return render(request, 'Global/faqs.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def student_faqs(request):
    group = request.user.groups.all()[0].name
    context = {'group': group, 'title': 'Preguntas Frecuentes'}
    return render(request, 'Student/faqs.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@teacher_only
def teacher_faqs(request):
    group = request.user.groups.all()[0].name
    context = {'group': group, 'title': 'Preguntas Frecuentes'}
    return render(request, 'Teacher/faqs.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def changePassword(request):
    user = request.user
    group = user.groups.all()[0].name
    form = ChangePasswordForm(user)
    
    if request.method == 'POST':
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Su contraseña fue actualizada con éxito!')
            return render(request, 'Global/password-change-done.html', {'group': group})
        else:
            messages.error(request, 'Corrija el error a continuación.')
            
    context = {'group': group, 'form': form, 'title': 'Cambiar Contraseña'}
    return render(request, 'Global/change-password.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def createStudent(request):
    data = ['id_fotoUsuario', 'id_institutoSeguridadSocial', 'id_numSeguridadSocial', 'id_expediente', 'id_correoElectronico', 'id_curp', 'id_anteproyecto']
    formE = EstudianteForm()
    formU = CreateUserForm()
    mensaje = ''
    if request.method == 'POST':
        formE = EstudianteForm(request.POST)
        formU = CreateUserForm(request.POST)        
        if formE.is_valid() and formU.is_valid():
            pre_num_control = formE.cleaned_data.get('numControl')
            try:
                pre_estudiante = Estudiante_Autorizado.objects.get(num_control = pre_num_control)
            except:
                pre_estudiante = None
            
            if pre_estudiante:
                pre_estudiante.is_registrado = True
                pre_estudiante.save()
                                
                str_numControl = formE.cleaned_data['numControl']
                str_email = formU.cleaned_data['email'].split('@')[0]                
                pattern = r'^\D*{}$'.format(re.escape(str_numControl))
                                
                email_is_valid = re.match(pattern, str_email) is not None and str_email.endswith(str_numControl)
                
                if email_is_valid:
                    student = formE.save()
                    user = formU.save()                                
                    group = Group.objects.get(name='student')
                    user.username = student.numControl
                    user.groups.add(group)
                    user.is_active = False
                    user.save()            
                    student.correoElectronico = formU.cleaned_data.get('email')
                    student.user = user    
                    student.estudiante_aut = pre_estudiante
                    student.save()  

                    user_name = student.nombre
                    current_site = get_current_site(request)
                    subject = "Activa tu cuenta."
                    email_template_name = 'Global/email_verify/email_verify_template.txt'
                    c = {
                    "user_name": user_name,    
			        "email":user.email,
			        'domain':current_site.domain,
			        'site_name': 'ITO Sistemas',
			        "uid": urlsafe_base64_encode(force_bytes(user.pk)),			
			        "user": user,
			        'token': default_token_generator.make_token(user),
			        'protocol': 'http',
			        }                        

                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

                    return redirect('email_verification', student.id)
                else:
                    mensaje = 'El correo institucional debe pertenecer al mismo estudiante. Verifique que su correo no tenga errores.'
            else:
                mensaje = 'Lamentamos informarle que usted no cumple con los requisitos para realizar su residencia.'

    context = {'formE': formE, 'formU': formU, 'data': data, 'mensaje': mensaje}
    return render(request, 'Student/create-account.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def estudianteViewProfile(request):
    user = request.user
    estudiante = user.estudiante    
    group = user.groups.all()[0].name
    domicilio = estudiante.domicilio
    form = DomicilioForm(instance=domicilio)
    context = {'form': form, 'estudiante': estudiante, 'domicilio': domicilio, 'group': group, 'title': 'Perfil'}
    return render(request, 'Student/viewProfile.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def estudianteSettings(request):    
    user = request.user
    group = user.groups.all()[0].name
    estudiante = user.estudiante
    domicilio = estudiante.domicilio
    formE = EstudianteForm(instance = estudiante)
    formU = CreateUserFormEmail(instance = user)    
    
    if domicilio is None:
        formD = DomicilioForm()
        if request.method == 'POST':
            formD = DomicilioForm(request.POST)
            formE = EstudianteForm(
                request.POST, request.FILES, instance=estudiante)
            formU = CreateUserFormEmail(request.POST, instance = user)               
            if formE.is_valid() and formU.is_valid():
                formE.save()
                formU.save()
                correo = formU.cleaned_data['email']
                estudiante.correoElectronico = correo                
                if formD.is_valid():
                    dom = formD.save()
                    estudiante.domicilio = dom                    
                estudiante.save()
                return redirect('studentProfile')
    else:
        formD = DomicilioForm(instance=domicilio)        
        if request.method == 'POST':
            formD = DomicilioForm(request.POST, instance=domicilio)
            formE = EstudianteForm(
                request.POST, request.FILES, instance=estudiante)            
            formU = CreateUserFormEmail(request.POST, instance = user)              
            if formE.is_valid() and formU.is_valid():                
                formE.save()
                formU.save()
                correo = formU.cleaned_data['email']
                estudiante.correoElectronico = correo                
                estudiante.save()
                if formD.is_valid():
                    formD.save()                    
                return redirect('studentProfile')

    context = {'formD': formD, 'formE': formE, 'formU': formU, 'estudiante': estudiante, 'domicilio': domicilio, 'group': group, 'title': 'Configuracion'}
    return render(request, 'Student/settings.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def expediente(request):
    data = ['id_dictamen', 'id_solicitudResidencia', 'id_anteproyecto', 'id_horario', 'id_cartaAceptacion', 'id_cartaCompromiso', 'id_cronograma', 'id_cartaPresentacion']    
    # Documentos a los que se le agrega una fecha limite para su entrega (5 Dias)
    data2 = ['id_anteproyecto', 'id_cartaLiberacion']
    user = request.user
    group = user.groups.all()[0].name
    estudiante = user.estudiante
    semestre = estudiante.semestre
    expediente = estudiante.expediente 
    estatus_lista = ['FINALIZADO', 'COMPLETO']
    
    all_anteproyectos = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')    
    all_residencias = Estudiante_Residencia.objects.filter(estudiante = estudiante, estado = 'ACTIVO')        
    
    if all_anteproyectos:        
        anteproyecto = all_anteproyectos[0].anteproyecto    
    else:
        anteproyecto = None      
    
    if all_residencias:        
        residencia = all_residencias[0].residencia    
    else:
        residencia = None      
        
    r1 = None    
    r2 = None
    rF = None
    fecha20d = None            
    fecha6w = None     
    formE = ExpedienteViewForm()                 
        
    try:
        estatus = anteproyecto.estatus                       
    except:
        estatus = None
    
    if anteproyecto and estatus == 'ACEPTADO' and residencia.periodoInicio:              
        fecha20d = residencia.periodoInicio + timedelta(days=20)        
        fecha6w = residencia.periodoInicio + timedelta(weeks=6)         
                                
    if expediente is None:         
        if estatus == 'ACEPTADO' and residencia.periodoInicio:            
            formE = ExpedienteForm()        
            if request.method == 'POST':
                formE = ExpedienteForm(request.POST, request.FILES)                        
                if formE.is_valid():                                
                    expediente = formE.save()                
                    expediente.save() 
                    estudiante.expediente = expediente                                                    
                    estudiante.save()                          
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))                
                    
    else:        
        r1 = expediente.reporteParcial1
        r2 = expediente.reporteParcial2
        rF = expediente.reporteFinal
                
        formE = ExpedienteForm(instance=expediente)                
        if request.method == 'POST':            
            formE = ExpedienteForm(request.POST, request.FILES, instance=expediente)                                                         
                             
            if formE.is_valid():                     
                formE.save()    
                expediente_list = Expediente.objects.filter(id = expediente.id).values()[0]        
                if not expediente.estatus in estatus_lista:                    
                    expediente_completo = validar_expediente(expediente_list, expediente, semestre)            
                    if expediente_completo:
                        expediente.estatus = 'COMPLETO'                
                        expediente.save()  
                        #! Aqui se obtiene el correo de la jefa del departamento de vinculacion                
                        mensaje = ('Estudiante: ' + str(estudiante) + '\n' 
                        + 'Numero de Control: ' + str(estudiante.numControl) + '\n' 
                        + 'Semestre: ' + str(estudiante.semestre) + '\n' 
                        + 'El estudiante ha subido todos sus documentos pertenecientes a su expediente.' + '\n' + '\n'
                        + 'Atentamente,' + '\n' + 'La Oficina de Proyectos de Vinculación del Depto. de Sistemas y Computación.')
                        enviar_email('Expediente del estudiante completo', mensaje, ['destiono-jefadeptovinculacion@itoaxaca.edu.mx'])                                  
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))             
    context = {'form': formE, 'expediente': expediente, 'anteproyecto': anteproyecto, 'r1': r1, 'r2': r2, 'rF': rF, 'data': data, 'data2': data2, 'fecha20d': fecha20d, 'fecha6w': fecha6w, 'estatus': estatus, 'group': group, 'semestre': semestre, 'residencia': residencia, 'title': 'Expediente'}    
    return render(request, 'Student/expediente.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def reportes(request):
    user = request.user
    group = user.groups.all()[0].name
    estudiante = user.estudiante
    semestre = estudiante.semestre
    expediente = estudiante.expediente
    estatus_lista = ['FINALIZADO', 'COMPLETO']
    
    all_anteproyectos = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')    
    all_residencias = Estudiante_Residencia.objects.filter(estudiante = estudiante, estado = 'ACTIVO')        
    
    if all_anteproyectos:        
        anteproyecto = all_anteproyectos[0].anteproyecto    
    else:
        anteproyecto = None      
    
    if all_residencias:        
        residencia = all_residencias[0].residencia    
    else:
        residencia = None      
            
    r1 = None    
    r2 = None
    rF = None
    form1 = None
    form2 = None
    formF = None    
    r1_fechaEntrega = None            
    r2_fechaEntrega = None            
    rF_fechaEntrega = None  
    
    try:
        estatus = anteproyecto.estatus                       
    except:
        estatus = None      
        
    if anteproyecto and estatus == 'ACEPTADO' and residencia.periodoInicio:            
        fechaInicio = residencia.periodoInicio
        r1_fechaEntrega = fechaInicio + timedelta(weeks=6)        
        r2_fechaEntrega = r1_fechaEntrega + timedelta(weeks=12)
        rF_fechaEntrega = r2_fechaEntrega + timedelta(weeks=6)
        r1_fechaEntrega = r1_fechaEntrega.strftime("%d/%b/%Y")
        r2_fechaEntrega = r2_fechaEntrega.strftime("%d/%b/%Y")        
        rF_fechaEntrega = rF_fechaEntrega.strftime("%d/%b/%Y")
        
    if expediente is not None:     
        mensaje = ('Estudiante: ' + str(estudiante) + '\n' 
                + 'Numero de Control: ' + str(estudiante.numControl) + '\n' 
                + 'Semestre: ' + str(estudiante.semestre) + '\n' 
                + 'El estudiante ha subido todos sus documentos pertenecientes a su expediente.' + '\n' + '\n'
                + 'Atentamente,' + '\n' + 'La Oficina de Proyectos de Vinculación del Depto. de Sistemas y Computación.')
        expediente_list = Expediente.objects.filter(id = expediente.id).values()[0]               
        r1 = expediente.reporteParcial1
        r2 = expediente.reporteParcial2
        rF = expediente.reporteFinal                   
                               
        if r1 is None:            
            form1 = Reporte1Form()
            if request.method == 'POST':
                form1 = Reporte1Form(request.POST, request.FILES)                    
                if form1.is_valid():                    
                    r1 = form1.save()
                    expediente.reporteParcial1 = r1
                    expediente.save()
                    
                    if not expediente.estatus in estatus_lista:                        
                        expediente_completo = validar_expediente(expediente_list, expediente, semestre)            
                        if expediente_completo:
                            expediente.estatus = 'COMPLETO'                
                            expediente.save()  
                            #! Aqui se obtiene el correo de la jefa del departamento de vinculacion                                        
                            enviar_email('Expediente del estudiante completo', mensaje, ['destiono-jefadeptovinculacion@itoaxaca.edu.mx'])                                  
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))        
        else:                        
            form1 = Reporte1Form(instance = r1)                  
            if not r1.r1_formatoEvaluacion or not r1.r1_hojaRevisores:
                if request.method == 'POST':
                    form1 = Reporte1Form(request.POST, request.FILES, instance = r1)                                                                                     
                    if form1.is_valid():                                                            
                        r1 = form1.save()  
                        expediente.reporteParcial1 = r1
                        expediente.save()
                        
                        if not expediente.estatus in estatus_lista:                            
                            expediente_completo = validar_expediente(expediente_list, expediente, semestre)            
                            if expediente_completo:
                                expediente.estatus = 'COMPLETO'                
                                expediente.save()  
                                #! Aqui se obtiene el correo de la jefa del departamento de vinculacion                                        
                                enviar_email('Expediente del estudiante completo', mensaje, ['destiono-jefadeptovinculacion@itoaxaca.edu.mx'])                                  
                        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))                                                                        
            
        if r2 is None:            
            form2 = Reporte2Form()
            if request.method == 'POST':
                form2 = Reporte2Form(request.POST, request.FILES)                
                if form2.is_valid():                     
                    r2 = form2.save()
                    expediente.reporteParcial2 = r2
                    expediente.save()
                    
                    if not expediente.estatus in estatus_lista:                        
                        expediente_completo = validar_expediente(expediente_list, expediente, semestre)
            
                        if expediente_completo:
                            expediente.estatus = 'COMPLETO'                
                            expediente.save()  
                            #! Aqui se obtiene el correo de la jefa del departamento de vinculacion                                        
                            enviar_email('Expediente del estudiante completo', mensaje, ['destiono-jefadeptovinculacion@itoaxaca.edu.mx'])                                  
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:            
            form2 = Reporte2Form(instance = r2)                          
            if not r2.r2_formatoEvaluacion or not r2.r2_hojaRevisores:
                if request.method == 'POST':                
                    form2 = Reporte2Form(request.POST, request.FILES, instance = r2)                     
                    if form2.is_valid():                            
                        r2 = form2.save()  
                        expediente.reporteParcial2 = r2
                        expediente.save()
                        
                        if not expediente.estatus in estatus_lista:                            
                            expediente_completo = validar_expediente(expediente_list, expediente, semestre)
                            if expediente_completo:
                                expediente.estatus = 'COMPLETO'                
                                expediente.save()  
                                #! Aqui se obtiene el correo de la jefa del departamento de vinculacion                                        
                                enviar_email('Expediente del estudiante completo', mensaje, ['destiono-jefadeptovinculacion@itoaxaca.edu.mx'])                                  
                        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            
        if rF is None:            
            formF = ReporteFinalForm()
            if request.method == 'POST':
                formF = ReporteFinalForm(request.POST, request.FILES)                                                                
                if formF.is_valid():                      
                    rF = formF.save()
                    expediente.reporteFinal = rF
                    expediente.save()
                    
                    if not expediente.estatus in estatus_lista:                        
                        expediente_completo = validar_expediente(expediente_list, expediente, semestre)
            
                        if expediente_completo:
                            expediente.estatus = 'COMPLETO'                
                            expediente.save()  
                            #! Aqui se obtiene el correo de la jefa del departamento de vinculacion                                        
                            enviar_email('Expediente del estudiante completo', mensaje, ['destiono-jefadeptovinculacion@itoaxaca.edu.mx'])                                  
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:            
            formF = ReporteFinalForm(instance = rF)                        
            if not rF.rf_formatoEvaluacion or not rF.rf_hojaRevisores:        
                if request.method == 'POST':
                    formF = ReporteFinalForm(request.POST, request.FILES, instance = rF)                                                
                    if formF.is_valid():                        
                        rF = formF.save()  
                        expediente.reporteFinal = rF
                        expediente.save()
                        
                        if not expediente.estatus in estatus_lista:                            
                            expediente_completo = validar_expediente(expediente_list, expediente, semestre)
            
                            if expediente_completo:
                                expediente.estatus = 'COMPLETO'                
                                expediente.save()  
                                #! Aqui se obtiene el correo de la jefa del departamento de vinculacion                                        
                                enviar_email('Expediente del estudiante completo', mensaje, ['destiono-jefadeptovinculacion@itoaxaca.edu.mx'])                                  
                        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))      
    else:        
        form1 = Reporte1Form()                       
        form2 = Reporte2Form()                       
        formF = ReporteFinalForm()
        if request.method == 'POST':
            form1 = Reporte1Form(request.POST, request.FILES)                    
            if form1.is_valid():                    
                r1 = form1.save()
                expediente_e = Expediente.objects.create(reporteParcial1=r1)
                estudiante.expediente = expediente_e
                estudiante.save()                          
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))        
            
    context = {'expediente': expediente, 'anteproyecto': anteproyecto, 'residencia': residencia, 'form1': form1, 'form2': form2, 'formF': formF, 'r1': r1, 'r2': r2, 'rF': rF, 'r1_fechaEntrega': r1_fechaEntrega, 'r2_fechaEntrega': r2_fechaEntrega, 'rF_fechaEntrega': rF_fechaEntrega, 'estatus': estatus, 'group': group, 'title': 'Reportes'}
    return render(request, 'Student/reportes.html', context)    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)    
@login_required(login_url='login')
def anteproyecto(request):
    data = ['id_codigoUnion', 'id_estatus', 'id_docentes', 'id_dependencia', 'id_asesorExterno', 'id_periodoInicio_month', 'id_periodoFin_month']
    user = request.user
    group = user.groups.all()[0].name
    estudiante = user.estudiante                    
    anteproyectos = Anteproyecto.objects.all()    
    all_anteproyectos = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')    
    if all_anteproyectos:        
        anteproyecto = all_anteproyectos[0].anteproyecto
        all_estudiantes = Estudiante_Anteproyecto.objects.filter(anteproyecto = anteproyecto)            
        estudiantes = [i.estudiante for i in all_estudiantes ]        
    else:
        anteproyecto = None            
        estudiantes = None        
        
    fechaObservacion = None
    fechaCorte = None
    fechaActual = None
    dependencia = None
    revisor1 = None
    revisor2 = None
    observaciones = None  
    formDoc = None
    tiempo_restante = 1   
                                   
    enviados = anteproyectos.exclude(codigoUnion='0000000000').filter(estatus='ENVIADO')                    
    codigo = '0000000000'     
    mensaje = ''       
    
    try:        
        observacion = anteproyecto.observacion
        fechaObservacion = observacion.fechaCreacion    
        observaciones = ObservacionDocente.objects.filter(observacion = observacion).order_by('-fechaElaboracion')                                
        dias = 5 + observacion.incrementarDias
        fechaObservacion = fechaObservacion + timedelta(days=dias)           
        fechaCorte = fechaObservacion + timedelta(days=1)             
        #fechaActual = date.today
        fechaActual = datetime.now().date()        
        
        tiempo_restante = fechaObservacion - fechaActual
        tiempo_restante = tiempo_restante.days
        tiempo_restante = max(0, tiempo_restante)
        
        fechaObservacion = fechaObservacion.strftime("%d/%b/%Y")               
    except:
        pass
    
    if anteproyecto is None:     
        try:
            invitacion = Invitacion.objects.get(estudiante_destinatario = estudiante.estudiante_aut)
        except:
            invitacion = None        
        formA = AnteproyectoEstForm()                
                
        if request.method == 'POST':          
            try:
                codigoU = request.POST['codigoAnteproyecto']
            except:
                codigoU = None
                                                
            if codigoU:                
                for i in enviados:                    
                    if i.codigoUnion == codigoU:                                                
                        numIntegrantes = Estudiante_Anteproyecto.objects.filter(anteproyecto=i).count()                                                
                        if numIntegrantes < i.numIntegrantes:                            
                            Estudiante_Anteproyecto.objects.create(estudiante=estudiante, anteproyecto=i)                            
                            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                        else:
                            mensaje = 'El anteproyecto al que intenta unirse ya cuenta con todos sus integrantes.'                            
                                                        
                if not mensaje: mensaje = 'Codigo invalido'                                                        
            else:                                              
                formA = AnteproyectoEstForm(request.POST, request.FILES)                                                                                                    
                if formA.is_valid():                                                                        
                    anteproyecto = formA.save()                    
                    if int(request.POST['numIntegrantes']) > 1:  
                        codigo = obtenerCodigo()                                                                                                                                    
                    anteproyecto.codigoUnion=codigo
                    anteproyecto.save()
                    Estudiante_Anteproyecto.objects.create(estudiante=estudiante, anteproyecto=anteproyecto)                                                                                 
                    return redirect('materias')                                        
        context = {'formA': formA, 'mensaje':mensaje, 'anteproyecto': anteproyecto, 'estudiantes': estudiantes, 'dependencia': dependencia, 'group': group,  'title': 'Registro Anteproyecto', 'invitacion': invitacion}    
        return render(request, 'Student/anteproyecto.html', context)
                    
    else:
        anteproyecto_materia = Anteproyecto_materia.objects.filter(anteproyecto = anteproyecto)        
                
        estudiantes_anteproyecto = Estudiante_Anteproyecto.objects.filter(anteproyecto = anteproyecto).count()                
        invitaciones = Invitacion.objects.filter(anteproyecto = anteproyecto)
        num_invitaciones = invitaciones.count()
        num_integrantes = estudiantes_anteproyecto + num_invitaciones
        
        
        if anteproyecto.numIntegrantes > num_integrantes:            
            invitar = True
        else:            
            invitar = False
        
        if anteproyecto_materia:
            data.clear()
            data.extend(['id_docentes', 'id_dependencia', 'id_asesorExterno', 'id_domicilio', 'id_titular', 'id_mision', 'id_d_nombre', 'id_calle'])    
            estados = ['ENVIADO', 'PENDIENTE', 'EN REVISION']                                     
            actualizaciones = Actualizacion_anteproyecto.objects.filter(anteproyecto = anteproyecto).order_by('-fecha')
            if anteproyecto.numIntegrantes == 1:            
                data.append('id_codigoUnion')  
                
            if anteproyecto.estatus in estados and tiempo_restante < 1:
                mensaje_dias = True
            else:
                mensaje_dias = False
            
            revisor1 = anteproyecto.revisor1
            revisor2 = anteproyecto.revisor2                 
            dependencia = anteproyecto.dependencia   
            
            if dependencia:
                titular = dependencia.titular
                domicilio = dependencia.domicilio
            else:
                titular = None
                domicilio = None               
            formA = AnteproyectoViewForm(instance = anteproyecto)                                        
            formD = DependenciaViewForm(instance = dependencia)
            formT = TitularViewForm(instance = titular)
            formDom = DomicilioViewForm(instance = domicilio)
            formDoc = AnteproyectoDocForm(instance = anteproyecto)
            formAE = AsesorEViewForm(instance = anteproyecto.asesorExterno)     
            
            if request.method == 'POST':                     
                formDoc = AnteproyectoDocForm(request.POST, request.FILES, instance=anteproyecto)                
                if formDoc.is_valid():   
                    formDoc.save()
                    actualizacion = Actualizacion_anteproyecto(anteproyecto = anteproyecto, descripcion = 'Se actualizó el documento del Anteproyecto')
                    actualizacion.save()
                    email_list = []
                    if revisor1:
                        email_list.append(revisor1.correoElectronico)
                    if revisor2:
                        email_list.append(revisor2.correoElectronico)
                    mensaje_email = ('Nombre del anteproyecto: ' + anteproyecto.a_nombre + '\n'
                                     + 'Se han realizado las correcciones necesarias en el documento del anteproyecto. Revisar las correcciones lo ' 
                                     + 'mas pronto posible.' + '\n' + '\n' 
                                     + 'Atentamente,' + "\n" + 'La Oficina de Proyectos de Vinculación del Depto. de Sistemas y Computación.')
                    enviar_email('Actualizacion Documento Anteproyecto', mensaje_email, email_list)
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))                                       
                else:
                    anteproyecto.anteproyectoDoc = None                                        
                    
            context = {'formA': formA, 'formD': formD, 'formT': formT, 'formAE': formAE ,'formDom': formDom, 'formDoc': formDoc, 'data': data, 'mensaje':mensaje, 'anteproyecto': anteproyecto, 'estudiantes': estudiantes, 'dependencia': dependencia, 'group': group, 'observaciones': observaciones, 'revisor1': revisor1, 'revisor2': revisor2, 'fechaObservacion': fechaObservacion, 'fechaCorte': fechaCorte, 'fechaActual': fechaActual, 'title': 'Anteproyecto', 'actualizaciones': actualizaciones, 'anteproyecto_materia': anteproyecto_materia, 'invitar': invitar, 'invitaciones': invitaciones, 'tiempo_restante': tiempo_restante, 'mensaje_dias': mensaje_dias}    
            return render(request, 'Student/anteproyecto.html', context)
        else:
            return redirect('materias')                                                        

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def dependencias(request, page, orderB):
    user = request.user
    group = user.groups.all()[0].name
    estudiante = user.estudiante  
    #anteproyecto = estudiante.anteproyecto   
    anteproyecto = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')[0].anteproyecto        
    dependencia = anteproyecto.dependencia
    all_dependencias = Dependencia.objects.all()               
    start = (page-1)*10    
    end = page*10
    
    if request.method == 'POST':        
        text = request.POST['search'] 
                        
        if text:            
            all_dependencias = all_dependencias.filter(d_nombre__icontains=text)
            dependencias = all_dependencias
            start = 0
            end = dependencias.count()
            totalD = all_dependencias.count()                        
            search = '.'             
            context = {'group': group, 'anteproyecto': anteproyecto, 'dependencia': dependencia, 'dependencias': dependencias, 'totalD': totalD, 'page': page, 'start': start+1, 'end': end, 'orderB': orderB, 'search': search, 'filter': filter, 'title': 'Anteproyectos'}
            return render(request, 'Student/dependencia.html', context)    
    
    all_dependencias = ordenar_dependencias(all_dependencias, orderB)                
    dependencias = all_dependencias[start:end]
    if end != dependencias.count():
        end = end-10+dependencias.count()
    totalD = all_dependencias.count()
    n_buttons = math.ceil(totalD/10)
    buttons = [item for item in range(1, n_buttons+1)]
    next_page = page+1
    prev_page = page-1    
    
    context = {'anteproyecto': anteproyecto, 'dependencia': dependencia, 'group': group, 'dependencias': dependencias, 'start': start+1, 'end': end, 'totalD': totalD, 'n_buttons': n_buttons , 'buttons': buttons, 'next_page': next_page, 'prev_page': prev_page, 'page': page, 'orderB': orderB, 'title': 'Organizaciones o Empresas'}    
    return render(request, 'Student/dependencia.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def asignar_dependencia(request, pk):    
    estudiante = request.user.estudiante                    
    #anteproyecto = estudiante.anteproyecto
    anteproyecto = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')[0].anteproyecto        
    dependencia = Dependencia.objects.get(id = pk)
    anteproyecto.dependencia = dependencia
    anteproyecto.save()    
    return redirect('anteproyecto')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def alta_dependencia(request):
    user = request.user
    group = user.groups.all()[0].name
    estudiante = user.estudiante                    
    #anteproyecto = estudiante.anteproyecto
    anteproyecto = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')[0].anteproyecto        
    dependencia = anteproyecto.dependencia
    dependencias = Dependencia.objects.all()
    formD = DependenciaForm()    
    
    if request.method == 'POST':
        formD = DependenciaForm(request.POST)        
        if formD.is_valid():
            dependencia = formD.save()                                    
            dependencia.save()
            anteproyecto.dependencia = dependencia
            anteproyecto.save()
            return redirect('alta_titular_d')                                                
    
    context = {'anteproyecto': anteproyecto, 'dependencia': dependencia, 'formD': formD, 'group': group, 'dependencias': dependencias,'title': 'Registro Organización o Empresa '}    
    return render(request, 'Student/altaDependencia.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def alta_titular_d(request):
    user = request.user
    group = user.groups.all()[0].name
    estudiante = user.estudiante                    
    #anteproyecto = estudiante.anteproyecto
    anteproyecto = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')[0].anteproyecto        
    dependencia = anteproyecto.dependencia
    formT = TitularForm()
    
    if request.method == 'POST':
        formT = TitularForm(request.POST)
        if formT.is_valid():
            titular = formT.save()
            titular.save()
            dependencia.titular = titular
            dependencia.save()
            if not dependencia.domicilio:
                return redirect('alta_domicilio_d')                                                            
            else:
                return redirect('anteproyecto')                                                
    
    context = {'anteproyecto': anteproyecto, 'dependencia': dependencia, 'formT': formT, 'group': group, 'dependencias': dependencias,'title': 'Alta Dependencia'}    
    return render(request, 'Student/altaTitularD.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def alta_domicilio_d(request):
    user = request.user
    group = user.groups.all()[0].name
    estudiante = user.estudiante                    
    #anteproyecto = estudiante.anteproyecto
    anteproyecto = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')[0].anteproyecto        
    dependencia = anteproyecto.dependencia
    formDom = DomicilioForm()
    
    if request.method == 'POST':
        formDom = DomicilioForm(request.POST)
        if formDom.is_valid():
            domicilio = formDom.save()
            domicilio.save()
            dependencia.domicilio = domicilio
            dependencia.save()
            if not dependencia.titular:
                return redirect('alta_titular_d')                                                            
            else:
                return redirect('anteproyecto')                                                
    
    context = {'anteproyecto': anteproyecto, 'dependencia': dependencia, 'formDom': formDom, 'group': group, 'dependencias': dependencias,'title': 'Alta Dependencia'}    
    return render(request, 'Student/altaDomicilioD.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def asesoresE(request):
    user = request.user
    group = user.groups.all()[0].name
    estudiante = user.estudiante
    #anteproyecto = estudiante.anteproyecto
    anteproyecto = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')[0].anteproyecto        
    asesorE = None    
    dependencia = None
    all_asesores = None
    if anteproyecto:        
        asesoreE = anteproyecto.asesorExterno
        dependencia = anteproyecto.dependencia
        all_asesores = AsesorExterno.objects.filter(dependencia=dependencia)
        
    context = {'group': group, 'asesorE': asesorE, 'dependencia': dependencia, 'all_asesores': all_asesores, 'title': 'Asesores Externos'}
    return render(request, 'Student/asesoresExt.html', context)

def asignar_asesorE(request, pk):
    user = request.user
    group = user.groups.all()[0].name
    estudiante = user.estudiante
    #anteproyecto = estudiante.anteproyecto
    anteproyecto = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')[0].anteproyecto        
    asesorE = AsesorExterno.objects.get(id = pk)
    anteproyecto.asesorExterno = asesorE
    anteproyecto.save()
    return redirect('anteproyecto')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def alta_asesorE(request):
    user = request.user
    group = user.groups.all()[0].name
    estudiante = user.estudiante
    #anteproyecto = estudiante.anteproyecto
    anteproyecto = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')[0].anteproyecto        
    asesorE = None
    dependencia = None
    form = AsesorEForm()
    if anteproyecto:
        asesorE = anteproyecto.asesorExterno
        dependencia = anteproyecto.dependencia
    
    if request.method == 'POST':
        form = AsesorEForm(request.POST)
        if form.is_valid():
            asesorE = form.save()
            asesorE.dependencia = dependencia
            asesorE.save()            
            anteproyecto.asesorExterno = asesorE
            anteproyecto.save()
            return redirect('anteproyecto')
    context = {'group': group, 'asesorE': asesorE, 'dependencia':dependencia, 'form': form, 'title': 'Alta Asesor Externo'}
    return render(request, 'Student/altaAsesorE.html', context)            

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')    
def editarAnteproyecto(request):    
    data = ['id_docentes', 'id_dependencia', 'id_asesorExterno', 'id_estatus', 'id_codigoUnion', 'id_domicilio', 'id_titular']
    group = request.user.groups.all()[0].name
    estudiante = request.user.estudiante         
    #anteproyecto = estudiante.anteproyecto
    anteproyecto = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')[0].anteproyecto        
    #estudiantes = Estudiante.objects.filter(anteproyecto = anteproyecto).count()                    
    all_estudiantes = Estudiante_Anteproyecto.objects.filter(anteproyecto = anteproyecto)            
    estudiantes = [i.estudiante for i in all_estudiantes ]        
    
    codigo = anteproyecto.codigoUnion
    numIntegrantes = anteproyecto.numIntegrantes
    mensaje = ''
    
    formA = AnteproyectoEditForm(instance = anteproyecto)                                                    
    
    if request.method == 'POST':                        
        formA = AnteproyectoEditForm(request.POST, instance = anteproyecto)                                          
                  
        if formA.is_valid():
            numIntegrantes2 = int(formA['numIntegrantes'].value())                        
            
            if numIntegrantes2 < 1:
                mensaje = 'El numero de integrantes no puede ser menor a 1'
            else:                
                if numIntegrantes == 1 and numIntegrantes2 >= 2:                    
                    codigo = obtenerCodigo()                    
                elif numIntegrantes >= 2 and numIntegrantes2 == 1 and estudiantes == 1:                    
                    codigo = '0000000000'                     
                                                                                                                                                                        
                if numIntegrantes > numIntegrantes2 and estudiantes > numIntegrantes2:                                        
                    mensaje = 'No se puede reducir el numero de integrantes. No se pueden eliminar integrantes'                    
                else:                                                                    
                    anteproyecto = formA.save()                                      
                    anteproyecto.save() 
                    return redirect('anteproyecto')                               
    
    context = {'formA': formA, 'data': data, 'anteproyecto': anteproyecto, 'mensaje': mensaje, 'group': group, 'title': 'Editar Anteproyecto'}    
    return render(request, 'Student/editarAnteproyecto.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def proyectoResidencia(request):
    data = ['id_codigoUnion', 'id_nombre', 'id_d_nombre', 'id_mision', 'id_calle']
    user = request.user
    group = user.groups.all()[0].name
    estudiante = user.estudiante        
    
    all_anteproyectos = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')    
    all_residencias = Estudiante_Residencia.objects.filter(estudiante = estudiante, estado = 'ACTIVO')        
    
    if all_anteproyectos:        
        anteproyecto = all_anteproyectos[0].anteproyecto    
    else:
        anteproyecto = None      
    
    if all_residencias:        
        residencia = all_residencias[0].residencia    
    else:
        residencia = None      
                                        
    mensaje = ''
        
    if residencia:                                                
        dependencia = residencia.dependencia                   
        asesorI = residencia.r_asesorInterno
        revisor = residencia.r_revisor
        #estudiantes = Estudiante.objects.filter(residencia = residencia)                
        all_estudiantes = Estudiante_Residencia.objects.filter(residencia = residencia)            
        estudiantes = [i.estudiante for i in all_estudiantes ]                    
        formR = ResidenciaViewForm(instance = residencia)   
        formRDate = ResidenciaDateForm(instance = residencia)                                
        formD = DependenciaViewForm(instance = dependencia)
        formT = TitularViewForm(instance = dependencia.titular)
        formDom = DomicilioViewForm(instance = dependencia.domicilio)
        formAE = AsesorEViewForm(instance = residencia.asesorExterno)     
        
        if request.method == 'POST':            
            formRDate = ResidenciaDateForm(request.POST, instance=residencia) 
            if formRDate.is_valid():
                formRDate.save()
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))                                                                        
            else:
                mensaje = 'Por favor, ingrese una fecha valida'            
                                                   
        context = {'group': group, 'mensaje': mensaje ,'formR': formR, 'formRDate': formRDate, 'formD': formD, 'formT': formT, 'formAE': formAE ,'formDom': formDom,'data': data, 'anteproyecto': anteproyecto, 'estudiantes': estudiantes, 'dependencia': dependencia, 'residencia': residencia, 'asesorI': asesorI, 'revisor': revisor, 'title': 'Residencia'}
        return render(request, 'Student/residencia.html', context)
        
    context = {'group': group, 'residencia': residencia, 'title': 'Residencia'}
    return render(request, 'Student/residencia.html', context)

@login_required(login_url='login')  
def removeDoc(request, pk):
    anteproyecto = Anteproyecto.objects.get(id = pk)
    anteproyecto.anteproyectoDoc.delete()        
    actualizacion = Actualizacion_anteproyecto(anteproyecto = anteproyecto, tipo='REMOVIDO', descripcion = 'Se removió el documento del Anteproyecto')
    actualizacion.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))        

def logoutUser(request):
    logout(request)
    return redirect('login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
def compatibilidadA(request, materiaPK):
    group = request.user.groups.all()[0].name
    estudiante = request.user.estudiante
    all_anteproyectos = Estudiante_Anteproyecto.objects.filter(estudiante = estudiante, estado = 'ACTIVO')    
    if all_anteproyectos:        
        anteproyecto = all_anteproyectos[0].anteproyecto    
    else:
        anteproyecto = None      
    materia = Materia.objects.get(id = materiaPK)
      
    if request.method == 'POST':        
        compatibilidad = int(request.POST['Compatibilidad'])
        anteproyecto_materia = Anteproyecto_materia(anteproyecto=anteproyecto, materia=materia, compatibilidad=compatibilidad)
        anteproyecto_materia.save()
        return redirect('materias')
        
    context = {'group': group, 'materia': materia, 'title': 'Comptabilidad'}    
    return render(request, 'Student/compatibilidadA.html', context)

@login_required(login_url='login')
def eliminar_materia(request, pk, materiaPK):
    anteproyecto = Anteproyecto.objects.get(id = pk)
    materia = Materia.objects.get(id = materiaPK)
    anteproyecto_materia = Anteproyecto_materia.objects.get(anteproyecto = anteproyecto, materia = materia)
    anteproyecto_materia.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required(login_url='login')
@student_only
def invitar(request, pk, page):
    group = request.user.groups.all()[0].name                
    anteproyecto = Anteproyecto.objects.get(id = pk)        
    all_estudiantes_aut = Estudiante_Autorizado.objects.all()
    estudiantes_ant = Estudiante_Anteproyecto.objects.filter(estado = 'ACTIVO')
    lista_ids = [estudiante_ant.estudiante.estudiante_aut.id for estudiante_ant in estudiantes_ant]   
    lista_est_invitados = Invitacion.objects.filter(estudiante_destinatario__in = all_estudiantes_aut).values_list('estudiante_destinatario_id', flat=True)   
    if lista_est_invitados:        
        lista_ids.extend(list(set(lista_est_invitados) - set(lista_ids)))
    all_estudiantes = all_estudiantes_aut.exclude(id__in = lista_ids)    
    start = (page-1)*10    
    end = page*10    
    search = None
               
    if request.method == 'POST':
        opc = int(request.POST['search_options'])
        text = request.POST['search'].upper()    
        search = True
        if opc == 1:                     
            all_estudiantes = all_estudiantes.filter(nombre_completo__contains = text)
        elif opc == 2:    
            try:
                all_estudiantes = all_estudiantes.filter(num_control__contains = text)
            except:
                all_estudiantes = None            
                
    estudiantes = all_estudiantes[start:end]    
    if end != estudiantes.count():
        end = end-10+estudiantes.count()
    totalE = all_estudiantes.count()
    n_buttons = math.ceil(totalE/10)
    buttons = [item for item in range(1, n_buttons+1)]
    next_page = page+1
    prev_page = page-1 
    
    context  = {'group': group, 'title': 'Invitar estudiante', 'anteproyecto': anteproyecto, 'estudiantes': estudiantes, 'totalE': totalE, 'buttons': buttons, 'page': page, 'start': start+1, 'end': end, 'next_page': next_page, 'prev_page': prev_page, 'n_buttons': n_buttons, 'search': search}
    return render(request, 'Student/invitar_e.html', context)

def crear_invitacion(request, pk_e, pk_a):    
    estudiante = request.user.estudiante         
    anteproyecto = Anteproyecto.objects.get(id = pk_a)
    estudiante_aut = Estudiante_Autorizado.objects.get(id = pk_e)    
    invitacion = Invitacion.objects.create(estudiante_remitente = estudiante, estudiante_destinatario = estudiante_aut, anteproyecto = anteproyecto)
    return redirect('anteproyecto')        

def aceptar_invitacion(request, pk):
    estudiante = request.user.estudiante         
    invitacion = Invitacion.objects.get(id = pk)
    anteproyecto = invitacion.anteproyecto        
    anteproyecto_est = Estudiante_Anteproyecto.objects.create(estudiante = estudiante, anteproyecto = anteproyecto)
    invitacion.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))        

def rechazar_invitacion(request, pk):
    invitacion = Invitacion.objects.get(id = pk)
    invitacion.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))        

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = ResetPasswordForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "Global/password_reset/password_reset_email.txt"
                    c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = ResetPasswordForm()
    return render(request=request, template_name="Global/password_reset/forgot-password.html", context={"password_reset_form":password_reset_form})
    
def generarCodigo():            
    length = 10
    letters = string.ascii_uppercase
    code = ''.join(random.choice(letters + string.digits) for i in range(length))                        
    return code   

def obtenerCodigo():
    while True:        
        codigo = generarCodigo()
        if not buscarCodigo(codigo):
            return codigo        
     
def buscarCodigo(codigo):
    proyectos = Anteproyecto.objects.exclude(codigoUnion='0000000000').filter(estatus='Enviado')     
    for p in proyectos:
        if p.codigoUnion == codigo:
            return True
    return False

def ordenar_dependencias(dependencias, orderB):
    all_dependencias = dependencias
    if orderB == 1:
        all_dependencias = all_dependencias.order_by('d_nombre')    
    elif orderB == 2:
        all_dependencias = all_dependencias.order_by('-d_nombre')    
    return all_dependencias
    
def convert_to_localtime(utctime):
    fmt = '%d-%m-%Y %H:%M'
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    return localtz.strftime(fmt)

def activate_user(request, uidb64, token):
    User = get_user_model()
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
                
    if user and default_token_generator.check_token(user, token):
        
        if user.is_active:
            return redirect('404')
        
        user.is_active = True        
        user.save()
        return render(request, 'Global/email_verify/email_verified.html')
    else:
        return HttpResponse('Activation link is invalid!')

def validar_expediente(expediente_list, expediente, semestre):
    expediente_completo = True    
    for i in expediente_list:
        if not expediente_list[i]:            
            if i == 'dictamen':
                if semestre > 12:                            
                    expediente_completo = False
            else:
                expediente_completo = False                                
            
    # Si el expediente esta completo -> Refiriendose a todos los documentos principales del expediente    
    if expediente_completo:        
        reporte1 = ReporteParcial1.objects.filter(id = expediente.reporteParcial1.id).values()[0]
        reporte2 = ReporteParcial2.objects.filter(id = expediente.reporteParcial2.id).values()[0]
        reporteF = ReporteFinal.objects.filter(id = expediente.reporteFinal.id).values()[0]
        all_reportes = [reporte1['r1_hojaRevisores'], reporte1['r1_formatoEvaluacion'], reporte2['r2_hojaRevisores'], reporte2['r2_formatoEvaluacion'], reporteF['rf_hojaRevisores'], reporteF['rf_formatoEvaluacion']]                        
    else:
        all_reportes = []    
    for i in all_reportes:
        if not i:            
            expediente_completo = False
                        
    return expediente_completo