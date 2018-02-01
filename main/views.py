from django.shortcuts import render,redirect
import json
import math
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from .uploader import *
import re
from .models import *
POSTS_PER_PAGE = 10
def forApi(request,format):
    if (not request.user.is_authenticated) and format == 'json':
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        u = authenticate(request,username=username,password=password)
        if u:
            login(request,u)
            return None
        else:
            return HttpResponse('{ "ok" : "false" , "error" : "you are not logged in" }')
def register(request):
    format = request.GET.get('format','html')
    if format != 'html' and format != 'json':
        return HttpResponse('Unknown format')
    if request.method == 'GET':
        if format == 'html':
            return render(request,'main/register.html',{})
        elif format == 'json':
            a = {'ok' : 'false','error':'method is not post!'}
            return HttpResponse(json.dumps(a,default=lambda o:o.__dict__))
    if request.method == 'POST':
        try:
            bio = request.POST.get('bio',None)
            name = request.POST.get('name',None)
            username = request.POST.get('username',None)
            username = username.lower()
            password = request.POST.get('password',None)
            re_password = request.POST.get('re-password',None)
            email = request.POST.get('email',None)
            email = email.lower()
            loc = request.POST.get('location',None)
            gender = request.POST.get('gender','male')
            phone = request.POST.get('phone',None)
            first = Gender.objects.filter(text=gender).count() > 0
            second = re.compile('[0-9]{11}').match(phone)
            third = Phone.objects.filter(number=int(phone)).count() == 0
            cons = first and second and third
            if username and password and re_password and email and phone and name and password == re_password and cons:
                user = User.objects.create_user(username=username,email=email,password=password)
                locations = Location.objects.filter(text=loc)
                if locations.count() > 0:
                    location = Location.objects.get(text=loc)
                else:
                    location = Location.objects.create(text=loc)
                g = Gender.objects.get(text=gender)
                if not re.compile('[0-9]{11}').match(phone):
                    if format == 'html':
                        return render(request, 'main/register.html', {'e':'شماره صحیح نمی باشد'})
                    elif format == 'json':
                        a = {'ok':'false','error':'Phone number is not correct'}
                        return HttpResponse(json.dumps(a,default=lambda o:o.__dict__))
                p = Phone.objects.filter(number=int(phone))
                if p.count() > 0:
                    if format == 'html':
                        return render(request, 'main/register.html', {'e':'شماره ثبت شده است'})
                    elif format == 'json':
                        a = {'ok':'false','error':'Phone number is already registered'}
                        return HttpResponse(json.dumps(a,default=lambda o:o.__dict__))
                ph = Phone.objects.create(number=int(phone))
                p = Profile.objects.create(bio=bio,name=name,user=user,location=location,gender=g,phone=ph)
                if format == 'html':
                    return redirect('/sign-in')
                elif format == 'json':
                    return HttpResponse('{ "ok" : "true" , "result" : ' + p.json() + '}')
            else:
                return render(request, 'main/register.html', {'e':'لطفا فیلد های مورد نیاز را به درستی پر کنید'})
        except Exception as e:
            if format == 'html':
                return render(request, 'main/register.html', {'e':e})
            elif format == 'json':
                return HttpResponse('{ "ok" : "false" , "error" : ' + e.__str__() + ' }')



def firstPage(request):
    format = request.GET.get('format','html')
    page = request.GET.get('page',1)
    page = int(page)
    user = request.user
    followings = FollowingFollower.objects.filter(follower__user__id=user.id)
    s = ''
    for f in followings:
        s += '\n' + f.follower.json()
        s += '\n' + f.following.json()
    my_list = []
    for follow in followings:
        posts = Post.objects.filter(user__id=follow.following.id)
        my_list = my_list + list(posts)
    my_list.sort(key=lambda x:x.id, reverse=True)
    first = (page - 1) * POSTS_PER_PAGE
    second = page * POSTS_PER_PAGE
    cnt = len(my_list)
    pages = math.ceil(cnt / POSTS_PER_PAGE)
    r = range(1 , pages + 1)
    my_list = my_list[first:second]
    if format == 'html':
        return render(request,'main/index.html',{'posts' : my_list , 'pages' : pages , 'range' : r,'page' : page,'pagep' : page - 1,'pagen' : page + 1})
    elif format == 'json':
        l = []
        for ml in my_list:
            l.append(ml.json())
        return HttpResponse('{ "ok" : "true" , "result" : ' + l.__str__() + ' , "pages" : ' + str(pages) + '}')



