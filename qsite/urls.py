from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from quotry.views import QuotryRegistrationView


urlpatterns = patterns('',
    # host/admin/, dja admin builtin pack
    url(r'^admin/', include(admin.site.urls)),

    # to override the default pattern in accounts
    url(r'^accounts/register/$', QuotryRegistrationView.as_view(), name='registration_register'),
    # host/accounts/, dja-reg-redux accounts (?)
    url(r'^accounts/', include('registration.backends.default.urls')),

    # host/[<anything-else>/], quotry app
    url(r'^', include('quotry.urls')),
)


# for static
if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)','serve',{'document_root': settings.MEDIA_ROOT}), 
    )

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)