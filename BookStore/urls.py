
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/', include('Store.urls', namespace='Store')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('Account.urls', namespace='Account')),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
