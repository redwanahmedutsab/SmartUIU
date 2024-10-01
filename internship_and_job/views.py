import json
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, CVProfile, Education, Experience, Skill, Language, Award
from .models import JobApplication


@login_required(login_url='/login')
def home(request):
    jobs = Job.objects.all()

    job_name = request.GET.get('job_name')
    if job_name:
        jobs = jobs.filter(title__icontains=job_name)

    category = request.GET.get('category')
    if category:
        jobs = jobs.filter(category__id=category)

    job_type = request.GET.get('job_type')
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    experience = request.GET.get('experience')
    if experience:
        jobs = jobs.filter(experience_level=experience)

    work_env = request.GET.get('work_env')
    if work_env:
        jobs = jobs.filter(work_env=work_env)

    industry = request.GET.get('industry')
    if industry:
        jobs = jobs.filter(industry__id=industry)

    sort = request.GET.get('sort')
    if sort == 'newest':
        jobs = jobs.order_by('-created_at')
    elif sort == 'oldest':
        jobs = jobs.order_by('created_at')
    elif sort == 'salary_min_to_max':
        jobs = jobs.order_by('salary')
    elif sort == 'salary_max_to_min':
        jobs = jobs.order_by('-salary')

    cv = CVProfile.objects.filter(user_id=request.user.id).first()
    print(cv)
    return render(request, 'internship_jobs/internship_jobs.html', {'jobs': jobs, 'cv': cv})


@login_required(login_url='/login')
def internship_job_post_view(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        company_name = request.POST.get('company_name')
        job_description = request.POST.get('job_description')
        responsibilities = request.POST.get('responsibilities')
        education_requirements = request.POST.get('education_requirements')
        previous_experience = request.POST.get('previous_experience')
        skills_needed = request.POST.get('skills_needed')
        other_requirements = request.POST.get('other_requirements')
        job_type = request.POST.get('job_type')
        gender = request.POST.get('gender')
        job_location = request.POST.get('job_location')
        salary = request.POST.get('salary')
        deadline = request.POST.get('deadline')
        experience_level = request.POST.get('experience_level')
        work_environment = request.POST.get('work_environment')
        industry = request.POST.get('industry')

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
            responsibilities=responsibilities,
            education_requirements=education_requirements,
            previous_experience=previous_experience,
            skills_needed=skills_needed,
            other_requirements=other_requirements,
            post_type=job_type,
            gender=gender,
            location=job_location,
            salary=salary,
            logo=company_logo_name,
            posted_by=request.user,
            deadline=deadline,
            experience_level=experience_level,
            work_environment=work_environment,
            industry=industry
        )

        job_post.save()

        messages.success(request, 'Job posted successfully!')
        return redirect('internship_and_job')

    return render(request, 'internship_jobs/internship_jobs_post.html')


@login_required(login_url='/login')
def internship_job_single_view(request, id):
    job = Job.objects.get(id=id)
    cv = CVProfile.objects.filter(user_id=request.user.id).first()
    job_check = JobApplication.objects.filter(job_id=id, cv_profile=cv)

    if request.method == 'POST' and cv:
        job_application = JobApplication.objects.create(
            job=job,
            cv_profile=cv,  # Use the user's CVProfile
        )
        job_application.save()
        messages.success(request, 'Application submitted successfully!')
        return redirect('internship_and_job')
    return render(request, 'internship_jobs/internship_jobs_single.html',
                  {'job': job, 'cv': cv, 'job_check': job_check})


@login_required(login_url='/login')
def internship_job_edit_view(request, id):
    job = Job.objects.get(id=id)
    return render(request, 'internship_jobs/internship_jobs_edit.html',
                  {'job': job})


