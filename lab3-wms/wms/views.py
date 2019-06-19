from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .models import TAccount, TDepartment, TStaff, TAttendance, TWage, TYearending
from decimal import Decimal

from .forms import LoginForm
from .forms import department_form, department_create_form
from .forms import staff_form, staff_create_form
from .forms import attendance_form, attendance_create_form

import io
from django.http import FileResponse

from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('SIMSUN', 'wms/font/SIMSUN.ttf'))

import json

# Create your views here.
# 登录
def login(request):
    # login_form = LoginForm()
    # if request.method == 'POST':
    #     login_form = LoginForm(request.POST)
    #     return redirect(request, 'wms/index')
    # return render(request, 'wms/login.html', {'login_form': login_form})
    return render(request, 'wms/login.html')
# 主页
def index(request):
    if 'wms_name' in request.POST and 'wms_password' in request.POST:
        # login_form = LoginForm(request.POST)
        wms_name = request.POST['wms_name']
        wms_password = request.POST['wms_password']
        try:
            wms_acc = TAccount.objects.get(name = wms_name)
            if wms_acc.password != wms_password:
                messages.error(request, "User or Password error!")
                # return render(request, 'wms/login.html', {'login_form': login_form})
                return render(request, 'wms/login.html')
            else:
                return render(request, 'wms/index.html')
        except:
            messages.error(request, "Sorry, but this User does not exist!")
            # return render(request, 'wms/login.html', {'login_form': login_form})
            return render(request, 'wms/login.html')
    else:
        # login_form = LoginForm()
        # return render(request, 'wms/index.html', {'login_form': login_form})
        return render(request, 'wms/index.html')

# 部门管理
def department(request):
    t_department = TDepartment.objects.all()
    number_list = []
    minimum_wage_list = []
    dname_list = []
    department_list = [[], [], []]
    element_list = ['部门人数', '部门最低薪资', '部门总工资']
    for each_t in t_department:
        number_list.append([each_t.dname, each_t.dnumber])
        minimum_wage_list.append([each_t.dname, float(each_t.minimum_wage)])
        department_list[0].append(each_t.dnumber)
        department_list[1].append(float(each_t.minimum_wage))
        department_list[2].append(float(each_t.dnumber * each_t.minimum_wage))
        dname_list.append(each_t.dname)
    print(number_list)
    print(minimum_wage_list)
    context = {}
    context['number_list'] = json.dumps(number_list)
    context['minimum_wage_list'] = json.dumps(minimum_wage_list)
    context['element_list'] = json.dumps(element_list)
    context['dname_list'] = dname_list
    context['department_list'] = department_list
    context['department'] = t_department
    return render(request, 'wms/department.html', context)
# 查询部门
def department_search(request):
    context = {}
    get_name = request.GET['q']
    t_department = TDepartment.objects.filter(dname = get_name)
    context['department'] = t_department
    return render(request, 'wms/department.html', context)
# 增加部门
def department_create(request):
    context = {}
    if request.method == 'POST':
        print("create with post method")
        # post_dcode = request.POST.get('wms_dcode')
        post_dname = request.POST.get('wms_dname')
        post_mininum_wage = request.POST.get('wms_minimum_wage')
        # post_dnumber = request.POST.get("wms_dnumber")
        TDepartment.objects.create(
            # dcode = post_dcode,
            dname = post_dname,
            minimum_wage = post_mininum_wage,
            # dnumber = post_dnumber
            dnumber = 0
        )
        messages.success(request, 'add a row to table succeed!')
        return redirect('department')
    print("create with get method")
    context['to_update'] = None
    context['create'] = True
    context['update'] = False
    return render(
        request,
        'wms/department-form.html',
        context
    )
