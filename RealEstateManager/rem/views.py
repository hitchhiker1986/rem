from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import *
from django.core.mail import EmailMessage
from .forms import DictForm, TenantForm, CheckForm, ApartmentCreateForm, PaymentBillForm, BillForm, BillAndPaymentBillFormSet, SentContractForm, CreateUtilityForm, task_form
from django.core import management
from datetime import datetime
from .handlers import handle_uploaded_file
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

    return render(request, 'apartment/apartment_list.html', {'apartments': apartments})


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

    return render(request, "apartment/apartment.html", {'apartment': apartment})


@login_required
def tenant_show(request, user_id):
    tenant = Tenant.objects.get(user__id=user_id)
    return render(request, "tenant_show.html", {"tenant": tenant})


@login_required
def owner_show(request, user_id):
    owner = Owner.objects.get(id=user_id)
    return render(request, "owner_show.html", {'owner': owner})


@login_required
def tenant_modify(request, user_id):
    tenant = Tenant.objects.get(id=user_id)
    form = TenantForm(request.POST, instance=tenant)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/test/')
        else:
            for error in form.errors:
                print(error)
            form=TenantForm(instance=tenant)

    return render(request, "tenant_modify.html", {'form': form, 'tenant': tenant})
##########################################################

@login_required
def home_view(request):
    return render(request, 'home.html')


def thanks(request):
    return render(request, 'thanks.html')


def dict_form(request, pk_id):
    if request.method == 'POST':
        utility = Utility.objects.get(id=pk_id)
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
                str(utility.get_serial()) + " diktalasa sikeres volt. A meroora uj erteke: " + str(utility.get_current()),
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


def apartment_createform(request):
    form = ApartmentCreateForm(request.POST)
    if request.method == 'POST':
        apartment = Apartment()
        if form.is_valid():
            apartment.address = form.cleaned_data['address']
            apartment.city = form.cleaned_data['city']
            apartment.zip = form.cleaned_data['zip']
            apartment.floor = form.cleaned_data['floor']
            apartment.district = form.cleaned_data['district']
            apartment.topographical_nr = form.cleaned_data['topographical_nr']
            apartment.size = form.cleaned_data['size']
            apartment.balcony_size = form.cleaned_data['balcony_size']
            apartment.rooms = form.cleaned_data['rooms']
            apartment.halfrooms = form.cleaned_data['halfrooms']
            apartment.save()

    return render(request, 'apartment/apartment_createform.html', {'form': form})



def apartment_checkform(request, apt_id):
    apartment = Apartment.objects.get(id=apt_id)
    form = CheckForm(request.POST)
    ch = CheckHistory()

    check_result = True
    print(request.method)
    if request.method == "POST":
        print('it was just submitted')
        if form.is_valid():
            ch.checkDate = datetime.now()
            ch.cleaning = form.cleaned_data['cleaning']
            ch.smoke = form.cleaned_data['smoke']
            ch.damage = form.cleaned_data['damage']
            ch.equipment_damage = form.cleaned_data['equipment_damage']
            ch.animal = form.cleaned_data['animal']
            ch.not_allowed_tenants = form.cleaned_data['not_allowed_tenants']
            ch.description = form.cleaned_data['description']
            ch.save()
            #apartment.check_history.add(ch)
            for data in form.cleaned_data.values():
                print(data)
                if data is False:
                    check_result = False
                    break
            if check_result:
                management.call_command('create_check_tasks', apt_id)
            else:
                apartment.check_status = False
                apartment.save()
                management.call_command('create_check_tasks', apt_id)

            return HttpResponseRedirect("/thanks")

    return render(request, 'apartment/apartment_checkform.html', {'form': form})


@login_required
def test_view(request):
    return render(request, 'test.html')


@login_required
def todo_list(request):
    if request.user.is_superuser:
        todos = ToDo.objects.all()
    else:
        todos = ToDo.objects.filter(task_responsible=request.user)
    return render(request, "todos/todo_list.html", {"todos": todos})

def task_show_and_modify(request, pk_id):
    task = ToDo.objects.get(pk=int(pk_id))
    if request.method == 'POST':
        form = task_form(request.POST, instance=task)
        if form.is_valid():
            new_task = form.save(commit=False)
            # new_task.task_responsible = form.cleaned_data['task_responsible']
            new_task.save()
    else:
        form = task_form(instance=task)

    return render(request, 'todos/todo_form.html', {'form': form})

