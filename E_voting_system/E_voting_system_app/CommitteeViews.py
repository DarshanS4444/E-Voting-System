import json
from datetime import datetime
from uuid import uuid4

from django.contrib import messages
from django.core import serializers
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from E_voting_system_app.models import Voters, Committees, CustomUser, Candidates


def committee_home(request):
    return render(request, "committee_template/committee_main_content.html")


def committee_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    committee = Committees.objects.get(admin=user)
    return render(request, "committee_template/committee_profile.html", {"user": user, "committee": committee})


def committee_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("committee_profile"))
    else:

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        ph_no = request.POST.get("ph_no")
        gender = request.POST.get("gender")

        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)

            customuser.first_name = first_name
            customuser.last_name = last_name

            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            committee = Committees.objects.get(admin=customuser.id)
            committee.address = address
            committee.gender = gender
            committee.ph_no = ph_no
            committee.save()

            messages.success(request, "Successfully Updated Password")
            return HttpResponseRedirect(reverse("committee_profile"))
        except:
            messages.error(request, "Failed to Update Password")
            return HttpResponseRedirect(reverse("committee_profile"))


def results(request):
    candidates = Candidates.objects.all()
    return render(request, "committee_template/results.html", {"candidates": candidates})
