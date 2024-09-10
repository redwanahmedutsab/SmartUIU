from django.shortcuts import render, redirect, get_object_or_404
from .models import Item


def home(request):
    items = Item.objects.all()
    return render(request, 'lost_and_found/lost_and_found.html', {'items': items})


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
            found_by_name=found_by_user.first_name + ' ' + found_by_user.last_name
        )
        item.save()
        return redirect('lost_and_found')
    return render(request, 'lost_and_found/lost_and_found_register.html')


# def lost_and_found_single_view(request, id):
#     return render(request, 'lost_and_found/lost_and_found_single.html')


def lost_and_found_single_view(request, id):
    # Retrieve the item by id
    item = get_object_or_404(Item, id=id)

    # Pass the item to the template for rendering
    return render(request, 'lost_and_found/lost_and_found_single.html', {'item': item})
