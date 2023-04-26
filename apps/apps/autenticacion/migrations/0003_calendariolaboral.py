# Generated by Django 4.2 on 2023-04-19 23:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacion', '0002_noticia'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarioLaboral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('horario_inicio', models.TimeField()),
                ('horario_fin', models.TimeField()),
                ('dia_libre', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]