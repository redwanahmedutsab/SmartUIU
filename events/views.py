from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.utils.html import strip_tags
from .models import Event, EventRegistration
from django.contrib import messages


@login_required(login_url='/login')
def home(request):
    club = request.GET.get('club')
    sort = request.GET.get('sort')

    events = Event.objects.all()

    if club and sort:
        events = events.filter(club=club)
        if sort == 'new_to_old':
            events = events.order_by('-date')
        elif sort == 'old_to_new':
            events = events.order_by('date')
        elif sort == 'upcoming':
            events = events.filter(date__gte=timezone.now()).order_by('date')

    elif club:
        events = events.filter(club=club)

    elif sort:
        if sort == 'new_to_old':
            events = events.order_by('-date')
        elif sort == 'old_to_new':
            events = events.order_by('date')
        elif sort == 'upcoming':
            events = events.filter(date__gte=timezone.now()).order_by('date')

    else:
        clubs = Event.CLUB_CHOICES
        return render(request, 'events/events.html', {'events': events, 'clubs': clubs})

    clubs = Event.CLUB_CHOICES

    return render(request, 'events/events.html', {'events': events, 'clubs': clubs})


@login_required(login_url='/login')
def event_post_event_view(request):
    if request.method == 'POST':
        title = request.POST.get('event_title')
        description = request.POST.get('event_description')
        date = request.POST.get('event_date')
        time = request.POST.get('event_time')
        location = request.POST.get('event_location')
        club = request.POST.get('club')
        banner = request.FILES.get('event_banner')

        event = Event(
            title=title,
            description=description,
            date=date,
            time=time,
            location=location,
            club=club,
            banner=banner,
            created_by_id=request.user.id
        )
        event.save()

        messages.success(request, 'Event created successfully!')
        return redirect('event')

    return render(request, 'events/event_post_event.html')


@login_required(login_url='/login')
def event_single_view(request, id):
    event = get_object_or_404(Event, id=id)
    current_time = timezone.now()
    registration = EventRegistration.objects.filter(user=request.user, event=event).first()
    current_date = current_time.date()  # Get the current date

    if current_date < event.date:
        available = 1
    else:
        available = 0
    return render(request, 'events/events_single.html', {
        'event': event,
        'registration': registration,
        'available': available,
    })


@login_required(login_url='/login')
def event_posted_event_view(request):
    club = request.GET.get('club')
    sort = request.GET.get('sort')

    events = Event.objects.filter(created_by=request.user)

    if club:
        events = events.filter(club=club)

    if sort:
        if sort == 'new_to_old':
            events = events.order_by('-date')
        elif sort == 'old_to_new':
            events = events.order_by('date')
        elif sort == 'upcoming':
            events = events.filter(date__gte=timezone.now()).order_by('date')

    clubs = Event.CLUB_CHOICES

    return render(request, 'events/event_posted_events.html', {'events': events, 'clubs': clubs})


@login_required(login_url='/login')
def event_registration_view(request, id):
    registration = EventRegistration.objects.filter(event=id, user=request.user).first()

    print(registration)

    if registration:
        registration.delete()
        messages.success(request, "You have successfully unregistered from the event.")
    else:
        event_registration = EventRegistration(
            event_id=id,
            user=request.user,
            registered_at=timezone.now()
        )
        event_registration.save()
        messages.success(request, "You have successfully registered for the event.")

    return redirect('event_single', id=id)


def send_invitation_email(recipient_email, event):
    subject = f"Invitation to {event.title}"

    html_message = render_to_string('emails/invitation_email.html', {'event': event})
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        'your_email@example.com',  # Replace with your email
        [recipient_email],
        html_message=html_message,
        fail_silently=False,
    )


@login_required(login_url='/login')
def event_send_email_view(request, id):
    event = get_object_or_404(Event, id=id)
    registrations = EventRegistration.objects.filter(event=event)

    if request.method == 'POST':
        if 'send_all' in request.POST:
            for registration in registrations:
                send_invitation_email(registration.user.email, event)
            messages.success(request, 'Invitation emails sent successfully to all registered users!')
        else:
            user_id = request.POST.get('user_id')
            registration = registrations.get(user__id=user_id)
            print(registration.user.email)
            send_invitation_email(registration.user.email, event)
            messages.success(request, 'Invitation emails sent successfully to the registered users!')

    return render(request, 'events/event_send_email.html', {'event': event, 'registrations': registrations})


@login_required(login_url='/login')
def event_registered_view(request):
    user = request.user

    registrations = EventRegistration.objects.filter(user=user)

    event_ids = [registration.event_id for registration in registrations]

    events = Event.objects.filter(id__in=event_ids)

    context = {
        'registrations': registrations,
        'events': events,
    }

    return render(request, 'events/event_registered.html', context)


@login_required(login_url='/login')
def event_edit_view(request, id):
    event = get_object_or_404(Event, id=id)

    if request.method == 'POST':
        event.title = request.POST.get('event_title')
        event.description = request.POST.get('event_description')
        event.date = request.POST.get('event_date')
        event.time = request.POST.get('event_time')
        event.location = request.POST.get('event_location')
        event.club = request.POST.get('club')

        if request.FILES.get('event_banner'):
            event.banner = request.FILES['event_banner']

        event.save()
        messages.success(request, 'Event updated successfully!')
        return redirect('event_edit', id=event.id)

    return render(request, 'events/event_edit.html', {'event': event})


@login_required(login_url='/login')
def event_delete_view(request, id):
    # Get the event object by ID or show 404 if not found
    event = get_object_or_404(Event, id=id)

    if request.method == 'POST':  # Handle POST request to delete the event
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('event_posted_event')  # Redirect to the list of events after deletion

    # Render a confirmation page for deleting the event
    return render(request, 'events/event_edit.html', {'event': event})
