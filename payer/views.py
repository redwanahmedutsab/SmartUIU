from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Event, Payment
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
import uuid
import pdfkit

def home(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'payer/home.html', {'events': events})


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


@login_required
def bkash_payment(request):
    if request.method == "POST":
        event_id = request.POST.get('event_id')
        event = get_object_or_404(Event, pk=event_id)

        # Generate fake transaction ID
        transaction_id = str(uuid.uuid4())

        # Create payment (mark success for demo)
        payment = Payment.objects.create(
            student=request.user,
            event=event,
            amount=event.fee_amount,
            transaction_id=transaction_id,
            status='Success'
        )

        checkout_url = f"/events/{event.id}/"  # redirect back to event page
        return JsonResponse({'checkout_url': checkout_url})

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def generate_receipt(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id, student=request.user)
    html_content = render_to_string('payer/receipt_template.html', {'payment': payment})
    pdf_file = pdfkit.from_string(html_content, False)

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{payment.id}.pdf"'
    return response