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
        if voter_model_new.voter_status == "No":
            try:
                # user = CustomUser.objects.get(id=request.user.id)
                # user.save()
                voter_model = Voters.objects.get(id=voter_set.id)
                voter_model.voter_status = voter_status
                voter_model.save()
                messages.success(request, "Successfully Voted")
                return HttpResponseRedirect(reverse("view_candidate", kwargs={"candidate_id": candidate_id}))
            except:
                messages.error(request, "Failed to Vote")
                return HttpResponseRedirect(reverse("view_candidate", kwargs={"candidate_id": candidate_id}))
        else:
            messages.error(request, "You have already cast your vote")
            return HttpResponseRedirect(reverse("view_candidate", kwargs={"candidate_id": candidate_id}))
