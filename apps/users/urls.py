from django.conf.urls import url, include
from apps.users import views


urlpatterns = [
    url(r'^login', views.LoginView.as_view(), name='login'),
    # 发送短信验证
    url(r'^send_message$', views.send_message, name='send_message'),
    # 极验验证
    url(r'^pc-geetest/register', views.pcgetcaptcha, name='pcgetcaptcha'),
]