def create_task(request):
    form = task_form(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.save()
    return render(request, 'todos/todo_form.html', {'form': form})


@login_required
def apartment_details(request, apt_id):
    apartment = Apartment.objects.get(id=apt_id)
    return render(request, "apartment/apartment_details.html", {"apartment": apartment})


@login_required
def apartment_owners(request, apt_id):
    apartment = Apartment.objects.get(id=apt_id)
    owners = apartment.owner.all()
    return render(request, "apartment/apartment_owners.html", {"owners": owners})


@login_required
def apartment_tenants(request, apt_id):
    apartment = Apartment.objects.get(id=apt_id)
    tenants = apartment.tenant.all()
    return render(request, "apartment/apartment_tenants.html", {"tenants": tenants})


@login_required
def apartment_contracts(request, apt_id):
    apartment = Apartment.objects.get(id=apt_id)
    return render(request, "apartment/apartment_contracts.html", {"apartment": apartment})


@login_required
def apartment_history(request, apt_id):
    apartment = Apartment.objects.get(id=apt_id)
    return render(request, "apartment/apartment_history.html", {"apartment": apartment})


@login_required
def apartment_utilities(request, apt_id):
    utilities = Utility.objects.filter(apartment_id=apt_id)
    # utilities = apartment.utilities.all()
    return render(request, "apartment/apartment_utilities.html", {"utilities": utilities})


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


def bill_form_view(request, pb_id):
    pb = PaymentBill.objects.get(id=pb_id)
    bill = Bill()
    form=BillForm(request.POST)
    if request.method == "POST" and form.is_valid():
        bill.bill_number = form.cleaned_data['bill_number']
        bill.amount = form.cleaned_data['amount']
        bill.save()
        return HttpResponseRedirect("#")

    return render(request, "bill_form.html", {'form': form})

class PaymentBillInline():
    form_class = PaymentBillForm
    model = PaymentBill
    template_name = 'paymentbill.html'

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()
        # for every formset, attempt to find a specific formset save function
        #otherwise, just save
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)

            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()

        return redirect('/test')

    def formset_bill_valid(self, formset):
        bills = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for bill in bills:
            bill.payment_bill = self.object
            bill.save()

def payment_bill_view(request):
    pb = PaymentBill()
    form = PaymentBillForm(request.POST)


    if request.method=='POST' and form.is_valid():
        pb.issuer=form.cleaned_data['issuer']
        pb.issuer_name = form.cleaned_data['issuer_name']
        pb.issuer_address = form.cleaned_data['issuer_address']
        pb.issuer_tax_nr = form.cleaned_data['issuer_tax_nr']
        pb.buyer_name = form.cleaned_data['buyer_name']
        pb.buyer_address = form.cleaned_data['buyer_address']
        pb.amount_text=form.cleaned_data['amount_text']
        pb.cashier=form.cleaned_data['cashier']
        pb.save()
        print(pb.id)

        return HttpResponseRedirect('bill_form/%s' % pb.id)
    return render(request, 'paymentbill.html', {'form': form})

def apartment_sent_contract_form(request, apt_id):
    apartment = Apartment.objects.get(id=apt_id)
    form = SentContractForm(request.POST, request.FILES, instance=apartment)
    if request.method == 'POST':
        if form.is_valid():
            print("this is valid")

            for file in request.FILES.getlist('file'):
                apartment.sent_contract = file
            apartment.save()
            return HttpResponseRedirect('/apartment/%s/contracts' % apt_id)
        else:
            print(form.errors)
    return render(request, 'apartment/sent_contract_form.html', {'form': form})

def create_utility_form(request):
    form = CreateUtilityForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            util = Utility()
            util.serial = form.cleaned_data['serial']
            util.current = form.cleaned_data['current']
            util.dict_start_day = form.cleaned_data['dict_start_day']
            util.dict_end_day = form.cleaned_data['dict_end_day']
            util.provider = form.cleaned_data['provider']
            util.utility = form.cleaned_data['utility_type']
            util.utility_unit = form.cleaned_data['utility_unit']
            util.apartment = form.cleaned_data['apartment']
            util.save()

            return HttpResponseRedirect("/test/")
        else:
            print(form.errors)
            form = CreateUtilityForm(request.POST)

    return render(request, 'utility/create_utility_form.html', {'form': form})
