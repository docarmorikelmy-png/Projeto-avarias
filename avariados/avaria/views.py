from django.db.models import Q
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import AvariaForm, DivergenciaForm
from .models import Divergencia, avarias as AvariaRecord, produto


def pagina_inicial(request):
    return render(request, "website/pagina_inicial.html")


def avarias(request):
    if request.method == "POST":
        form = AvariaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("avarias")
    else:
        form = AvariaForm()

    return render(request, "website/avarias.html", {"form": form})


def buscar_produtos(request):
    termo = request.GET.get("q", "").strip()
    if len(termo) < 2:
        return JsonResponse({"resultados": []})

    produtos = produto.objects.filter(
        Q(nome_produto__icontains=termo) |
        Q(codigo_produto__icontains=termo)
    ).order_by("nome_produto")[:20]

    return JsonResponse({
        "resultados": [
            {
                "id": item.pk,
                "nome": item.nome_produto,
                "codigo": item.codigo_produto,
                "texto": str(item),
            }
            for item in produtos
        ]
    })


def divergencia(request, tipo):
    if tipo not in {"positivo", "negativo"}:
        return redirect("pagina_inicial")

    if request.method == "POST":
        form = DivergenciaForm(request.POST)
        if form.is_valid() and form.cleaned_data["tipo"] == tipo:
            form.save()
            return redirect(tipo)
    else:
        form = DivergenciaForm(initial={"tipo": tipo})

    return render(request, "website/divergencia.html", {
        "form": form,
        "tipo": tipo,
        "titulo": "Divergência positiva" if tipo == "positivo" else "Divergência negativa",
        "descricao": "Registre onde foi encontrada a quantidade excedente." if tipo == "positivo" else "Registre onde foi identificada a falta do produto.",
    })


def positivo(request):
    return divergencia(request, "positivo")


def negativo(request):
    return divergencia(request, "negativo")


def chamados_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        if user.is_staff:
            login(request, user)
            return redirect("chamados")
        form.add_error(None, "Este usuário não tem permissão para acessar os chamados.")

    return render(request, "website/chamados_login.html", {"form": form})


@staff_member_required(login_url="/chamados/login/")
def chamados(request):
    status = request.GET.get("status", "pendentes")
    avarias_qs = AvariaRecord.objects.select_related("produto").order_by("-data")
    divergencias_qs = Divergencia.objects.select_related("produto").order_by("-data")

    if status == "pendentes":
        avarias_qs = avarias_qs.exclude(status="concluido")
        divergencias_qs = divergencias_qs.exclude(status="concluido")
    elif status in {"aberto", "andamento", "concluido"}:
        avarias_qs = avarias_qs.filter(status=status)
        divergencias_qs = divergencias_qs.filter(status=status)

    return render(request, "website/chamados.html", {
        "avarias": avarias_qs,
        "divergencias": divergencias_qs,
        "filtro_atual": status,
        "contagens": {
            "aberto": AvariaRecord.objects.filter(status="aberto").count() + Divergencia.objects.filter(status="aberto").count(),
            "andamento": AvariaRecord.objects.filter(status="andamento").count() + Divergencia.objects.filter(status="andamento").count(),
            "concluido": AvariaRecord.objects.filter(status="concluido").count() + Divergencia.objects.filter(status="concluido").count(),
        },
    })


@staff_member_required(login_url="/chamados/login/")
def atualizar_chamado(request, tipo, chamado_id):
    status = request.POST.get("status")
    if request.method == "POST" and status in {"aberto", "andamento", "concluido"}:
        modelo = AvariaRecord if tipo == "avaria" else Divergencia
        chamado = modelo.objects.get(pk=chamado_id)
        chamado.status = status
        chamado.concluido_em = timezone.now() if status == "concluido" else None
        chamado.save(update_fields=["status", "concluido_em"])
    return redirect("chamados")


@staff_member_required(login_url="/chamados/login/")
def excluir_chamado(request, tipo, chamado_id):
    if request.method == "POST":
        modelo = AvariaRecord if tipo == "avaria" else Divergencia
        chamado = modelo.objects.get(pk=chamado_id)
        if chamado.status == "concluido":
            chamado.delete()
    return redirect("chamados")
