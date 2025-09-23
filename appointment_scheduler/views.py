from django.shortcuts import render, get_object_or_404, redirect
from .models import FacultyProfile, FacultyAvailability, Appointment
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render
from django.db.models import Q
from django.contrib import messages
from datetime import datetime, timedelta
from django.http import JsonResponse


def home(request):
    email = request.user.email.lower() if request.user.is_authenticated else ""

    student_domains = [
        "@bscse.uiu.ac.bd", "@bseds.uiu.ac.bd", "@bsmsj.uiu.ac.bd",
        "@bsce.uiu.ac.bd", "@bseee.uiu.ac.bd", "@bsbba.uiu.ac.bd"
    ]
    faculty_domains = [
        "@cse.uiu.ac.bd", "@eds.uiu.ac.bd", "@msj.uiu.ac.bd",
        "@ce.uiu.ac.bd", "@eee.uiu.ac.bd", "@bba.uiu.ac.bd"
    ]

    if any(domain in email for domain in student_domains):
        role = "student"
    elif any(domain in email for domain in faculty_domains):
        role = "faculty"
    elif email.endswith("@uiu.ac.bd"):
        role = "admin"
    else:
        role = "unknown"

    # Search filters (only needed for students browsing faculties)
    query_name = request.GET.get('name', '').strip()
    query_designation = request.GET.get('designation', '').strip()
    query_department = request.GET.get('department', '').strip()

    faculties = FacultyProfile.objects.all()

    if query_name:
        faculties = faculties.filter(
            Q(first_name__icontains=query_name) | Q(last_name__icontains=query_name)
        )
    if query_designation:
        faculties = faculties.filter(designation__icontains=query_designation)
    if query_department:
        faculties = faculties.filter(department__icontains=query_department)

    # Decide which template
    if role == "student":
        template = "appointment_scheduler/appointment_student_home.html"
        context = {
            "faculties": faculties,
            "query_name": query_name,
            "query_designation": query_designation,
            "query_department": query_department,
        }
    else:
        template = "appointment_scheduler/appointment_faculty_home.html"
        context = {}

    print(role)

    return render(request, template, context)


@login_required
def book_appointment_student(request, faculty_id):
    faculty = get_object_or_404(FacultyProfile, id=faculty_id)
    availabilities = faculty.availabilities.all()
    message = ""

    if request.method == "POST":
        availability_id = request.POST.get("availability_id")
        availability = get_object_or_404(FacultyAvailability, id=availability_id)

        from datetime import datetime, timedelta
        start_time = datetime.combine(datetime.today(), availability.start_time)
        end_time = start_time + timedelta(minutes=availability.duration_minutes)
        end_time = end_time.time()

        if Appointment.objects.filter(availability=availability, start_time=availability.start_time,
                                      is_cancelled=False).exists():
            message = "This slot is already booked. Please select another."
        else:
            appointment = Appointment.objects.create(
                availability=availability,
                student=request.user,
                start_time=availability.start_time,
                end_time=end_time
            )

            # Send Email to Student
            subject_student = f"Appointment Confirmed with {faculty.first_name} {faculty.last_name}"
            html_message_student = render_to_string(
                'appointment_scheduler/email_student.html',
                {'appointment': appointment, 'faculty': faculty}
            )
            plain_message_student = strip_tags(html_message_student)
            send_mail(subject_student, plain_message_student, None,
                      [request.user.email], html_message=html_message_student)

            # Send Email to Faculty
            subject_faculty = f"New Appointment Booked by {request.user.get_full_name()}"
            html_message_faculty = render_to_string(
                'appointment_scheduler/email_faculty.html',
                {'appointment': appointment, 'student': request.user}
            )
            plain_message_faculty = strip_tags(html_message_faculty)
            send_mail(subject_faculty, plain_message_faculty, None,
                      [faculty.user.email], html_message=html_message_faculty)

            # Instead of redirect, show success message on the same page
            message = "Appointment booked successfully!"

    return render(request, 'appointment_scheduler/appointment_booking_student.html', {
        'faculty': faculty,
        'availabilities': availabilities,
        'message': message
    })


@login_required
def student_bookings(request):
    bookings = Appointment.objects.filter(student=request.user, is_cancelled=False).order_by('start_time')
    return render(request, 'appointment_scheduler/appointment_remove_student.html', {'bookings': bookings})


@login_required
def remove_booking(request, booking_id):
    booking = get_object_or_404(Appointment, id=booking_id, student=request.user)

    if request.method == 'POST':
        # Mark appointment as cancelled (optional: you can delete it too)
        booking.is_cancelled = True
        booking.save()

        # Send email to student
        subject_student = f"Appointment Cancelled with {booking.availability.faculty.first_name} {booking.availability.faculty.last_name}"
        html_message_student = render_to_string(
            'appointment_scheduler/email_appointment_cancelled_student.html',
            {'appointment': booking}
        )
        plain_message_student = strip_tags(html_message_student)
        send_mail(subject_student, plain_message_student, None,
                  [booking.student.email], html_message=html_message_student)

        # Send email to faculty
        subject_faculty = f"Appointment Cancelled by {booking.student.get_full_name()}"
        html_message_faculty = render_to_string(
            'appointment_scheduler/email_appointment_cancelled_faculty.html',
            {'appointment': booking}
        )
        plain_message_faculty = strip_tags(html_message_faculty)
        send_mail(subject_faculty, plain_message_faculty, None,
                  [booking.availability.faculty.user.email], html_message=html_message_faculty)

        # Redirect back to bookings page
        return redirect('student_bookings')