# 删除部门
def department_delete(request):
    get_dcode = request.GET.get('wms_dcode')
    t_department = TDepartment.objects.get(dcode = get_dcode)
    if TStaff.objects.filter(dcode = t_department).count() != 0:
        messages.error(request, '该部门人数不为零，暂时无法删除')
        return redirect('department')
    TDepartment.objects.filter(dcode = get_dcode).delete()
    messages.success(request, "删除成功!")
    return redirect('department')
# 更新部门
def department_update(request):
    context = {}
    if request.method == 'POST':
        print("update with post method")
        get_dcode = request.GET.get('wms_dcode')
        post_dname = request.POST.get('wms_dname')
        post_mininum_wage = request.POST.get('wms_minimum_wage')
        # post_dnumber = request.POST.get("wms_dnumber")
        TDepartment.objects.filter(dcode = get_dcode).update(
            dname = post_dname,
            minimum_wage = post_mininum_wage
            # dnumber = post_dnumber
        )
        messages.success(request, 'update a row to department table succeed!')
        return redirect('department')
    print("update with get method")
    get_dcode = request.GET.get('wms_dcode')
    to_update = TDepartment.objects.get(dcode = get_dcode)
    context['create'] = False
    context['update'] = True
    context['to_update'] = to_update
    return render(
        request,
        'wms/department-form.html',
        context
    )
# 部门报表
def department_report(request):
    pdf_gen = SimpleDocTemplate("wms/pdf/department-table.pdf")
    elements = []
    data = [["部门代码", "部门名称", "最低薪资", "部门人数"]]
    t_department = TDepartment.objects.all()
    for each_d in t_department:
        data.append([each_d.dcode, each_d.dname, each_d.minimum_wage, each_d.dnumber])
    style = TableStyle([
                        ('ALIGN', (0,0), (-1, -1), 'CENTER'), # 所有行左右居中，
                        ('VALIGN', (0,0), (-1, -1), 'MIDDLE'), # 所有行上下居中
                        ('FACE',(0,0),(-1,-1),'SIMSUN'), #字体 
                        ('FONTSIZE',(1,1),(-1,-1),12),
                        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)                   
                      ])
    t = Table(data)
    t.setStyle(style)
    elements.append(t)
    pdf_gen.build(elements)
    file_resp = FileResponse(open('wms/pdf/department-table.pdf', 'rb'))
    file_resp['Content-Type'] = 'application/octet-stream'
    file_resp['Content-Disposition'] = 'attachment;filename="department-table.pdf"'
    return file_resp
# 员工管理
def staff(request):
    t_staff = TStaff.objects.all()
    return render(request, 'wms/staff.html', {'staff': t_staff})
# 增加员工
def staff_create(request):
    context = {}
    if request.method == 'POST':
        print("create with post method")
        # post_scode = request.POST.get('wms_scode')
        post_dcode = request.POST.get('wms_dcode')
        if TDepartment.objects.filter(dcode = post_dcode).count() == 0:  # 没有该部门
            messages.error(request, '所属部门不存在！')
            return redirect('staff')
        TStaff.objects.create(
            # scode = post_scode,
            sname = request.POST.get('wms_sname'),
            sgender = request.POST.get('wms_sgender'),
            sage = request.POST.get('wms_sage'),
            dcode = TDepartment.objects.get(dcode = post_dcode)
        )
        post_dnumber = TDepartment.objects.get(dcode = post_dcode).dnumber
        TDepartment.objects.filter(dcode = post_dcode).update(dnumber = post_dnumber + 1)
        messages.success(request, 'add a row to table succeed!')
        return redirect('staff')
    print("create with get method")
    wms_form = staff_create_form()
    context['staff_form'] = wms_form
    context['create'] = True
    context['update'] = False
    return render(
        request,
        'wms/staff-form.html',
        context
    )
