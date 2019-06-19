from django import forms

class LoginForm(forms.Form):
    pass
    wms_name = forms.CharField(label = "Name",
                    required = True)
    wms_password = forms.CharField(widget = forms.PasswordInput(),
                    label = 'Password',
                    required = True)


class department_form(forms.Form):
    wms_dname = forms.CharField(label = '部门名称',
                    required = True)
    wms_minimum_wage = forms.DecimalField(
        max_digits = 12,
        decimal_places = 3,
        label = '最低薪资',
        required = True
    )
    # wms_dnumber = forms.IntegerField(
    #     label = '部门人数',
    #     required = True
    # )

class department_create_form(department_form):
    # wms_dcode = forms.IntegerField(label = '部门代码',
    #                 required = True)
    pass

class staff_form(forms.Form):
    wms_sname = forms.CharField(
        label = '员工名称',
        required = True
    )
    wms_sgender = forms.CharField(
        label = '员工性别',
        required = True
    )
    wms_sage = forms.IntegerField(
        label = '员工年龄',
        required = True
    )
    wms_dcode = forms.IntegerField(
        label = '所属部门代码',
        required = True
    )

class staff_create_form(staff_form):
    # wms_scode = forms.IntegerField(
    #     label = '员工代码',
    #     required = True
    # )
    pass

class attendance_form(forms.Form):
    wms_overtime_num = forms.IntegerField(
        label = '本月加班数',
        required = True
    )
    wms_absent_num = forms.IntegerField(
        label = '本月缺勤数',
        required = True
    )

class attendance_create_form(attendance_form):
    wms_scode = forms.IntegerField(
        label = '员工代码',
        required = True
    )
    wms_ayear = forms.IntegerField(
        label = '出勤年份',
        required = True
    )
    wms_amonth = forms.IntegerField(
        label = '出勤月份',
        required = True
    )