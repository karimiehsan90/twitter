from django.db import models
from django.contrib.auth.models import User
class Photo(models.Model):
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.location

class Location(models.Model):
    text = models.CharField(max_length=20)

    def __str__(self):
        return self.text

class Phone(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return str(self.number)

class Gender(models.Model):
    text = models.CharField(max_length=6,primary_key=True)

    def __str__(self):
        return self.text

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bio = models.CharField(max_length=70, null=True,blank=True)
    name = models.CharField(max_length=20)
    location = models.ForeignKey(Location,on_delete=models.CASCADE,null=True,blank=True)
    phone = models.ForeignKey(Phone,on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender,on_delete=models.CASCADE,null=True)
    time = models.DateTimeField(auto_now=True)

    def json(self):
        s = '{ "id" : ' + str(self.id) + ',"username" : '
        s += '"' + self.user.username + '"'
        s += ' , "email" : '
        s += '"' + self.user.email + '"'
        s += ' , "name" : '
        s += '"' + str(self.name) + '"'
        if self.location:
            s += ' , "location" : ' + '"' + self.location.text + '"'
        s += ' , "gender" : ' + '"' + self.gender.text + '"' + '}'
        return s

    def __str__(self):
        return self.user.username

class Post(models.Model):
    text = models.CharField(max_length=100)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    forward = models.ForeignKey('Post',on_delete=models.DO_NOTHING,null=True,blank=True)
    pic = models.ForeignKey(Photo,on_delete=models.DO_NOTHING,null=True,blank=True)
    def json(self):
        s = '{ "id" : ' + str(self.id) + ', "text" : ' + '"' + str(self.text) + '" , "user" : ' + self.user.json()
        if self.forward:
            s += ', "forward" : ' + str(self.forward.id)
        if self.pic:
            s += ', "pic" : ' + str(self.pic.location)
        return s + ' }'
    def __str__(self):
        return self.text

class Hashtag(models.Model):
    text = models.CharField(max_length=20)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    def json(self):
        return '{ "post" : ' + str(self.post.id) + ' , "user" : ' + str(self.user.id) + ' }'

class Comment(models.Model):
    text = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def json(self):
        return '{ "text" : "' + str(self.text) + '" , "post" : ' + str(self.post.id) + ' , "user" : ' + str(self.user.id) + ' }'

    def __str__(self):
        return self.text

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)

class FollowingFollower(models.Model):
    follower = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='follower')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='following')

class Chat(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    photo = models.ForeignKey(Photo,on_delete=models.DO_NOTHING,null=True,blank=True)
    creator = models.ForeignKey(Profile,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title

class ChatMember(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.user.username + ' ' + self.chat.title

class Message(models.Model):
    text = models.TextField()
    photo = models.ForeignKey(Photo,on_delete=models.DO_NOTHING,null=True,blank=True)
    user = models.ForeignKey(Profile,on_delete=models.DO_NOTHING)
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE)

    def __str__(self):
        return self.text