# 删除员工
def staff_delete(request):
    get_scode = request.GET.get('wms_scode')
    original_dcode = TStaff.objects.get(scode = get_scode).dcode.dcode
    print(original_dcode)
    TStaff.objects.get(scode = get_scode).delete()
    original_dnumber = TDepartment.objects.get(dcode = original_dcode).dnumber
    TDepartment.objects.filter(dcode = original_dcode).update(dnumber = original_dnumber - 1)
    messages.success(request, '删除员工成功')
    return redirect('staff')
# 更新员工
def staff_update(request):
    get_scode = request.GET.get('wms_scode')
    if request.method == 'POST':
        print('update with method post')
        original_dcode = TStaff.objects.get(scode = get_scode).dcode.dcode
        post_dcode = request.POST.get('wms_dcode')
        if TDepartment.objects.filter(dcode = post_dcode).count() == 0:
            messages.error("抱歉！该部门不存在！")
            return redirect('staff')
        TStaff.objects.filter(scode = get_scode).update(
            sname = request.POST.get('wms_sname'),
            sgender = request.POST.get('wms_sgender'),
            sage = request.POST.get('wms_sage'),
            dcode = TDepartment.objects.get(dcode = post_dcode)
        )
        original_dnumber = TDepartment.objects.get(dcode = original_dcode).dnumber
        post_dnumber = TDepartment.objects.get(dcode = post_dcode).dnumber
        TDepartment.objects.filter(dcode = original_dcode).update(dnumber = original_dnumber - 1)
        TDepartment.objects.filter(dcode = post_dcode).update(dnumber = post_dnumber + 1)
        messages.success(request, '修改员工成功！')
        return redirect('staff')
    else:   # request.method == get
        context = {}
        wms_form = staff_form()
        to_update = TStaff.objects.get(scode = get_scode)
        print('update with method get')
        print(get_scode)
        print(to_update)
        context['staff_form'] = wms_form
        context['create'] = False
        context['update'] = True
        context['to_update'] = to_update
        return render(request, 'wms/staff-form.html', context)
# 按员工代码查询
def staff_search_scode(request):
    context = {}
    get_scode = request.GET['q']
    m_staff = TStaff.objects.get(scode = get_scode)
    m_wage = TWage.objects.filter(scode = m_staff)
    context['t_wage'] = m_wage
    return render(request, 'wms/wage.html', context)
def staff_search_sname(request):
    return HttpResponse('TODO: the same thing')
# 出勤信息管理
def attendance(request):
    t_attendance = TAttendance.objects.all()
    return render(request, 'wms/attendance.html', {'t_attendance': t_attendance})
# 增加出勤信息
def attendance_create(request):
    context = {}
    if request.method == 'POST':
        print("create with post method")
        post_scode = request.POST.get('wms_scode')
        if TStaff.objects.filter(scode = post_scode).count() == 0:  # 没有该员工
            messages.error(request, '该员工不存在')
            return redirect('attendance')
        TAttendance.objects.create(
            scode = TStaff.objects.get(scode = post_scode),
            ayear = request.POST.get('wms_ayear'),
            amonth = request.POST.get('wms_amonth'),
            overtime_num = request.POST.get('wms_overtime_num'),
            absent_num = request.POST.get('wms_absent_num'),
        )
        messages.success(request, 'add a row to table succeed!')
        return redirect('attendance')
    print("create with get method")
    wms_form = attendance_create_form()
    context['attendance_form'] = wms_form
    context['create'] = True
    context['update'] = False
    return render(
        request,
        'wms/attendance-form.html',
        context
    )
# 删除出勤信息
def attendance_delete(request):
    get_scode = request.GET.get('wms_scode')
    get_ayear = request.GET.get('wms_ayear')
    get_amonth = request.GET.get('wms_amonth')
    TAttendance.objects.get(
        scode = TStaff.objects.get(scode = get_scode),
        ayear = get_ayear,
        amonth = get_amonth
    ).delete()
    messages.success(request, '删除出勤信息成功')
    return redirect('attendance')
