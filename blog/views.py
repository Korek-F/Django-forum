from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from .models import Profile, Post, ProfileImage, Post_comment, FriendInvitation, ChatMessage, ChatBox, Report_Post
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm, ProfileImageForm, ReportPostForm
from django.http import JsonResponse
import json
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
# Create your views here.
def MainPage(request):
    profiles = Profile.objects.all()
    paginator = Paginator(profiles,8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'profiles':page_obj,
    }
    
    if request.user.is_authenticated:
        profile = request.user.profile
        new_friend_request = 0
        friend_requests = FriendInvitation.objects.all().filter(profile_to=profile)
        for friend_request in friend_requests:
            if friend_request.displayed == False:
                new_friend_request += 1
        context["new_friend_request"] = new_friend_request

        new_messages = 0
        profile_chats = profile.chats.all()
        for chat in profile_chats:
            for message in chat.messages.all():
                if not message.displayed:
                    if not message.owner == profile:
                        new_messages +=1
        context["new_messages"] = new_messages
    return render(request, "blog/mainpage.html",context=context)

class RegistrationView(View):
    def get(self, request):
        return render(request, "blog/registration.html")
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        birth_date = request.POST['date']
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password)<6:
                    messages.error(request,"Hasło jest za krótkie!")
                    return render(request, "blog/registration.html")
                user= User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.save() 
                profile = Profile(user=user,birth_date=birth_date)
                profile.save()
                return redirect('login_to_blog')
            messages.error(request, "Konto z tym emailem już istnieje!")
            return render(request, "blog/registration.html")
        messages.error(request, "Ta nazwa jest już zajęta!")
        return render(request, "blog/registration.html")

def login(request):
    username = request.POST['username']  
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return redirect('mainpage')
    else: 
        messages.error(request,"Błędne dane logowania.")
        return render(request, 'blog/login.html')
class LoginView(View):
    def get(self, request):
        return render(request, 'blog/login.html')
 
class ProfileView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request, pk):
        profile = Profile.objects.all().get(id=pk)
        friends_id = []
        for friend in profile.friends.all():
            friends_id.append(friend.id)
        context={
            'profile':profile,
            'friends_id':friends_id,
        }
        user1 = request.user.profile
        user2 = get_object_or_404(Profile, id=pk)
        chats = ChatBox.objects.all()
        for chat in chats:
            if user1 in chat.users.all() and user2 in chat.users.all():
                context["have_chat"]=True
                context["chat"]=chat
            else: 
                context["have_chat"]=False
        return render(request, 'blog/profile.html',context)
    def post(self, request, pk):
        user = request.user.profile
        title = request.POST["title"]
        text = request.POST["text"]
        if len(text)>0 and len(title)>0:
            post = Post(owner=user,title=title, text=text)
            post.save()
            user.posts.add(post)
            user.save()
            messages.success(request, "Twój post został dodany!")
        else:
            messages.error(request, "Twój post nie został dodany. Prawdopodobnie był pusty.")
        return redirect('profile', pk=pk)

