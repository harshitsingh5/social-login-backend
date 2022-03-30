from django.urls import include, path
from django.views.generic.base import TemplateView

from django.urls import re_path
from .views import *

urlpatterns = [
     # path('accounts/', include('django.contrib.auth.urls')),
     # path('', TemplateView.as_view(template_name = 'home.html'), name = 'home'),
     # path('social-auth/', include('social_django.urls', namespace='social'))

     # re_path('rest-auth/', include('rest_auth.urls'))

     path('facebook', FacebookSocialAuthView.as_view()),

]