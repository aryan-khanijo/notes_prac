from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('',views.index),
    path('maths1',views.maths1),
    path('tc',views.tc),
    path('phy',views.phy),
    path('c',views.c),
    path('fit',views.fit),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('signup',views.signup),
    path('login',views.login_view),
    path('logout',views.logout_view),
    path('upload',views.add_notes)
]