class EditProfileView(LoginRequiredMixin,View):
    login_url = '/login/'
    def get(self, request, pk):
        profile = Profile.objects.all().get(id=pk)
        if not profile == request.user.profile:
            return redirect('auth_error')
        form = EditProfileForm(
            initial={
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'birth_date': profile.birth_date,
            'country': profile.country,
            'city': profile.city,
            'height': profile.height,
            'weight': profile.weight,
            'gender': profile.gender,
            'description': profile.description,
            })
        context = {
            "profile":profile,
            'form': form,
        }
        return render(request, 'blog/edit_profile.html',context)
    def post(self, request, pk):
        profile = Profile.objects.all().get(id=pk) 
        birth_date = request.POST["birth_date"]
        description = request.POST["description"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        country = request.POST["country"]
        city = request.POST["city"]
        dzero = 0
        height = request.POST["height"]
        height = height if height else dzero
        weight = request.POST["weight"]
        weight = weight if weight else dzero
        gender = request.POST["gender"]
        profile.birth_date = birth_date
        profile.description = description
        profile.first_name = first_name
        profile.last_name = last_name
        profile.country = country
        profile.city = city
        profile.height = height
        profile.weight = weight
        profile.gender = gender
        profile.save()
        messages.success(request, "Profil został pomyślnie zedytowany!")
        return redirect('profile', pk=pk)

def RemoveImage(request, pk, id):
    image = get_object_or_404(ProfileImage, id=pk)
    profile_id = id
    image.delete()
    return redirect('profile_images', pk=profile_id)

class FriendListView(View):
    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        if not profile == request.user.profile:
            return redirect('auth_error')
        friend_requests = FriendInvitation.objects.all().filter(profile_to=profile)
        for friend_request in friend_requests:
            friend_request.displayed = True
        friends_id = []
        for friend in profile.friends.all():
            friends_id.append(friend.id)
        context={
            'profile':profile,
            'friend_requests':friend_requests,
            'friends_id':friends_id,
        }
        
        return render(request, 'blog/friends_list.html', context)

def CreateFriendRequest(request, pk):
    profile_from = request.user.profile
    profile_to = get_object_or_404(Profile, id=pk)
    profile_id = pk
    f_request = FriendInvitation(profile_from=profile_from, profile_to=profile_to)
    f_request.save()
    messages.success(request, "Wysłano zaproszenie do znajomych.")
    return redirect('profile', pk=profile_id)

def AkceptFriendRequest(request, id, pk):
    friend_request = get_object_or_404(FriendInvitation,id=id)
    user1 = get_object_or_404(Profile,id=friend_request.profile_from.id)
    user2 = get_object_or_404(Profile,id=friend_request.profile_to.id)
    if not user2 in user1.friends.all():
        user1.friends.add(user2)
        messages.success(request, "Użytkownik został dodany do listy znajomych.")
    friend_request.delete()
    profile_id = pk
    return redirect('friend_list', pk=profile_id)

def RejectFriendRequest(request, id, pk):
    friend_request = get_object_or_404(FriendInvitation,id=id)
    user1 = get_object_or_404(Profile,id=friend_request.profile_from.id)
    user2 = get_object_or_404(Profile,id=friend_request.profile_to.id)
    friend_request.delete()
    profile_id = pk
    messages.success(request, "Zaproszenie do znajomych zostało odrzucone.")
    return redirect('friend_list', pk=profile_id)

def RemoveFriend(request, id1,id2,pk1):
    profile_from = get_object_or_404(Profile, id=id1)
    profile_to = get_object_or_404(Profile, id=id2)
    profile_id = pk1
    profile_to.friends.remove(profile_from)
    profile_to.save()
    messages.success(request, "Użytkownik został usunięty z listy znajomych.")
    return redirect('profile', pk=profile_id)

def startchat(request, id):
    user1 = request.user.profile
    user2 = get_object_or_404(Profile, id=id)
    chats = ChatBox.objects.all()
    for chat in chats:
        if user1 in chat.users.all() and user2 in chat.users.all():
            return redirect('chat', id=chat.id)
    
    new_chat= ChatBox()
    new_chat.save()
    new_chat.users.add(user1)
    new_chat.save()
    new_chat.users.add(user2)
    new_chat.save()
    user1.chats.add(new_chat)
    user1.save()
    user2.chats.add(new_chat)
    user2.save()
    return redirect('chat', id=new_chat.id)

class ChatView(View):
    def get(self, request, id):
        context={}
        user = request.user.profile
        if ChatBox.objects.all().filter(id=id).exists():
            chat = ChatBox.objects.all().get(id=id)
            context["chat"] = chat
            for user_x in chat.users.all():
                if not user_x == user:
                    context["second_user"] = user_x
                else:
                    context["first_user"] = user_x

            if not user in chat.users.all():
                context["error"]=True
                return render(request, "blog/chat.html", context)
        else:
            return redirect('auth_error')
        return render(request, "blog/chat.html", context)

class DeleteProfileView(View):
    def get(self, request, pk):
        profile = Profile.objects.all().get(id=pk)
        if not profile == request.user.profile:
            return redirect('auth_error')
        context={
            'profile':profile,
        }
        return render(request, "blog/deleteaccount.html", context)

    def post(self, request, pk):
        current_user = request.user
        password = request.POST["password"]
        profile = Profile.objects.all().get(id=pk)
        context={
            'profile':profile,
        }
        if not profile == request.user.profile:
            return redirect('auth_error')
        if not current_user.check_password(password):
            context["message"] = "złe hasło"
            print(profile.user.password)
            return render(request, "blog/deleteaccount.html", context)
        current_user.profile.delete()
        current_user.delete()
        return redirect('mainpage')
from django.utils import timezone


class ChatMessageCreate(View):
    def post(self, request):
        data = json.loads(request.body)
        chat_id = data["chat_id"]
        owner_id = data["owner_id"]
        content = data["content"]
        now = timezone.now()  
        owner = Profile.objects.all().get(id=owner_id)
        chat = ChatBox.objects.all().get(id=chat_id)
        chat.last_message_date = now
        m = ChatMessage(content=content, owner=owner)
        m.save()
        chat.messages.add(m)
        chat.save()
        return JsonResponse(list("ok"),safe=False)

class GetChatMessages(View):
    def post(self,request):
        data = json.loads(request.body)
        chat_id = data["chat_id"]
        profile_id = data["user_id"]
        profile = Profile.objects.all().get(id=profile_id)
        
        chat = ChatBox.objects.all().get(id=chat_id)
        messages = chat.messages.all().order_by("date").reverse()[:20]
        data = messages.values()
        
        for message in chat.messages.all():
            if not message.owner == profile:
                if message.displayed == False:
                    message.displayed=True
                    message.save()
        return JsonResponse(list(data), safe=False)

class AllProfileChats(View):
    def get(self, request):
        context={}
        current_user = request.user.profile
        if not current_user == request.user.profile:
            return redirect('auth_error')
        context["chats"] =  current_user.chats.all().order_by("-last_message_date")
        return render(request,"blog/all_chats.html", context)

class AuthorizationError(View):
    def get(self, request):
        return render(request,"blog/autherror.html")

class FindFriendView(View):
    def get(self,request):
        return render(request, "blog/find_friend.html")
    def post(self, request):
        name = request.POST["name"]
        lastname = request.POST["surname"]
        nickname = request.POST["nickname"]
        profileid = request.POST["profileid"]
        profiles = Profile.objects.all()
        context={
            'fieldValues': request.POST
        }
        lookup_error = "Niestety nie znaleźliśmy osoby którą szukasz. Sprawdz czy poprawnie wpisałeś dane."
        if name:
            profiles = profiles.filter(first_name__contains=str(name))
            if not profiles:
                context["lookup_error"] = lookup_error
                return render(request, "blog/find_friend.html",context)
        if lastname:
            profiles = profiles.filter(last_name__contains=str(lastname))
            if not profiles:
                context["lookup_error"] = lookup_error
                return render(request, "blog/find_friend.html",context)
        if nickname:
            profiles = profiles.filter(user__username__contains=str(nickname))
            if not profiles:
                context["lookup_error"] = lookup_error
                return render(request, "blog/find_friend.html",context)
        if profileid:
            profiles = profiles.filter(pk=profileid)
            if not profiles:
                context["lookup_error"] = lookup_error
                return render(request, "blog/find_friend.html", context)

        context["profiles"]=profiles

        return render(request, "blog/find_friend.html", context)

class ProfileImagesView(View):
    def get(self,request, pk):
        profile = Profile.objects.all().get(id=pk)
        form = ProfileImageForm(request.POST, request.FILES) 
        context={
            "profile":profile,
            "form":form,
        }
        return render(request, "blog/profile_images.html", context)
    def post(self, request, pk):
        try:
            image = request.FILES["image"]
            profile = Profile.objects.all().get(id=pk)
            user = profile.user
            profile_image = ProfileImage(profile=user,image=image)
            profile_image.save()
            profile.images.add(profile_image)
            profile.save()
            return redirect('profile_images', pk=pk)
        except:
            return redirect('profile_images', pk=pk)

class ProfileFriendsView(View):
    def get(self, request, pk):
        profile = Profile.objects.all().get(id=pk)
        context={
            "profile": profile,
        }
        return render(request, "blog/profile_friends.html", context)

class PostsView(View):
    def get(self, request):
        user = request.user.profile
        posts= []
        def myFunc(e):
            e.date_time
            return e.date_time

        for friend in user.friends.all():
            for post in friend.posts.all():
                posts.append(post)
        posts.sort(reverse=True, key=myFunc)  
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
        context={
            'profile':user,
            'posts':posts,
        }
        return render(request, "blog/posts.html", context)
    def post(self, request):
        user = request.user.profile
        posts= []
        title = request.POST["title"]
        title2 = request.POST["title2"]

        print(title2)
        def myFunc(e):
            e.date_time
            return e.date_time

        if title2 == "text":
            for friend in user.friends.all():
                for post in friend.posts.filter(Q(text__contains=str(title))):
                    posts.append(post)
        else: 
            for friend in user.friends.all():
                for post in friend.posts.filter(Q(title__contains=str(title))):
                    posts.append(post)
        posts.sort(reverse=True, key=myFunc)  
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
        context={
            'profile':user,
            'posts':posts,
        }
        print(posts)
        return render(request, "blog/posts.html", context)

class PostView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        form = ReportPostForm()
        context={
            'post':post,
            'form':form,
        }
        return render(request, "blog/post.html", context)
    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        user = request.user.profile
        text = request.POST["comment"]
        if len(text)>0 and len(text)<2000:
            comment = Post_comment(owner=user, text=text, post=post)
            comment.save()
            post.comments.add(comment)
            post.save()
        return redirect('post', pk=pk)

def DeleteComment(request, pk):
    comment = get_object_or_404(Post_comment,id=pk)
    post = comment.post
    comment_author = comment.owner
    user = request.user.profile
    if user == comment_author or user == post.owner:
        comment.delete()
        return redirect('post', pk=post.id)
    else:
        return redirect('auth_error')

def DeletePost(request, pk):
    post = get_object_or_404(Post,id=pk)
    post.delete()
    messages.success(request, "Post został usunięty")
    return redirect('posts')

def CreatePostReport(request, pk):
    post = Post.objects.get(id=pk)

    if Report_Post.objects.filter(post=post).exists():
        messages.success(request,"Post został zgłoszony!")
        return redirect('post', pk)
    else: 
        messages.success(request,"Post został zgłoszony!")
        report_type = request.POST["report_type"]
        report = Report_Post.objects.create(post=post,report_type=report_type)
        report.save()
        return redirect('post', pk)



from .forms import ResetPassword
from django.contrib.auth import update_session_auth_hash
class ChangePasswordView(View):
    def get(self, request):
        form  = ResetPassword(request.user)
        return render(request, "blog/change_password.html",{"form":form})
    def post(self, request):
        form = ResetPassword(request.user,request.POST)
        if form.is_valid():
            user = request.user
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Hasło zmienione pomyślnie")
            return redirect("change_password")
        else:
            print(form.errors)
            messages.error(request, "Błąd")
            return render(request, "blog/change_password.html",{"form":form})

