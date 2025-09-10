from django.shortcuts import render, redirect
from .models import *
from .forms import BookingForm
from django.contrib import messages



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


def inf(request):
    return render(request, 'inf.html')


def hall_detail(request, pk):
    try:
        hall = Hall.objects.get(pk=pk)
    except Hall.DoesNotExist:
        raise ("Зал не знайдений")
    places = Place.objects.filter(hall=hall)
    return render(request, 'hall_detail.html', {'hall': hall, 'places': places})

def create_bookingg(request, place_id):
    try:
        place = Place.objects.get(id=place_id)
    except Place.DoesNotExist:
        raise ("Місце не знайдено")
    if request.method == "POST":
        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        # Перевірка, чи всі поля передані
        if not date or not start_time or not end_time:
            messages.error(request, "Будь ласка, заповніть усі поля.")
            #return redirect("create_booking", place_id=place.id)

        # Перевірка на конфлікт
        conflict = Booking.objects.filter(
            place=place,
            date=date,
            start_time__lt=end_time,  # існуюче починається раніше нового кінця
            end_time__gt=start_time   # існуюче закінчується пізніше нового початку
        ).exists()

        if conflict:
            messages.error(request, "Цей стіл вже заброньований на вибраний час.")
            #ТАЙМЕР
            #return redirect("hall_detail", pk=place.hall.id)
        if not conflict:
        # Створюємо бронювання
            Booking.objects.create(
                place=place,
                user=request.user,
                date=date,
                start_time=start_time,
                end_time=end_time,
            )

            messages.success(request, "Бронювання успішно створене!")
            return redirect("hall_detail", pk=place.hall.id)

        # Якщо GET — показуємо форму
    return render(request, "booking_form2.html", {"place": place})