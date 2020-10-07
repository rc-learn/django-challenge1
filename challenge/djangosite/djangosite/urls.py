"""djangosite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from weather import views
from note.views import notepad, del_note
from weathernote.views import homepage, d_note

urlpatterns = [
    path('admin/', admin.site.urls),
	path('weather', views.whome, name='whome'),   
	path('notes', notepad, name='notepad'),
	path('del_note/<int:noteid>/', del_note, name='del_note'),
	path('d_note/<int:noteid>/', d_note, name='d_note'),
	path('wenotes', homepage, name='homepage'),
	path('', homepage, name='homepage'), 
]

	#
	#'' makes it the homepage