@login_required
def faculty_set_schedule(request):
    # Get faculty profile safely
    try:
        faculty = request.user.faculty_profile
    except FacultyProfile.DoesNotExist:
        messages.error(request, "You do not have a faculty profile. Contact admin.")
        data = {
            "status": "failed",
            "message": "You have no faculty profile. Create a faculty profile first.",
        }
        return render(request, 'appointment_scheduler/appointment_faculty_home.html', data)

    # Generate years for dropdown (2025 to 2035)
    years = list(range(2025, 2036))

    if request.method == 'POST':
        # Get selected days
        days = request.POST.getlist('day[]')
        interval_str = request.POST.get('interval')

        # Validate interval
        try:
            interval = int(interval_str)
        except (ValueError, TypeError):
            messages.error(request, "Interval must be a number.")
            return redirect('faculty_set_schedule')

        slots_created = 0

        # Loop through each day index
        for idx, day in enumerate(days):
            start_times = request.POST.getlist(f'start_time[{idx}][]')
            end_times = request.POST.getlist(f'end_time[{idx}][]')

            for i in range(len(start_times)):
                st = start_times[i]
                et = end_times[i]

                # Parse time from flatpickr (h:i K → 12h with AM/PM)
                try:
                    start_dt = datetime.strptime(st, "%I:%M %p")
                    end_dt = datetime.strptime(et, "%I:%M %p")
                except ValueError:
                    messages.warning(
                        request,
                        f"Invalid time format for slot {i + 1} on {day}. Skipping."
                    )
                    continue

                current_time = start_dt

                # Create slots with the given interval
                while current_time + timedelta(minutes=interval) <= end_dt:
                    slot_start = current_time.time()
                    slot_end = (current_time + timedelta(minutes=interval)).time()

                    # Avoid overlapping slots
                    if not FacultyAvailability.objects.filter(
                            faculty=faculty,
                            day_of_week=day,
                            start_time=slot_start,
                            end_time=slot_end
                    ).exists():
                        FacultyAvailability.objects.create(
                            faculty=faculty,
                            day_of_week=day,
                            start_time=slot_start,
                            end_time=slot_end,
                            duration_minutes=interval
                        )
                        slots_created += 1

                    current_time += timedelta(minutes=interval)

        messages.success(request, f"{slots_created} slots created successfully!")
        return redirect('faculty_manage_schedule')

    return render(
        request,
        'appointment_scheduler/appointment_faculty_make_schedule.html',
        {
            'faculty': faculty,
            'years': years  # ✅ pass years for dropdown
        }
    )


@login_required
def faculty_manage_schedule(request):
    # Handle missing faculty profile safely
    try:
        faculty = request.user.faculty_profile
    except FacultyProfile.DoesNotExist:
        messages.error(request, "You do not have a faculty profile. Contact admin.")
        return redirect('homepage')

    availabilities = faculty.availabilities.all().order_by('day_of_week', 'start_time')
    return render(request, 'appointment_scheduler/appointment_faculty_make_schedule.html', {
        'availabilities': availabilities,
    })


@login_required
def faculty_create_profile(request):
    # Try to get existing profile or None
    faculty, created = FacultyProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # Update fields from form
        faculty.first_name = request.POST.get('first_name', request.user.first_name)
        faculty.last_name = request.POST.get('last_name', request.user.last_name)
        faculty.designation = request.POST.get('designation', faculty.designation)
        # Optional: department (if you have a field in form)
        faculty.department = request.POST.get('department', faculty.department)

        # Handle image upload
        if request.FILES.get('image'):
            faculty.image = request.FILES['image']

        faculty.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('faculty_profile_create')  # reload the same page

    context = {
        'faculty': faculty
    }
    return render(request, 'appointment_scheduler/appointment_faculty_profile.html', context)


def faculty_routine(request):
    try:
        faculty = request.user.faculty_profile
        availabilities = FacultyAvailability.objects.filter(faculty=faculty)
    except FacultyProfile.DoesNotExist:
        return JsonResponse({
            "status": "failed",
            "message": "You have no faculty profile.",
            "weekdays": []
        })

    weekdays = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    schedule_by_day = {}
    for avail in availabilities:
        # Check if this availability slot is booked
        booked = Appointment.objects.filter(availability_id=avail.id, is_cancelled=False).exists()

        # Store as dict with booked info
        schedule_by_day.setdefault(avail.day_of_week, []).append({
            "time": f"{avail.start_time} - {avail.end_time}",
            "booked": booked
        })

    return JsonResponse({
        "status": "success",
        "weekdays": weekdays,
        "schedule_by_day": schedule_by_day
    })
