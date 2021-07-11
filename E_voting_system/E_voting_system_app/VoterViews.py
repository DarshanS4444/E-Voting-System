import datetime
import math
#import sympy
from random import randint
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
    candidates = Candidates.objects.all()
    return render(request, "voter_template/voting_panel.html", {"candidates": candidates})


def view_candidate(request, candidate_id):
    candidate = Candidates.objects.get(id=candidate_id)
    return render(request, "voter_template/view_candidate_template.html", {"candidate": candidate, "id": candidate_id})


def view_candidate_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        candidate_id = request.POST.get("candidate_id")
        voter_status = request.POST.get("voter_status")
        voter_set = Voters.objects.get(admin_id=request.user.id)
        voter_model_new = Voters.objects.get(id=voter_set.id)
        candidate_model = Candidates.objects.get(id=candidate_id)
        candidate_message = candidate_model.message
        def lf(x, n):
            return ((x - 1) // n)

        def enc(g, m, n):
            r = randint(1, n)
            while math.gcd(r, n) != 1:
                r = randint(1, n)
            n2 = n * n
            return ((g ** m) * (r ** n)) % n2

        def mod_Inv(x, y):
            for i in range(y):
                if (x * i) % y == 1:
                    return i
            return -1

        def MuWithoutInverse(lam, n2):
            g = 296446#randint(1, n2)
            z = pow(g, lam, n2)
            l = lf(z, n)
            ln = mod_Inv(l, n)
            return ln, g

        p = 29 #sympy.randprime(100, 500)
        q = 23 #sympy.randprime(100, 500)

        while math.gcd((p * q), ((p - 1) * (q - 1))) != 1 or p == q:
             p = 29#sympy.randprime(100, 500)
             q = 23 #sympy.randprime(100, 500)
        else:
            p = p
            q = q

        n = p * q
        n2 = pow(n, 2)

        lam = math.lcm((p - 1), (q - 1))

        ln, g = MuWithoutInverse(lam, n2)

        while ln == -1:
            ln, g = MuWithoutInverse(lam, n2)

        Mu = ln % n

        m = int(candidate_message)
        c = enc(g, m, n)
        c = c % n2
        print("this is the cipher text", c)
        if voter_model_new.voter_status == "No":
            try:
                voter_model = Voters.objects.get(id=voter_set.id)
                voter_model.voter_status = voter_status
                candidate_model = Candidates.objects.get(id=candidate_id)
                candidate_model.ciphertext_candidates = int(candidate_model.ciphertext_candidates) * c
                voter_model.cipher_text = c
                voter_model.save()
                candidate_model.save()
                messages.success(request, "Successfully Voted")
                return HttpResponseRedirect(reverse("view_candidate", kwargs={"candidate_id": candidate_id}))
            except:
                messages.error(request, "Failed to Vote")
                return HttpResponseRedirect(reverse("view_candidate", kwargs={"candidate_id": candidate_id}))
        else:
            messages.error(request, "You have already cast your vote")
            return HttpResponseRedirect(reverse("view_candidate", kwargs={"candidate_id": candidate_id}))
