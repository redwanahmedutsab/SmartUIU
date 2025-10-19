from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Event, Payment
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
import uuid
import pdfkit
import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

from django.shortcuts import render
from .models import Event, Payment
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    user = request.user
    search_query = request.GET.get('search', '')

    # Filter events by search query if provided
    if search_query:
        events = Event.objects.filter(name__icontains=search_query).order_by('-date')
    else:
        events = Event.objects.all().order_by('-date')

    # Precompute registration status for the logged-in user
    user_payments = Payment.objects.filter(student=user, status='Success')
    registered_event_ids = set(user_payments.values_list('event_id', flat=True))

    # Annotate each event with 'is_registered' attribute
    for event in events:
        event.is_registered = event.id in registered_event_ids

    context = {
        'events': events,
        'search_query': search_query,
    }
    return render(request, 'payer/home.html', context)


# -----------------------------
# Event Detail
# -----------------------------
@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    payment_success = False
    payment = None

    try:
        payment = Payment.objects.get(student=request.user, event=event, status='Success')
        payment_success = True
    except Payment.DoesNotExist:
        pass

    return render(request, 'payer/event_detail.html', {
        'event': event,
        'payment_success': payment_success,
        'payment': payment
    })


# -----------------------------
# SSLCommerz Payment Initiate
# -----------------------------
@login_required
def ssl_payment_init(request):
    if request.method == "POST":
        # --- DEBUG: Log POST data ---
        print("POST data:", request.POST)

        event_id = request.POST.get("event_id")
        print("Received event_id:", event_id)

        if not event_id:
            return JsonResponse({'error': 'Event ID is missing.'}, status=400)

        event = get_object_or_404(Event, pk=event_id)
        user = request.user

        tran_id = str(uuid.uuid4())
        post_data = {
            'store_id': settings.SSL_STORE_ID,
            'store_passwd': settings.SSL_STORE_PASSWORD,
            'total_amount': float(event.fee_amount),
            'currency': 'BDT',
            'tran_id': tran_id,
            'success_url': request.build_absolute_uri('/payer/ssl-success/'),
            'fail_url': request.build_absolute_uri('/payer/ssl-fail/'),
            'cancel_url': request.build_absolute_uri('/payer/ssl-cancel/'),
            'cus_name': user.get_full_name() or user.username,
            'cus_email': user.email or 'example@email.com',
            'cus_add1': 'Dhaka',
            'cus_city': 'Dhaka',
            'cus_postcode': '1207',
            'cus_country': 'Bangladesh',
            'cus_phone': '01711111111',
            'product_name': event.name,
            'product_category': 'Event',
            'product_profile': 'general',
            'shipping_method': 'NO',
        }

        try:
            response = requests.post(settings.SSL_SANDBOX_URL, data=post_data)
            data = response.json()
            print("SSLCommerz Response:", data)
        except Exception as e:
            print("Error contacting SSLCommerz:", e)
            return JsonResponse({'error': 'Failed to connect to SSLCommerz.'}, status=500)

        if data.get('GatewayPageURL'):
            Payment.objects.create(
                student=user,
                event=event,
                amount=event.fee_amount,
                transaction_id=tran_id,
                status='Pending'
            )
            return JsonResponse({'checkout_url': data['GatewayPageURL']})
        else:
            return JsonResponse({'error': 'Failed to initiate payment.'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


# -----------------------------
# SSLCommerz Callbacks
# -----------------------------
@csrf_exempt
def ssl_payment_success(request):
    data = request.POST
    print("Success callback data:", data)

    tran_id = data.get('tran_id')
    val_id = data.get('val_id')

    validation_payload = {
        'store_id': settings.SSL_STORE_ID,
        'store_passwd': settings.SSL_STORE_PASSWORD,
        'val_id': val_id,
        'format': 'json'
    }

    try:
        response = requests.get(settings.SSL_VALID_URL, params=validation_payload)
        result = response.json()
        print("Validation Response:", result)
    except Exception as e:
        print("Validation request failed:", e)
        return render(request, 'payer/payment_status.html', {'success': False})

    if result.get('status') in ['VALID', 'VALIDATED']:
        payment = Payment.objects.get(transaction_id=tran_id)
        payment.status = 'Success'
        payment.save()
        return render(request, 'payer/payment_status.html', {'success': True})
    else:
        return render(request, 'payer/payment_status.html', {'success': False})


@csrf_exempt
def ssl_payment_fail(request):
    print("Payment failed callback:", request.POST)
    return render(request, 'payer/payment_status.html', {'success': False})


@csrf_exempt
def ssl_payment_cancel(request):
    print("Payment cancelled callback:", request.POST)
    return render(request, 'payer/payment_status.html', {'cancelled': True})


from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
from django.conf import settings
from .models import Payment
import os
from django.utils import timezone

@login_required
def generate_receipt(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id, student=request.user)

    # Absolute path to the logo
    logo_path = os.path.join(settings.BASE_DIR, 'static/images/smartuiu.png')

    html_content = render_to_string('payer/receipt_template.html', {
        'payment': payment,
        'logo_path': logo_path,
        'now': timezone.now()
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{payment.id}.pdf"'

    pisa_status = pisa.CreatePDF(html_content, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors generating the PDF', status=500)

    return response