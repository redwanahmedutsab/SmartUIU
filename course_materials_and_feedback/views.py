from django.contrib import messages
from django.http import FileResponse

from .models import CourseMaterial, MaterialFile
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url='/login')
def home(request):
    return render(request, 'course_materials/course_materials.html')


@login_required(login_url='/login')
def course_materials_add_view(request):
    if request.method == 'POST':
        degree = request.POST.get('degree')
        trimester = request.POST.get('trimester')
        course_code = request.POST.get('course_code')
        course_title = request.POST.get('course_title')
        material_type = request.POST.get('material_type')
        material_description = request.POST.get('material_description')
        admin_email = request.POST.get('admin_email')
        materials = request.FILES.getlist('materials')

        course_material = CourseMaterial.objects.create(
            degree=degree,
            trimester=trimester,
            course_code=course_code,
            course_title=course_title,
            material_type=material_type,
            material_description=material_description,
            admin_email=admin_email,
            user=request.user
        )

        for material in materials:
            MaterialFile.objects.create(
                course_material=course_material,
                file=material
            )

        return redirect('course_materials')

    return render(request, 'course_materials/course_materials_add.html')


@login_required(login_url='/login')
def course_materials_my_materials_view(request):
    materials = CourseMaterial.objects.all()
    return render(request, 'course_materials/course_materials_my_materials.html', {'materials': materials})


@login_required(login_url='/login')
def edit_course_material(request, id):
    course_material = get_object_or_404(CourseMaterial, id=id)

    if request.method == 'POST':
        course_material.degree = request.POST.get('degree')
        course_material.trimester = request.POST.get('trimester')
        course_material.course_title = request.POST.get('course_title')
        course_material.course_code = request.POST.get('course_code')
        course_material.material_type = request.POST.get('material_type')
        course_material.material_description = request.POST.get('material_description')
        course_material.admin_email = request.POST.get('admin_email')

        course_material.save()

        if request.FILES.getlist('materials'):
            existing_files = MaterialFile.objects.filter(course_material=course_material)
            for file in existing_files:
                file.file.delete()
                file.delete()

            for file in request.FILES.getlist('materials'):
                MaterialFile.objects.create(course_material=course_material, file=file)

        messages.success(request, 'Course material updated successfully!')
        return redirect('course_materials_my_materials')

    existing_files = course_material.files.all()

    return render(request, 'course_materials/course_materials_edit.html', {
        'course_material': course_material,
        'existing_files': existing_files,
    })


@login_required(login_url='/login')
def delete_course_material(request, id):
    material = get_object_or_404(CourseMaterial, id=id)
    material.delete()
    return redirect('course_materials_my_materials')


def to_ordinal(n):
    if 10 <= n % 100 < 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"


@login_required(login_url='/login')
def course_materials_search_view(request):
    degree = request.GET.get('degree')
    course_name = request.GET.get('course_name', '')
    trimester = request.GET.get('trimester')
    material_type = request.GET.get('material_type')

    if degree:
        request.session['degree'] = degree
        print(f'Degree set in session: {request.session["degree"]}')
    else:
        degree = request.session.get('degree')
        print(f'Degree retrieved from session: {degree}')

    materials = CourseMaterial.objects.all()

    if degree:
        materials = materials.filter(degree=degree)

    if course_name:
        materials = materials.filter(course_title__icontains=course_name)

    if trimester:
        materials = materials.filter(trimester=trimester)

    if material_type:
        materials = materials.filter(material_type=material_type)

    ordinal_trimester_range = [to_ordinal(i) for i in range(1, 13)]

    context = {
        'materials': materials,
        'degree': degree,
        'trimester_range': ordinal_trimester_range,
    }
    return render(request, 'course_materials/course_materials_search.html', context)


@login_required(login_url='/login')
def download_material_file(request, file_id):
    material_file = get_object_or_404(MaterialFile, id=file_id)
    file_path = material_file.file.path

    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=material_file.file.name)
