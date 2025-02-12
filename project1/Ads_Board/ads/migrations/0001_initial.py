# Generated by Django 5.1.1 on 2025-02-08 20:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('category', models.CharField(choices=[('tanks', 'Танки'), ('healers', 'Хилы'), ('dd', 'ДД'), ('traders', 'Торговцы'), ('guildmasters', 'Гилдмастеры'), ('questgivers', 'Квестгиверы'), ('blacksmiths', 'Кузнецы'), ('leatherworkers', 'Кожевники'), ('alchemists', 'Зельевары'), ('spellmasters', 'Мастера заклинаний')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
