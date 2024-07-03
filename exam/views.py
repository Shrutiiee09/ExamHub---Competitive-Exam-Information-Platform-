from django.shortcuts import render, redirect
from .models import Exam, UserProfile
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url="/login/")
def home(request):
    exams = Exam.objects.all()
    context = {'exams': exams}
    return render(request, 'home.html', context)

@login_required(login_url="/login/")
def api_exams(request):
    exams_objs = Exam.objects.all()
    
    state = request.GET.get('state')
    if state:
        exams_objs = exams_objs.filter(state__name=state)
        
    exam_type = request.GET.get('exam_type')
    if exam_type:
        exams_objs = exams_objs.filter(exam_type__name=exam_type)
    
    educational_level = request.GET.get('educational_level')
    if educational_level:
        exams_objs = exams_objs.filter(educational_level__level=educational_level)
    
    payload = [{'name': exam_obj.name,
                'description': exam_obj.description,
                'syllabus': exam_obj.syllabus,
                'exam_pattern': exam_obj.exam_pattern,
                'eligibility_criteria': exam_obj.eligibility_criteria,
                'registration_procedure': exam_obj.registration_procedure,
                'important_dates': exam_obj.important_dates,
                'exam_centres': exam_obj.exam_centres} for exam_obj in exams_objs]
    
    return JsonResponse(payload, safe=False)

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username)
        
        if not user_obj.exists():
            messages.error(request, "Username not found")
            return redirect('/login/')
        
        user_obj = authenticate(username=username, password=password)
        
        if user_obj:
            login(request, user_obj)
            return redirect('/')
        
        messages.error(request, "Wrong Password")
        return redirect('/login/')
    
    return render(request, "login.html")

def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username)
        
        if user_obj.exists():
            messages.error(request, "Username is taken")
            return redirect('/register/')
        
        user_obj = User.objects.create(username=username)
        user_obj.set_password(password)
        user_obj.save()
        
        messages.success(request, "Account created")
        return redirect('/login/')
    
    return render(request, "register.html")

def custom_logout(request):
    logout(request)
    return redirect('/login/')

@login_required(login_url="/login/")
def feedback_page(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        if feedback_text:
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.feedback = feedback_text
            user_profile.save()
            messages.success(request, 'Thank you for your feedback!')
        else:
            messages.error(request, 'Please enter your feedback.')
        return redirect('feedback')
    
    return render(request, 'feedback.html')
