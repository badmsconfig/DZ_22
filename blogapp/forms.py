from django import forms
from .models import Post
from .models import Tag


class Contact(forms.Form):
    name = forms.CharField(label='Название')
    email = forms.EmailField(label='email')
    message = forms.CharField(label='Сообщение')


class Anketa(forms.Form):
    name = forms.CharField(label='Имя')
    lname = forms.CharField(label='Фамилия')
    adres = forms.CharField(label='Адрес')
    sex = forms.ChoiceField(label='Пол', choices=[('M', 'Мужской'), ('F', 'Женский')])
    email = forms.EmailField(label='email')
    message = forms.CharField(label='Сообщение')
    favorite_book = forms.CharField(label='Любимая книга')
    favorite_movie = forms.CharField(label='Любимый фильм')


# class SearchForm(forms.Form):
#     q = forms.CharField(label='Поиск')

#class SearchForm(forms.Form):
    q = forms.CharField(label='Поиск')


class PostForm(forms.ModelForm):
    name = forms.CharField(label='Название',
                           widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'}))
    text = forms.CharField(label='Текст',
                           widget=forms.TextInput(attrs={'placeholder': 'Введите текст', 'class': 'form-control'}))
    #category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', widget=forms.Select(attrs={'class': 'form-control'}))

    # Чекбоксы
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                          widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = Post
        #fields = '__all__'
        #fields = ('name', 'category')
        exclude = ('user',)
class PostCreateViev():
    pass