from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from forms.models import WebbForm , Responses
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def profile(request):
    context = dict()
    context['accountactive'] = 'active'
    if request.user.is_authenticated:
        froms = WebbForm.objects.filter(user = request.user)
        formNumber = len(froms)
        context['formNumber'] = formNumber
        context['responses'] = 0
        formSet= []
        for form in froms:
            responseNum = len(Responses.objects.filter(form=form))
            context['responses'] += responseNum
            formSet.append((form , responseNum ))
        context['forms'] = formSet
        return render(request , 'profile.html' , context)

    return redirect('login')

def editProfile(request):
    context = dict()
    context['accountactive'] = 'active'
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            user.first_name = request.POST['fname']
            user.last_name = request.POST['lname']
            user.email = request.POST['email']
            user.save()
            return redirect('profile') 
        return render(request , 'editprofile.html' , context)
    return redirect('login')



def userLogout(request):
    logout(request)
    try:
        if request.GET['next']:
            return redirect(request.GET['next'])
    except:
        pass
    return redirect('home')

def register(request):
    context = dict()
    context['accountactive'] = 'active'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        try:
            user = User.objects.get(username=username)
            context['error'] = 'Username already exists'
        except:
            user = User()
            user.username = username
            user.set_password(password)
            user.save()
            login(request , user)
            return redirect('editprofile')
    return render(request , 'register.html' , context)

def userLogin(reqeust):
    context = dict()
    context['accountactive'] = 'active'
    if reqeust.method == 'POST':
        username = reqeust.POST['username']
        password = reqeust.POST['pass']
        user = authenticate(username=username , password=password)
        if user==None:
            context['error'] = 'Invalid username or password'
        else:
            login(reqeust , user)
            try:
                if reqeust.GET['next']:
                    return redirect(reqeust.GET['next'])
            except:
                pass
            return redirect('profile')
    return render(reqeust , 'login.html' , context)

def resetPass(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = dict()
    context['accountactive'] = 'active'
    if request.method == 'POST':
        user  = request.user
        if user.check_password(request.POST['oldpass']):
            user.set_password(request.POST['pass'])
            user.save()
            login(request , user)
            return redirect('profile')
        else:
            context['error'] = 'Old password is incorrect'
    return render(request , 'resetPass.html' , context)

# def forgotPass(request):
#     return render(request , 'forgotPass.html' , {})