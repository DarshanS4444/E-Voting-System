import json
import math
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



            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            messages.success(request, "Successfully Updated Password")
            return HttpResponseRedirect(reverse("committee_profile"))
        except:
            messages.error(request, "Failed to Update Password")
            return HttpResponseRedirect(reverse("committee_profile"))


def results(request):
    candidates = Candidates.objects.all()
    return render(request, "committee_template/results.html", {"candidates": candidates})

def candidate_result(request, candidate_id):
    candidate = Candidates.objects.get(id=candidate_id)
    return render(request, "committee_template/candidate_result.html", {"candidate": candidate, "id": candidate_id})


def candidate_result_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        candidate_id = request.POST.get("candidate_id")
        candidate_model = Candidates.objects.get(id=candidate_id)
        candidate_message = candidate_model.message

        def lf(x, n):
            return ((x - 1) // n)

        def dec(c, lam, Mu, n):
            n2 = n * n
            z = lf(pow(c, lam, (n2)), n)
            return ((z * Mu) % n)

        def final(c, n):
            return (c) % (n * n)

        c = int(candidate_model.ciphertext_candidates)
        n = 667  # int(input("n = "))
        lam = 308  # int(input("lam = "))
        Mu = 356  # int(input("Mu = "))
        c1 = final(c, n)
        #print(f"c = {c1}")
        s = dec(c, lam, Mu, n)
        print("bbbbbbbbbbbbbbb", s)
        s = s/int(candidate_message)
        print("hiiiiiiiiiiii", s)
        candidate_model = Candidates.objects.get(id=candidate_id)
        candidate_model.vote_count = s
        candidate_model.save()
        return HttpResponseRedirect(reverse("candidate_result", kwargs={"candidate_id": candidate_id}))



