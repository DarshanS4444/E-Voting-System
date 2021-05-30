import datetime

import json

# import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from E_voting_system_app.models import CustomUser, Committees, Voters, Candidates


def admin_home(request):
    voter_count1 =  Voters.objects.all().count()
    committee_count = Committees.objects.all().count()
    candidate_count = Candidates.objects.all().count()




    return render(request, "admin_template/main_content.html",
                  {"voter_count": voter_count1, "committee_count": committee_count,
                   "candidate_count": candidate_count
                  })


def add_committee(request):
    return render(request, "admin_template/add_committee_template.html")


def add_committee_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        qualification = request.POST.get("qualification")
        dob = request.POST.get("dob")
        blood_group = request.POST.get("blood_group")
        committee_number = request.POST.get("committee_number")
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        ph_no = request.POST.get("ph_no")

        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                  last_name=last_name, first_name=first_name, user_type=2)
            user.committees.gender = gender
            user.committees.address = address
            user.committees.ph_no = ph_no
            user.committees.dob = dob
            user.committees.qualification = qualification
            user.committees.blood_group = blood_group
            user.committees.committee_number = committee_number
            user.committees.profile_pic = profile_pic_url
            user.save()
            messages.success(request, "Successfully Added Committee member")
            return HttpResponseRedirect(reverse("add_committee"))
        except:
            messages.error(request, "Failed to Add Committee member")
            return HttpResponseRedirect(reverse("add_committee"))

def add_voter(request):
    return render(request, "admin_template/add_voter_template.html")


def add_voter_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        first_name = request.POST.get("first_name")
        password = request.POST.get("password")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")

        blood_group = request.POST.get("blood_group")
        email = request.POST.get("email")
        address = request.POST.get("address")
        voter_number = request.POST.get("voter_number")

        gender = request.POST.get("gender")
        ph_no = request.POST.get("ph_no")
        dob = request.POST.get("dob")


        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)

        try:
            user = CustomUser.objects.create_user(username=username, password=password,
                                                  email=email, last_name=last_name, first_name=first_name, user_type=3)

            user.voters.address = address



            user.voters.gender = gender
            user.voters.voter_number = voter_number

            user.voters.dob = dob
            user.voters.blood_group = blood_group

            user.voters.ph_no = ph_no
            user.voters.profile_pic = profile_pic_url
            user.save()

            messages.success(request, "Successfully Added Voter Details")
            return HttpResponseRedirect(reverse("add_voter"))

        except:
            messages.error(request, "Failed to Add Voter Details")
            return HttpResponseRedirect(reverse("add_voter"))

def add_candidate(request):

    return render(request, "admin_template/add_candidate_template.html")


def add_candidate_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        blood_group = request.POST.get("blood_group")
        email = request.POST.get("email")
        address = request.POST.get("address")
        candidate_number = request.POST.get("candidate_number")
        gender = request.POST.get("gender")
        ph_no = request.POST.get("ph_no")
        dob = request.POST.get("dob")
        profile_pic = request.FILES['profile_pic']
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)


        #try:
        candidate = Candidates(username=username,profile_pic = profile_pic_url, email=email, last_name=last_name, first_name=first_name,address=address,gender=gender,candidate_number=candidate_number,dob=dob,blood_group=blood_group,ph_no=ph_no)


        candidate.save()

        messages.success(request, "Successfully Added Candidate Details")
        return HttpResponseRedirect(reverse("add_candidate"))
        #except:
          #  messages.error(request, "Failed to Add Candidate Details")
            #return HttpResponseRedirect(reverse("add_candidate"))

def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "admin_template/admin_profile.html", {"user": user})


def admin_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))

def manage_committee(request):
    committees = Committees.objects.all()
    return render(request, "admin_template/manage_committee_template.html", {"committees": committees})

def manage_candidate(request):
    candidates = Candidates.objects.all()
    return render(request, "admin_template/manage_candidate_template.html", {"candidates": candidates})

def manage_voter(request):
    voters = Voters.objects.all()

    return render(request, "admin_template/manage_voter_template.html", {"voters": voters})





