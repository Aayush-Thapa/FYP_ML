from django.urls import path
from django.urls import include, re_path
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.views import LogoutView
from requests import request
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path('^$', views.login_page, name='login'),
    re_path('not_found', views.not_found, name='not_found'),
    re_path('index', views.index, name='index'),
    re_path('get_info', views.get_info, name='get_info'),
    re_path('test_data', views.test_data, name='test_data'),
    re_path('analyze_data', views.analyze_data, name='analyze_data'),
    
    re_path('item_basket_size', views.item_basket_size, name='item_basket_size'),


      re_path(
        'password',
        auth_views.PasswordChangeView.as_view(
            template_name='change-password.html',
            success_url = '/'
        ),
        name='change_password'
    ),
    re_path(r'^logout/$', login_required(LogoutView.as_view()), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout')
]



