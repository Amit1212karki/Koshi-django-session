
from django.shortcuts import render, get_object_or_404, redirect
from event.models import *
from booking.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.

def index(request):
    index_events = Event.objects.all()
    print(index_events)
    return render(request, 'frontend/pages/index.html', {'events':index_events})

def viewDetails(request, id):
    single_event = Event.objects.get(id=id)
    tickets = Ticket.objects.filter(event=single_event)

    context = {
        'event':single_event,
        'tickets':tickets
    }

    print(context)
    return render(request, 'frontend/pages/event_detail.html', context)

def buyTicket(request, id, ticket_id):
    event = get_object_or_404(Event, pk=id)
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            quantity = int(request.POST['quantity'])
            total_amount = ticket.price * quantity
            full_name = request.POST['full_name']
            
            booking = Booking(
                user=request.user,
                full_name=full_name,
                event=event,
                ticket=ticket,
                quantity=quantity,
                total_amount=total_amount,
                payment_status='unpaid'
            )
            booking.save()
            return redirect('/booking-success/')
        else:
            return redirect("/sign-in/")  
    return render(request, 'frontend/pages/buy_ticket.html', {'event': event, 'ticket': ticket})
   
def signIn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()
        loggedinuser = authenticate(request, username= user.username, password= password)
        if loggedinuser:
            login(request, loggedinuser)
            return redirect('/')
        else:
            return render(request,{'error':'Invalid Credentials'})
    return render(request, 'auth/login.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if User.objects.filter(username=username).exists():
            return render(request, 'auth/register.html', {'error':'User name already exist'})
        if User.objects.filter(email=email).exists():
            return render(request, 'auth/register.html', {'error':'Email already exist'})
        if password==confirm_password:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return redirect('/sign-in/')
        else:
            return render(request, 'auth/register.html', {'error':'Password didnot match'})

    return render(request, 'auth/register.html')

def bookingSuccess(request):
    return render(request,'frontend/pages/bookingSuccess.html')