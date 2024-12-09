from django.contrib.auth import logout
from django.shortcuts import redirect

'''
    *! Esta es una version mejorada al metodo anterior, ya que aqui no se le tiene que pasar la lista con los roles que permite
    * Solo se verifica que el usuario que este ingresando pertenezca a alguno de los roles. 
'''
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func           

def dashboard(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            
        if group == 'student':
            return redirect('student')
        elif group == 'teacher':
            return redirect('teacher')
        elif group == 'admin' or group == 'jefe_carrera_sistemas':
            return view_func(request, *args, **kwargs)    
        else:
            logout(request)
            return redirect('404')
    return wrapper_func            

def publicView(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            
        if group == 'admin' or group == 'teacher' or group == 'jefe_carrera_sistemas':
            return view_func(request, *args, **kwargs)            
        else:            
            return redirect('404')
    return wrapper_func   

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            
        if group == 'admin' or group == 'jefe_carrera_sistemas':
            return view_func(request, *args, **kwargs)            
        else:            
            return redirect('404')
    return wrapper_func            

def teacher_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            
        if group == 'teacher':
            return view_func(request, *args, **kwargs)            
        else:            
            return redirect('404')
    return wrapper_func   

def student_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            
        if group == 'student':
            return view_func(request, *args, **kwargs)            
        else:            
            return redirect('404')
    return wrapper_func   
   
def d_faqs(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            
        if group == 'student':
            return redirect('student_faqs')
        elif group == 'teacher':
            return redirect('teacher_faqs')
        elif group == 'admin' or group == 'jefe_carrera_sistemas':
            return view_func(request, *args, **kwargs)    
        else:
            logout(request)
            return redirect('404')
    return wrapper_func            

def d_teacher_student(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            
        if group == 'student' or group == 'teacher':
            return view_func(request, *args, **kwargs)                    
        else:            
            return redirect('404')
    return wrapper_func            
