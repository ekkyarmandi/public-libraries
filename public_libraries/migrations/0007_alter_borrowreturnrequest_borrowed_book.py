# Generated by Django 4.2.1 on 2023-06-05 03:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public_libraries', '0006_borrowreturnrequest_is_rejected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowreturnrequest',
            name='borrowed_book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='public_libraries.borrowedbook'),
        ),
    ]