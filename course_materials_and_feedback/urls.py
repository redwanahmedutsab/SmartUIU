from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='course_materials'),
    path('course_materials_add/', views.course_materials_add_view, name='course_materials_add'),
    path('course_materials_search/', views.course_materials_search_view, name='course_materials_search'),
    path('course_materials_my_materials/', views.course_materials_my_materials_view,
         name='course_materials_my_materials'),
    path('course_materials/edit/<int:id>/', views.edit_course_material, name='edit_course_material'),
    path('course_materials/delete/<int:id>/', views.delete_course_material, name='delete_course_material'),
    path('download/<int:file_id>/', views.download_material_file, name='download_material_file'),
]
