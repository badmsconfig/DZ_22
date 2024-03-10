from django.urls import path
from blogapp import views
from blogapp.views import AboutView, ContactView, AnketaView

app_name = 'blogapp'

#views.main_view()
urlpatterns = [
    path('', views.main_view, name='index'),
    path('post/<int:id>/', views.post, name='post'),
    #path('about/', views.about, name='about'),
    #path('anketa/', views.anketa, name='anketa'),
    #path('search/', views.search, name='search'),
    #path('create/', views.create_post, name='create'),
    #path('contact/', views.contact_view, name='contact'),
    path('tag-list/', views.TagListView.as_view(), name='tag_list'),
    path('tag-detail/<int:pk>/', views.TagDetailView.as_view(), name='tag_detail'),
    path('tag-create/', views.TagCreateView.as_view(), name='tag_create'),
    path('tag-update/<int:pk>/', views.TagUpdateView.as_view(), name='tag_update'),
    path('tag-delete/<int:pk>/', views.TagDeleteView.as_view(), name='tag_delete'),
    path('create/', views.PostCreateView.as_view(), name='create'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('anketa/', AnketaView.as_view(), name='anketa'),
]


