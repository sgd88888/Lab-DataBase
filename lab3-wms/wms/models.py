# import os, django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dbAppDesign.settings")# project_name 项目名称
# django.setup()

from django.db import models

# Create your models here.
# TODO: add index for field of table
# 部门信息表
class TDepartment(models.Model):
    # dcode = models.IntegerField(primary_key = True)
    dcode = models.AutoField(primary_key = True)
    dname = models.CharField(max_length = 20, blank = False)
    minimum_wage = models.DecimalField(max_digits = 12, decimal_places = 3)
    dnumber = models.IntegerField() # 部门人数
    # def __str__(self):
    #     return ("code: " + self.dcode + " name: " + self.dname + " minimum_wage: " + self.minimum_wage + " number of staff: " + self.dnumber)
    def __str__(self):
        return ("department name: " + self.dname)
# 员工基本信息表
class TStaff(models.Model):
    # scode = models.IntegerField(primary_key = True)
    scode = models.AutoField(primary_key = True)
    sname = models.CharField(max_length = 20, blank = False)
    # spassword = models.CharField(max_length = 20, blank = False)
    sgender = models.CharField(max_length = 2)
    sage = models.IntegerField()
    dcode = models.ForeignKey(TDepartment, on_delete = models.PROTECT)
    def __str__(self):
        return ("staff name: " + self.sname)
# 奖金信息表
# 可以通过出勤信息表算出来
# class TBonus(models.Model):
#     scode = models.ForeignKey(TStaff, on_delete = models.CASCADE)
#     byear = models.IntegerField(blank = False)
#     bmonth = models.IntegerField(blank = False)
#     full_work_bonus = models.DecimalField(max_digits = 12, decimal_places = 3)  # 全勤奖
#     overtime_bonus = models.DecimalField(max_digits = 12, decimal_places = 3)   # 加班奖
#     # yearend_bonus = models.DecimalField(max_digits = 12, decimal_places = 3)  # 年终奖
#     class Meta:
#         unique_together = ('scode', 'byear', 'bmonth')
# 工资信息表
class TWage(models.Model):
    scode = models.ForeignKey(TStaff, on_delete = models.CASCADE)
    wyear = models.IntegerField(blank = False)
    wmonth = models.IntegerField(blank = False)
    basic_wage = models.DecimalField(max_digits = 12, decimal_places = 3)
    bonus = models.DecimalField(max_digits = 12, decimal_places = 3)
    due_wage = models.DecimalField(max_digits = 12, decimal_places = 3)
    withhold = models.DecimalField(max_digits = 12, decimal_places = 3)
    final_wage = models.DecimalField(max_digits = 12, decimal_places = 3)
    class Meta:
        unique_together = ('scode', 'wyear', 'wmonth')
# 出勤信息表
class TAttendance(models.Model):
    scode = models.ForeignKey(TStaff, on_delete = models.CASCADE)
    ayear = models.IntegerField(blank = False)
    amonth = models.IntegerField(blank = False)
    overtime_num = models.IntegerField()
    absent_num = models.IntegerField()
    class Meta:
        unique_together = ('scode', 'ayear', 'amonth')
# 年终奖信息表
class TYearending(models.Model):
    scode =  models.ForeignKey(TStaff, on_delete = models.CASCADE)
    year = models.IntegerField(blank = False)
    total_amount = models.DecimalField(max_digits = 12, decimal_places = 3)
    year_bonus = models.DecimalField(max_digits = 12, decimal_places = 3)
    class Meta:
        unique_together = ('scode', 'year')
# 账号信息表
class TAccount(models.Model):
    # acc_id = models.IntegerField(primary_key = True)
    acc_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    # isAdmin = models.BooleanField()
    # def __str__(self):
    #     return ("id: " + self.acc_id + ", name: " + self.name)