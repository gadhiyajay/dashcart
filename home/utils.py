from users.models import Profile

def is_seller(user):
    return user.is_authenticated and Profile.user_type == 'seller'