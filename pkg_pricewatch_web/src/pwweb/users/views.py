from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from pwweb.users.forms import UserRegisterForm
from pwweb.users.models import UserProduct
from pwweb.users.serializers import UserProductSerializer


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You are now able to login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'title': 'Register'})


class UserProductViewSet(viewsets.ModelViewSet):
    queryset = UserProduct.objects.all()
    serializer_class = UserProductSerializer
    permission_classes = [IsAuthenticated]
