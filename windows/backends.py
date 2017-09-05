from django.contrib.auth.models import User

import urllib2, urllib

def authenticate(credential, password):
	params = { 'password' : password}
	sURL = "https://beta-janus.gameloft.com/{}/authenticate?{}".format(credential, urllib.urlencode(params))
	try:
		result = urllib2.urlopen(sURL, timeout=30)
		return True
	except Exception as e:
		return False

class GLBackend(object):
    def authenticate(self, username=None, password=None):
        user_name = username[:username.find('@')]
        first_name = user_name[:user_name.find('.')]

        access_token = authenticate('ldap:'+username, password)
        if access_token == True:
            try:
                return User.objects.get(username=user_name)
            except User.DoesNotExist:
                user = User(username=user_name)
                user.set_password(User.objects.make_random_password(length=30))
                user.is_staff = True
                user.first_name = first_name
                user.email = username
                user.save()

                return user
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None