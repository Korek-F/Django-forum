from django.db import models
from django.contrib.auth.models import User


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
    posts = models.ManyToManyField("Post", related_name='+',blank=True)
    def get_age(self):
        import datetime
        age = int((datetime.date.today() - self.birth_date).days/365.25)
        return age
    def get_name(self):
        if self.first_name and self.last_name:
            return str(str(self.first_name)+" "+str(self.last_name)) #+" ("+str(self.user.username)+")"
        elif self.first_name:
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
    date = models.DateTimeField(auto_now_add=True)
    chat = models.ManyToManyField("ChatBox", related_name='+')
    displayed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.owner.get_name())+ ": " +str(self.content)

class ChatBox(models.Model):
    date = models.DateField(auto_now_add=True)
    messages = models.ManyToManyField("ChatMessage", related_name='+', blank=True)
    users = models.ManyToManyField("Profile", related_name='+',blank=True)
    last_message_date = models.DateTimeField(blank=True)
    def __str__(self):
        chat_name = " "
        for user in self.users.all():
            chat_name += str(user.user.username)
        return str(chat_name)
    
    def get_last_message(self):
        last_message = self.messages.all().latest("date")
        return last_message
        

class Post(models.Model):
    owner =  models.ForeignKey("Profile", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    date_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=4000)
    comments = models.ManyToManyField("Post_comment", related_name='+')

    class Meta: 
        ordering = ["-date","-date_time"]

    def __str__(self):
        return str(self.title)

class Post_comment(models.Model):
    owner =  models.ForeignKey("Profile", on_delete=models.CASCADE)
    post =  models.ForeignKey("Post", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    date_time = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=2000)
    
    class Meta: 
        ordering = ["-date","-date_time"]
        
    def __str__(self):
        return str(self.text)

class Report_Post(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    post =  models.ForeignKey("Post", on_delete=models.CASCADE)
    REPORT_TYPE=[
        ("N","Nagość"),
        ("T","Obraźliwa treść"),
        ("S","Spam"),
        ("I","Inne"),
    ]
    report_type = models.CharField(max_length=2, choices=REPORT_TYPE, default="T")

    def __str__(self):
        return str(self.report_type)+" "+str(self.post) 
    