@login_required(login_url='/login')
def internship_job_create_cv_view(request):
    if request.method == 'POST':
        user = request.user

        try:
            with transaction.atomic():
                # Print user information
                print(f"Creating CV for user: {user}")

                # Get the POST data
                bio = request.POST.get('bio')
                contact_email = request.POST.get('contact_email')
                contact_address = request.POST.get('contact_address')
                contact_phone = request.POST.get('contact_phone')
                profile_image = request.FILES.get('profile_image')

                # Print basic CV information
                print(
                    f"Bio: {bio}, Contact Email: {contact_email}, Contact Phone: {contact_phone}, Address: {contact_address}")
                print(f"Profile Image: {profile_image}")

                # Create CV Profile
                cv_profile = CVProfile.objects.create(
                    user=user,
                    bio=bio,
                    contact_email=contact_email,
                    contact_phone=contact_phone,
                    address=contact_address,
                    profile_image=profile_image,
                )
                print("CV Profile created successfully!")

                # Handle Education data
                education_data = json.loads(request.POST.get('education', '[]'))
                print(f"Education Data: {education_data}")
                for edu in education_data:
                    print(f"Processing education: {edu}")
                    Education.objects.create(
                        cv_profile=cv_profile,
                        degree=edu['degree'],
                        institution=edu['institution'],
                        start_year=edu['startYear'],
                        end_year=edu['endYear'],
                        cgpa=edu['cgpa'],
                    )

                # Handle Experience data
                experience_data = json.loads(request.POST.get('experience', '[]'))
                print(f"Experience Data: {experience_data}")
                for exp in experience_data:
                    print(f"Processing experience: {exp}")
                    Experience.objects.create(
                        cv_profile=cv_profile,
                        company=exp['company'],
                        position=exp['jobTitle'],
                        start_date=exp['startDate'],
                        end_date=exp['endDate'],
                    )

                # Handle Skills data
                skills_data = json.loads(request.POST.get('skills', '[]'))
                print(f"Skills Data: {skills_data}")
                for skill in skills_data:
                    print(f"Processing skill: {skill}")
                    Skill.objects.create(cv_profile=cv_profile, skill_name=skill)

                # Handle Languages data
                languages_data = json.loads(request.POST.get('languages', '[]'))
                print(f"Languages Data: {languages_data}")
                for lang in languages_data:
                    print(f"Processing language: {lang}")
                    Language.objects.create(
                        cv_profile=cv_profile,
                        language=lang['language'],
                        proficiency=lang['proficiency']
                    )

                # Handle Awards data
                awards_data = json.loads(request.POST.get('awards', '[]'))
                print(f"Awards Data: {awards_data}")
                for award in awards_data:
                    print(f"Processing award: {award}")
                    Award.objects.create(
                        cv_profile=cv_profile,
                        title=award['title'],
                        position=award['position'],
                        date_awarded=award['awardDate']
                    )

            # Success message and redirect
            messages.success(request, 'CV has been created!')
            print("CV creation successful!")
            return redirect('internship_and_job')

        except Exception as e:
            # Print error and rollback transaction
            print(f"Error occurred: {str(e)}")
            messages.error(request, f"Error while creating CV: {str(e)}")
            transaction.rollback()

    # Render the create CV template
    return render(request, 'internship_jobs/internship_jobs_create_cv.html')


@login_required(login_url='/login')
def internship_job_posted_jobs_view(request):
    jobs = Job.objects.filter(posted_by_id=request.user.id)
    print(jobs)
    return render(request, 'internship_jobs/internship_jobs_posted_jobs.html', {'jobs': jobs})


@login_required(login_url='/login')
def internship_job_edit_cv_view(request):
    cv_profile = get_object_or_404(CVProfile, user=request.user)

    if request.method == 'POST':
        # Update basic CVProfile fields
        cv_profile.bio = request.POST.get('bio')
        cv_profile.contact_phone = request.POST.get('contact_phone')
        cv_profile.contact_email = request.POST.get('contact_email')
        cv_profile.address = request.POST.get('address')

        cv_profile.save()

        # Update experiences
        for experience in cv_profile.experiences.all():
            position = request.POST.get(f'experience_position_{experience.id}')
            company = request.POST.get(f'experience_company_{experience.id}')
            description = request.POST.get(f'experience_description_{experience.id}')

            if position and company:
                experience.position = position
                experience.company = company
                experience.description = description
                experience.save()

        # Update education
        for education in cv_profile.educations.all():
            institution = request.POST.get(f'education_institution_{education.id}')
            degree = request.POST.get(f'education_degree_{education.id}')
            cgpa = request.POST.get(f'education_cgpa_{education.id}')
            start_year = request.POST.get(f'education_start_year_{education.id}')
            end_year = request.POST.get(f'education_end_year_{education.id}')

            if institution and degree:  # Ensure at least some fields are filled
                education.institution = institution
                education.degree = degree
                education.cgpa = cgpa

                # Parse and format start_year and end_year
                try:
                    education.start_year = datetime.strptime(start_year, "%b. %d, %Y").date()
                    education.end_year = datetime.strptime(end_year, "%b. %d, %Y").date()
                except ValueError:
                    print(f"Invalid date format for start_year: {start_year} or end_year: {end_year}")
                    messages.error(request, f"Invalid date format for years: {start_year}, {end_year}")

                education.save()

        # Update skills
        for skill in cv_profile.skills.all():
            skill_name = request.POST.get(f'skill_name_{skill.id}')
            if skill_name:  # Check if the skill name is provided
                skill.skill_name = skill_name
                skill.save()

        # Update languages
        for language in cv_profile.languages.all():
            lang_name = request.POST.get(f'language_name_{language.id}')
            proficiency = request.POST.get(f'language_proficiency_{language.id}')
            if lang_name:  # Ensure language name is provided
                language.language = lang_name
                language.proficiency = proficiency
                language.save()

        # Update awards
        for award in cv_profile.awards.all():
            title = request.POST.get(f'award_title_{award.id}')
            position = request.POST.get(f'award_position_{award.id}')
            date_awarded = request.POST.get(f'award_date_awarded_{award.id}')

            if title:  # Ensure title is provided
                award.title = title
                award.position = position

                # Parse the date if needed
                if date_awarded:
                    try:
                        award.date_awarded = datetime.strptime(date_awarded, "%b. %d, %Y").date()
                    except ValueError:
                        print(f"Invalid date format for award date: {date_awarded}")
                        messages.error(request, f"Invalid date format for award date: {date_awarded}")

                award.save()

        # Optionally, show a success message to the user
        messages.success(request, 'CV profile updated successfully!')

        # Redirect to the edit page
        return redirect('internship_job_edit_cv_id', cv_profile.id)

    # Render the form with the existing CVProfile data if not a POST request
    return render(request, 'internship_jobs/internship_jobs_edit_cv.html', {'cv_profile': cv_profile})


