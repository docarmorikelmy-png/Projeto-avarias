from django import forms
from .models import Divergencia, avarias, produto

COLABORADORES = [
    ("Samuel Kadan", "Samuel Kadan"),
    ("Sandro Soares", "Sandro Soares"),
    ("Simon Alberto", "Simon Alberto"),
    ("Victor Hugo", "Victor Hugo"),
    ("Vinicius Daniel", "Vinicius Daniel"),
    ("Weslley Leite", "Weslley Leite"),
    ("Yassel Rafael", "Yassel Rafael"),
]

class AvariaForm(forms.ModelForm):
    colaborador = forms.ChoiceField(choices=COLABORADORES, label="Colaborador")
    produto = forms.ModelChoiceField(
        queryset=produto.objects.all().order_by("nome_produto"),
        label="Produto",
        empty_label="Selecione o produto",
        widget=forms.HiddenInput(),
    )
    produto_busca = forms.CharField(
        label="Produto",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Digite o nome ou código do produto...",
            "autocomplete": "off",
            "role": "combobox",
            "aria-autocomplete": "list",
            "aria-controls": "produto-resultados",
            "aria-expanded": "false",
        }),
    )

    class Meta:
        model = avarias
        fields = ["colaborador", "produto", "descricao_avaria", "quantidade"]
        widgets = {
            "descricao_avaria": forms.Textarea(attrs={
                "rows": 4,
                "class": "form-control",
                "placeholder": "Descreva como o produto está avariado...",
            }),
            "quantidade": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["colaborador"].widget.attrs.update({"class": "form-control"})
        if self.instance and self.instance.pk:
            self.fields["produto_busca"].initial = str(self.instance.produto)

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("produto"):
            self.add_error("produto_busca", "Selecione um produto da lista de resultados.")
        return cleaned_data


class DivergenciaForm(forms.ModelForm):
    tipo = forms.CharField(widget=forms.HiddenInput())
    colaborador = forms.ChoiceField(choices=COLABORADORES, label="Colaborador")
    produto = forms.ModelChoiceField(
        queryset=produto.objects.all().order_by("nome_produto"),
        label="Produto",
        widget=forms.HiddenInput(),
    )
    produto_busca = forms.CharField(
        label="Produto",
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Digite o nome ou código do produto...",
            "autocomplete": "off",
            "role": "combobox",
            "aria-autocomplete": "list",
            "aria-controls": "produto-resultados",
            "aria-expanded": "false",
        }),
    )

    class Meta:
        model = Divergencia
        fields = ["tipo", "colaborador", "produto", "local", "quantidade"]
        widgets = {
            "local": forms.TextInput(attrs={
                "class": "form-control",
                "type": "text",
                "placeholder": "Ex.: depósito, loja ou corredor...",
            }),
            "quantidade": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["colaborador"].widget.attrs.update({"class": "form-control"})

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("produto"):
            self.add_error("produto_busca", "Selecione um produto da lista de resultados.")
        return cleaned_data