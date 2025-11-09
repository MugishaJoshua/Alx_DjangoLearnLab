from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from relationship_app.views import SignUpView
  # Keep if you need signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/',
         TemplateView.as_view(template_name='accounts/profile.html'),
         name='profile'),
    path('signup/', SignUpView.as_view(), name='signup'),

    # ✅ Include the app-level URLs
    path('', include('relationship_app.urls')),
]
