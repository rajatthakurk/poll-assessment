from django.shortcuts import render, redirect
from django.http import HttpResponse

from Poll_App.forms import CreatePollForm
from Poll_App.models import Poll,User
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from Poll_Project.tasks import delete_ex_poll

@login_required(login_url='login')
def home(request):
    delete_ex_poll.delay() # for deleting 24 hours old poll
    polls = Poll.objects.all()
    context = {
        'polls' : polls
    }
    return render(request, 'home.html', context)

@login_required(login_url='login')
def create(request):
    n = Poll.objects.filter(user=request.user)
    dd = int(len(n))
    # print(dd)
    if request.method == 'POST':
        if dd <= 4:
            form = CreatePollForm(request.POST)
            if form.is_valid():
                user = request.user
                question = form.cleaned_data['question']
                option_one = form.cleaned_data['option_one']
                option_two = form.cleaned_data['option_two']
                option_three = form.cleaned_data['option_three']
                option_four = form.cleaned_data['option_four']
                poll = Poll(user=user,question=question,option_one=option_one,option_two=option_two,option_three=option_three,option_four=option_four)
                poll.save()
                return redirect('home')
        else:
            messages.info(request,'User can create max 5 poll')
            return redirect('create')
    else:
        form = CreatePollForm()
    context = {
        'form' : form
    }
    return render(request, 'create.html', context)

@login_required(login_url='login')
def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':

        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        elif selected_option == 'option4':
            poll.option_four_count += 1
        else:
            return HttpResponse(400, 'Invalid form')

        poll.save()

        return redirect('results', poll.id)

    context = {
        'poll' : poll
    }
    return render(request, 'vote.html', context)

@login_required(login_url='login')
def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    context = {
        'poll' : poll
    }
    return render(request, 'results.html', context)

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password == password1:
            if User.objects.filter(email=email).exists():
                messages.info(request,'email already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,mobile=mobile,password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request,'Password does not matching.....')
            return redirect('register')
    else:
        return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Incorrect username/password')
            return redirect('login')
        
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile(request):
    ud = Poll.objects.filter(user=request.user)
    return render(request,'profile.html',{'ud':ud})