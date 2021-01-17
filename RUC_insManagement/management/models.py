
# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError


class Student(models.Model):
    student_id = models.CharField(max_length=20, primary_key=True)  # 学号/用户名
    password = models.CharField(max_length=20, blank=False, null=False, default="password")  # 密码，，暂时未采取加密
    name = models.CharField(max_length=256, blank=False, null=False)
    school = models.CharField(max_length=256)  # 学校
    department = models.CharField(max_length=256)  # 院系
    major = models.CharField(max_length=256)  # 专业
    grade = models.IntegerField()  # 年级
    email = models.CharField(max_length=256)  # 邮箱
    phone = models.CharField(max_length=256)  # 电话
    comment = models.CharField(max_length=256)  # 备注


class Teacher(models.Model):
    teacher_id = models.CharField(max_length=20, primary_key=True)  # 教师号/用户名
    password = models.CharField(max_length=20, blank=False, null=False, default="password")  # 密码，，暂时未采取加密
    name = models.CharField(max_length=256, blank=False, null=False)
    school = models.CharField(max_length=256)  # 学校
    department = models.CharField(max_length=256)  # 院系
    email = models.CharField(max_length=256)  # 邮箱
    phone = models.CharField(max_length=256)  # 电话
    comment = models.CharField(max_length=256)  # 备注


class Group(models.Model):  # 课题组
    group_id = models.CharField(max_length=256, blank=False, null=False, primary_key=True)  # 课题组id
    group_name = models.CharField(max_length=256, blank=False, null=False)  # 课题组名称
    topic = models.CharField(max_length=256, blank=False, null=False)  # 研究的课题
    leader = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # 课题组负责人
    comment = models.CharField(max_length=256)  # 备注


