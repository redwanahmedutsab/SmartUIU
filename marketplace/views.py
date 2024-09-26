from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Product, Tag, ProductImage


def marketplace_post_view(request):
    if request.method == 'POST':
        # Handle product data
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        condition = request.POST.get('condition')
        shipping_details = request.POST.get('shipping_details')
        tags = request.POST.get('tags').split(',')
        images = request.FILES.getlist('images')  # Handle multiple images

        print(images)

        product = Product(
            name=name,
            description=description,
            price=price,
            category=category,
            phone=phone,
            location=location,
            condition=condition,
            shipping_details=shipping_details,
            seller=request.user
        )
        product.save()

        # Handle tags
        for tag_name in tags:
            tag_name = tag_name.strip()
            tag, created = Tag.objects.get_or_create(name=tag_name)
            product.tags.add(tag)

        # Handle images
        for image in images:
            ProductImage.objects.create(product=product, image=image)

        return redirect('marketplace')

    return render(request, 'marketplace/marketplace_post.html')


@login_required(login_url='/login')
def home(request):
    items = Product.objects.all()
    return render(request, 'marketplace/marketplace.html', {'items': items})


@login_required(login_url='/login')
def marketplace_single_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'marketplace/marketplace_single.html', {'product': product})


@login_required(login_url='/login')
def marketplace_my_post_view(request):
    if request.method == 'POST':
        # Handle product deletion
        product_id = request.POST.get('delete_product_id')
        if product_id:
            product = get_object_or_404(Product, id=product_id, seller=request.user)
            product.delete()
            return redirect('marketplace_my_post')  # Redirect to the same page to reflect the changes

    # Display user's posts
    items = Product.objects.filter(seller=request.user)
    return render(request, 'marketplace/marketplace_my_post.html', {'items': items})


@login_required(login_url='/login')
def delete_product_image(request):
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        image = get_object_or_404(ProductImage, id=image_id)
        image.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required(login_url='/login')
def marketplace_edit_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.category = request.POST.get('category')
        product.phone = request.POST.get('phone')
        product.location = request.POST.get('location')
        product.condition = request.POST.get('condition')
        product.shipping_details = request.POST.get('shipping_details')
        product.save()

        new_images = request.FILES.getlist('new_images')
        print('here is called')
        print(new_images)
        for image in new_images:
            ProductImage.objects.create(product=product, image=image)

        return redirect('marketplace_my_post')  # Redirect to the desired page after saving
    return render(request, 'marketplace/marketplace_edit.html', {'product': product})
