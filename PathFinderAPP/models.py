from django.db import models

# Create your models here.


# Any time you make a change to your models (adding a field, deleting a model, etc.), you’ll need to make and run new migrations.
# to do so run `python manage.py makemigrations PathFinderAPP`
class User(models.Model):
    # user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    user_password = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50)
    user_address = models.CharField(max_length=50)
    user_country = models.CharField(max_length=50)
