from django.contrib.auth import views as auth_views
from django.urls import path, register_converter
from .views import *
from .adminViews import *
from .teacherViews import *
import uuid

urlpatterns = [    
    # Globales           
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('404/', errorPage, name='404'),    
    path('email_verification/<uuid:pk>', email_verification, name='email_verification'),    
    path('', home, name='home'),   
    path('changePassword', changePassword, name='changePassword'), 
    path('student/', studentPage, name='student'),
    path('teacher/', teacherPage, name='teacher'),
    path('createStudent/', createStudent, name='createStudent'),                    
    path('faqs/', faqs, name='faqs'),                    
    path('faqs_s/', student_faqs, name='student_faqs'),                    
    path('faqs_t/', teacher_faqs, name='teacher_faqs'),   
    path('password_reset', password_reset_request, name='password_reset'),    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Global/password_reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="Global/password_reset/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='Global/password_reset/password_reset_complete.html'), name='password_reset_complete'),             
    path('activate_user/<uidb64>/<token>/', activate_user, name='activate_user'),    
    
    # Estudiante                
    path('profile/', estudianteViewProfile, name='studentProfile'),
    path('settings/', estudianteSettings, name='studentSettings'),
    path('expediente/', expediente, name='expediente'),    
    path('anteproyecto/', anteproyecto, name='anteproyecto'),
    path('dependencias/<int:page>/<int:orderB>', dependencias, name='dependencias'),
    path('asignarDependencia/<uuid:pk>', asignar_dependencia, name='asignar_dependencia'),
    path('altaDependencia/', alta_dependencia, name='alta_dependencia'),
    path('altaTitularD/', alta_titular_d, name='alta_titular_d'),
    path('altaDomicilioD/', alta_domicilio_d, name='alta_domicilio_d'),
    path('asesoresExternos/', asesoresE, name='asesoresExternos'),
    path('asignarAsesorE/<uuid:pk>', asignar_asesorE, name='asignar_asesorE'),
    path('altaAsesorE/', alta_asesorE, name='alta_asesorE'),
    path('editAnteproyecto/', editarAnteproyecto, name='editarAnteproyecto'),
    path('reportes/', reportes, name='reportes'),    
    path('removeDoc/<uuid:pk>', removeDoc, name='removeDoc'),    
    path('residencia/', proyectoResidencia, name='residencia'),  
      
    path('compatibilidadA/<materiaPK>', compatibilidadA, name='compatibilidadA'),    
    path('eliminar_materia/<uuid:pk>/<materiaPK>', eliminar_materia, name='eliminar_materia'),    
            
    path('invitar/<uuid:pk>/<int:page>', invitar, name='invitar'),    
    path('crear_invitacion/<uuid:pk_e>/<uuid:pk_a>', crear_invitacion, name='crear_invitacion'),    
    path('aceptar_invitacion/<uuid:pk>', aceptar_invitacion, name='aceptar_invitacion'),    
    path('rechazar_invitacion/<uuid:pk>', rechazar_invitacion, name='rechazar_invitacion'),    
        
    # Admin
    path('anteproyectos/<int:page>/<int:orderB><int:filter>', anteproyectos, name='anteproyectos'),    
    path('residencias/<int:page>/<int:orderB><int:filter>', residencias, name='residencias'),        
    path('expedientes/<int:page>/<int:orderB><int:filter>', expedientes, name='expedientes'),        
    path('estudiantes/<int:page>/<int:orderB>', estudiantes, name='estudiantes'),        
    path('docentes/<int:page>/<int:orderB>', docentes, name='docentes'),           
    path('materias_a/<int:page>/<int:orderB>/<int:filter>', materias_a, name='materias_a'),           
    path('dependencias_a/<int:page>/<int:orderB>/<int:filter>', dependencias_a, name='dependencias_a'),           
    
    path('verExpediente/<uuid:pk>', verExpediente, name='verExpediente'),           
    path('eliminarExpediente/<uuid:pk>', eliminarExpediente, name='eliminarExpediente'),           
     
    path('verAnteproyecto/<uuid:pk>', verAnteproyecto, name='verAnteproyecto'),        
    path('editarAnteproyectoAdmin/<uuid:pk>', editarAnteproyectoAdmin, name='editarAnteproyectoAdmin'),        
    path('eliminarAnteproyecto/<uuid:pk>', eliminarAnteproyecto, name='eliminarAnteproyecto'),        
    
    path('editarObservaciones/<uuid:pk>', editarObservaciones, name='editarObservaciones'),        
    path('eliminarObservacion/<uuid:pk>', eliminarObservacion, name='eliminarObservacion'),   
    
    path('verEstudiante/<uuid:pk>', verEstudiante, name='verEstudiante'),       
    path('editarEstudiante/<uuid:pk>', editarEstudiante, name='editarEstudiante'),       
    path('removeEstudiante/<uuid:pk>', removeEstudiante, name='removeEstudiante'),       
    
    path('asignarRevisor1/<int:page>/<uuid:pk>', asignarRevisor1, name='asignarRevisor1'),           
    path('asignarRevisor1I/<uuid:pkA>/<uuid:pkD>', asignarRevisor1I, name='asignarRevisor1I'),           
    path('removeRevisor1/<uuid:pk>', removeRevisor1, name='removeRevisor1'),           
    
    path('asignarRevisor2/<int:page>/<uuid:pk>', asignarRevisor2, name='asignarRevisor2'),           
    path('asignarRevisor2I/<uuid:pkA>/<uuid:pkD>', asignarRevisor2I, name='asignarRevisor2I'),           
    path('removeRevisor2/<uuid:pk>', removeRevisor2, name='removeRevisor2'),           
    
    path('asignarAsesorIL/<int:page>/<uuid:pk>', asignarAsesorIL, name='asignarAsesorIL'),           
    path('asignarAsesorI/<uuid:pkR>/<uuid:pkD>', asignarAsesorI, name='asignarAsesorI'),           
    path('removeAsesorI/<uuid:pk>', removeAsesorI, name='removeAsesorI'),           
    
    path('asignarRevisorL/<int:page>/<uuid:pk>', asignarRevisorL, name='asignarRevisorL'),           
    path('asignarRevisor/<uuid:pkR>/<uuid:pkD>', asignarRevisor, name='asignarRevisor'),           
    path('removeRevisor/<uuid:pk>', removeRevisor, name='removeRevisor'),           
    
    path('verDocente/<uuid:pk>', verDocente, name='verDocente'),           
    path('editarDocente/<uuid:pk>', editarDocente, name='editarDocente'),           
    path('altaDocente/', altaDocente, name='altaDocente'), 
    path('act_docente_anteproyectosA/<uuid:pk>', act_docente_anteproyectosA, name='act_docente_anteproyectosA'), 
    path('act_docente_anteproyectosH/<uuid:pk>/<int:page1><int:page2>/<int:orderB1><int:orderB2>/<int:filter1><int:filter2>', act_docente_anteproyectosH, name='act_docente_anteproyectosH'),     
    path('act_docente_residenciasA/<uuid:pk>', act_docente_residenciasA, name='act_docente_residenciasA'), 
    path('act_docente_residenciasH/<uuid:pk>/<int:page1><int:page2>/<int:orderB1><int:orderB2>/<int:filter1><int:filter2>', act_docente_residenciasH, name='act_docente_residenciasH'), 
    
    
    path('editarMateria/<uuid:pk>', editarMateria, name='editarMateria'),           
    path('altaMateria/', altaMateria, name='altaMateria'),       
    
    path('altaDependencia_a/', altaDependencia, name='altaDependencia_a'),       
    path('alta_titular_dep/<uuid:pk>', alta_titular_dep, name='alta_titular_dep'),       
    path('alta_domicilio_dep/<uuid:pk>', alta_domicilio_dep, name='alta_domicilio_dep'),       
    path('ver_dependencia/<uuid:pk>', ver_dependencia, name='ver_dependencia'),              
    path('editar_dependencia/<uuid:pk>', editar_dependencia, name='editar_dependencia'),              
    
    path('verResidencia/<uuid:pk>', verResidencia, name='verResidencia'),        
    path('eliminarResidencia/<uuid:pk>', eliminarResidencia, name='eliminarResidencia'),        
    path('editarResidenciaAdmin/<uuid:pk>', editarResidenciaAdmin, name='editarResidenciaAdmin'),    
    
    path('historial_estudiante/<uuid:pk>', historial_estudiante, name='historial_estudiante'),    
    
    path('eliminarEstudiante/<uuid:pk>', eliminarEstudiante, name='eliminarEstudiante'),       
    path('eliminarDocente/<uuid:pk>', eliminarDocente, name='eliminarDocente'),
    path('eliminarMateria/<uuid:pk>', eliminarMateria, name='eliminarMateria'),
    path('eliminar_dependencia/<uuid:pk>', eliminar_dependencia, name='eliminar_dependencia'),
    path('eliminarDocExpediente/<uuid:pk>/<file_name>', eliminarDocExpediente, name='eliminarDocExpediente'),
    path('eliminarDocR1/<uuid:pk>/<file_name>', eliminarDocR1, name='eliminarDocR1'),
    path('eliminarDocR2/<uuid:pk>/<file_name>', eliminarDocR2, name='eliminarDocR2'),
    path('eliminarDocRF/<uuid:pk>/<file_name>', eliminarDocRF, name='eliminarDocRF'),
    
    path('avisos/', avisos, name='avisos'), 
    path('crear_aviso/', crear_aviso, name='crear_aviso'), 
    path('eliminar_aviso/<uuid:pk>', eliminar_aviso, name='eliminar_aviso'), 
        
    path('cancelar_anteproyecto/<uuid:pk>', cancelar_anteproyecto, name='cancelar_anteproyecto'),         
    path('cancelar_residencia/<uuid:pk>', cancelar_residencia, name='cancelar_residencia'),         
    
    path('generar_reportes/', generar_reportes, name='generar_reportes'), 
    path('generar_reporte_estudiante/<int:filter1>/<filter2>/<int:filter3>/<int:filter4>', generar_reporte_estudiantes, name='generar_reporte_estudiante'), 
    path('generar_reporte_anteproyectos/<int:filter1>/<int:filter2>/<str:filter3>/<str:filter4>/<int:filter5>/<int:filter6>/<int:filter7>/<filter8>', generar_reporte_anteproyectos, name='generar_reporte_anteproyectos'), 
    path('generar_reporte_residencias/<int:filter1>/<int:filter2>/<int:filter3>/<filter4>/<str:filter5>/<str:filter6>/<str:filter7>/<str:filter8>', generar_reporte_residencias, name='generar_reporte_residencias'),     
    path('export_excel/<int:tipo>/<str:name>', export_excel, name='export_excel'), 
    
    path('estudiantes_autorizados/<int:page>/<int:filter1>/<filter2>', estudiantes_autorizados, name='estudiantes_autorizados'), 
    path('subir_estudiantes_a/', subir_estudiantes_a, name='subir_estudiantes_a'), 
        
    path('export_pdf/<int:tipo>/<str:name>', export_pdf, name='export_pdf'),    
    
    # Teacher 
    path('tProfile/', teacherProfile, name='teacherProfile'),      
    path('tSettings/', teacherSettings, name='teacherSettings'),
    
    path('anteproyectosTeacher/', anteproyectosTeacher, name='anteproyectosTeacher'),      
    path('anteproyectoA/<uuid:pk>', anteproyectoA, name='anteproyectoA'),
    path('anteproyectoH/<uuid:pk>', anteproyectoH, name='anteproyectoH'),
    path('agregarComentario/<uuid:pk>', agregarComentario, name='agregarComentario'),
    #path('anteproyectoH/', anteproyectoH, name='anteproyectoH'),    
    path('residenciasTeacher/', residenciasTeacher, name='residenciasTeacher'), 
    path('verResidenciaH/<uuid:pk>', residenciaH, name='verResidenciaH'),             
    path('verReporte/<uuid:pk>', verReporte, name='verReporte'),          
    
    path('tomarRevisor1/<uuid:pk>', tomarRevisor1, name='tomarRevisor1'),      
    path('tomarRevisor2/<uuid:pk>', tomarRevisor2, name='tomarRevisor2'),      
    path('anteproyectosH/<int:page1><int:page2>/<int:orderB1><int:orderB2>/<int:filter1><int:filter2>', anteproyectosH, name='anteproyectosH'),      
    path('residenciasH/<int:page1><int:page2>/<int:orderB1><int:orderB2>/<int:filter1><int:filter2>', residenciasH, name='residenciasH'),      
    path('materias/', materias, name='materias'),          
    path('seleccionarMateria/<materiaPK>', seleccionarMateria, name='seleccionarMateria'),  
    path('removeMateria/<materiaPK>', removeMateria, name='removeMateria'),  
    path('actualizacionEstDocumento/<uuid:pk>', actualizacion_est_leido, name='actualizacionEstDocumento'),  
]
