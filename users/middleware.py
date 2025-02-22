
from django.contrib.auth import login    
from django.utils.deprecation import MiddlewareMixin 

class PreserveSessionMiddleware(MiddlewareMixin):
    def Process_request(self, request):
        if request.user.is_authenticated:
        #     request.session['user_id'] = request.user.id
        #     request.session['username'] = request.user.username
        #     request.session['email'] = request.user.email
        #     request.session['is_staff'] = request.user.is_staff
        #     request.session['is_superuser'] = request.user.is_superuser
        # return None
            login(request, request.user)