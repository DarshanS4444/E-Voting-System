import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from E_voting_system_app.models import Voters, Candidates, CustomUser


def voter_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    voter = Voters.objects.get(admin=user)
    return render(request, "voter_template/voter_profile.html", {"user": user, "voter": voter})


def voter_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("voter_profile"))
    else:

        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            messages.success(request, "Successfully Updated Password")
            return HttpResponseRedirect(reverse("voter_profile"))
        except:
            messages.error(request, "Failed to Update Password")
            return HttpResponseRedirect(reverse("voter_profile"))

def voter_home(request):
    return render(request, "voter_template/voter_main_content.html")

def voting_panel(request):
    return render(request, "voter_template/voting_panel.html")