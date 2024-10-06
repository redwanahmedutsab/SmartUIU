from study_group_app.models import NotificationStudy


def notifications_processor(request):
    notifications_study = []
    all_notifications_study = []

    if request.user.is_authenticated:
        notifications_study = NotificationStudy.objects.filter(user=request.user, is_read=0)
        all_notifications_study = NotificationStudy.objects.filter(user=request.user)

    return {
        'notifications_study': notifications_study,
        'all_notifications_study': all_notifications_study,
    }
