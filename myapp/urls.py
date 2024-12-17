from django.urls import path
from .views import home_view,create_board,list_board,detail_board,remove_from_favorites,notification_list,mark_notifications_as_read,favorite_ads,add_favorite,search_title,delete_board,delete_comment,logout_view,edit_notice,RegisterUser,LoginUser

app_name = 'myapp'
urlpatterns = [
    path('', home_view, name='home'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('create/', create_board, name = 'create'),
    path('list', list_board, name = 'list'),
    path('detail/<int:pattern_id>/', detail_board, name='detail_board'),
    path('logout/', logout_view, name='logout'), 
    path('edit/<int:id>/', edit_notice, name = 'edit'),
    path('comments/delete/<int:comment_id>/<int:pattern_id>/',delete_comment, name='delete_comment'),
    path('delete_board/<int:pattern_id>/', delete_board, name='delete_board'),
    path('search_title/', search_title, name = 'search_title'),
    path('add_favorite/<int:id>/', add_favorite, name='add_favorite'),
    path('favorites/', favorite_ads, name='favorite_ads'),
    path('remove_from_favorites/<int:id>/', remove_from_favorites, name='remove_from_favorites'),
    path('notifications/', notification_list, name='notifications'),
    path('notifications/mark-read/', mark_notifications_as_read, name='mark_notifications_as_read'),

       
    
  

    
]