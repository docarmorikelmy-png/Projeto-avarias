from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ("avaria", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Divergencia",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tipo", models.CharField(choices=[("positivo", "Positiva"), ("negativo", "Negativa")], max_length=10)),
                ("colaborador", models.CharField(max_length=100)),
                ("local", models.CharField(max_length=100)),
                ("quantidade", models.DecimalField(decimal_places=0, max_digits=10)),
                ("data", models.DateTimeField(auto_now_add=True)),
                ("produto", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="avaria.produto")),
            ],
        ),
    ]