# Generated by Django 4.1.6 on 2023-02-08 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_alter_userbasicdetails_salary"),
    ]

    operations = [
        migrations.AlterField(
            model_name="useradditionaldetail",
            name="profile_photo",
            field=models.ImageField(
                default="default_profile_pic.png", null=True, upload_to="userprofile"
            ),
        ),
    ]
