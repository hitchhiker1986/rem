from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import *
from django.core.mail import EmailMessage
from .forms import DictForm

# Create your views here.


@login_required
def apartment_list(request):
    apartments = {}
    if request.user.is_staff:
        apartments = Apartment.objects.all()

    if request.user.groups.filter(name="Tenants").exists():
        apartments = Apartment.objects.filter(tenant__user__username__contains=request.user)

    if request.user.groups.filter(name="Owners").exists():
        apartments = Apartment.objects.filter(owner__user__username__contains=request.user)

    return render(request, 'apartment_list.html', {'apartments': apartments})


@login_required
def tenant_list(request):
    tenants = None

    if request.user.is_staff:
        print("admin is logged in")
        tenants = Tenant.objects.all()

    if request.user.groups.filter(name="Tenants").exists():
        tenants = Tenant.objects.filter(user__username__contains=request.user)

    for tenant in tenants:
        print(tenant.user.username)

    return render(request, 'tenant_list.html', {'tenants': tenants})


@login_required
def owner_list(request):
    owners = None
    if request.user.is_staff:
        owners = Owner.objects.all()

    if request.user.groups.filter(name="Owners").exists():
        owners = Owner.objects.filter(user__username__contains=request.user)
        for owner in owners:
            print(owner.user)

    return render(request, "owner_list.html", {'owners': owners})


@login_required
def utility_list(request):
    utilities = Utility.objects.all()
    return render(request, 'utility_list.html', {'utilities': utilities})


##########################################################
##########################################################
# functions to display selected element
@login_required
def apartment_show(request, apt_id):
    apartment = Apartment.objects.get(id=apt_id)

    return render(request, "apartment.html", {'apartment': apartment})


@login_required
def tenant_show(request, user_id):
    tenant = Tenant.objects.get(user__id=user_id)
    return render(request, "tenant_show.html", {"tenant": tenant})


@login_required
def owner_show(request, user_id):
    owner = Owner.objects.get(user__id=user_id)
    return render(request, "owner_show.html", {'owner': owner})


##########################################################
@login_required
def home_view(request):
    return render(request, 'home.html')


def dict_form(request, serial):
    if request.method == 'POST':
        utility = Utility.objects.get(serial = serial)
        form = DictForm(request.POST, instance=utility)
        if form.is_valid():
            form.save()
            utility.set_current(request.POST['current'])
            utility.save()
            dh = DictHistory()
            dh.update_serial(utility.get_serial())
            dh.dict_value = request.POST['current']
            dh.save()
            email = EmailMessage(
                "Dict successful",
                str(serial) + " diktalasa sikeres volt. A meroora uj erteke: " + str(utility.get_current()),
                "papplaszlopft@gmail.com",
                {"papp.l@icloud.com"},
            )
            email.send()
            return HttpResponseRedirect("/test/")

        else:
            for error in form.errors:
                print(error)
            form = DictForm()
    else:
        form = DictForm(request.POST)
    return render(request, 'dict.html', {'form': form})


@login_required
def test_view(request):
    return render(request, 'test.html')


@login_required
def todo_list(request):
    todos = ToDo.objects.filter(responsible=request.user)
    return render(request, "todo_list.html", {"todos": todos})


@login_required
def apartment_details(request, apt_id):
    apartment = Apartment.objects.get(id=apt_id)
    return render(request, "apartment_details.html", {"apartment": apartment})


@login_required
def apartment_owners(request, apt_id):
    apartment = Apartment.objects.get(id=apt_id)
    owners = apartment.owner.all()
    return render(request, "apartment_owners.html", {"owners": owners})


@login_required
def apartment_tenants(request, apt_id):
    apartment = Apartment.objects.get(id=apt_id)
    tenants = apartment.tenant.all()
    return render(request, "apartment_tenants.html", {"tenants": tenants})


@login_required
def apartment_contracts(request, apt_id):
    apartment = Apartment.objects.get(id=apt_id)
    return render(request, "apartment_contracts.html", {"apartment": apartment})


@login_required
def apartment_history(request, apt_id):
    apartment = Apartment.objects.get(id=apt_id)
    return render(request, "apartment_history.html", {"apartment": apartment})


@login_required
def apartment_utilities(request, apt_id):
    apartment = Apartment.objects.get(id=apt_id)
    utilities = apartment.utilities.all()
    return render(request, "apartment_utilities.html", {"utilities": utilities})


def dict_years(request):
    dict_history = DictHistory.objects.all().values()
    years = []
    for dh in dict_history:
        years.append(dh['dict_date'].year)

    years = list(dict.fromkeys(years))

    return render(request, "dict_years.html", {"years": years})


def dict_list(request, year):
    dict_history = DictHistory.objects.filter(dict_date__year=year)
    dict_history = dict_history.order_by('utility_serial').values()
    serials = dict_history.values('utility_serial').distinct()

    dicts = []
    for serial in serials:
        arr = []
        for dh in dict_history:
            if dh['utility_serial'] == serial['utility_serial']:
                arr.append({'value': dh['dict_value'], 'month': dh['dict_date'].month})

        util = {'serial': serial['utility_serial'], 'arr': arr}

        dicts.append(util)

    return render(request, "dict_list.html", {"dicts": dicts})
