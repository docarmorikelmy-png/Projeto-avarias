from django.contrib import admin
from django.utils import timezone

from .models import Divergencia, avarias, produto


def marcar_andamento(modeladmin, request, queryset):
	queryset.update(status="andamento", concluido_em=None)


marcar_andamento.short_description = "Marcar chamados como em andamento"


def concluir_chamados(modeladmin, request, queryset):
	queryset.update(status="concluido", concluido_em=timezone.now())


concluir_chamados.short_description = "Concluir chamados selecionados"


def reabrir_chamados(modeladmin, request, queryset):
	queryset.update(status="aberto", concluido_em=None)


reabrir_chamados.short_description = "Reabrir chamados selecionados"


class ChamadoAdminMixin:
	list_display = ("status", "produto", "colaborador", "quantidade", "data", "concluido_em")
	list_filter = ("status", "data", "concluido_em")
	actions = (marcar_andamento, concluir_chamados, reabrir_chamados)
	ordering = ("status", "-data")

	def get_queryset(self, request):
		queryset = super().get_queryset(request)
		if "status" not in request.GET:
			queryset = queryset.exclude(status="concluido")
		return queryset

	def save_model(self, request, obj, form, change):
		if obj.status == "concluido" and not obj.concluido_em:
			obj.concluido_em = timezone.now()
		elif obj.status != "concluido":
			obj.concluido_em = None
		super().save_model(request, obj, form, change)


@admin.register(Divergencia)
class DivergenciaAdmin(ChamadoAdminMixin, admin.ModelAdmin):
	list_display = ("status", "tipo", "produto", "colaborador", "local", "quantidade", "data", "concluido_em")
	list_filter = ("status", "tipo", "local", "data")
	search_fields = ("produto__nome_produto", "produto__codigo_produto", "colaborador", "local")


@admin.register(avarias)
class AvariaAdmin(ChamadoAdminMixin, admin.ModelAdmin):
	search_fields = ("produto__nome_produto", "produto__codigo_produto", "colaborador", "descricao_avaria")


admin.site.register(produto)

# Register your models here.
