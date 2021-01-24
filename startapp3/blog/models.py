from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProfileImage(models.Model):
    profile = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="images/user_images/")
    add_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return (self.profile.username + " "+str(self.add_date))
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    first_name = models.CharField(blank=True, null=True, max_length=40)
    last_name = models.CharField(blank=True, null=True, max_length=40)
    country = models.CharField(blank=True, null=True, max_length=40)
    city = models.CharField(blank=True, null=True, max_length=40)
    height = models.DecimalField(blank=True,null=True, decimal_places=0, max_digits=120)
    weight = models.DecimalField(blank=True,null=True, decimal_places=0, max_digits=120)
    gender = models.CharField(blank=True,null=True, max_length=222)
    friends = models.ManyToManyField('self', blank=True)
    images = models.ManyToManyField("ProfileImage", related_name='+',blank=True)
    chats = models.ManyToManyField("ChatBox", related_name='+',blank=True)
    def get_age(self):
        import datetime
        age = int((datetime.date.today() - self.birth_date).days/365.25)
        return age
    def get_name(self):
        if self.first_name:
            return self.first_name
        else: 
            return self.user.username
    def __str__(self):
        return str(self.user.username)

class FriendInvitation(models.Model):
    profile_from = models.ForeignKey(Profile, related_name='+', null=True,on_delete=models.CASCADE)
    profile_to = models.ForeignKey(Profile,related_name='+' , null=True, on_delete=models.CASCADE)
    displayed = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

class ChatMessage(models.Model):
    content = models.CharField(max_length=300)
    owner = models.ForeignKey(Profile, related_name='+', null=True,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    chat = models.ManyToManyField("ChatBox", related_name='+')
    displayed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.owner)+ " " +str(self.content)

class ChatBox(models.Model):
    date = models.DateField(auto_now_add=True)
    messages = models.ManyToManyField("ChatMessage", related_name='+', blank=True)
    users = models.ManyToManyField("Profile", related_name='+',blank=True)
    def __str__(self):
        chat_name = " "
        for user in self.users.all():
            chat_name += str(user.user.username)
        return str(chat_name)

