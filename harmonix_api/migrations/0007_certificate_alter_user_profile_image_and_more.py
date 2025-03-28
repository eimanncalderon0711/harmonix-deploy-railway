# Generated by Django 5.1.1 on 2024-12-16 10:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('harmonix_api', '0006_alter_user_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate', models.ImageField(upload_to='certificate_pics/')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
        migrations.CreateModel(
            name='AccountVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_id', models.ImageField(upload_to='credential_pics/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='harmonix_api.user')),
                ('certificate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='harmonix_api.certificate')),
            ],
        ),
    ]
