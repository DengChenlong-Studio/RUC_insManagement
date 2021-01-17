from django.shortcuts import render
import requests
# Create your views here.

from django.http import HttpResponseRedirect
from django.db import connections
from management.models import *
from django.http import HttpResponse
import json

def dictfetchall(cursor):
	desc = cursor.description
	return [
	dict(zip([col[0] for col in desc], row))
		for row in cursor.fetchall()
		]

def index(request):
    return render(request, "index.html")


def login(request):
    error_msg = ""
    if request.method == 'POST' and request.POST:
        user_id = request.POST.get("username")
        password = request.POST.get("password")
        identity = request.POST.get("identity")
        valid = request.POST.get("flag")
        #extra = request.POST.get("extra_message") #extra = "/app_list" 或 ""
        print("student_id: ", user_id)
        print("password: ", password)
        print("identity: ", identity)
        print("captcha is_valid", valid)

        if identity == "student":
            e = Student.objects.filter(student_id=user_id).first()
        if identity == "teacher":
            e = Teacher.objects.filter(teacher_id=user_id).first()
        if identity == "manager":
            e = InstrumentManager.objects.filter(manager_id=user_id).first()
        if (valid == "0"):
            error_msg = '请拖拽下方验证码至合适位置'
        elif e:
            now_password = password
            db_password = e.password
            if now_password == db_password:
                if identity == "student":
                    response = HttpResponseRedirect('../Student/' + user_id)
                if identity == "teacher":
                    response = HttpResponseRedirect('../Teacher/' + user_id)
                if identity == "manager":
                    response = HttpResponseRedirect('../Manager/' + user_id)

                #response.set_cookie("student_id", e.student_id)
                #hzh 2020.11.22 modified
                #-----#
                #补一个身份-id比对，完成
                request.session['is_login'] = True
                request.session['user_id'] = user_id
                request.session['identity'] = identity
                #-----#
                return response
            else:
                error_msg = '用户名或密码错误'
        else:
            error_msg = '用户不存在'

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
    return render(request, "student/ins_listv2.html")

def apply_for_group(request):
    group_list = Group.objects.all()
    context = {
        'groups': group_list
    }

    return render(request, 'ApplyFor_Group.html', context=context)

def submit_application_for_group(request):
    groupid = request.GET['grouid']
    cursor = connections['default'].cursor()
    # cursor.execute()
    response = HttpResponse(json.dumps({"status": 1}), content_type="application/json")

    return response

#hzh modified on 2020.11.15
def getdata(request):
    cursor = connections['default'].cursor()
    context = {}
    #context['group_table'] = group_table
    context['group_table'] = Group.objects.all()
    context['teacher_table'] = Teacher.objects.all()
    context['student_table'] = Student.objects.all()
    context['account_table'] = account.objects.all()
    context['GroupTeacherStudent_table'] = GroupTeacherStudent.objects.all()
    context['appointment_table'] = Appointment.objects.all()
    context['Application_For_Group_table'] = Application_For_Group.objects.all()
    context['Instrument_table'] = Instrument.objects.all()
    context['InstrumentManager_table'] = InstrumentManager.objects.all()
    return render(request, "getData.html", context = context)

#hzh modified on 2020.11.29
'''
def get_banner(request):
    banner = Banner.objects.only('image_url', 'news__title').select_related('news').filter(is_delete=False)\
        .order_by('priority')
    print(banner)
    banner_info = []
    for i in banner:
        banner_info.append({
            "image_url": i.image_url,
            "news_title": i.news.title,
            "news_id": i.news.id,
        })
    data = {
        "banner": banner_info
    }
    print(data)
    #return ResultResponse(data=data)
    return HttpResponse(data = data)
'''

