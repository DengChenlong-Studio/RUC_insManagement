# -*- coding: utf-8 -*-
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.static import serve
from .views import index_views,student_views,manager_views,teacher_views
import datetime

urlpatterns = [
    path('', index_views.index),

    path('logruc/', index_views.login_ruc),
    path('cas/', index_views.cas),
    path('index/', index_views.index),
    path('getdata/', index_views.getdata),  #hzh modified on 2020.11.15
    path('banner/', index_views.get_banner),    #hzh modified on 2020.11.29
    path('login/', index_views.login),
    path('sign/', index_views.sign_up),
    path('forget/', index_views.forget),
    path('text/', index_views.text),
    path('Student/', index_views.text),  # 测试视图，后续改为学生界面的首页
    # 下面写的时候后面注意加注释，，主要是这个界面或功能是干什么的 marked by ws
    url(r'^media/picture/(?P<path>.*)$', serve, {'document_root': 'media/picture/'}), #加载图片路径
    path(r'Student/<int:id>',student_views.student_view.student_index2),  # 学生首页
    path(r'Student/<int:id>/get_info',student_views.student_view.get_student_info),  # 学生个人信息页
    path(r'Student/<int:id>/get_my_group',student_views.student_view.get_my_group),  # 学生已加入的课题组信息
    path(r'Student/<id>/submit_application_for_group/', student_views.student_view.submit_application_for_group),# 学生申请加入课题组
    path(r'Student/<int:id>/inslist', student_views.student_view.get_ins_list),  # 学生查看的仪器列表
    path(r'Student/<int:id>/get_instrument_detail_information',student_views.student_view.get_instrument_detail_information),  # 学生查看仪器详细信息
    path(r'Student/<int:id>/myapp',student_views.student_view.get_app_list),  # 学生查看的仪器列表
    path(r'Student/<int:id>/sendapp',student_views.student_view.send_app),  # 学生发送仪器申请
    path(r'Student/<int:id>/send_feedback',student_views.student_view.send_feedback),  # 学生发送仪器申请
    path(r'Student/<int:id>/getinfo',student_views.student_view.get_info),  # 测试，，以后可能不用
    path(r'Student/<int:id>/quxiao',student_views.student_view.delete_app),  # 学生取消预约
    path(r'Student/pick_app_time',student_views.student_view.pick_app_time),  # 返回当天可用的预约时间段
    path(r'Student/<int:id>/search', student_views.student_view.search), # 搜索可预约的仪器
    path(r'Manager/<int:id>', manager_views.manager.manager_index3),  # 管理员首页
    path(r'Manager/<int:id>/getinfo',manager_views.manager.get_manager_info), # 管理员查看个人信息
    path(r'Manager/<int:id>/applist', manager_views.manager.get_app_list),  # 管理员获得的申请列表
    path(r'Manager/<id>/instrument_list', manager_views.manager.my_instrument_list),  # 管理员查看仪器列表
    path(r'Manager/<id>/get_instrument_detail_information',manager_views.manager.get_instrument_detail_information), # 管理员查看仪器详细信息
    path(r'Manager/<id>/update_instrument_information',manager_views.manager.update_instrument_information), # 管理员修改仪器信息
    path(r'Manager/<id>/create_instrument_html', manager_views.manager.create_instrument_html), 
    path(r'Manager/<id>/create_instrument', manager_views.manager.create_instrument), # 管理员创建仪器
    path(r'Manager/<id>/delete_instrument',manager_views.manager.delete_instrument), # 管理员删除仪器
    path(r'Manager/<int:id>/approvalapp', manager_views.manager.approval_app),  # 管理员同意学生的申请
    path(r'Manager/<int:id>/refuseapp', manager_views.manager.refuse_app),  # 管理员拒绝申请
    path(r'Manager/<int:id>/get_feedback', manager_views.manager.get_feedback), # 管理员查看反馈
    path(r'Teacher/<id>', teacher_views.teacher_view.teacher_index3),  # 教师主页
    path(r'Teacher/<id>/getinfo', teacher_views.teacher_view.get_teacher_info), # 教师查看个人信息
    path(r'Teacher/<id>/grouplist', teacher_views.teacher_view.my_group_list),  # 教师查看课程组列表
    path(r'Teacher/<id>/create_group_html', teacher_views.teacher_view.create_group_html),
    path(r'Teacher/<id>/create_group', teacher_views.teacher_view.create_group),
    path(r'Teacher/<id>/delete_group', teacher_views.teacher_view.delete_group),
    path(r'Teacher/<id>/delete_student', teacher_views.teacher_view.delete_student),
    path(r'Student/<id>/applyfor_group/', student_views.student_view.apply_for_group),
    path(r'Teacher/<id>/CheckApplyFor_Group/', teacher_views.teacher_view.get_my_application_of_groups),
    path(r'Teacher/<id>/agree_application_for_group', teacher_views.teacher_view.agree_application_for_group),
    path(r'Teacher/<id>/disagree_application_for_group', teacher_views.teacher_view.disagree_application_for_group),
    path(r'Student/<int:id>/index', student_views.student_view.student_index2),# 测试新学生首页
    path(r'Manager/<int:id>/index', manager_views.manager.manager_index2),# 测试新管理员首页
    path(r'Teacher/<id>/index', teacher_views.teacher_view.teacher_index2),# 测试新教师首页
    path(r'Manager/<int:id>/ins_time', manager_views.manager.time_table),# 仪器使用时间表
    path(r'Group/<id>', index_views.get_group_info), # 得到组内详细信息
    path(r'welcome',index_views.welcome) # 进入系统的首页
    #path('captcha/', include('captcha.urls')) # 验证码
]
