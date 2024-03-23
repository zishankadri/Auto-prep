from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

from .models import Klass, Student, Faq
from customadmin.models import GeneralData
from .forms import KlassForm

# PayPal Integration
from django.urls import reverse
from .forms import CustomPayPalPaymentsForm
from django.utils import timezone


def has_access(user):
    return user.is_paid_member


def home(request):
    if request.user.is_authenticated:
        return redirect('/classes/')
    
    faq_list = Faq.objects.all()
    return render(request, "home.html", {'faq_list': faq_list})


def payment_page(request):
    import uuid
    uid = str(uuid.uuid4()).replace("-", "")[:12]
    domain_name = request.build_absolute_uri('/')[:-1]
    general_data = GeneralData.get_or_create()
    MONTHLY_PRICE = general_data.monthly_price
    YEARLY_PRICE = general_data.yearly_price

    monthly = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        # "amount": "10.00",
        "item_name": "Monthly",
        "invoice": uid,

        # Subscription
        #  - First month discount.
        "a1": MONTHLY_PRICE,
        "p1": 1,
        "t1": "M",

        "cmd": "_xclick-subscriptions",
        "a3": MONTHLY_PRICE,      # monthly price
        # duration of each unit (depends on unit)
        "p3": 1,
        "t3": "M",                         # duration unit ("M for Month")
        "src": "1",                        # make payments recur
        "sra": "1",                        # reattempt payment on payment error
        "no_note": "1",                    # remove extra notes (optional)

        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment_successful')),
        "cancel_return": request.build_absolute_uri(reverse('payment_failed')),
        # Custom command to correlate to some function later (optional)
        "custom": request.user.id,
    }
    # YEARLY
    yearly = monthly.copy()
    # - first year discount.
    yearly["a1"] = YEARLY_PRICE
    yearly["t1"] = "Y"

    yearly["a3"] = YEARLY_PRICE
    yearly["t3"] = "Y"
    yearly["item_name"] = "Yearly"

    # Create the instance.
    monthly_form = CustomPayPalPaymentsForm(
        initial=monthly, button_type="subscribe")
    yearly_form = CustomPayPalPaymentsForm(
        initial=yearly, button_type="subscribe")

    context = {
        "MONTHLY_PRICE": MONTHLY_PRICE,
        "YEARLY_PRICE": YEARLY_PRICE,
        "monthly_form": monthly_form,
        "yearly_form": yearly_form,

    }

    return render(request, "payment_page.html", context)


def payment_successful_view(request):
    request.user.is_paid_member = True
    request.user.save()
    return render(request, "payment-successfull.html")


def payment_failed_view(request):
    return render(request, "payment-failed.html")


@login_required
@user_passes_test(has_access, login_url="/payment/")
def classes(request, klass_id=None):
    klass = None

    if request.method == "POST":
        print("hello")
        print(request.POST)
        klass = Klass.objects.get(id=klass_id)
        student_list = Student.objects.filter(klass=klass)

        if 'add_student' in request.POST:
            first_name = request.POST['fname']
            last_name = request.POST['lname']
            klass_id = request.POST['klass_id']

            klass = Klass.objects.get(id=klass_id)

            new_student = Student(first_name=first_name,
                                  last_name=last_name, klass=klass)
            # Add grade columns if already exist
            if len(student_list) >= 1:
                for i in range(len(student_list[0].grades)):
                    new_student.grades.append(None)

            new_student.save()
            # redirect

        if 'add_column' in request.POST:
            klass.add_grade_column()

        if 'removeGradeColumn' in request.POST:
            try:
                klass_id = request.POST['klass_id']
                index = int(request.POST['index'])
                if klass_id!=None or index!=None:
                    klass = Klass.objects.get(id=klass_id)
                    klass.remove_grade_column(index)
                    # return redirect('/classes/')
            except:
                messages.error(request, "Quelque chose s'est mal passé. Essayez de rafraîchir la page.")

    klasses = Klass.objects.filter(user=request.user)

    if not klass:
        try:
            klass = Klass.objects.get(id=klass_id)
        except:
            if len(klasses) <= 0:
                return redirect("/create_class/")
            return redirect(f"/classes/{klasses[0].id}/")

    student_list = Student.objects.filter(klass=klass)

    context = {
        'klass': klass,
        'klasses': klasses,
        'student_list': student_list,
    }

    return render(request, "classes.html", context)


@login_required
@user_passes_test(has_access, login_url="/payment/")
def create_class(request):
    if request.method == 'POST':
        # class_name = request.POST['class-name']
        first_names = request.POST.getlist('fname')
        last_names = request.POST.getlist('lname')

        # Validate
        if len(first_names) != len(last_names):
            return

        form = KlassForm(request.POST)
        # new_klass = Klass(name=class_name, user=request.user)
        # new_klass.save()
        if form.is_valid():
            new_klass = form.save(commit=False)
            new_klass.user = request.user
            new_klass = form.save()
        # Create all students and assign this klass
        for i in range(len(first_names)):
            new_student = Student(
                first_name=first_names[i], last_name=last_names[i])
            new_student.klass = new_klass
            new_student.save()

        return redirect('classes')

    form = KlassForm()

    return render(request, 'create_class.html', {'form': form})


# APIs
@login_required
@csrf_exempt
def update_klass(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        klass_name = data.get('name', '')
        klass_id = data.get('id', '')

        if klass_id and klass_name:
            klass = Klass.objects.get(id=klass_id)
            klass.name = klass_name
            klass.save()
            return JsonResponse({'id': klass.id, 'name': klass.name})
        else:
            return JsonResponse({'error': f'id and name are required'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)


@login_required
@csrf_exempt
def update_student(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        student_id = data.get('student_id', '')
        name = data.get('name', '')
        new_value = data.get('new_value', '')

        if not student_id or not name or not new_value:
            return JsonResponse({'error': f'students_id, name, and new_value are required.'}, status=400)

        student = Student.objects.get(id=student_id)
        if name == "fname":
            student.first_name = new_value
        elif name == "lname":
            student.last_name = new_value

        student.save()
        return JsonResponse({'success': 'Success!'})

    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)


@login_required
@csrf_exempt
def update_student_grade(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        student_id = data.get('student_id', '')
        index = data.get('index', '')
        new_value = data.get('new_value', '')

        if student_id == None or index == None or new_value == None:
            return JsonResponse({'error': f'students_id, name, and new_value are required.'}, status=401)

        try:
            student = Student.objects.get(id=student_id)
            student.grades[index] = new_value
            student.save()
        except:
            return JsonResponse({'error': f'invalid values provided, check the data types.'}, status=400)
        print("success")
        return JsonResponse({'success': 'Success!'}, status=200)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)


@login_required
@csrf_exempt
def delete_student(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        student_id = data.get('student_id', '')

        if student_id:
            student = Student.objects.get(id=student_id)
            student.delete()
            return JsonResponse({}, status=200)
        else:
            return JsonResponse({'error': f'student_id is required'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)


def cgv(request):
    return render(request, "cgv.html")