from django.db import models
from django.contrib.auth.models import User
from django.forms import ImageField

# Create your models here.


# Any time you make a change to your models (adding a field, deleting a model, etc.), you’ll need to make and run new migrations.
# to do so run `python manage.py makemigrations PathFinderAPP`
class User(models.Model):
    # user_id = models.AutoField(primary_key=True)
    username = models.CharField(User, max_length=50)
    user_password = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50)
    user_address = models.CharField(max_length=50)
    user_country = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.username

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


#For Blog
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# create meep model
class Meep(models.Model):
	user = models.ForeignKey(
		User, related_name="meeps", 
		on_delete=models.DO_NOTHING
		)
	body = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	likes = models.ManyToManyField(User, related_name="meep_like", blank=True)


	# Keep track or count of likes
	def number_of_likes(self):
		return self.likes.count()



	def __str__(self):
		return(
			f"{self.user} "
			f"({self.created_at:%Y-%m-%d %H:%M}): "
			f"{self.body}..."
			)


# Create A User Profile Model
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	follows = models.ManyToManyField("self", 
		related_name="followed_by",
		symmetrical=False,
		blank=True)	
	
	date_modified = models.DateTimeField(User, auto_now=True)	
	profile_image = models.ImageField(null=True, blank=True, upload_to="img/")

	
	def __str__(self):
		return self.user.username

# Create Profile When New User Signs Up
#@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		user_profile = Profile(user=instance)
		user_profile.save()
		# Have the user follow themselves
		user_profile.follows.set([instance.profile.id])
		user_profile.save()

post_save.connect(create_profile, sender=User)