def index(request):
    format = request.GET.get('format','html')
    s = forApi(request,format)
    if request.user.is_authenticated:
        return firstPage(request)
    else:
        return register(request)



def sign_in(request):
    format = request.GET.get('format','html')
    username = request.POST.get('username' , '')
    username = username.lower()
    password = request.POST.get('password' , None)
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'GET':
        if format == 'html':
            return render(request,'main/sign-in.html',{})
        elif format == 'json':
            return HttpResponse('{ "ok" : "false" , "error" : "method is not post" }')
    elif request.method == 'POST':
        user = authenticate(request,username=username,password=password)
        if user:
            if format == 'html':
                login(request,user)
                return redirect('/')
            elif format == 'json':
                profile = Profile.objects.get(user__id=user.id)
                return HttpResponse('{ "ok" : "true" , "user" : ' + profile.json() + ' }')
        else:
            return render(request,'main/sign-in.html',{'e':'username or password is wrong'})


def sign_out(request):
    format = request.GET.get('format','html')
    if request.user:
        logout(request)
    if format == 'html':
        return redirect('/login')
    elif format == 'json':
        return HttpResponse('{ "ok" : "true" , "result" : "you are logged out" }')


def post(request):
    format = request.GET.get('format','html')
    s = forApi(request, format)
    if (s):
        return s
    user = request.user
    text = request.POST.get('text',None)
    if request.method == 'GET':
        if user.is_authenticated:
            if format == 'html':
                return render(request,'main/post.html',{})
            else:
                return HttpResponse('{ "ok" : "false" , "error" : "method is not post" }')
        else:
            if format == 'html':
                return redirect('/login')
            else:
                return HttpResponse('{ "ok" : "false" , "error" : "you are not logged in" }')
    else:
        url = request.FILES.get('pic',None)
        pic = None
        if url:
            url = saveOnProfile(request,'pic')
            pic = Photo.objects.create(location=url)
        if text:
            e = 'sent'
            profile = Profile.objects.get(user__id=user.id)
            p = Post.objects.create(user=profile,text=text,forward=None,pic=pic)
            words = re.compile('\n| ').split(text)
            for word in words:
                if len(word) > 0 and word[0] == '#':
                    w = word[1:]
                    Hashtag.objects.create(text=w,post=p)
        else:
            e = 'text is empty'
        if format == 'html':
            return render(request,'main/post.html',{'e':e})
        else:
            if e == 'sent':
                return HttpResponse('{ "ok" : "true" , "result" : ' + p.json() + ' }')
            else:
                return HttpResponse('{ "ok" : "false" , "result" : "' + e + '" }')

