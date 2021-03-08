from django.contrib import admin
from .models import Profile, Post_comment, Report_Post, ProfileImage, FriendInvitation, ChatBox, ChatMessage, Post
# Register your models here.
admin.site.register(Profile)
admin.site.register(ProfileImage)
admin.site.register(FriendInvitation)
admin.site.register(ChatBox)
admin.site.register(ChatMessage)
admin.site.register(Post)
admin.site.register(Post_comment)
admin.site.register(Report_Post)