# Generated by Django 4.2 on 2023-05-02 15:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='pharmacy',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='appointments.pharmacy'),
        ),
    ]