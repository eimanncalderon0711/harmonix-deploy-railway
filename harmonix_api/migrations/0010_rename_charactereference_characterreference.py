# Generated by Django 5.1.1 on 2024-12-17 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('harmonix_api', '0009_rename_attestor_accountverification_character_references'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CharacteReference',
            new_name='CharacterReference',
        ),
    ]