def user_profile(request,username):
    format = request.GET.get('format','html')
    s = forApi(request, format)
    if (s):
        return s
    user = request.user
    username = username.lower()
    profile = Profile.objects.get(user__username=username)
    ps = Post.objects.filter(user__id=profile.id)
    page = request.GET.get('page',1)
    page = int(page)
    pages = math.ceil(ps.count() / POSTS_PER_PAGE)
    r = range(1 , pages + 1)
    first = (page - 1) * POSTS_PER_PAGE
    second = page * POSTS_PER_PAGE
    ps = list(ps)
    ps.sort(key=lambda x:x.id,reverse=True)
    ps = ps[first:second]
    if request.method == 'GET':
        if user.is_authenticated:
            follower = Profile.objects.get(user__id=user.id)
        else:
            if format == 'html':
                return redirect('/login')
            else:
                return HttpResponse('{ "ok" : "false" , "error" : "you are not logged in" }')
        ff = FollowingFollower.objects.filter(following=profile, follower=follower)
        if ff.count == 0:
            s = 'false'
        else:
            s = 'true'
        if format == 'html':
            return render(request,'main/user.html',{'profile' : profile,'follow' : s , 'posts' : ps,'pages' : pages,'range' : r,'page' : page,'pagep' : page - 1,'pagen' : page + 1})
        else:
            l = []
            for post in ps:
                l.append(post.json())
            return HttpResponse('{ "ok" : "true" , "user" : ' + profile.json() + ' , "posts" : ' + str(l) + ', "followed" : "' + s + '" }')
    elif request.method == 'POST' and 'follow' in request.POST:
        if user.is_authenticated:
            follower = Profile.objects.get(user__id=user.id)
        else:
            return HttpResponse('{ "ok" : "false" , "error" : "you are not logged in" }')
        ff = FollowingFollower.objects.filter(following=profile,follower=follower)
        e = 'you are followed this username before'
        if(ff.count() == 0 and follower.user.id != profile.user.id):
            FollowingFollower.objects.create(following=profile,follower=follower)
            e = 'followed successfully'
        if format == 'html':
            return render(request,'main/user.html',{'profile' : profile,'user' : user,'follow' : 'true','posts' : ps,'pages' : pages,'range' : r,'page' : page,'pagep' : page - 1,'pagen' : page + 1})
        else :
            return HttpResponse('{ "ok" : "true" , "result" : "' + e + '" }')
    else:
            l = []
            for post in ps:
                l.append(post.json())
            return HttpResponse('{ "ok" : "true" , "user" : ' + profile.json() + ' , "posts" : ' + str(
                l) + ', "followed" : "' + str(s) + '" }')


def hashtag(request,text):
    format = request.GET.get('format' , 'html')
    s = forApi(request, format)
    if (s):
        return s
    page = request.GET.get('page',1)
    page = int(page)
    hs = Hashtag.objects.filter(text=text)
    l = []
    for h in hs:
        l.append(h.post)
    l.sort(key=lambda x:x.id , reverse=True)
    first = (page - 1) * POSTS_PER_PAGE
    second = page * POSTS_PER_PAGE
    cnt = len(l)
    pages = math.ceil(cnt / POSTS_PER_PAGE)
    r = range(1, pages + 1)
    l = l[first:second]
    if format == 'html':
        return render(request,'main/hashtag.html',{'posts':l,'pages':pages,'range':r,'page' : page,'pagep' : page - 1,'pagen' : page + 1})
    else:
        ls = []
        for ll in l:
            ls.append(ll.json())
        return HttpResponse('{ "ok" : "true" , "result" : ' + str(ls) + ' , "pages" : ' + str(pages) + '}')


def posts(request,pid):
    format = request.GET.get('format','html')
    s = forApi(request, format)
    if (s):
        return s
    r = ''
    p = Post.objects.get(id=pid)
    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.get(user__id=user.id)
    if not user:
        if format == 'html':
            return redirect('/login')
        else:
            return HttpResponse('{ "ok" , "false" , "error" : "you are not logged in" }')
    elif request.method == 'POST':
        if 'text' in request.POST:
            Comment.objects.create(text=request.POST['text'],post=p,user=profile)
            r = 'comment added'
        elif 'r' in request.POST:
            Post.objects.create(text=p.text,user=profile,forward=p)
            r = 'retwitted'
        else:
            r = 'liked'
            ls = Like.objects.filter(post__id=pid,user__user__id=user.id)
            if ls.count() == 0:
                Like.objects.create(user=profile,post=p)
    comments = Comment.objects.filter(post__id=pid)
    likes = Like.objects.filter(post__id=pid)
    comments = list(comments)
    comments.sort(key=lambda x:x.id,reverse=True)
    likes = list(likes)
    likes.sort(key=lambda x:x.id,reverse=True)
    if format == 'html':
        return render(request,'main/posts.html',{'post' : p,'comments' : comments,'likes' : likes,'r':r})
    else:
        cs = []
        ls = []
        for c in comments:
            cs.append(c.json())
        for l in likes:
            ls.append(l.json())
        return HttpResponse('{ "ok" : "true" , "post" : ' + p.json() + ' , "likes" : ' + str(ls) + ' , "comments" : ' + str(cs) + ' }')