@login_required(login_url='/login')
def internship_job_edit_cv_id_view(request, id):
    cv_profile = get_object_or_404(CVProfile, id=id)

    if request.method == 'POST':
        # Print CVProfile related data
        bio = request.POST.get('bio')
        contact_phone = request.POST.get('contact_phone')
        contact_email = request.POST.get('contact_email')
        address = request.POST.get('address')

        print(f"Bio: {bio}")
        print(f"Contact Phone: {contact_phone}")
        print(f"Contact Email: {contact_email}")
        print(f"Address: {address}")

        # Update CVProfile fields
        cv_profile.bio = bio
        cv_profile.contact_phone = contact_phone
        cv_profile.contact_email = contact_email
        cv_profile.address = address
        cv_profile.save()

        # Handle updating experiences
        experience_ids = request.POST.getlist('experience_ids')
        print(f"Experience IDs: {experience_ids}")

        for exp_id in experience_ids:
            experience = get_object_or_404(Experience, id=exp_id)

            position = request.POST.get(f'edit-position-{exp_id}')
            company = request.POST.get(f'edit-company-{exp_id}')
            start_date = request.POST.get(f'edit-start-date-{exp_id}')
            end_date = request.POST.get(f'edit-end-date-{exp_id}')
            description = request.POST.get(f'edit-description-{exp_id}')

            print(f"Updating Experience ID {exp_id}:")
            print(f"Position: {position}")
            print(f"Company: {company}")
            print(f"Start Date: {start_date}")
            print(f"End Date: {end_date}")
            print(f"Description: {description}")

            experience.position = position
            experience.company = company
            experience.start_date = start_date
            experience.end_date = end_date
            experience.description = description
            experience.save()

        # Handle updating education
        education_ids = request.POST.getlist('education_ids')
        print(f"Education IDs: {education_ids}")

        for edu_id in education_ids:
            education = get_object_or_404(Education, id=edu_id)

            institution = request.POST.get(f'edit-institution-{edu_id}')
            degree = request.POST.get(f'edit-degree-{edu_id}')
            cgpa = request.POST.get(f'edit-cgpa-{edu_id}')
            start_year = request.POST.get(f'edit-start-year-{edu_id}')
            end_year = request.POST.get(f'edit-end-year-{edu_id}')

            print(f"Updating Education ID {edu_id}:")
            print(f"Institution: {institution}")
            print(f"Degree: {degree}")
            print(f"CGPA: {cgpa}")
            print(f"Start Year: {start_year}")
            print(f"End Year: {end_year}")

            education.institution = institution
            education.degree = degree
            education.cgpa = cgpa
            education.start_year = start_year
            education.end_year = end_year
            education.save()

        # Handle updating skills
        skill_ids = request.POST.getlist('skill_ids')
        print(f"Skill IDs: {skill_ids}")

        for skill_id in skill_ids:
            skill = get_object_or_404(Skill, id=skill_id)
            skill_name = request.POST.get(f'edit-skill-{skill_id}')

            print(f"Updating Skill ID {skill_id}:")
            print(f"Skill Name: {skill_name}")

            skill.skill_name = skill_name
            skill.save()

        # Handle updating languages
        language_ids = request.POST.getlist('language_ids')
        print(f"Language IDs: {language_ids}")

        for lang_id in language_ids:
            language = get_object_or_404(Language, id=lang_id)
            lang_name = request.POST.get(f'edit-language-{lang_id}')
            proficiency = request.POST.get(f'edit-proficiency-{lang_id}')

            print(f"Updating Language ID {lang_id}:")
            print(f"Language: {lang_name}")
            print(f"Proficiency: {proficiency}")

            language.language = lang_name
            language.proficiency = proficiency
            language.save()

        # Handle updating awards
        award_ids = request.POST.getlist('award_ids')
        print(f"Award IDs: {award_ids}")

        for award_id in award_ids:
            award = get_object_or_404(Award, id=award_id)
            award_title = request.POST.get(f'edit-award-title-{award_id}')
            award_position = request.POST.get(f'edit-position-{award_id}')
            award_date = request.POST.get(f'edit-date-awarded-{award_id}')

            print(f"Updating Award ID {award_id}:")
            print(f"Award Title: {award_title}")
            print(f"Position: {award_position}")
            print(f"Date Awarded: {award_date}")

            award.title = award_title
            award.position = award_position
            award.date_awarded = award_date
            award.save()

        # Redirect to the internship and job page after saving
        return redirect('internship_and_job')

    # If it's a GET request, render the form with current data
    context = {
        'cv_profile': cv_profile,
    }
    return render(request, 'internship_jobs/internship_jobs_edit_cv.html', context)


