from django.shortcuts import render
from django.db import connections
from django.db import transaction
from django.http import HttpResponseRedirect
from django.http import HttpResponse,JsonResponse,HttpRequest
from datetime import datetime
from ..models import *
from django.template import loader
import json

def dictfetchall(cursor):
    desc = cursor.description
    return [
    dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
        ]

def check(request,id):
    if 'user_id' not in request.session.keys() or request.session['user_id'] != str(id):
        return False
    return True

class teacher_view():
    @staticmethod
    def teacher_index(request,id):
        if isinstance(request, HttpRequest):
            template = loader.get_template("teacher.html")
            # 检查是否有非法调用url的情况
            if check(request,id):
                teacher_name = Teacher.objects.get(teacher_id=id).name
                return HttpResponse(template.render({"teacher_name": teacher_name,
                                                    "short_name": teacher_name}, request))
            else:
                print(id, request.session['user_id'])
                return HttpResponseRedirect('/login')


    @staticmethod
    def teacher_index2(request,id):
        if isinstance(request, HttpRequest):
            template = loader.get_template("teacher/teacherv2.html")
            # 检查是否有非法调用url的情况
            if check(request,id):
                teacher_name = Teacher.objects.get(teacher_id=id).name
                return HttpResponse(template.render({"teacher_name": teacher_name,
                                                    "short_name": teacher_name}, request))
            else:
                print(id, request.session['user_id'])
                return HttpResponseRedirect('/login')

    @staticmethod
    def teacher_index3(request,id):
        if isinstance(request, HttpRequest):
            template = loader.get_template("teacher/teacherv3.html")
            # 检查是否有非法调用url的情况
            if check(request,id):
                teacher_name = Teacher.objects.get(teacher_id=id).name
                return HttpResponse(template.render({"teacher_name": teacher_name,
                                                    "short_name": teacher_name}, request))
            else:
                print(id, request.session['user_id'])
                return HttpResponseRedirect('/login')


    @staticmethod
    def get_teacher_info(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            cursor = connections['default'].cursor()
            cursor.execute("select * from management_teacher where teacher_id='"+str(id)+"'")
            raw = dictfetchall(cursor)
            print(raw[0])
            context={}
            context['teacher_info'] = raw[0]
            return render(request, "teacher/teacher_info.html", context)

        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')

    @staticmethod
    def my_group_list(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            cursor = connections['default'].cursor()
            cursor.execute("select * from management_group where management_group.leader_id='"+str(id)+"'")
            raw = dictfetchall(cursor)
            cursor.execute("select g1.group_id,g1.group_name,g1.topic,s.student_id,s.name student_name from management_group g1,management_groupteacherstudent g2,management_student s \
                where g1.group_id=g2.group_id and g2.student_id=s.student_id and g1.leader_id='"+str(id)+"'")
            raw2 = dictfetchall(cursor)
            context          = {}
            context['teacher_groups'] = raw
            context['teacher_groups_detail_info'] = raw2
            return render(request, "teacher_group_list.html", context)
        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')
    
    @staticmethod
    def create_group_html(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            return render(request, "teacher_create_group.html")
        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')

    @staticmethod
    def create_group(request, id):
        # 检查是否有非法调用url的情况
        if check(request, id):
            with transaction.atomic():
                group_id = request.GET['group_id']
                group_name = request.GET['group_name']
                topic = request.GET['topic']
                leader_id = str(id)
                comment = request.GET['comment']
                Group.objects.create(
                    group_id=group_id,
                    group_name=group_name,
                    topic=topic,
                    leader=Teacher.objects.filter(teacher_id=leader_id).first(), # 此处应为leader与models中group类的属性对应，而非与数据库里的leader_id对应
                    comment=comment  
                )
            print("已成功创建")
            return JsonResponse({
                'code': 1,
                'msg':''
            })
        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')

    @staticmethod
    def delete_group(request, id):
        # 检查是否有非法调用url的情况
        if check(request, id):
            with transaction.atomic():
                _group_id = request.GET['group_id']
                # cursor = connections['default'].cursor()
                # cursor.execute("delete from management_group where management_group.group_id='"+str(group_id)+"'")
                group_obj = Group.objects.get(group_id = _group_id)
                group_obj.delete()
            print("已成功删除课题组")
            return JsonResponse({
                'code': 1,
                'msg':''
            })
        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')

    @staticmethod
    def delete_student(request, id):
        # 检查是否有非法调用url的情况
        if check(request, id):
            with transaction.atomic():
                group_id = request.GET['group_id']
                student_id = request.GET['student_id']
                obj = GroupTeacherStudent.objects.get(group = group_id, student = student_id)
                obj.delete()
            print("已成功删除该成员")
            return JsonResponse({
                'code': 1,
                'msg':''
            })
        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')
    


    @staticmethod
    def get_my_application_of_groups(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            cursor = connections['default'].cursor()
            cursor.execute('select * from management_application_for_group afg, management_group g, management_student s\
            where afg.student_id_id=s.student_id and g.leader_id = "{}" and afg.approve_status = "未审批" and afg.group_id_id = g.group_id'.format(id))
            raw=dictfetchall(cursor)
            print(raw)
            context = {
                'applications': raw
            }
            return render(request, "CheckApplyFor_Group.html", context)
        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')


    @staticmethod
    def agree_application_for_group(request, id):
        # 检查是否有非法调用url的情况
        if check(request, id):
            with transaction.atomic():
                groupid = request.GET['groupid']
                studentid = request.GET['studentid']
                appset = Application_For_Group.objects.filter(group_id=groupid, student_id=studentid, approve_status='未审批')
                app = appset.first()
                app.approve_status = '通过'
                app.save()
                GroupTeacherStudent.objects.create(
                    comment='****',
                    group=Group.objects.filter(group_id=groupid).first(),
                    student=Student.objects.filter(student_id=studentid).first(),
                    teacher=Teacher.objects.filter(teacher_id=id).first(), 
                )

            return JsonResponse({
                'code': 1,
                'msg': '批准通过成功！'
            })
        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')

    @staticmethod
    def disagree_application_for_group(request, id):
        # 检查是否有非法调用url的情况
        if check(request, id):
            with transaction.atomic():
                groupid = request.GET['groupid']
                studentid = request.GET['studentid']
                appset = Application_For_Group.objects.filter(group_id=groupid, student_id=studentid, approve_status='未审批')
                app = appset.first()
                app.approve_status = '不通过'
                app.save()

            return JsonResponse({
                'code': 1,
                'msg': '批准拒绝成功！'
            })
        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')
