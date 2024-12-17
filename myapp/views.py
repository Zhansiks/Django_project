from django.shortcuts import render,redirect
from .forms import NoticeForm
from .models import Notice_board,Favorite,Item,Rating
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Notice_board, Comment
from .forms import CommentForm,LoginUserForm,RegisterUserForm,SearchForm
from django.urls import  reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.db.models import Q, Avg
from django.contrib import messages


#авторизация
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'myapp/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('myapp:list')

#регистрация
class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'myapp/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('myapp:login')

#выход
def logout_view(request):
    logout(request)  
    return redirect('myapp:login')


#домашняя страницв
@login_required
def home_view(request):
    unread_notifications_count = request.user.notifications.filter(is_read=False).count()
    return render(request, 'myapp/base.html', { 'unread_notifications_count': unread_notifications_count})



#создание объявления
@login_required
def create_board(request):
    if request.method == "POST":
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)  
            notice.user = request.user  
            notice.save()  
            return redirect('myapp:list')  
    else:
        form = NoticeForm()
    return render(request, 'myapp/create.html', {'form': form})

# Отображение списка объявлений
@login_required
def list_board(request):
    notices = Notice_board.objects.all()
    unread_notifications_count = request.user.notifications.filter(is_read=False).count()
    paginator = Paginator(notices, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'myapp/list_board.html', {'page_obj': page_obj,  'unread_notifications_count': unread_notifications_count})




#детальное представлнение
@login_required
def detail_board(request, pattern_id):
    notice = get_object_or_404(Notice_board, pk=pattern_id)
    comments = notice.comments.all()

    #обработка формы комментария
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.notice = notice
            comment.user = request.user
            comment.save()
            return redirect('myapp:detail_board', pattern_id=pattern_id)
    else:
        form = CommentForm()

    #обработка выставления оценки
    if request.method == "POST" and 'rating' in request.POST:
        score = int(request.POST.get('rating'))
        Rating.objects.update_or_create(
            user=request.user,
            notice_board=notice,
            defaults={'score': score}
        )
        notice.update_average_rating()#обновляю средний рейтинг объявления

        return redirect('myapp:detail_board', pattern_id=pattern_id)

    #получение оценки пользователя 
    user_rating = Rating.objects.filter(user=request.user, notice_board=notice).first()

    return render(request, 'myapp/detail.html', {
        'detail': notice,
        'comments': comments,
        'form': form,
        'user_rating': user_rating,
    })


#удаление объявления
@login_required
def delete_board(request, pattern_id):
    detail = get_object_or_404(Notice_board, id=pattern_id)
    if request.method == 'POST':
        detail.delete()
        return redirect('myapp:list')  
    return HttpResponseForbidden('Вы не авторизованы для удаления этого объекта.')

#удаление комментария
@login_required
def delete_comment(request, comment_id, pattern_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user or request.user.is_staff:
        comment.delete()
    return redirect('myapp:detail_board', pattern_id=pattern_id)







#Изменения объявления
@login_required
def edit_notice(request, id):
    notice = get_object_or_404(Notice_board, id=id)

    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('myapp:list') 
        
    else:
        form = NoticeForm(instance=notice)

    return render(request, 'myapp/edit.html', {'form': form, 'pattern': notice})

#поиск по названию 
def search_title(request):
    form = SearchForm(request.GET or None)  
    notices = Notice_board.objects.all()  

    if request.method == "GET" and form.is_valid():  
        query = form.cleaned_data.get('query')  
        if query:  
            notices = notices.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

    return render(request, 'myapp/search_title.html', {'form': form, 'notices': notices})


#добавление в избранные
def add_favorite(request, id):
    ad = get_object_or_404(Notice_board, id=id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, ad=ad)
    if created:
        # Если добавлено в избранное, можно добавить сообщение
        messages.success(request, 'Объявление добавлено в избранное.')
    else:
        messages.info(request, 'Объявление уже в избранном.')
    return redirect('myapp:detail_board', pattern_id=ad.id)

#отображение в избранные 
def favorite_ads(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'myapp/favorites.html', {'favorites': favorites})


#удаление из избранного
def remove_from_favorites(request, id):
    if request.method == 'POST':
        favorite = get_object_or_404(Favorite, id=id)
        favorite.delete()  
        return redirect('myapp:favorite_ads')  
    


#отображение уведомлений
def notification_list(request):
    notifications = request.user.notifications.order_by('-created_at')
    return render(request, 'myapp/notification_list.html', {'notifications': notifications})


#помечает непрочитанные как прочитанные увед.
def mark_notifications_as_read(request):
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return redirect('myapp:notifications')