# 在news目录下views.py中创建如下视图
'''
class NewsBannerView(View):
    """
    轮播图
    GET /news/banners/
    """
    def get(self, request):
        # 读取到图片,文章id和标题, 由于标题是外键, 发送json的话就需要重命名
        banners = Banner.objects.values('image_url', 'news_id').annotate(
            news_title=F('news__title')).filter(is_delete=False)[:constants.SHOW_BANNER_COUNT]
        data = {
            'banners': list(banners)
        }
        return json_response(data=data)
'''
def get_banner(request):
    return render(request, "Demo_banner.html")

''' 得到课题组信息：由于学生和老师都可以看到这个页面，故放到公共index_views '''
def get_group_info(request,id):
    group_id = request.GET['group_id']
    cursor = connections['default'].cursor()
    print(group_id)

    # 先得到教师信息
    cursor.execute('select * from management_teacher t, management_group g where t.teacher_id = g.leader_id and g.group_id = "{}"'.format(group_id))
    teacher_list = dictfetchall(cursor)
    #print(raw)
    # 再得到组内学生信息
    cursor.execute('select * from management_groupteacherstudent gts, management_student s where gts.group_id = "{}" and gts.student_id = s.student_id'.format(group_id))
    student_list = dictfetchall(cursor)
    print(student_list)

    res = []
    # 先存入老师信息
    d = dict()
    d['id'] = teacher_list[0]['teacher_id']
    d['name'] = teacher_list[0]['name']
    d['school'] = teacher_list[0]['school']
    d['department'] = teacher_list[0]['department']
    d['status'] = '负责教师'
    res.append(d)

    # 再存入学生信息
    for stu in student_list:
        d = dict()
        d['id'] = stu['student_id']
        d['name'] = stu['name']
        d['school'] = stu['school']
        d['department'] = stu['department']
        d['status'] = '学生'
        res.append(d)
    print(res)

    return HttpResponse(json.dumps(res), content_type='applications/json')

def welcome(request):
    return render(request, "welcome.html")

def login_ruc(request):
 loginServer = "http://cas.ruc.edu.cn/cas/login"
 validateServer = "http://cas.ruc.edu.cn/cas/serviceValidate"
 myurl = "http://127.0.0.1:8000/cas"
 return HttpResponseRedirect(loginServer+'?service='+myurl,{'code':302})


def cas(request):
    ticket=request.GET["ticket"]
    #print(ticket)
    myurl = "http://127.0.0.1:8000/cas"
    validateServer = "http://cas.ruc.edu.cn/cas/serviceValidate"
    validateurl = validateServer+"?ticket="+ticket+'&service='+myurl
    #return redirect(validateurl,code=302)
    from xml.etree import ElementTree
    from xml.dom.minidom import parseString #导入解析字符串的包
    content = requests.get(validateurl)
    #print(type(content))
    #print(content.text)
    root = ElementTree.XML(content.text)    # 读取字符串，将字符串转为Element对象
    #print(root[0][1])
    uid=''
    name=''
    for i in root[0][1]:
        if i.attrib["name"]=='uid':
            uid = i.attrib["value"]
        if i.attrib['name']=='cn':
            name=i.attrib["value"]

    print(uid,name)
    
    # 下面是转到你登录界面
    if len(uid) == 10:
        #学生
        students = Student.objects.filter(student_id=uid)
        if len(students) == 0:
            # 没有这个用户，创建
            Student.objects.create(
                student_id=uid,
                name=name,
                grade=uid[0:4]
            )
        
        request.session['is_login'] = True
        request.session['user_id'] = uid
        request.session['identity'] = "student"
        return HttpResponseRedirect('../Student/' + uid)
    
    if len(uid) == 8:
        #教师
        teachers = Teacher.objects.filter(student_id=uid)
        if len(teachers) == 0:
            # 没有这个用户，创建
            Teacher.objects.create(
                teacher_id=uid,
                name=name
            )
        
        request.session['is_login'] = True
        request.session['user_id'] = uid
        request.session['identity'] = "teacher"
        return HttpResponseRedirect('../Teacher/' + uid)
    return render(request, "login.html", {'error_msg': "登陆失败"})


