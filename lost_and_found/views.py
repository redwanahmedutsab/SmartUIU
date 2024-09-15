from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Item


@login_required(login_url='/login')
def home(request):
    items = Item.objects.all()
    return render(request, 'lost_and_found/lost_and_found.html', {'items': items})


@login_required(login_url='/login')
def lost_and_found_user_section_view(request):
    if request.method == 'POST':
        # Handle item deletion
        item_id = request.POST.get('item_id')
        if item_id:
            item = get_object_or_404(Item, id=item_id, user=request.user)
            item.delete()
        return redirect('lost_and_found_user_section')  # Redirect to the same view

    # Handle displaying items
    items = Item.objects.filter(user=request.user)
    return render(request, 'lost_and_found/lost_and_found_user_section.html', {'items': items})


@login_required(login_url='/login')
def lost_and_found_register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        item_name = request.POST.get('item_name')
        location = request.POST.get('location')
        time_date = request.POST.get('time_date')
        description = request.POST.get('description')
        item_image = request.FILES.get('item_image', None)

        found_by_user = request.user

        item = Item(
            email=email,
            mobile=mobile,
            item_name=item_name,
            location=location,
            time_date=time_date,
            description=description,
            item_image=item_image,
            found_by_name=found_by_user.first_name + ' ' + found_by_user.last_name,
            user_id=found_by_user.id
        )
        item.save()
        return redirect('lost_and_found')
    user = User.objects.get(id=request.user.id)
    return render(request, 'lost_and_found/lost_and_found_register.html', {'user': user})


@login_required(login_url='/login')
def lost_and_found_single_view(request, id):
    item = get_object_or_404(Item, id=id)

    return render(request, 'lost_and_found/lost_and_found_single.html', {'item': item})
