#main urls
from django.contrib import admin
from django.urls import path, include
admin.site.site_header =  "EyeQ" 
admin.site.site_title =  "VC Techno Solutions" 
admin.site.index_title = "Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('account.urls')),
]
