# Generated by Django 4.2.1 on 2023-05-16 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lokikirja_app', '0003_alter_logbook_user_logentry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logbook',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='logbook',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='log_entries', to='lokikirja_app.logbook'),
        ),
    ]