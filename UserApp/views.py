from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import logout

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Enregistrer l'utilisateur
            return redirect('login')  # Redirige vers la page de connexion
    else:
        form = UserRegisterForm()  # Si GET ou formulaire invalide

    return render(request, 'register.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('login')
