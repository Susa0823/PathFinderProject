from django.db import models
from django.forms import ImageField

# Create your models here.


# Any time you make a change to your models (adding a field, deleting a model, etc.), you’ll need to make and run new migrations.
# to do so run `python manage.py makemigrations PathFinderAPP`
class User(models.Model):
    # user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    user_password = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50)
    user_address = models.CharField(max_length=50)
    user_country = models.CharField(max_length=50)

    USERNAME_FIELD = 'username'
    def save(self, *args, **kwargs):
        super().save()

        img = ImageField.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

class UserChatPrompt(models.Model):
    # query_id = models.AutoField(primary_key=True)
    # need to figure out how to get user model after authentication
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    query = models.CharField(max_length=1000)
    # query_response = models.CharField(max_length=1000)
    # query_date = models.DateField()
    # query_time = models.TimeField()


class Notes(models.Model):
    STATUS = (
        ("new", "NEWEST"),
        ("old", "OLDEST"),
        ("title", "TITLE"),
    )
    heading = models.CharField(max_length=200)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS, default="old")
    def __str__(self):
        return self.heading
