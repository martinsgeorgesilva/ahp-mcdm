from django.contrib import admin
from django.urls import path, include
from groups.views import AjaxPostView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('criterion.urls', namespace='home')),
    path('criterion/', include('criterion.urls', namespace='criterion')),
    path('user/', include('user.urls', namespace='user')),
    path('groups/', include('groups.urls', namespace='groups')),
    path('research/', include('research.urls', namespace='research')),
    path('ajax-post', AjaxPostView, name='ajax-post'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)







# auth/login/ [name='login']
# auth/logout/ [name='logout']
# auth/password_change/ [name='password_change']
# auth/password_change/done/ [name='password_change_done']
# auth/password_reset/ [name='password_reset']
# auth/password_reset/done/ [name='password_reset_done']
# auth/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# auth/reset/done/ [name='password_reset_complete']