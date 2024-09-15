from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import ThesisMemberProfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


@login_required(login_url='/login')
def home(request):
    current_user_id = request.user.id

    thesis_profiles = ThesisMemberProfile.objects.exclude(user_id=current_user_id)

    user_profile_exists = ThesisMemberProfile.objects.filter(user_id=current_user_id).exists()

    return render(request, 'thesis_finder/thesis_finder.html', {
        'thesis': thesis_profiles,
        'user': user_profile_exists
    })


@login_required(login_url='/login')
def thesis_finder_profile_view(request):
    user_id = request.user.id
    user_info = ThesisMemberProfile.objects.get(user_id=user_id)

    if request.method == 'POST':
        if 'delete_profile' in request.POST:
            user_info.delete()
            return redirect('thesis_finder')

        user_info.name = request.POST.get('name')
        user_info.department = request.POST.get('department')
        user_info.university_id = request.POST.get('university_id')
        user_info.skills = request.POST.get('skills')
        user_info.research_interests = request.POST.get('research_interests')
        user_info.thesis_supervisor = request.POST.get('thesis_supervisor')
        user_info.availability = request.POST.get('availability') == 'True'
        user_info.contact_info = request.POST.get('contact_info')
        user_info.thesis_topic = request.POST.get('thesis_topic')

        if 'profile_picture' in request.FILES:
            user_info.profile_picture = request.FILES['profile_picture']

        user_info.save()

        return redirect('thesis_finder_profile')

    return render(request, 'thesis_finder/thesis_finder_profile.html', {'user': user_info})


@login_required(login_url='/login')
def thesis_member_single_view(request, id):
    thesis_profile = get_object_or_404(ThesisMemberProfile, id=id)
    return render(request, 'thesis_finder/thesis_finder_single.html', {'thesis': thesis_profile})


@login_required(login_url='/login')
def thesis_member_create_profile_view(request):
    if request.method == 'POST':
        user = request.user
        department = request.POST.get('department')
        university_id = request.POST.get('university_id')
        skills = request.POST.get('skills')
        research_interests = request.POST.get('research_interests')
        thesis_supervisor = request.POST.get('thesis_supervisor', None)
        availability = request.POST.get('availability', False) == 'on'
        contact_info = request.POST.get('contact_info', None)
        thesis_topic = request.POST.get('thesis_topic', None)
        profile_picture = request.FILES.get('profile_picture', None)
        email = request.POST.get('email')
        name = request.POST.get('name')

        if not department or not university_id or not skills or not research_interests:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'thesis_finder/thesis_finder_create_profile.html')

        if ThesisMemberProfile.objects.filter(university_id=university_id).exists():
            messages.error(request, "A profile with this university ID already exists.")
            return render(request, 'thesis_finder/thesis_finder_create_profile.html')

        profile = ThesisMemberProfile(
            user=user,
            name=name,
            email=email,
            department=department,
            university_id=university_id,
            skills=skills,
            research_interests=research_interests,
            thesis_supervisor=thesis_supervisor,
            availability=availability,
            contact_info=contact_info,
            thesis_topic=thesis_topic,
            profile_picture=profile_picture
        )

        profile.save()
        messages.success(request, "Profile created successfully!")
        return redirect('thesis_finder')
    user = User.objects.get(id=request.user.id)
    return render(request, 'thesis_finder/thesis_finder_create_profile.html', {'email': user.email})
