from mongoengine import *
import datetime

class User(Document):
    username = StringField(max_length=50, required=True)
    email = EmailField(required=True)
    encrypted_password = StringField(max_length=80)#use default encryption algorithm in Django
    registration_date = DateTimeField(default=datetime.datetime.now)
    
    @classmethod
    def get_user(cls, username):
        user = cls.objects.filter(username=username)
        return user[0] if len(user) == 1 else None
    
    @classmethod
    def user2json(cls, user):
        obj = {}
        if user.username:
            obj['username'] = user.username
        if user.email:
            obj['email'] = user.email
        if user.encrypted_password:
            obj['encrypted_password'] = user.encrypted_password
        #TODO: Datetime
        return obj