from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from .forms import CVProfileForm, EducationForm, ExperienceForm, SkillForm, LanguageForm, AwardForm
from .models import Job


@login_required(login_url='/login')
def home(request):
    jobs = Job.objects.all()

    # Filter by job name (can be combined with other filters)
    job_name = request.GET.get('job_name')
    if job_name:
        jobs = jobs.filter(title__icontains=job_name)

    # Filter by category (can be combined with other filters)
    category = request.GET.get('category')
    if category:
        jobs = jobs.filter(category__id=category)

    # Filter by job type (can be combined with other filters)
    job_type = request.GET.get('job_type')
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    # Filter by experience level (can be combined with other filters)
    experience = request.GET.get('experience')
    if experience:
        jobs = jobs.filter(experience_level=experience)

    # Filter by work environment (can be combined with other filters)
    work_env = request.GET.get('work_env')
    if work_env:
        jobs = jobs.filter(work_env=work_env)

    # Filter by industry (can be combined with other filters)
    industry = request.GET.get('industry')
    if industry:
        jobs = jobs.filter(industry__id=industry)

    # Sorting
    sort = request.GET.get('sort')
    if sort == 'newest':
        jobs = jobs.order_by('-created_at')
    elif sort == 'oldest':
        jobs = jobs.order_by('created_at')
    elif sort == 'salary_min_to_max':
        jobs = jobs.order_by('salary')
    elif sort == 'salary_max_to_min':
        jobs = jobs.order_by('-salary')

    return render(request, 'internship_jobs/internship_jobs.html', {'jobs': jobs})


@login_required(login_url='/login')
def internship_job_post_view(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        company_name = request.POST.get('company_name')
        job_description = request.POST.get('job_description')
        job_type = request.POST.get('job_type')
        job_location = request.POST.get('job_location')
        salary = request.POST.get('salary')
        deadline = request.POST.get('deadline')
        experience_level = request.POST.get('experience_level')
        work_environment = request.POST.get('work_environment')
        industry = request.POST.get('industry')

        # Handling the uploaded company logo
        if 'company_logo' in request.FILES:
            company_logo = request.FILES['company_logo']
            fs = FileSystemStorage()
            company_logo_name = fs.save(company_logo.name, company_logo)
        else:
            company_logo_name = None  # Optional if no logo provided

        # Save the data to Job model
        job_post = Job.objects.create(
            title=job_title,
            company=company_name,
            description=job_description,
            post_type=job_type,
            location=job_location,
            salary=salary,
            logo=company_logo_name,
            posted_by=request.user,
            deadline=deadline,
            experience_level=experience_level,
            work_environment=work_environment,
            industry=industry
        )

        messages.success(request, 'Job posted successfully!')
        return redirect('internship_and_job')

    return render(request, 'internship_jobs/internship_jobs_post.html')


def job_detail_view(request):
    return None


def internship_job_create_cv_view(request):
    if request.method == 'POST':
        cv_profile_form = CVProfileForm(request.POST, request.FILES)
        if cv_profile_form.is_valid():
            cv_profile = cv_profile_form.save(commit=False)
            cv_profile.user = request.user  # Assuming the user is logged in
            cv_profile.save()

            # Handle multiple education entries
            for i in range(int(request.POST.get('education_count', 0))):
                education_form = EducationForm(request.POST, prefix=f'education_{i}')
                if education_form.is_valid():
                    education = education_form.save(commit=False)
                    education.cv_profile = cv_profile
                    education.save()

            # Handle multiple experience entries
            for i in range(int(request.POST.get('experience_count', 0))):
                experience_form = ExperienceForm(request.POST, prefix=f'experience_{i}')
                if experience_form.is_valid():
                    experience = experience_form.save(commit=False)
                    experience.cv_profile = cv_profile
                    experience.save()

            # Handle multiple skills
            for i in range(int(request.POST.get('skills_count', 0))):
                skill_form = SkillForm(request.POST, prefix=f'skill_{i}')
                if skill_form.is_valid():
                    skill = skill_form.save(commit=False)
                    skill.cv_profile = cv_profile
                    skill.save()

            # Handle multiple languages
            for i in range(int(request.POST.get('languages_count', 0))):
                language_form = LanguageForm(request.POST, prefix=f'language_{i}')
                if language_form.is_valid():
                    language = language_form.save(commit=False)
                    language.cv_profile = cv_profile
                    language.save()

            # Handle multiple awards
            for i in range(int(request.POST.get('awards_count', 0))):
                award_form = AwardForm(request.POST, prefix=f'award_{i}')
                if award_form.is_valid():
                    award = award_form.save(commit=False)
                    award.cv_profile = cv_profile
                    award.save()

            return redirect('success_url')  # Redirect to a success page or the profile page

    else:
        cv_profile_form = CVProfileForm()

    return render(request, 'internship_jobs/internship_jobs_create_cv.html', {
        'cv_profile_form': cv_profile_form,
        # Add context for other forms if necessary
    })
