from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ClassRoutine, Course, Note, Task, Reminder
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@login_required
def home(request):
    notes = Note.objects.filter(user=request.user)
    tasks = Task.objects.filter(user=request.user)
    routines = ClassRoutine.objects.filter(user=request.user)
    reminders = Reminder.objects.filter(user=request.user)
    courses = Course.objects.all()  # For modal select

    context = {
        'notes': notes,
        'tasks': tasks,
        'routines': routines,
        'courses': courses,
        'reminders': reminders,
    }
    return render(request, 'digital_desk/digital_desk_home.html', context)


@login_required
def add_class_routine(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        faculty_name = request.POST.get('faculty_name')  # get from form
        day = request.POST.get('day_of_week')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        location = request.POST.get('location', '')

        # Create or update course dynamically
        ClassRoutine.objects.create(
            user=request.user,
            course_name=course_name,
            faculty_name=faculty_name,
            day_of_week=day,
            start_time=start_time,
            end_time=end_time,
            location=location
        )
    return redirect('digital_desk_home')


@login_required
def add_note(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        tags = request.POST.get('tags', '')

        Note.objects.create(
            user=request.user,
            title=title,
            content=content,
            tags=tags
        )
    return redirect('digital_desk_home')


@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')

        Task.objects.create(
            user=request.user,
            title=title,
            due_date=due_date
        )
    return redirect('digital_desk_home')


@login_required
def toggle_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('digital_desk_home')


@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'digital_desk/note_detail.html', {'note': note})


@login_required
def add_reminder(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        reminder_date_str = request.POST.get('reminder_date')
        notify_days_before = int(request.POST.get('notify_days_before', 1))

        # Parse datetime from input
        reminder_date = datetime.strptime(reminder_date_str, '%Y-%m-%dT%H:%M')

        Reminder.objects.create(
            user=request.user,
            title=title,
            description=description,
            reminder_date=reminder_date,
            notify_days_before=notify_days_before
        )
        return redirect('digital_desk_home')  # consistent with URL name

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def delete_reminder(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id, user=request.user)
    reminder.delete()
    return redirect('digital_desk_home')


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    return redirect('digital_desk_home')


@login_required
@csrf_exempt
def edit_note(request, pk):
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=pk, user=request.user)
        data = json.loads(request.body)
        note.title = data.get('title', note.title)
        note.tags = data.get('tags', note.tags)
        note.content = data.get('content', note.content)
        note.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def delete_routine(request, pk):
    routine = get_object_or_404(ClassRoutine, pk=pk, user=request.user)
    routine.delete()
    return redirect('digital_desk_home')
