# employee/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .forms  import EmployeeForm
from django.contrib import messages
from django.shortcuts import redirect, render

def employee_list(request):
    employees   = list(Employee.objects.order_by('employee_id'))
    create_form = EmployeeForm()
    edit_forms  = {e.id: EmployeeForm(instance=e) for e in employees}
    for e in employees: e.form = edit_forms[e.id]

    if request.method == 'POST':
        if 'create_employee' in request.POST:
            form = EmployeeForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                # Added alert message
                messages.success(request, "Employee created successfully!")
                return redirect('employee_list')
            else:
                print("⚠️ CREATE form invalid:", form.errors)

        # UPDATE
        elif 'edit_employee' in request.POST:
            emp = get_object_or_404(Employee, pk=request.POST['employee_id'])
            form = EmployeeForm(request.POST, request.FILES, instance=emp)
            if form.is_valid():
                form.save()
                # Added alert message
                messages.info(request, "Employee updated successfully!")
                return redirect('employee_list')
            else:
                print("⚠️ EDIT form invalid:", form.errors) 

        # DELETE
        elif 'delete_employee' in request.POST:
            eid = request.POST['employee_id']
            emp = get_object_or_404(Employee, pk=eid)
            emp.delete()
            # Added alert message
            messages.error(request, "Employee deleted successfully!")
            return redirect('employee_list')

    return render(request, 'employee/index.html', {
        'employees': employees,
        'create_form': create_form,
        'active_page': 'employees',
    })


