# Generated by Django 5.1.1 on 2024-12-17 01:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('harmonix_api', '0008_charactereference_accountverification_status_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accountverification',
            old_name='attestor',
            new_name='character_references',
        ),
    ]
