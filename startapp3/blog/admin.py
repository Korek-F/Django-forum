from django.contrib import admin
from .models import Profile, ProfileImage, FriendInvitation, ChatBox, ChatMessage
# Register your models here.
admin.site.register(Profile)
admin.site.register(ProfileImage)
admin.site.register(FriendInvitation)
admin.site.register(ChatBox)
admin.site.register(ChatMessage)