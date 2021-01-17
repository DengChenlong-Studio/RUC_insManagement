from django.shortcuts import render
from django.db import connections
from django.http import HttpResponseRedirect
from management.models import *

# Create your views here.


def index(request):
    return render(request, "index.html")


def login(request):
    error_msg = ""
    if request.method == 'POST' and request.POST:
        student_id = request.POST.get("username")
        password = request.POST.get("password")
        e = Student.objects.filter(student_id=student_id).first()
        if e:
            now_password = password
            db_password = e.password
            if now_password == db_password:
                response = HttpResponseRedirect('/Student/')
                response.set_cookie("student_id", e.student_id)
                return response
            else:
                error_msg = '用户名或密码错误'

    return render(request, "login.html", {'error_msg': error_msg})


def sign(request):
    return render(request, "sign.html")


def sign_up(request):
    if request.method == "POST" and request.POST:
        data = request.POST
        username = data.get("username")
        password = data.get("password")
        name = data.get("name")
        school = data.get("school")
        department = data.get("department")
        major = data.get("major")
        grade = data.get("grade")
        email = data.get("email")
        phone = data.get("phone")
        Student.objects.create(
            student_id=username,
            password=password,
            name=name,
            school=school,
            department=department,
            major=major,
            grade=grade,
            email=email,
            phone=phone
        )
        return HttpResponseRedirect('/login/')
    return render(request, "sign.html")


def forget(request):
    return render(request, "forget.html")


def text(request):
    return render(request, "text.html")


def login_ruc():
 loginServer = "http://cas.ruc.edu.cn/cas/login"
 validateServer = "http://cas.ruc.edu.cn/cas/serviceValidate"
 myurl = "http://127.0.0.1:7000/cas"
 return redirect(loginServer+'?service='+myurl,code=302)


def cas():
 ticket = request.args.get("ticket")
 print(ticket)
 myurl = "http://127.0.0.1:7000/cas"
 validateServer = "http://cas.ruc.edu.cn/cas/serviceValidate"
 validateurl = validateServer+"?ticket="+ticket+'&service='+myurl
 #return redirect(validateurl,code=302)
 content = requests.get(validateurl)