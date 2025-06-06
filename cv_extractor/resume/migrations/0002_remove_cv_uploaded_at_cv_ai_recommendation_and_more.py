# Generated by Django 5.1.3 on 2024-11-16 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cv',
            name='uploaded_at',
        ),
        migrations.AddField(
            model_name='cv',
            name='ai_recommendation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cv',
            name='doctor_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cv',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='cv',
            name='extracted_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cv',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cv',
            name='university',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='cv',
            name='cv_file',
            field=models.FileField(upload_to='cv_files/'),
        ),
    ]
