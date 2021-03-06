from django.contrib import admin
from django.urls import path
from . import views 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path("", views.MainPage, name="mainpage"),
    path("registration/", views.RegistrationView.as_view(), name="registration"),
    path("login/", views.LoginView.as_view(), name="login_to_blog"),
    path("login2/", views.login, name="login2"),
    path("profile/<int:pk>", views.ProfileView.as_view(), name="profile"),
    path("profile/edit/<int:pk>", views.EditProfileView.as_view(), name="edit_profile"),
    path("profile/delete/<int:pk>", views.DeleteProfileView.as_view(), name="delete_profile"),
    path("remove_image/<int:pk>/<int:id>", views.RemoveImage, name="remove_image"),
    path("profile/friend_list/<int:pk>", views.FriendListView.as_view(), name="friend_list"),
    path("invite/<int:pk>", views.CreateFriendRequest, name="create_friend_request"),
    path("akcept_friend_invite/<int:id>/<int:pk>", views.AkceptFriendRequest, name="akcept_firend_request"),
    path("reject_friend_invite/<int:id>/<int:pk>", views.RejectFriendRequest, name="reject_firend_request"),
    path("remove_friend/<int:id1>/<int:id2>/<int:pk1>", views.RemoveFriend, name="remove_friend"),
    path("create_chat/<int:id>", views.startchat, name="create_chat"),
    path("chat/<int:id>", views.ChatView.as_view(), name="chat"),
    path('chat/create_message', csrf_exempt(views.ChatMessageCreate.as_view()), name='create_message'),
    path('chat/get_messages', csrf_exempt(views.GetChatMessages.as_view()), name='get_messages'),
    path('all_chats', views.AllProfileChats.as_view(), name='all_chats'),
    path('auth_error', views.AuthorizationError.as_view(), name='auth_error'),
    path('find_friend', views.FindFriendView.as_view(), name='find_friend'),
    path("profile/images/<int:pk>", views.ProfileImagesView.as_view(), name="profile_images"),
    path("profile/friends/<int:pk>", views.ProfileFriendsView.as_view(), name="profile_friends"),
    path("posts", views.PostsView.as_view(), name="posts"),
    path("post/<int:pk>", views.PostView.as_view(), name="post"),
    path("delete_post/<int:pk>", views.DeletePost, name="delete_post"),
    path("report_post/<int:pk>", views.CreatePostReport, name="report_post"),
    path("change_password", views.ChangePasswordView.as_view(), name="change_password"),
    path("delete_comment/<int:pk>", views.DeleteComment, name="delete_comments"),
]

