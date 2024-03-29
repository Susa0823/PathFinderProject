# Generated by Django 4.2 on 2023-04-28 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PathFinderApp', '0004_remove_userchatprompt_query_response'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('new', 'NEWEST'), ('old', 'OLDEST'), ('title', 'TITLE')], default='old', max_length=50)),
            ],
        ),
    ]
