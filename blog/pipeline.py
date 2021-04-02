from .models import Profile

def save_profile(backend, user, response, *args, **kwargs):
    if Profile.objects.filter(user_id=user.id).count() == 0 :
        profile = Profile(user=user)
        profile.save()