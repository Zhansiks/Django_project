from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone




class Notice_board(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Информация")
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name="Изображение")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    is_favorite = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name="Средняя оценка")

    def update_average_rating(self):
        ratings = self.rating_set.all()# Получаю все оценки для данного объявления
        if ratings.exists():
            self.average_rating = sum(rating.score for rating in ratings) / ratings.count()
        else:
            self.average_rating = 0
        self.save()
    


    class Meta:
        verbose_name = "Объявление"
        ordering = ['-published_date'] 
    def __str__(self):
        return self.title


class Comment(models.Model):
    notice = models.ForeignKey(Notice_board, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    text = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата комментария")

    class Meta:
        verbose_name = "Комментарий"
        ordering = ['created_at']
        
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    ad = models.ForeignKey(Notice_board, on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        unique_together = ('user', 'ad')  # Чтобы каждый пользователь мог добавить объявление в избранное только один раз

    def __str__(self):
        return f"{self.user.username} - {self.ad.title}"
    
class Item(models.Model):
    # Ваши другие поля
    is_favorite = models.BooleanField(default=False)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    content_type = models.CharField(max_length=50)  # Например, 'comment' или 'reply'

    def __str__(self):
        return f"Notification for {self.user} - {self.message}"
    
from django.contrib.auth.models import User

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем
    notice_board = models.ForeignKey(Notice_board, on_delete=models.CASCADE)  # Связь с доской объявлений
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Оценка от 1 до 5

    class Meta:
        unique_together = ('user', 'notice_board')  # Уникальная оценка для каждого пользователя и объявления

    def __str__(self):
        return f"{self.user.username} - {self.notice_board.title}: {self.score}"