from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404
from datetime import datetime, date, time, timedelta
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

def inf(request):
    return render(request, 'inf.html')

def hall_detail(request, pk):
    try:
        hall = Hall.objects.get(pk=pk)
    except Hall.DoesNotExist:
        raise Http404("Зал не знайдений")
    
    places = Place.objects.filter(hall=hall)
    days = list(range(1, 32))
    years = [2025, 2026, 2027]
    
    place = places.first() if places.exists() else None
    
    return render(request, 'hall_detail.html', {
        'hall': hall,
        'places': places,
        'place': place,
        'days': days,
        'years': years
    })

def create_bookingg(request, place_id):
    try:
        place = Place.objects.get(id=place_id)
    except Place.DoesNotExist:
        raise Http404("Місце не знайдено")
    
    if request.method == "POST":
        try:
            day = request.POST.get("day")
            month = request.POST.get("month")
            year = request.POST.get("year")
            start_time = request.POST.get("start_time")
            end_time = request.POST.get("end_time")
            
            if not all([day, month, year, start_time, end_time]):
                messages.error(request, "Будь ласка, заповніть усі поля.")
                return redirect('place_detail', place_id=place.id)
            
            booking_date = date(int(year), int(month), int(day))
            
            conflict = Booking.objects.filter(
                place=place,
                date=booking_date
            ).filter(
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exists()

            if conflict:
                messages.error(request, "Цей стіл вже заброньований на вибраний час.")
            else:
                Booking.objects.create(
                    place=place,
                    user=request.user if request.user.is_authenticated else None,
                    date=booking_date,
                    start_time=start_time,
                    end_time=end_time,
                )
                messages.success(request, "Бронювання успішно створене!")
                return redirect("place_detail", place_id=place.id)
                
        except Exception as e:
            messages.error(request, f"Помилка: {str(e)}")
    
    return redirect('place_detail', place_id=place.id)

def booking_view(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    bookings = Booking.objects.filter(place=place).order_by("start_time")
    
    all_hours = [(h, h+1) for h in range(12, 24)]
    booked_hours = [(b.start_time.hour, b.end_time.hour) for b in bookings]
    free_slots = [
        f"{start}:00-{end}:00" for start, end in all_hours 
        if (start, end) not in booked_hours
    ]
    
    return render(request, "booking.html", {
        "place": place,
        "bookings": bookings,
        "free_slots": free_slots,
    })

def place_detail(request, place_id):
    """Детальная страница конкретного стола"""
    place = get_object_or_404(Place, id=place_id)
    days = list(range(1, 32))
    current_year = datetime.now().year
    years = [current_year, current_year + 1, current_year + 2]
    
    bookings = Booking.objects.filter(place=place).order_by('date', 'start_time')
    
    today = date.today()
    opening_time = time(12, 0)
    closing_time = time(23, 0)
    
    time_slots = []
    current_time = datetime.combine(datetime.today(), opening_time)
    close_time = datetime.combine(datetime.today(), closing_time)
    
    while current_time < close_time:
        slot_end = current_time + timedelta(hours=1)
        time_slots.append({
            'start': current_time.time(),
            'end': slot_end.time(),
            'booked': False
        })
        current_time = slot_end
    
    today_bookings = bookings.filter(date=today)
    
    for booking in today_bookings:
        for slot in time_slots:
            if (slot['start'] < booking.end_time and slot['end'] > booking.start_time):
                slot['booked'] = True
    
    return render(request, 'hall_detail.html', {
        'place': place,
        'days': days,
        'years': years,
        'bookings': bookings,
        'time_slots': time_slots,
        'today': today
    })
