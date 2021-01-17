from django.shortcuts import render
from django.db import connections
from django.db import transaction
from django.http import HttpResponseRedirect,HttpResponse,HttpRequest,JsonResponse
from django.template import loader
from ..models import *
from .func import str2time,date2str,str2date
import datetime


# from .models import *
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

class manager():
    @staticmethod
    def manager_index(request,id):
        if isinstance(request, HttpRequest):
            template = loader.get_template("manager.html")
            # 检查是否有非法调用url的情况
            if check(request,id):
                manager_name = InstrumentManager.objects.get(manager_id=id).name
                return HttpResponse(template.render({"manager_name": manager_name,
                                                    "short_name": manager_name}, request))
            
            else:
                print(id, request.session['user_id'])
                return HttpResponseRedirect('/login')
    
    @staticmethod
    def manager_index2(request,id):
        if isinstance(request, HttpRequest):
            template = loader.get_template("manager/managerv2.html")
            # 检查是否有非法调用url的情况
            if check(request,id):
                manager_name = InstrumentManager.objects.get(manager_id=id).name
                return HttpResponse(template.render({"manager_name": manager_name,
                                                    "short_name": manager_name}, request))
            
            else:
                print(id, request.session['user_id'])
                return HttpResponseRedirect('/login')


    @staticmethod
    def manager_index3(request,id):
        if isinstance(request, HttpRequest):
            template = loader.get_template("manager/managerv3.html")
            # 检查是否有非法调用url的情况
            if check(request,id):
                manager_name = InstrumentManager.objects.get(manager_id=id).name
                return HttpResponse(template.render({"manager_name": manager_name,
                                                    "short_name": manager_name}, request))
            
            else:
                print(id, request.session['user_id'])
                return HttpResponseRedirect('/login')

    @staticmethod
    def get_manager_info(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            cursor = connections['default'].cursor()
            cursor.execute("begin transaction;")
            cursor.execute("select * from management_instrumentmanager where manager_id=" + str(id)+ ";")
            raw=dictfetchall(cursor)
            cursor.execute("commit;")
            # print(raw[0])
            context={}
            context['manager_info'] = raw[0]
            return render(request, "manager/manager_info.html", context)

        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')

    @staticmethod
    def get_app_list(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            # 查询已有的该管理员管理的所有预约
            cursor = connections['default'].cursor()
            cursor.execute("select management_appointment.app_id,management_appointment.app_datetime,management_appointment.use_date,management_appointment.use_time,management_appointment.ins_id_id, \
                management_appointment.user_id_id,management_appointment.state,management_instrument.name,management_appointment.comment,management_student.name sname\
                from management_appointment,management_instrument,management_student where management_appointment.ins_id_id=management_instrument.id and management_appointment.user_id_id=management_student.student_id\
                and management_instrument.manager_id=" + str(id) +" and management_appointment.state='等待审批' "+" order by management_appointment.app_datetime DESC;")
            print(cursor)    
            raw2 = dictfetchall(cursor)
            print(raw2)
            #print(type(raw2))
            for item in raw2:
                #print(type(item))
                item['use_time'] = str2time(item['use_time'])
                item['use_date'] = date2str(item['use_date'])
                #print(raw2['use_time'])
            context = {}
            context['groups'] = raw2
            
            # 查询已经处理过的预约
            cursor = connections['default'].cursor()
            cursor.execute("select management_appointment.app_id,management_appointment.app_datetime,management_appointment.use_date,management_appointment.use_time,management_appointment.ins_id_id,management_student.name sname, \
                management_appointment.user_id_id,management_appointment.state,management_instrument.name,management_appointment.comment\
                from management_appointment,management_instrument,management_student where management_appointment.ins_id_id=management_instrument.id and management_appointment.user_id_id=management_student.student_id\
                and management_instrument.manager_id=" + str(id) +" and management_appointment.state!='等待审批'"+" order by management_appointment.app_datetime DESC;")
            raw = dictfetchall(cursor)
            #print(raw)
            #print(type(raw))
            for item in raw:
                #print(type(item))
                item['use_time'] = str2time(item['use_time'])
                item['use_date'] = date2str(item['use_date'])
                #print(raw2['use_time'])
            context['appgroups'] = raw

            return render(request, "manager/manager_app_list.html", context)
        
        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')
    
    @staticmethod
    def approval_app(request, id):  # 通过申请
        # 检查是否有非法调用url的情况
        if check(request,id):
            app_id = request.GET['app_id']
            appset = Appointment.objects.filter(app_id=app_id)
            #print(appset)
            if len(appset) == 0:
                return JsonResponse({
                    "code": -1,
                    "msg": "no such appoint with id %d" % app_id
                })
            else:
                app = appset.first()
                app.state = "通过"
                app.save()
                return JsonResponse({
                    "code": 1,
                    "msg": ""
                })

        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')

    @staticmethod
    def refuse_app(request, id):  # 拒绝申请
        # 检查是否有非法调用url的情况
        if check(request,id):
            app_id = request.GET['app_id']
            appset = Appointment.objects.filter(app_id=app_id)
            #print(appset)
            if len(appset) == 0:
                return JsonResponse({
                    "code": -1,
                    "msg": "no such appoint with id %d" % app_id
                })
            else:
                app = appset.first()
                app.state = "未通过"
                app.save()
                return JsonResponse({
                    "code": 1,
                    "msg": ""
                })

        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')

    @staticmethod
    def my_instrument_list(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            cursor = connections['default'].cursor()
            cursor.execute("select * from management_instrument where management_instrument.manager_id='"+str(id)+"'")
            raw = dictfetchall(cursor)
            # print(20*'-',raw)
            context          = {}
            context['manager_instruments'] = raw
            return render(request, "manager/manager_instrument_list.html", context)
        
        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')

    
    @staticmethod
    def get_instrument_detail_information(request, id):
        if check(request, id):
            ins_id = request.GET['ins_id']
            cursor = connections['default'].cursor()
            cursor.execute("select * from management_instrument where id='"+str(ins_id)+"'")
            raw = dictfetchall(cursor)
            #print(raw)
            return JsonResponse({
                    'code': 1,
                    'msg': '',
                    'name': raw[0]['name'],
                    'address': raw[0]['address'],
                    'state': raw[0]['state'],
                    'func': raw[0]['func'],
                    'manufacturer': raw[0]['manufacturer'],
                    'type': raw[0]['type'],
                    'purchaseDate': raw[0]['purchaseDate'],
                    'technicalParameters': raw[0]['technicalParameters'],
                    'picture': raw[0]['picture']
                })

        else:
            # print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')

    
    @staticmethod
    def update_instrument_information(request,id):
        if check(request, id):
            with transaction.atomic():
                _id = request.GET['ins_id']
                new_name = request.GET['new_name']
                new_state = request.GET['new_state']
                new_type = request.GET['new_type']
                new_address = request.GET['new_address']
                new_manufacturer = request.GET['new_manufacturer']
                new_technicalParameters = request.GET['new_technicalParameters']
                new_purchaseDate = request.GET['new_purchaseDate']
                new_function = request.GET['new_function']
                new_picture = request.GET['new_picture']

                # print(20*'-',_id,new_name,new_state,new_type,new_address,new_manufacturer,new_technicalParameters,new_purchaseDate,new_function,new_picture)

                instrument_obj = Instrument.objects.get(id=_id)
                instrument_obj.name = new_name
                instrument_obj.state = new_state
                instrument_obj.type = new_type
                instrument_obj.address = new_address
                instrument_obj.manufacturer = new_manufacturer
                instrument_obj.technicalParameters = new_technicalParameters
                instrument_obj.purchaseDate = new_purchaseDate
                instrument_obj.func = new_function
                instrument_obj.picture = new_picture
                instrument_obj.save()

            print("已成功修改仪器信息")
            return JsonResponse({
                'code': 1,
                'msg':''
            })

        else:
            # print(id, request.session['user_id'])
            return HttpResponseRedirect('/login') 
    
    

    @staticmethod
    def create_instrument_html(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            return render(request, "manager/manager_create_instrument.html")

        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')

    @staticmethod
    def create_instrument(request, id):
        # 检查是否有非法调用url的情况
        if check(request, id):
            with transaction.atomic():
                instrument_name = request.GET['instrument_name']
                instrument_type = request.GET['instrument_type']
                instrument_function = request.GET['instrument_function']
                instrument_state = request.GET['instrument_state']
                instrument_address = request.GET['instrument_address']
                instrument_manufacturer = request.GET['instrument_manufacturer']
                instrument_technicalParameters = request.GET['instrument_technicalParameters']
                instrument_picture = request.GET['instrument_picture']
                manager_id = str(id)            
                Instrument.objects.create(
                    name=instrument_name,
                    type=instrument_type,
                    state=instrument_state,
                    address=instrument_address,
                    func=instrument_function,
                    manufacturer=instrument_manufacturer,
                    technicalParameters=instrument_technicalParameters,
                    picture=instrument_picture,
                    manager=InstrumentManager.objects.filter(manager_id=manager_id).first()# 此处应为manager,与models中Istrument类的属性对应，而非与数据库里的manager_id对应
                )
            print("已成功创建仪器")
            return JsonResponse({
                'code': 1,
                'msg':''
            })

        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')

    @staticmethod
    def delete_instrument(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            _id = request.GET['id']
            with transaction.atomic():
                instrument_obj = Instrument.objects.get(id=_id)
                instrument_obj.delete()
            print("已成功删除仪器")
            return JsonResponse({
                'code': 1,
                'msg':''
            })
        
        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')
    
    @staticmethod
    def get_feedback(request, id):
        # 检查是否有非法调用url的情况
        if check(request,id):
            app_id = request.GET['app_id']
            
            cursor = connections['default'].cursor()
            cursor.execute("select * from management_feedback where management_feedback.app_id_id="+str(app_id))
            raw = dictfetchall(cursor)
            #print(raw)
            if len(raw) > 0:
                feedback_comment = raw[0]['comments']
            else:
                feedback_comment = "用户还未填写反馈！"
            return JsonResponse({
                'code': 1,
                'msg': '',
                'feedback': feedback_comment
            })
        
        else:
            print(id, request.session['user_id'])
            return HttpResponseRedirect('/login')
    @staticmethod
    def time_table(request,id):
        year=datetime.datetime.now().year
        month=datetime.datetime.now().month
        cursor = connections['default'].cursor()
        cursor.execute("select name,use_time,strftime('%d',use_date) as day from management_appointment,management_student \
        where ins_id_id= "+str(id)+" and strftime('%m',use_date)= '"+str(month)+"' and strftime('%Y',use_date)='"+str(year)+"' and state!='未通过' \
        and management_student.student_id=management_appointment.user_id_id ;")
        raw = dictfetchall(cursor) # 每一个代表一条预约记录
        print("raw")
        print(raw)
        context          = {}
        # 像前端返回每一个预约的情况 人名字，开始时间，结束时间，天
        app_info = []
        for item in raw:
            for i in range(8,22):
                if item['use_time'][i] == '1':
                    l = [item['name'],i,int(item['day'])]
                    app_info.append(l)
            
        context['app_info'] = app_info

        # 需要筛选每一天预约了多长时间
        time_everyday = {i:0 for i in range(32)}
        time_table = ['000000000000000000000000']*32
        new_hour = 0
        for item in raw:
            for i in range(24):
                if time_table[int(item['day'])][i] == '0' and item['use_time'][i] == '1':
                    new_hour += 1
                    
            time_everyday[int(item['day'])] += new_hour
            new_hour=0
        
        context['time_everyday'] = time_everyday
        # 仪器名称
        ins_name = Instrument.objects.filter(id=id).all().first().name
        context['ins_name'] = ins_name
        print(time_everyday)
        return render(request, "manager/timetablev2.html", context)