@login_required(login_url='/login')
def internship_job_applied_jobs_view(request):
    # Retrieve the user's CVProfile
    cv_profile = CVProfile.objects.filter(user_id=request.user.id).first()

    if not cv_profile:
        # If no CVProfile exists, handle it (e.g., redirect or show message)
        return render(request, 'internship_jobs/internship_jobs_applied_jobs.html', {'jobs': None})

    # Get all job applications for the user's CVProfile
    job_applications = JobApplication.objects.filter(cv_profile=cv_profile)

    # Extract the job IDs from the applications
    job_ids = job_applications.values_list('job_id', flat=True)

    # Get all jobs that the user has applied to
    jobs = Job.objects.filter(id__in=job_ids)

    return render(request, 'internship_jobs/internship_jobs_applied_jobs.html', {'jobs': jobs})


@login_required(login_url='/login')
def internship_job_applied_candidate_view(request, id):
    job = get_object_or_404(Job, id=id)

    job_applications = JobApplication.objects.filter(job_id=job.id)
    print(job_applications)
    applicants = CVProfile.objects.filter(user__in=job_applications.values('cv_profile__user'))
    print(applicants)

    return render(request, 'internship_jobs/internship_jobs_applied_candidates.html', {
        'job': job,
        'applicants': applicants
    })


@login_required(login_url='/login')
def internship_job_view_cv_view(request, id):
    cv_profile = get_object_or_404(CVProfile, id=id)
    return render(request, 'internship_jobs/internship_jobs_view_cv.html', {'cv_profile': cv_profile})


@login_required(login_url='/login')
def internship_job_edit_job_view(request, id):
    job = get_object_or_404(Job, id=id)  # Retrieve the job object

    if request.method == 'POST':
        job.title = request.POST.get('title', job.title)
        job.company = request.POST.get('company', job.company)
        job.description = request.POST.get('description', job.description)
        job.responsibilities = request.POST.get('responsibilities', job.responsibilities)
        job.education_requirements = request.POST.get('education_requirements', job.education_requirements)
        job.previous_experience = request.POST.get('previous_experience', job.previous_experience)
        job.skills_needed = request.POST.get('skills_needed', job.skills_needed)
        job.other_requirements = request.POST.get('other_requirements', job.other_requirements)
        job.post_type = request.POST.get('post_type', job.post_type)
        job.gender = request.POST.get('gender', job.gender)
        job.location = request.POST.get('location', job.location)
        job.salary = request.POST.get('salary', job.salary)
        job.logo = request.FILES.get('logo', job.logo)  # Handle file upload
        job.experience_level = request.POST.get('experience_level', job.experience_level)
        job.work_environment = request.POST.get('work_environment', job.work_environment)
        job.industry = request.POST.get('industry', job.industry)
        job.industry_specification = request.POST.get('industry_specification', job.industry_specification)
        job.deadline = request.POST.get('deadline', job.deadline)
        job.save()  # Save the updated job
        return redirect('internship_job_edit_job', id)  # Redirect after successful update

    return render(request, 'internship_jobs/internship_jobs_edit_jobs.html', {'job': job})


@login_required(login_url='/login')
def internship_job_delete_job_view(request, id):
    job = get_object_or_404(Job, id=id)
    job.delete()
    messages.success(request, 'Job deleted successfully.')
    return redirect('internship_job_posted_jobs')  # Redirect to the jobs listing page after deletion


@login_required(login_url='/login')
def delete_cv(request, cv_id):
    if request.method == "POST":
        cv_profile = get_object_or_404(CVProfile, id=cv_id)
        cv_profile.delete()
        return redirect('internship_and_job')  # Redirect to a success page or profile list
