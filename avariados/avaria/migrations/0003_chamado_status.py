from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("avaria", "0002_divergencia"),
    ]

    operations = [
        migrations.AddField(
            model_name="avarias",
            name="concluido_em",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="avarias",
            name="status",
            field=models.CharField(choices=[("aberto", "Em aberto"), ("andamento", "Em andamento"), ("concluido", "Concluído")], default="aberto", max_length=10),
        ),
        migrations.AddField(
            model_name="divergencia",
            name="concluido_em",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="divergencia",
            name="status",
            field=models.CharField(choices=[("aberto", "Em aberto"), ("andamento", "Em andamento"), ("concluido", "Concluído")], default="aberto", max_length=10),
        ),
    ]