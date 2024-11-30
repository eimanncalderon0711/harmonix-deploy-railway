# Generated by Django 5.1.1 on 2024-11-27 02:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_name', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('canceled', 'Canceled'), ('inprogress', 'Inprogress'), ('done', 'Done')], db_index=True, default='pending', max_length=20)),
                ('request_time', models.DateTimeField(auto_now_add=True)),
                ('schedule_time', models.DateTimeField(blank=True, null=True)),
                ('schedule_date', models.DateTimeField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypeOfService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_rating', models.FloatField(default=0)),
                ('avg_qualityOfWork', models.FloatField(default=0)),
                ('avg_affordability', models.FloatField(default=0)),
                ('avg_punctuality', models.FloatField(default=0)),
                ('avg_professionalism', models.FloatField(default=0)),
                ('total_reviews', models.IntegerField(default=0)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='harmonix_api.booking')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualityOfWork', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=3)),
                ('affordability', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=3)),
                ('punctuality', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=3)),
                ('professionalism', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=3)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='harmonix_api.review')),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='portfolio_pics/')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolios', to='harmonix_api.services')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='harmonix_api.services'),
        ),
        migrations.AddField(
            model_name='services',
            name='TypeOfService',
            field=models.ManyToManyField(related_name='services', to='harmonix_api.typeofservice'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='harmonix_api.address')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='harmonix_api.location')),
                ('TypeOfService', models.ManyToManyField(related_name='tasks', to='harmonix_api.typeofservice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='harmonix_api.user')),
            ],
        ),
        migrations.AddField(
            model_name='services',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='harmonix_api.user'),
        ),
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='harmonix_api.user'),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('decline', 'Declined'), ('accepted', 'Accepted')], db_index=True, default='pending', max_length=20)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request', to='harmonix_api.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request', to='harmonix_api.user')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='harmonix_api.user'),
        ),
    ]
