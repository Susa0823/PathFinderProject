# Generated by Django 4.1.7 on 2023-04-25 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("PathFinderApp", "0002_rename_user_name_user_username_userchatprompt"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userchatprompt",
            name="query_date",
        ),
        migrations.RemoveField(
            model_name="userchatprompt",
            name="query_time",
        ),
        migrations.AlterField(
            model_name="userchatprompt",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="PathFinderApp.user",
            ),
        ),
    ]