def api(request):
    if request.user.is_authenticated:
        return render(request,'main/api.html',{})
    else:
        return redirect('/login')
def upload(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file_url = saveOnProfile(request,'file')
        return render(request, 'main/upload.html', {
            'url': uploaded_file_url
        })
    return render(request, 'main/upload.html')

def add_member(request,cid):
    username = request.POST.get('user',None)
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request,'main/add-member.html')
        else:
            try:
                adder = Profile.objects.get(user__id=request.user.id)
                e = 'chat not found'
                chat = Chat.objects.get(id=cid)
                e = 'you are not in chat'
                cm = ChatMember.objects.get(user=adder,chat=chat)
                e = 'user not found'
                user = Profile.objects.get(user__username=username)
                e = 'user already is in chat'
                cm = ChatMember.objects.filter(user=user,chat=chat)
                if(cm.count() == 0):
                    ChatMember.objects.create(user=user,chat=chat)
                    e = 'added successfully'
                return render(request,'main/add-member.html',{'e' : e})
            except Exception:
                return render(request,'main/add-member.html',{'e' : e})
    return redirect('/login')

def remove_member(request,cid):
    username = request.POST.get('user', None)
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'main/remove-member.html')
        else:
            try:
                remover = Profile.objects.get(user=request.user)
                e = 'chat not found'
                chat = Chat.objects.get(id=cid)
                if chat.creator != remover:
                    e = 'you are not creator of the chat'
                    raise Exception()
                e = 'user not found'
                user = Profile.objects.get(user__username=username)
                if user == remover:
                    e = 'you cannot remove your self from chat created by yours'
                    raise Exception()
                e = 'user is not in chat'
                cm = ChatMember.objects.filter(user=user, chat=chat)
                if (cm.count() > 0):
                    ChatMember.objects.get(user=user, chat=chat).delete()
                    e = 'removed successfully'
                return render(request, 'main/remove-member.html', {'e': e})
            except Exception:
                return render(request, 'main/remove-member.html', {'e': e})
    return redirect('/login')

def create_chat(request):
    format = request.GET.get('format','html')
    forApi(request,format)
    des = request.POST.get('des',None)
    title = request.POST.get('title',None)
    pic = request.FILES.get('pic',None)
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request,'main/create-chat.html',{})
        else:
            c = None
            e = 'title is blank'
            p = None
            profile = Profile.objects.get(user__id=request.user.id)
            if title and pic:
                p = saveOnProfile(request,'pic')
                p = Photo.objects.create(location=p)
            if title:
                c = Chat.objects.create(title=title,description=des,photo=p,creator=profile)
                ChatMember.objects.create(user=profile,chat=c)
                e = 'created'
            return render(request,'main/create-chat.html',{'e':e,'c':c.id})
    return redirect('/login')

def send_message(request,cid):
    text = request.POST.get('text',None)
    pic = request.FILES.get('pic',None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                user = Profile.objects.get(user__id=request.user.id)
                e = 'chat not found'
                chat = Chat.objects.get(id=cid)
                e = 'you are not in chat'
                cm = ChatMember.objects.get(user=user,chat=chat)
                p = None
                e = 'text is empty'
                if text and pic:
                    p = saveOnProfile(request,'pic')
                    p = Photo.objects.create(location=p)
                if text:
                    e = 'sent'
                    Message.objects.create(text=text,photo=p,user=user,chat=chat)
                return render(request,'main/send-message.html',{'e' : e})
            except Exception:
                return render(request,'main/send-message.html',{'e' : e})
        return render(request,'main/send-message.html')
    return redirect('/login')

def get_messages(request,cid):
    if request.user.is_authenticated:
        try:
            user = Profile.objects.get(user=request.user)
            e = 'chat not found'
            chat = Chat.objects.get(id=cid)
            e = 'you are not in chat'
            ChatMember.objects.get(user=user,chat=chat)
            messages = Message.objects.filter(chat=chat)
            messages = list(messages)
            messages.sort(key=lambda x:x.id,reverse=True)
            return render(request, 'main/get-messages.html', {'messages': messages})
        except Exception:
            return render(request,'main/get-messages.html',{'e' : e})
    return redirect('/login')