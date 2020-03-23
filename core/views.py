from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Pet

# Create your views here.
@login_required(login_url='/login/')
def list_all_pets(request):
    pets = Pet.objects.filter(active=True)
    print(pets.query)
    return render(request, 'list.html', {'pets': pets})

@login_required(login_url='/login/')
def register_pet(request):
    pet_id = request.GET.get('id')
    if pet_id :
        pet = Pet.objects.get(id=pet_id)
        if pet.user == request.user:
            return render(request, 'register-pet.html', {'pet':pet})

    return render(request, 'register-pet.html')

@login_required(login_url='/login/')
def set_pet(request):
    city = request.POST.get("city")
    email = request.POST.get("email")
    phone = request.POST.get("phone")
    description = request.POST.get("description")
    photo = request.FILES.get("file")
    pet_id = request.POST.get("id")
    user = request.user
    pet = None
    if pet_id:
        pet = Pet.objects.get(id=pet_id)
        if user == pet.user:
            pet.email = email
            pet.city = city
            pet.phone = phone
            pet.description = description
            if photo:
                pet.photo = photo
            pet.save()
    else:  
        pet = Pet.objects.create(city=city, email=email, phone=phone, description=description, photo=photo, user=user)

    url = '/pet/detail/{}/'.format(pet.id)
    return redirect(url)

@login_required(login_url='/login/')
def delete_pet(request, id):
    pet = Pet.objects.get(id=id)
    if pet.user == request.user:
        pet.delete()
    return redirect('/')

def list_user_pets(request):
    pets = Pet.objects.filter(active=True, user=request.user)
    return render(request, 'list.html', {'pets': pets})

def pet_detail(request, id):
    pet = Pet.objects.get(active=True, id=id)
    return render(request, 'pet.html', {'pet': pet})

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/login/')

@csrf_protect
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password') 
        user = authenticate (username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Usário e senha inválido. Favor tentar novamente')
    return redirect('/login/')

def error_404_view(request, exception):
    return render(request, 'page-not-found.html')

