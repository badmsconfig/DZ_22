from django.shortcuts import render, get_object_or_404
from .models import Post, Tag
from .forms import Contact, SearchForm, PostForm
from .forms import Anketa
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import ContextMixin, TemplateView, View
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test



# Create your views here.
def main_view(request):
    posts = Post.objects.all()
    return render(request, 'blogapp/index.html', context={'posts': posts})


# def create_post(request):
#     if request.method == 'GET':
#         form = PostForm()
#         return render(request, 'blogapp/create.html', context={'form': form})
#     else:
#         form = PostForm(request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('blog:index'))
#         else:
#             return render(request, 'blogapp/create.html', context={'form': form})

@login_required
def create_post(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'blogapp/create.html', context={'form': form})
    else:
        form = PostForm(request.POST, files=request.FILES)
        if form.is_valid():
            # Добавляем user_id к создаваемому посту
            post = form.save(commit=False)
            post.user_id = request.user.id  # Используем id текущего пользователя
            post.save()
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            return render(request, 'blogapp/create.html', context={'form': form})

# class PostCreateView(CreateView):
#     # form_class =
#     fields = '__all__'
#     model = Tag
#     success_url = reverse_lazy('blogapp:tag_list')
#     template_name = 'blogapp/tag_create.html'
#
#     def form_valid(self, form):
#         """
#         Метод срабатывает после того как форма валидна
#         :param form:
#         :return:
#         """
#         # self.request.user - текущий пользователь
#         # form.instance.user = self.request.user
#         return super().form_valid(form)

# Рабочий код но вернулись от класса к функции так как возникает ошибка FOREIGN KEY constraint failed
# class PostCreateView(CreateView):
#     model = Post
#     form_class = PostForm
#     #fields = ['name', 'text', 'tags']
#     template_name = 'blogapp/create.html'
#     success_url = reverse_lazy('blog:index')
#
#     # def form_valid(self, form):
#     #     form.instance.category_id = 7  # Установите желаемое значение category_id
#     #     return super().form_valid(form)

# Функция к коду class PostCreateView(CreateView)
#     def form_valid(self, form):
#         if self.request.user.is_authenticated:
#             form.instance.user = self.request.user
#             form.instance.category_id = 7  # Установите желаемое значение category_id
#             return super().form_valid(form)
#         else:
#             return redirect('login')

class NameContextMixin(ContextMixin):
    def get_context_data(self, *args, **kwargs):
        """
        Отвечает за передачу параметров в контекст
        :param args:
        :param kwargs:
        :return:
        """
        context = super().get_context_data(*args, **kwargs)
        context['name'] = 'Список тегов'
        return context


# CRUD - CREATE, READ, UPDATE, DELETE
# список тегов
class TagListView(ListView, NameContextMixin):
    model = Tag
    template_name = 'blogapp/tag_list.html'
    context_object_name = 'tags'

    def get_queryset(self):
        """
        Получение данных
        :return:
        """
        return Tag.objects.all()

# детальная информация
class TagDetailView(UserPassesTestMixin, DetailView, NameContextMixin):
    model = Tag
    template_name = 'blogapp/tag_detail.html'

    def test_func(self):
        return self.request.user.is_superuser
    def get(self, request, *args, **kwargs):
        """
        Метод обработки get запроса
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.tag_id = kwargs['pk']
        return super().get(request, *args, **kwargs)
    def get_context_data(self, request, *args, **kwargs):
        """
        Отвечает за передачу параметров в контекст
        :param args:
        :param kwargs:
        :return:
        """
        # self.tag_id = kwargs['pk']
        # return super().get(request,*args, **kwargs)
        context = super().get_context_data(*args, **kwargs)
        context['name'] = 'Список тегов'
        return context


    def get_object(self, queryset=None):
        """
        Получение этого объекта
        :param queryset:
        :return:
        """
        return get_object_or_404(Tag, pk=self.tag_id)

# создание тега
class TagCreateView(LoginRequiredMixin, CreateView, NameContextMixin):
    # form_class =
    fields = '__all__'
    model = Tag
    success_url = reverse_lazy('blogapp:tag_list')
    template_name = 'blogapp/tag_create.html'

    def post(self, request, *args, **kwargs):
        """
        Пришел пост запрос
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Метод срабатывает после того как форма валидна
        :param form:
        :return:
        """
        # self.request.user - текущий пользователь
        # form.instance.user = self.request.user
        return super().form_valid(form)

class TagUpdateView(LoginRequiredMixin, UpdateView):
    fields = '__all__'
    model = Tag
    success_url = reverse_lazy('blogapp:tag_list')
    template_name = 'blogapp/tag_create.html'

class TagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    success_url = reverse_lazy('blogapp:tag_list')
    template_name = 'blogapp/tag_delete_confirm.html'


# может читать только админ
#@user_passes_test(lambda u: u.is_superuser)
def post(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blogapp/post.html', context={'post': post})

# def about(request):
#     return render(request, 'blogapp/about.html')
class AboutView(TemplateView):
    template_name = 'blogapp/about.html'

# def anketa(request):
#     if request.method == 'POST':
#         form = Anketa(request.POST)
#         if form.is_valid():  # Проверка валидности формы
#             # Переносим получение данных внутрь блока is_valid()
#             name = form.cleaned_data['name']
#             lname = form.cleaned_data['lname']
#             adres = form.cleaned_data['adres']
#             sex = form.cleaned_data['sex']
#             email = form.cleaned_data['email']
#             message = form.cleaned_data['message']
#             favorite_book = form.cleaned_data['favorite_book']
#             favorite_movie = form.cleaned_data['favorite_movie']
#             # Здесь можно добавить дополнительную обработку данных, например, сохранение в базу данных
#             return render(request, 'blogapp/anketa.html', {'name': name, 'lname': lname, 'adres': adres, 'sex': sex, 'email': email, 'message': message, 'favorite_book': favorite_book, 'favorite_movie': favorite_movie})
#     else:
#         form = Anketa()
#     return render(request, 'blogapp/anketa.html', {'form': form})

class AnketaView(FormView):
    template_name = 'blogapp/anketa.html'
    form_class = Anketa
    success_url = '/anketa/success/'  # Укажите ваш URL для успешного завершения анкеты

    def form_valid(self, form):
        # Обработка валидной формы
        name = form.cleaned_data['name']
        lname = form.cleaned_data['lname']
        adres = form.cleaned_data['adres']
        sex = form.cleaned_data['sex']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        favorite_book = form.cleaned_data['favorite_book']
        favorite_movie = form.cleaned_data['favorite_movie']
        # Здесь можно добавить дополнительную обработку данных, например, сохранение в базу данных
        return render(self.request, 'blogapp/anketa.html', {'name': name, 'lname': lname, 'adres': adres, 'sex': sex, 'email': email, 'message': message, 'favorite_book': favorite_book, 'favorite_movie': favorite_movie})


class ContactView(View):
    def get(self, request):
        form = Contact()
        return render(request, 'blogapp/contact.html', {'form': form})

    def post(self, request):
        form = Contact(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']

            send_mail(
                'Contact message',
                f'Ваше сообщение {message} принято',
                'from@example.com',
                [email],
                fail_silently=True,
            )

            return HttpResponseRedirect(reverse('contact_success'))  # замените на ваше имя URL
        else:
            return render(request, 'blogapp/contact.html', {'form': form})