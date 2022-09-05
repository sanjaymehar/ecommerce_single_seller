"""applesite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from apple import views
from apple import views as v


from django.conf.urls.static import static
from django.conf import settings

app_name='apple'
app_name='customer'
urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("categorylove/",views.categorypage,name='categorypage'),
    path("product/<int:pk>",views.product,name='product'),
    
    path('',include('apple.controller')),
    path("okay/",include('customer.controller')),
    
]

urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

