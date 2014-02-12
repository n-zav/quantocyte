from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.views.generic import RedirectView

from .views import HomePageView, grid_handler, \
    grid_config, grid_view, grid_crud

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', HomePageView.as_view(), name='home'),
                       # auth urls
                       url(r'^accounts/login/$', login, name='login'),
                       url(r'^accounts/logout/$', logout,
                           {'next_page': '/'},
                           name='logout'),
                       url(r'^accounts/profile/$', RedirectView.as_view(url='/'),
                           name='accounts-profile'),
                       url(r'^accounts/$', RedirectView.as_view(url='/'),
                           name='accounts'),

                       url(r'^item/grid/$', grid_handler, name='grid_handler'),
                       url(r'^item/grid/cfg/$', grid_config, name='grid_config'),
                       url(r'^item/grid/crud/$', grid_crud, name='grid_crud'),
                       url(r'^grid$', grid_view, name='grid'),
                    )
