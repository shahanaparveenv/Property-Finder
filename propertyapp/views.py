from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from propertyapp.filters import LocationFilter
from propertyapp.forms import LoginRegister, TenantRegister, AgentRegister, PropertyAgentForm, TenantFeedbackForm
from propertyapp.models import Agent, Property, Tenant, AddToCart, BuyNow, Payment, TenantFeedback


# Create your views here.
#index page-home
def home(request):
    return render(request, 'main/index.html')
def services(request):
    return render(request, 'main/services.html')
def contact(request):
    return render(request, 'main/contact.html')
def about(request):
    return render(request, 'main/about.html')


#add new tenant
def tenant_add(request):
    form1 = LoginRegister()
    form2 = TenantRegister()
    if request.method == 'POST':
        form1 = LoginRegister(request.POST)
        form2 = TenantRegister(request.POST, request.FILES)

        if form1.is_valid() and form2.is_valid():
            a = form1.save(commit=False)
            a.is_tenant = True
            a.save()
            user1 = form2.save(commit=False)
            user1.user = a
            user1.save()
            return redirect('tenant_dashboard')
    return render(request, 'tenant/tenant_add.html', {'form1': form1, 'form2': form2})


#add new agent
def agent_add(request):
    form1 = LoginRegister()
    form2 = AgentRegister()
    if request.method == 'POST':
        form1 = LoginRegister(request.POST)
        form2 = AgentRegister(request.POST)

        if form1.is_valid() and form2.is_valid():
            a = form1.save(commit=False)
            a.is_agent = True
            a.save()
            user1 = form2.save(commit=False)
            user1.user = a
            user1.save()
            return redirect('agent_dashboard')
    return render(request, 'agent/agent_add.html', {'form1': form1, 'form2': form2})


#login for admin,tenants and agents
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('soldListAdmin')
            elif user.is_tenant:
                return redirect('tenant_property_view')
            elif user.is_agent:
                return redirect('viewProperty')
        else:
            messages.info(request, 'Invalid Credentials')
    return render(request, 'main/indexlogin.html')


#Propertys
@login_required(login_url='login_view')
def property_agent(request):
    user = request.user
    agentProperty = Agent.objects.get(user=user)
    form = PropertyAgentForm()
    if request.method == 'POST':
        form1 = PropertyAgentForm(request.POST, request.FILES)
        if form1.is_valid():
            a = form1.save(commit=False)
            a.agent = agentProperty
            a.save()
            messages.info(request, 'Property added')
            return redirect('viewProperty')
    return render(request, 'agent/add_property.html', {'form': form})


def property_display(request):
    user = request.user
    agentProperty = Agent.objects.get(user=user)
    data = Property.objects.filter(agent=agentProperty)
    return render(request, 'agent/property_display.html', {'data': data})


def property_view_general(request):
    data=Property.objects.all()
    return render(request,'main/property_view.html',{'data':data})
@login_required(login_url='login_view')
def property_delete(request, id):
    data = Property.objects.get(id=id)
    data.delete()
    return redirect('viewProperty')


# #general Property view
@login_required(login_url='login_view')
def property_view(request):
    data = Property.objects.all()
    return render(request, 'admin/property_view.html', {'data': data})


#Property view by tenant using decorator

@login_required(login_url='login_view')
def tenant_property_view(request):
    data = Property.objects.all()
    propertyFilter = LocationFilter(request.GET, queryset=data)
    propertys = propertyFilter.qs
    return render(request, 'tenant/tenant_property_view.html', {'data': propertys, 'propertys': propertyFilter})




#add Property to cart
@login_required(login_url='login_view')
def add_to_wishlist(request, id):
    user = request.user
    tenant = Tenant.objects.get(user=user)
    property = Property.objects.get(id=id)
    cart_item = AddToCart.objects.filter(tenant=tenant, property=property)
    if cart_item.exists():
        messages.info(request, "Item already exists")
        return redirect('tenant_property_view')
    else:
        obj = AddToCart(tenant=tenant, property=property)
        obj.save()
        return redirect('viewCart')


@login_required(login_url='login_view')
def viewCart(request):
    user = request.user
    tenant = Tenant.objects.get(user=user)
    data = AddToCart.objects.filter(tenant=tenant)
    return render(request, 'tenant/view_cart.html', {'data': data})


# buy now function
@login_required(login_url='login_view')
def buynow(request, id):
    user = request.user
    userid = Tenant.objects.get(user=user)
    property = Property.objects.get(id=id)
    if request.method == 'POST':

        address = request.POST.get('address')
        phonenumber = request.POST.get('phone')
        postcode = request.POST.get('post')

        a = Property.price
        total = int(a)
        obj = BuyNow()
        obj.user = userid
        obj.property = property
        obj.totalprice = total
        obj.address = address
        obj.phone = phonenumber
        obj.post = postcode
        obj.save()
        return redirect('payment', id=obj.id)
    return render(request, 'tenant/buy_now.html', {'user': user, 'userid': userid, 'property': property})


