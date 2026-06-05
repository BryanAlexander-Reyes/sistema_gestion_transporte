# Generated manually for Auditoría de registros

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        # Auditoría de registros
        migrations.CreateModel(
            name='AuditoriaRegistro',
            fields=[
                ('id_auditoria', models.AutoField(primary_key=True, serialize=False)),
                ('modelo', models.CharField(max_length=100)),
                ('registro_id', models.CharField(blank=True, max_length=100, null=True)),
                ('accion', models.CharField(max_length=50)),
                ('metodo', models.CharField(max_length=10)),
                ('ruta', models.CharField(max_length=255)),
                ('datos_anteriores', models.JSONField(blank=True, null=True)),
                ('datos_nuevos', models.JSONField(blank=True, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                (
                    'usuario',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    )
                ),
            ],
            options={
                'db_table': 'auditoria_registro',
                'ordering': ['-fecha'],
            },
        ),
    ]
