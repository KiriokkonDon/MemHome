
from django.contrib import admin
from django.urls import path
from mysite.views import HomeView, LoginView, LogoutView
from mysite.views import ProfilePage
from mysite.views import ProfilePage, RegisterView, EditProfileView, ProfileList
from mysite import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(r'^accounts/register/$', RegisterView.as_view(), name="register"),
    path('accounts/login/', LoginView.as_view(), name="login"),
    path('accounts/logout/', LogoutView.as_view(), name="logout"),
    path('accounts/profile/', ProfilePage.as_view(), name="profile"),
    path(r'^accounts/profile/edit/$', EditProfileView.as_view(), name="edit_profile"),
    path('accounts/profile/profilelist', ProfileList.as_view(), name="profilelist"),
    path('', HomeView.as_view(), name="home"),
    path('admin/', admin.site.urls),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+\
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
