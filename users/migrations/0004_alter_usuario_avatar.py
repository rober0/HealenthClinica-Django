# Generated by Django 5.2.3 on 2025-07-07 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_usuario_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='avatar',
            field=models.ImageField(blank=True, default='/avatars/default.png', upload_to='media/avatars'),
        ),
    ]
