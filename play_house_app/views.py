from django.shortcuts import render, redirect
from .models import *
from .forms import BookingForm



# Create your views here.
def hall_list(request):
    halls = Hall.objects.all()
    return render(request, 'hall_list.html', {'halls': halls})


def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('hall_list')
    else:
        form = BookingForm()
    return render(request, 'booking_form.html', {'form': form})