from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView  # 👈 Add this

urlpatterns = [
    path('admin/', admin.site.urls),
    path('help-me-find-doctor/', include('helpmefind.urls')),
    path('', RedirectView.as_view(url='/help-me-find-doctor/', permanent=False)),  # 👈 Redirect root to app
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
