from django.conf import settings
import debug_toolbar
from django.conf.urls.static import static 
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path("", include('core.urls', namespace="core")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
