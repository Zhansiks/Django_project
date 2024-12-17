from django.contrib import admin
from .models import Notice_board,Comment,Rating,Favorite


admin.site.register(Notice_board)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Favorite)