class GroupTeacherStudent(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    comment = models.CharField(max_length=256)  # 备注

    class Meta:
        unique_together = ("group", "teacher", "student")  # 三个主键
        managed = True


'''
#将课题和课题组统一成课题组
class Project(models.Model):  # 课题/项目
    project_id = models.CharField(max_length=20, primary_key=True)  # 课题号
    name = models.CharField(max_length=256, blank=False, null=False)  # 课题名
    type = models.CharField(max_length=256, blank=False, null=False)  # 课题类型，考虑另设一张表？？？
    leader = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # 课题负责老师
'''


class InstrumentManager(models.Model):  # 仪器管理员
    manager_id = models.CharField(max_length=20, primary_key=True)  # 管理员号/用户名
    name = models.CharField(max_length=256, blank=False, null=False)
    password = models.CharField(max_length=20, blank=False, null=False, default="password")  # 密码，，暂时未采取加密
    email = models.CharField(max_length=256)  # 邮箱
    phone = models.CharField(max_length=256)  # 电话
    comment = models.CharField(max_length=256)  # 备注


class Timestamp(models.Model):
    # 使用默认pk作为键
    # 每一个小时作为一列，表示时间段，0-23，比如0代表0:00-1:00
    t0 = models.CharField(max_length=1, default='0')
    t1 = models.CharField(max_length=1, default='0')
    t2 = models.CharField(max_length=1, default='0')
    t3 = models.CharField(max_length=1, default='0')
    t4 = models.CharField(max_length=1, default='0')
    t5 = models.CharField(max_length=1, default='0')
    t6 = models.CharField(max_length=1, default='0')
    t7 = models.CharField(max_length=1, default='0')
    t8 = models.CharField(max_length=1, default='0')
    t9 = models.CharField(max_length=1, default='0')
    t10 = models.CharField(max_length=1, default='0')
    t11 = models.CharField(max_length=1, default='0')
    t12 = models.CharField(max_length=1, default='0')
    t13 = models.CharField(max_length=1, default='0')
    t14 = models.CharField(max_length=1, default='0')
    t15 = models.CharField(max_length=1, default='0')
    t16 = models.CharField(max_length=1, default='0')
    t17 = models.CharField(max_length=1, default='0')
    t18 = models.CharField(max_length=1, default='0')
    t19 = models.CharField(max_length=1, default='0')
    t20 = models.CharField(max_length=1, default='0')
    t21 = models.CharField(max_length=1, default='0')
    t22 = models.CharField(max_length=1, default='0')
    t23 = models.CharField(max_length=1, default='0')


class Instrument(models.Model):
    # 使用默认仪器id
    # ins_id = models.CharField(max_length=20, primary_key=True)  # 仪器id
    name = models.CharField(max_length=256, blank=False, null=False)
    func = models.CharField(max_length=1024, blank=False, null=False)  # 功能描述
    manager = models.ForeignKey(InstrumentManager, on_delete=models.CASCADE)  # 级联删除仪器，不合理，暂时这么处理！！！！

    state = models.CharField(max_length=200, blank=False, null=False) # 仪器状态（空闲、正在使用、维修）
    address = models.CharField(max_length=500, blank=False, null=False) # 仪器所在位置
    manufacturer = models.CharField(max_length=500, blank=False, null=False) # 仪器生产商
    purchaseDate = models.DateField('购买日期', auto_now=True)  # 购买日期
    type = models.CharField(max_length=1024, blank=False, null=False)  # 型号规格
    technicalParameters = models.CharField(max_length=1024, blank=False, null=False)  # 技术参数
    picture = models.ImageField(upload_to='picture', default="media/default.png") # 仪器图片


class account(models.Model):
    user_id = models.CharField(max_length=50)
    password = models.CharField(max_length=50, default='0000')
    student_name = models.CharField(max_length=50, default='Walden')
    masterOrStudent = models.CharField(max_length=50, default='student')


class Appointment(models.Model):
    app_id = models.CharField(max_length=20, primary_key=True)  # 预约id，主码
    user_id = models.ForeignKey(Student, on_delete=models.CASCADE, null=False, blank=False)  # 预约学生
    ins_id = models.ForeignKey(Instrument, on_delete=models.CASCADE, null=False, blank=False)  # 预约的仪器
    #2020.11.28 hzh补充：添加了db_index
    app_datetime = models.DateTimeField('申请日期', auto_now=True, db_index=True)
    use_date = models.DateField('使用日期', auto_now=True)
    use_time = models.CharField(max_length=24, default='000000000000000000000000')  # 时间bitmap，代表24个小时，1代表申请的时段
    state = models.CharField(max_length=20, default='等待审批')  # 等待审批，审批通过，审批未通过
    comment = models.CharField(max_length=256)  # 备注


class Application_For_Group(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    approve_status = models.CharField(max_length=32)

    class Meta:
        unique_together = ('student_id', 'group_id')

    def save(self, *args, **kwargs):
        if self.approve_status not in ['未审批', '通过', '不通过']:
            raise ValidationError('审批状态出错')
        super().save(*args, **kwargs)

class Feedback(models.Model):
    app_id = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    comments = models.CharField(max_length=512)

from django.utils.html import format_html
#hzh modified on 2020.11.29
class Index_Rolling_Pictures(models.Model):
    image_url = models.CharField(verbose_name='图片',max_length=100)

    def image_data(self):
        return format_html(
            '<img src="{}" width="100px"/>',
            self.image_url,
        )
    image_data.short_description = u'图片'

# 轮播图
#hzh modified on 2020.11.29
'''
class Banner(models.Model):
    image_url = models.URLField(default="", verbose_name="轮播图链接")
    priority = models.IntegerField(verbose_name="优先级")
    #news = models.OneToOneField("News", on_delete=models.CASCADE)

    class Meta:
        # 默认排序
        #ordering = ["-update_time", "-id"]
        # 指明数据库名
        db_table = "tb_banner"
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"Banner({self.id}, {self.image_url})"

'''

'''
from datetime import datetime


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"轮播图", max_length=100)
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name
'''
