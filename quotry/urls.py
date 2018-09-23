from django.conf.urls import patterns, url
from quotry import views

urlpatterns = patterns('',
    ## Intro
    # host/
    url(r'^$', views.index, name='index'),
    # host/about/
    url(r'^about/$', views.about, name='about'),
    # host/restricted/
    url(r'^restricted/$', views.restricted, name='restricted'),

    ## Profile
    # host/add_profile/
    url(r'^add_profile/$', views.add_profile, name='add_profile'),
    # host/profile/
    url(r'^profile/$', views.profile, name='profile'),

    ## Payload
    # host/tag/<tag_name_slug>/
    url(r'^tag/(?P<tag_name_slug>[\w\-]+)/$', views.tag, name='tag'),
    # host/add_tag/
    url(r'^add_tag/$', views.add_tag, name='add_tag'),
    # host/tag/<tag_name_slug>/add_quote/
    url(r'^tag/(?P<tag_name_slug>[\w\-]+)/add_quote/$', views.add_quote, name='add_quote'),
    # host/add_quote_custom/
    url(r'^add_quote_custom/$', views.add_quote_custom, name='add_quote_custom'),

    ## Utils
    # host/fav_tag/
    url(r'^fav_tag/$', views.fav_tag, name='fav_tag'),
    # host/suggest_tag/
    url(r'^suggest_tag/$', views.suggest_tag, name='suggest_tag'),
)