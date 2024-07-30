from django.urls import path
from . import views
urlpatterns = [
    path( '' , views.docsHome , name='docshome' ),
]