from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from relationship_app.views import SignUpView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/',
         TemplateView.as_view(template_name='accounts/profile.html'),
         name='profile'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', include('relationship_app.urls')),
]

# IMPORTANT: serve static files even when DEBUG=False
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)