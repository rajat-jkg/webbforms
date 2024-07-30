from django.urls import path
from . import views
urlpatterns = [
    path('addnew', views.addForm, name='addForm' ), 
    path('editform/<formId>', views.editForm, name='editForm'),
    path('webbform/<formId>' , views.webbForm ),
    path('responses/<formId>', views.responses),
    path('delete/<formId>' , views.deleteForm ),
    path('deleteresponse/<responseID>' , views.deleteResponse),
]