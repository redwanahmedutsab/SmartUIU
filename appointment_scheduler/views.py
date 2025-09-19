from django.shortcuts import render, get_object_or_404, redirect
from .models import FacultyProfile, FacultyAvailability, Appointment
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.db.models import Q


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

    # Get search query params
    query_name = request.GET.get('name', '').strip()
    query_designation = request.GET.get('designation', '').strip()
    query_department = request.GET.get('department', '').strip()

    # Start with all faculties
    faculties = FacultyProfile.objects.all()

    # Apply filters if any
    if query_name:
        faculties = faculties.filter(
            Q(first_name__icontains=query_name) | Q(last_name__icontains=query_name)
        )
    if query_designation:
        faculties = faculties.filter(designation__icontains=query_designation)
    if query_department:
        faculties = faculties.filter(department__icontains=query_department)

    return render(
        request,
        'appointment_scheduler/appointment_scheduler.html',
        {
            "role": role,
            "faculties": faculties,
            "query_name": query_name,
            "query_designation": query_designation,
            "query_department": query_department,
        }
    )


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
