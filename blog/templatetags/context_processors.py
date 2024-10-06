from blog.models import Notification


def notifications_processor(request):
    notifications = []
    all_notifications = []

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
        all_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    return {
        'notifications': notifications,
        'all_notifications': all_notifications,
    }
