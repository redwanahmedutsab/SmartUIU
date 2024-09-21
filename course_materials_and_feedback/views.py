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

        # Create MaterialFile objects for each uploaded file
        for material in materials:
            MaterialFile.objects.create(
                course_material=course_material,
                file=material
            )

        return redirect('course_materials')  # Ensure this URL name exists

    return render(request, 'course_materials/course_materials_add.html')


def course_materials_my_materials_view(request):
    materials = CourseMaterial.objects.all()
    return render(request, 'course_materials/course_materials_my_materials.html', {'materials': materials})


def edit_course_material(request):
    return None


@login_required(login_url='/login')
def delete_course_material(request, id):
    material = get_object_or_404(CourseMaterial, id=id)
    material.delete()
    return redirect('course_materials_my_materials')


@login_required(login_url='/login')
def course_materials_search_view(request):
    return render(request, 'course_materials/course_materials_search.html')
