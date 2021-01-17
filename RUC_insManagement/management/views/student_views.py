from django.shortcuts import render
from django.db import connections
from django.http import HttpResponseRedirect,HttpResponse
from django.http import JsonResponse,HttpRequest
from django.template import loader
from ..models import *
from .func import str2time,date2str,str2date
import datetime
import json
from django.forms.models import model_to_dict


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


class student_view():

    @staticmethod
    def student_index(request,id):
        if isinstance(request, HttpRequest):
            template = loader.get_template("student.html")
            #hzh modified at 11.24
            if check(request,id):
                student_name = Student.objects.get(student_id=id).name
                return HttpResponse(template.render({"student_name": student_name,
                                                 "short_name": student_name}, request))
            else:
                print(id, request.session['user_id'])
                return HttpResponseRedirect('/login')
            #hzh modified at 11.24

    #测试新首页
    @staticmethod
    def student_index2(request,id):
        if isinstance(request, HttpRequest):
            template = loader.get_template("student/studentv3.html")
            #hzh modified at 11.24
            
            student_name = Student.objects.get(student_id=id).name
            return HttpResponse(template.render({"student_name": student_name,
                                            "short_name": student_name}, request))

    @staticmethod
    def get_student_info(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            cursor = connections['default'].cursor()
            cursor.execute("select * from management_student where student_id="+str(id))
            raw = dictfetchall(cursor)
            #print(raw[0])
            context={}
            context['student_info'] = raw[0]
            return render(request, "student/student_info.html", context)

        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')


    @staticmethod
    def get_app_list(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            cursor = connections['default'].cursor()
            cursor.execute("select a.app_id,a.app_datetime,a.use_date,a.use_time,a.ins_id_id,a.state,a.comment,i.name from management_appointment a,management_instrument i\
                where user_id_id="+str(id) +" and a.ins_id_id=i.id\
                    order by app_datetime DESC") 
            raw2 = dictfetchall(cursor)
            for item in raw2:
                #print(type(item))
                item['use_time'] = str2time(item['use_time'])
                item['use_date'] = date2str(item['use_date'])
                #print(raw2['use_time'])
            # print(raw2)
            context={}
            context['appgroups'] = raw2
            print(raw2)  
            
            return render(request, "student/student_app_list.html", context)
            
        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')


    @staticmethod
    def get_ins_list(request,id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            #template = loader.get_template('ins_list,html')
            cursor = connections['default'].cursor()
            # cursor.execute("select * from user limit 1")
            '''
            cursor.execute("select *\
                from management_instrument i,management_instrumentmanager m\
                where i.manager_id=m.manager_id")
            '''
            cursor.execute("select i.id ins_id,i.name ins_name,i.state ins_state,i.address ins_address,i.picture ins_picture,m.name man_name,m.phone man_phone\
                from management_instrument i,management_instrumentmanager m\
                where i.manager_id=m.manager_id")
            context={}
            raw = dictfetchall(cursor)
            for dic in raw:
                dic['picture_id'] = "instrument_picture" + str(dic['ins_id'])
                dic['picture_path'] = "../../media/" + str(dic['ins_picture'])
                
            # print(raw)
            context['groups'] = raw

            # 查询已有的预约
            
            cursor.execute("select a.app_id,a.app_datetime,a.use_date,a.use_time,a.ins_id_id,a.state,a.comment,i.name from management_appointment a,management_instrument i\
                where user_id_id="+str(id) +" and a.ins_id_id=i.id\
                    order by app_datetime DESC") 
            raw2 = dictfetchall(cursor)
            for item in raw2:
                #print(type(item))
                item['use_time'] = str2time(item['use_time'])
                item['use_date'] = date2str(item['use_date'])
                #print(raw2['use_time'])
            # print(raw2)
            context['appgroups'] = raw2  
            
            return render(request, "student/ins_listv2.html", context)
        
        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')

    @staticmethod
    def get_instrument_detail_information(request, id):
        
        ins_id = request.GET['ins_id']
        cursor = connections['default'].cursor()
        cursor.execute("select * from management_instrument i where i.id='"+str(ins_id)+"'")
        raw = dictfetchall(cursor)
        #print(raw)
        context = {}
        context['ins_detail_information'] = raw
        return JsonResponse({
                'code': 1,
                'msg': '',
                'name': raw[0]['name'],
                'func': raw[0]['func'],
                'manufacturer': raw[0]['manufacturer'],
                'type': raw[0]['type'],
                'purchaseDate': raw[0]['purchaseDate'],
                'technicalParameters': raw[0]['technicalParameters']
            })
            
       

    @staticmethod
    def send_app(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            ins_id = request.GET['ins']
            comment = request.GET["comment"]
            time = request.GET["time"]
            user_id = str(id)
            date = request.GET["date"]
            date = str2date(date).date()
            #print(type(date))
            #print(ins_id,user_id,comment,time)
            #last_id = int(Appointment.objects.all())
            cursor = connections['default'].cursor()
            cursor.execute("select app_id from management_appointment")
            raw = dictfetchall(cursor)
            #print(raw)
            last_id = 0
            
            for item in raw:
                if last_id < int(item['app_id']):
                    last_id = int(item['app_id'])
        
            new_id = last_id+1
            Appointment.objects.create(
                app_id=str(new_id),
                ins_id=Instrument.objects.filter(id=ins_id).first(),
                user_id=Student.objects.filter(student_id=id).first(),
                comment = comment,
                use_time = time,
                use_date=date
                #use_date=
            )
            #print("已提交申请")
            return JsonResponse({
                'code':1,
                'msg':''
            }
            )

        else:
            #print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')

    @staticmethod
    def apply_for_group(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            # 查询目前存在的所有的组
            cursor = connections['default'].cursor()
            cursor.execute("select * from management_group g, management_teacher t\
                        where g.leader_id = t.teacher_id")
            raw = dictfetchall(cursor)

            # 查询自己已选的组
            cursor.execute("select group_id from management_groupteacherstudent\
                        where student_id = {}".format(id))
            raw2 = dictfetchall(cursor)
            #print(raw2)

            # 给disabled打标签
            selected_list = [each['group_id'] for each in raw2]
            for each in raw:
                if(each['group_id'] in selected_list):
                    each['disabled'] = True
                else:
                    each['disabled'] = False
            #print(raw)
            context = {
                'groups': raw
            }

            return render(request, 'student/ApplyFor_Group.html', context=context)
        
        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')

    @staticmethod
    def submit_application_for_group(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            groupid = request.GET['groupid']

            # 查看数据库中是否有同样学生和组，但未审批的数据条目
            appset = Application_For_Group.objects.filter(group_id=groupid, student_id=id, approve_status='未审批'or'通过')
            #print(len(appset))
            if len(appset) == 0:
                # 增加相应条目
                student = Student.objects.get(student_id=id)
                group = Group.objects.get(group_id=groupid)
                app_table = Application_For_Group(student_id=student, group_id=group, approve_status='未审批')
                app_table.save()

                return JsonResponse({
                    'code': 1,
                    'msg': ''
                })
            else:
                return 'error'
            # cursor.execute()
            # response = HttpResponse(json.dumps({"status": 1}), content_type="application/json")
        
        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')

    # 查询我加入的课题组
    @staticmethod
    def get_my_group(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            cursor = connections['default'].cursor()
            cursor.execute("select g.group_id,g.group_name,g.topic,t.name from management_group g, management_groupteacherstudent gts,management_teacher t\
                        where g.group_id=gts.group_id and g.leader_id=t.teacher_id and gts.student_id="+str(id))
            raw = dictfetchall(cursor)
            context={}
            context['my_group'] = raw
            return render(request, 'student/my_group.html', context)
            
        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')
    
    # 查看我加入的课题组的成员,,未完成
    @staticmethod 
    def get_my_group_student(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            groupid = request.GET['groupid']
            cursor = connections['default'].cursor()
            cursor.execute("select s.student_id ,s.name from  management_groupteacherstudent gts,management_student s t\
                        where  gts.student_id=s.student_id and gts.group_id="+str(group_id))
            raw = dictfetchall(cursor)
            #print(raw)


            context={}
            return JsonResponse({
                'code':0,
                'msg':'',
                'teacher':'',
                'students':''
            })
        
        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')


    @staticmethod
    def get_info(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            if isinstance(request, HttpRequest):
                #print("getinfo")
                comment = request.POST.get("comment")
                time = request.POST.get("time")
                #print(comment,time)
            
            return JsonResponse({
                'code':1,
                'msg':''
            })

        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')
                
    @staticmethod
    def delete_app(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            if isinstance(request, HttpRequest):
                #print('取消预约')
                app_id = request.GET['delete_app']
                print(app_id)
                #cursor = connections['default'].cursor()
                #cursor.execute("delete from management_appointment where app_id="+str(app_id))
                del_one = Appointment.objects.filter(app_id=app_id).delete()

            return JsonResponse({
                'code':1,
                'msg':''
            })

        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')
    
    @staticmethod
    def pick_app_time(request):
        # 检查是否有非法调用url的情况
        
        date = request.GET["date"]
        print(date)
        cursor = connections['default'].cursor()
        cursor.execute("select * from management_appointment where management_appointment.state!='未通过'")
        raw = dictfetchall(cursor)
        print(raw)
        time=''
        #print(datetime.datetime.strptime(date,'%Y-%m-%d').date())
        #print(raw[2]['use_date'])
        flag = 0
        #for item in raw:
            #print(item['use_time'])
        for i in range(24):
            for item in raw:
                if item['use_date'] == datetime.datetime.strptime(date,'%Y-%m-%d').date():
                    if(item['use_time'][i] == '1'):
                            #print(i,item['id'])
                            flag=1
                            break
                    else:
                            flag=0
            if flag == 1 :
                time+='1'
            else:
                time+='0'
        print(time)

        return JsonResponse({
            'code':1,
            'msg':'',
            'picktime':time
        })
        
        

    @staticmethod
    def send_feedback(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            _app_id = request.GET['app_id']
            comment = request.GET["comment"]
            print("test appid")
            print(Appointment.objects.filter(app_id=_app_id).first().app_id)
            Feedback.objects.create(
                app_id=Appointment.objects.filter(app_id=_app_id).first(),
                comments=comment
            )
            #print("已提交反馈")
            return JsonResponse({
                'code': 1,
                'msg': ''
            })
        
        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')
    
    @staticmethod
    def search(request, id):
        keyword = request.GET['keyword'] # 关键字
        print(keyword)

        # 输入为空时，返回所有结果
        cursor = connections['default'].cursor()
        if not keyword:
            cursor.execute('select m.name as man_name, id, ins.name as ins_name, type, func, state, comment, address, phone from management_instrumentmanager m, management_instrument ins where m.manager_id = ins.manager_id')
        else:
            cursor.execute('select m.name as man_name, id, ins.name as ins_name, type, func, state, comment, address, phone from management_instrumentmanager m, management_instrument ins where m.manager_id = ins.manager_id and ins.name like "%{0}%"'.format(keyword))
        response_list = dictfetchall(cursor)

        
        print(response_list)
        res = []
        for r in response_list:
            d = dict()
            d['id'] = r['id']
            d['name'] = r['ins_name']
            d['type'] = r['type']
            d['func'] = r['func']
            d['picture_id'] = "instrument_picture" + str(r['id'])
            d['picture_path'] = "../../media/picture/instrument" + str(r['id']) + ".png"
            d['state'] = r['state']
            d['man_name'] = str(r['man_name'])
            d['address'] = r['address']
            d['phone'] = r['phone']
            res.append(d)
        
        # print(res)
        # print(json.dumps(res))


        return HttpResponse(json.dumps(res), content_type='applications/json')

