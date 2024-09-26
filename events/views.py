from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
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

    registration = EventRegistration.objects.filter(user=request.user, event=event).first()
    return render(request, 'events/events_single.html', {
        'event': event,
        'registration': registration  # This will be None if not registered
    })


@login_required(login_url='/login')
def event_posted_event_view(request):
    # Get parameters from the request
    club = request.GET.get('club')
    sort = request.GET.get('sort')

    # Start with all events created by the logged-in user
    events = Event.objects.filter(created_by=request.user)

    # Filter by club if specified
    if club:
        events = events.filter(club=club)

    # Sort events based on the specified criteria
    if sort:
        if sort == 'new_to_old':
            events = events.order_by('-date')
        elif sort == 'old_to_new':
            events = events.order_by('date')
        elif sort == 'upcoming':
            events = events.filter(date__gte=timezone.now()).order_by('date')

    # Get the list of clubs for the template
    clubs = Event.CLUB_CHOICES

    # Render the template with the filtered events and clubs
    return render(request, 'events/event_posted_events.html', {'events': events, 'clubs': clubs})


@login_required(login_url='/login')
def event_registration_view(request, id):
    registration = EventRegistration.objects.filter(event=id, user=request.user).first()

    print(registration)  # Debugging line to check the registration status

    if registration:
        # User is already registered; proceed to unregister
        registration.delete()
        messages.success(request, "You have successfully unregistered from the event.")
    else:
        # User is not registered; proceed to register
        event_registration = EventRegistration(
            event_id=id,  # Set the event using the event ID
            user=request.user,  # Directly assign the User instance
            registered_at=timezone.now()  # Set the registered_at field to the current time
        )
        event_registration.save()  # Save the registration to the database
        messages.success(request, "You have successfully registered for the event.")

    # Redirect back to the event detail view
    return redirect('event_single', id=id)  # Redirecting to the event_single view


def send_invitation_email(email, event):
    pass


@login_required(login_url='/login')
def event_send_email_view(request, id):
    event = Event.objects.get(id=id)
    registrations = EventRegistration.objects.filter(event=event)

    print(id)

    if request.method == 'POST':
        # Logic to send invitations to all registered users
        for registration in registrations:
            print(id)
            # send_invitation_email(registration.user.email, event)  # Replace with your email sending logic

    return render(request, 'events/event_send_email.html', {'event': event, 'registrations': registrations})
