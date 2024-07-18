from django.shortcuts import render, redirect
from .models import User
from .forms import CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


@login_required
def edit_profile(request):
    user = request.user  # Get the current logged-in user

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()  # Save form data to update the user object
            messages.success(request, "Profil muvaffaqiyatli yangilandi.")
            return redirect('index')  # Redirect to 'index' after successful update
    else:
        form = CustomUserChangeForm(instance=user)  # Initialize form with user's current data
    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'registration/edit-profile.html',  context)


