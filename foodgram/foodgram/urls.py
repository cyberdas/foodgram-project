from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

handler404 = "foodgram.views.page_not_found" # noqa
handler500 = "foodgram.views.server_error" # noqa


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('api.urls')),
    path('', include('recipes.urls')),
]


urlpatterns += [
    path('about/author/', views.flatpage, {'url': 'about/author/'}, name='about_author'),
    path('about/technologies/', views.flatpage, {'url': '/about/technologies/'}, name='technologies'),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
