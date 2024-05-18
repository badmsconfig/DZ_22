from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from .models import Post, Tag, Category
from .forms import Contact, PostCategoryForm
from .forms import Anketa
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import ContextMixin, TemplateView, View
from django.contrib.auth import get_user_model
from .forms import PostForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
# def main_view(request):
#     posts = Post.objects.all()
#     return render(request, 'blogapp/index.html', context={'posts': posts})

def main_view(request):
    #posts = Post.objects.all()
    #posts = Post.objects.filter(is_active=True)
    #posts = Post.active_objects.all()
    posts = Post.active_objects.select_related('category', 'user').all()
    paginator = Paginator(posts, 100)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    title = 'главная страница'
    #title = title.capitalize()

    return render(request, 'blogapp/index.html', context={'posts': posts, 'title': title})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blogapp/create.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        # Убеждаемся, что пользователь аутентифицирован перед сохранением поста
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
            return super().form_valid(form)
        else:
            # Если пользователь не аутентифицирован, вы можете перенаправить его на страницу входа или выполнить другие действия
            return HttpResponseForbidden("You must be logged in to create a post.")

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
class TagListView(LoginRequiredMixin, ListView, NameContextMixin):
    model = Tag
    template_name = 'blogapp/tag_list.html'
    context_object_name = 'tags'
    paginate_by = 4

    def get_queryset(self):
        """
        Получение данных
        :return:
        """
        #return Tag.objects.all()
        return Tag.objects.filter(is_active=True )

# детальная информация
class TagDetailView(UserPassesTestMixin, DetailView, NameContextMixin):
    model = Tag
    template_name = 'blogapp/tag_detail.html'

    # def test_func(self):
    #     return self.request.user.is_superuser

    def test_func(self):
        tag_id = self.kwargs.get('pk')
        try:
            tag = Tag.objects.get(pk=tag_id)
            # Проверяем, имеет ли текущий пользователь права на просмотр этого тега
            return tag.author == self.request.user or self.request.user.is_superuser
        except Tag.DoesNotExist:
            return False

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
# Важно LoginRequiredMixin - он должен идти первым.
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
        form.instance.author = self.request.user
        return super().form_valid(form)

class TagUpdateView(UpdateView):
    fields = '__all__'
    model = Tag
    success_url = reverse_lazy('blogapp:tag_list')
    template_name = 'blogapp/tag_create.html'

class TagDeleteView(DeleteView):
    model = Tag
    success_url = reverse_lazy('blogapp:tag_list')
    template_name = 'blogapp/tag_delete_confirm.html'

# может читать только админ
@user_passes_test(lambda u: u.is_superuser)
def post(request, id):
    post = get_object_or_404(Post, id=id)

    all_tags = post.get_all_tags
    for item in all_tags:
        print(item)
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


# def contact_view(request):
#     if request.method == 'POST':
#         form = Contact(request.POST)
#         if form.is_valid():
#             # Получить данные из формы
#             name = form.cleaned_data['name']
#             message = form.cleaned_data['message']
#             email = form.cleaned_data['email']
#
#             send_mail(
#             'Contact message',
#             f'Ваше сообщение {message} принято',
#             'from@example.com',
#             [email],
#             fail_silently=True,
#             )
#
#         return HttpResponseRedirect(reverse('contact_success'))  # замените на ваше имя URL
#     else:
#         form = Contact()
#     return render(request, 'blogapp/contact.html', {'form': form})

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

            return HttpResponseRedirect(reverse('/'))  # замените на ваше имя URL
        else:
            return render(request, 'blogapp/contact.html', {'form': form})

class CategoryDetailView(DetailView):
    template_name = 'blogapp/category_detail.html'
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostCategoryForm()
        return context

# class PostCategoryCreateView(CreateView):
#     model = Post
#     template_name = 'blogapp/category_detail.html'
#     success_url = '/'
#     form_class = PostCategoryForm
#
#     def post(self, request, *args, **kwargs):
#         self.category_pk = kwargs['pk']
#         return super().post(request, *args, **kwargs)
#
#     def form_valid(self, form):
#         user = self.request.user
#         form.instanсe.user = user
#         category = get_object_or_404(Category, pk=self.category_pk)
#         form.instanсe.category = category
#         return super().form_valid()

class PostCategoryCreateView(CreateView):
    model = Post
    template_name = 'blogapp/category_detail.html'
    success_url = reverse_lazy('')
    form_class = PostCategoryForm

    def post(self, request, *args, **kwargs):
        self.category_pk = kwargs['pk']
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        category = get_object_or_404(Category, pk=self.category_pk)
        form.instance.category = category
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:category_detail', kwargs={'pk': self.category_pk})