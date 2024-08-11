
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

admin.site.site_header = "TRENDIFY"
admin.site.site_title = "ADMIN"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("api.urls")),
    path('auth/', include("authentication.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
