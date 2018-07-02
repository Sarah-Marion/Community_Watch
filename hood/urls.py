from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from hood import views as core_views

urlpatterns = [
    url('^$', views.index, name='homepage'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^new/post/$', views.new_post, name='post'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^profile/(?P<profile_id>[-\w]+)/$', views.profile, name='profile'),
    url(r'^new/business/$', views.business, name='business'),
    url(r'^social/$', views.social_ammenities, name='social'),
    url(r'^hood/$', views.neighbourhood, name='neighbourhood'),
    url(r'^business/$', views.bizdisplay, name='bizdisplay'),
    url(r'^neighbourhood_display/$', views.hooddisplay, name='displayhood'),
    url(r'^join/(\d+)', views.join, name='joinHood'),
    url(r'^exitHood/(\d+)', views.exitHood, name='exitHood'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
