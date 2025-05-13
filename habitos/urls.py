from django.urls import path
from .views import index, HabitoListView, HabitoCreateView, HabitoDetailView, HabitoUpdateView, HabitoDeleteView
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('registro/', views.registrar, name='registro'),
    path('habito/', HabitoListView.as_view(), name='listar-habito'),
    path('novo/', HabitoCreateView.as_view(), name='criar-habito'),
    path('<int:pk>/', HabitoDetailView.as_view(), name='detalhe-habito'),
    path('habitos/<int:pk>/editar/', HabitoUpdateView.as_view(), name='editar-habito'),
    path('habitos/<int:pk>/excluir/', HabitoDeleteView.as_view(), name='excluir-habito'),
    path('habitos/<int:pk>/confirmar_exclusao/', HabitoDeleteView.as_view(), name='confirmar_exclusao'), 

]