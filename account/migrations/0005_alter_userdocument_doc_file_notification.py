# Generated by Django 4.1.6 on 2023-02-17 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0004_alter_previousorganisationdetail_experience_in_years_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdocument',
            name='doc_file',
            field=models.FileField(upload_to='userdocs'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('description', models.TextField(null=True)),
                ('notification_date', models.DateField(auto_now_add=True)),
                ('notification_time', models.TimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('emp_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