# 更新出勤信息
def attendance_update(request):
    get_scode = request.GET.get('wms_scode')
    get_ayear = request.GET.get('wms_ayear')
    get_amonth = request.GET.get('wms_amonth')
    if request.method == 'POST':
        print('update with method post')
        TAttendance.objects.filter(
            scode = TStaff.objects.get(scode = get_scode),
            ayear = get_ayear,
            amonth = get_amonth
        ).update(
            overtime_num = request.POST.get('wms_overtime_num'),
            absent_num = request.POST.get('wms_absent_num')
        )
        messages.success(request, '修改出勤信息成功！')
        return redirect('attendance')
    else:   # request.method == get
        context = {}
        wms_form = attendance_form()
        to_update = TAttendance.objects.get(
            scode = TStaff.objects.get(scode = get_scode),
            ayear = get_ayear,
            amonth = get_amonth
        )
        print('update with method get')
        context['attendance_form'] = wms_form
        context['create'] = False
        context['update'] = True
        context['to_update'] = to_update
        return render(request, 'wms/attendance-form.html', context)

# 工资信息管理，这部分应该是系统中最复杂的了，因为牵扯的关系比较多
def wage(request):
    # return HttpResponse('TODO: the most difficult part in the system design')
    t_attendance = TAttendance.objects.all()
    for each_a in t_attendance:
        each_w, created = TWage.objects.get_or_create(
            scode = each_a.scode,
            wyear = each_a.ayear,
            wmonth = each_a.amonth,
            defaults = {
                'basic_wage': Decimal('0.000'),
                'bonus': Decimal('0.000'),
                'withhold': Decimal('0.000'),
                'due_wage': Decimal('0.000'),
                'final_wage': Decimal('0.000')
            }
        )
        each_w = TWage.objects.filter(
            scode = each_a.scode,
            wyear = each_a.ayear,
            wmonth = each_a.amonth,
        )
        w_basic_wage = each_a.scode.dcode.minimum_wage
        w_full_time_bonus = Decimal('0.000')
        w_withhold = Decimal('0.000')
        if each_a.absent_num <= 0:
            w_full_time_bonus = w_basic_wage * Decimal('0.300')
        else:
            w_withhold = each_a.absent_num * w_basic_wage * Decimal('0.030')
        w_bonus = each_a.overtime_num * w_basic_wage * Decimal('0.050') + w_full_time_bonus
        each_w.update(
            basic_wage = w_basic_wage,
            bonus = w_bonus,
            withhold = w_withhold,
            due_wage = w_basic_wage + w_bonus - w_withhold,
            final_wage = w_basic_wage + w_bonus - w_withhold
        )
    t_wage = TWage.objects.all()
    return render(request, 'wms/wage.html', {'t_wage': t_wage})

# 年终奖模块
def yearending(request):
    TYearending.objects.all().update(
        total_amount = Decimal('0.000'),
        year_bonus = Decimal('0.000')
    )
    t_wage = TWage.objects.all()
    for each_w in t_wage:
        each_yb, created = TYearending.objects.get_or_create(
            scode = each_w.scode,
            year = each_w.wyear,
            defaults = {
                'total_amount': Decimal('0.000'),
                'year_bonus': Decimal('0.000')
            }
        )
        each_yb = TYearending.objects.filter(
            scode = each_w.scode,
            year = each_w.wyear
        ).update(
            year_bonus = (each_yb.total_amount + each_w.final_wage) / (Decimal('12.000')),
            total_amount = each_yb.total_amount + each_w.final_wage
        )
    t_yb = TYearending.objects.all()
    return render(request, 'wms/yearending.html', {'t_yb': t_yb})
def wage_report(request):
    t_department = TDepartment.objects.all()
    data_list = []
    for each_t in t_department:
        data_list.append([each_t.dname, each_t.dnumber])
    print(data_list)
    return render(
        request,
        'wms/wage-report.html',
        {'List': json.dumps(data_list)}
    )