@login_required(login_url='login_view')
def paynow(request, id):
    buynow_id = BuyNow.objects.get(id=id)

    user = Tenant.objects.get(user=request.user)
    data = buynow_id
    c = data.property
    if request.method == 'POST':
        cardnumber = request.POST.get('cardnumber')
        cvv = request.POST.get('cvv')
        date = request.POST.get('date')
        Payment.objects.create(cardnumber=cardnumber, cvv=cvv, expiry_date=date, buynowProperty=buynow_id)
        data.buynow_status = 1
        data.save()
        return redirect('tenant_property_view')

    return render(request, 'tenant/payment.html', {'buynow_id': buynow_id, 'user': user})


@login_required(login_url='login_view')
def deleteItems(request, id):
    property = AddToCart.objects.get(id=id)
    property.delete()
    return redirect('viewCart')


@login_required(login_url='login_view')
def wishlistbuy(request, id):
    user = request.user
    userid = Tenant.objects.get(user=user)
    cartProperty = AddToCart.objects.get(id=id)
    property = cartProperty.property

    if request.method == 'POST':
        address = request.POST.get('address')
        phonenumber = request.POST.get('phone')
        postcode = request.POST.get('post')
        if len(phonenumber) == 10 :

            a = property.price
            total = int(a)
            obj = BuyNow()
            obj.user = userid
            obj.property = property
            obj.totalprice = total
            obj.address = address
            obj.phone = phonenumber
            obj.post = postcode
            obj.save()
            return redirect('payment', id=obj.id)
        else:
            messages.info(request, 'invalid phone number')
    return render(request, 'tenant/buy_from_cart.html', {'property': cartProperty, 'item': property})


#Log out
def logout_view(request):
    logout(request)
    return redirect('login_view')


# agents sold Propertys
def soldProperty(request):
    user = request.user
    agent_name = Agent.objects.get(user=user)
    data = Property.objects.filter(agent=agent_name, status_available=False)
    return render(request, 'agent/sold_propertys.html', {'data': data})


#list of sold Propertys to admin
def soldListAdmin(request):
    data = BuyNow.objects.filter(buynow_status=True)
    return render(request, 'admin/soldlist.html', {'data': data})

def tenant_view(request):
    data = Tenant.objects.all()
    return render(request,'admin/tenant_view.html',{'data':data})
def agent_view(request):
    data=Agent.objects.all()
    return render(request,'admin/agent_view.html',{'data':data})

def agent_delete(request,id):
    data=Agent.objects.get(id=id)
    data.delete()
    return redirect('agent_view')

def tenant_delete(request,id):
    data=Tenant.objects.get(id=id)
    data.delete()
    return redirect('tenant_view')
#list of ordered Propertys to tenant
def orderedProperty(request):
    user = request.user
    tenant = Tenant.objects.get(user=user)
    data = BuyNow.objects.filter(buynow_status=True, user=tenant)
    return render(request, 'tenant/order_list.html', {'data': data})

def error(request):
    return render(request,'main/error.html')
#admin dashboard
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')


#agent dashboard
def agent_dashboard(request):
    return render(request, 'agent/agentdashboard.html')


#tenant dashboard
def tenant_dashboard(request):
    return render(request, 'tenant/tenant_dashboard.html')

#feedback
@login_required(login_url='login_view')
def save_feedback(request):
    user=request.user
    tenant=Tenant.objects.get(user=user)
    data=TenantFeedbackForm()
    if request.method == 'POST':
        form = TenantFeedbackForm(request.POST)
        if form.is_valid():
            a=form.save(commit=False)
            a.user=tenant
            a.save()
            return redirect('tenant_feedback')
    return render(request,'tenant/feedback_form.html',{'form': data})


#tenant feedback viewing
@login_required(login_url='login_view')
def tenant_feedback(request):
    user=request.user
    tenant=Tenant.objects.get(user=user)
    data = TenantFeedback.objects.filter(user=tenant)
    return render(request, 'tenant/tenant_feedback.html', {'data': data})




@login_required(login_url='login_view')
def view_tenant_feedback(request):
    data = TenantFeedback.objects.all()
    return render(request, 'admin/feedback_view.html', {'data': data})


@login_required(login_url='login_view')
def admin_reply_feedback(request,id):

    feedback = TenantFeedback.objects.get(id=id)
    if request.method == 'POST' :
        r = request.POST.get('reply')
        feedback.reply = r
        feedback.save()
        messages.info(request,'Reply send for complaint')
        return redirect('view_tenant_feedback')
    return render(request,'admin/feedback_reply.html',{'feedback':feedback})



