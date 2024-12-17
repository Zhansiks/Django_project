from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Notification  # Подключите ваши модели Comment и Notification

@receiver(post_save, sender=Comment)
def create_notification(sender, instance, created, **kwargs):
    if created:
        # Получаем автора объявления, связанного с комментарием
        notice_author = instance.notice.user
        # Создаем уведомление для автора объявления
        Notification.objects.create(
            user=notice_author,
            message=f"Новый комментарий к вашему объявлению: '{instance.text}'",
            content_type='comment'
        )
