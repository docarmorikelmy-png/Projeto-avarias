from django.contrib import admin
from django.urls import path
from avaria import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.pagina_inicial, name='pagina_inicial'),
    path('avarias/', views.avarias, name='avarias'),
    path('api/produtos/', views.buscar_produtos, name='buscar_produtos'),
    path('positivo/', views.positivo, name='positivo'),
    path('negativo/', views.negativo, name='negativo'),
    path('chamados/', views.chamados, name='chamados'),
    path('chamados/login/', views.chamados_login, name='chamados_login'),
    path('chamados/<str:tipo>/<int:chamado_id>/status/', views.atualizar_chamado, name='atualizar_chamado'),
    path('chamados/<str:tipo>/<int:chamado_id>/excluir/', views.excluir_chamado, name='excluir_chamado'),
    path('divergencia/<str:tipo>/', views.divergencia, name='divergencia'),

]
