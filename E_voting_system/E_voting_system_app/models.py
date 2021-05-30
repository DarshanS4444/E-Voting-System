from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
'''class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    object = models.Manager()'''


class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "Committee"), (3, "Voter"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


'''
class Parents(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    father_occupation = models.CharField(max_length=255)
    # parent_roll_number = models.CharField(max_length=50)
    mother_occupation = models.CharField(max_length=255)
    parent_ph_no = models.CharField(max_length=10)
    fcm_token = models.TextField(default="")
    parent_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
'''


class Committees(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    committee_number = models.CharField(max_length=50)
    dob = models.DateField()
    blood_group = models.CharField(max_length=10)
    qualification = models.CharField(max_length=50)
    gender = models.CharField(max_length=255)
    profile_pic = models.FileField()
    ph_no = models.CharField(max_length=10)
    address = models.TextField()
    fcm_token = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


'''
class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
'''


class Voters(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255)
    voter_number = models.CharField(max_length=50)
    blood_group = models.CharField(max_length=10)
    profile_pic = models.FileField()
    ph_no = models.CharField(max_length=10)
    dob = models.DateField()
    fcm_token = models.TextField(default="")
    address = models.TextField()
    voter_status = models.TextField(default="No")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Candidates(models.Model):
    id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=255)
    candidate_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    blood_group = models.CharField(max_length=10)
    profile_pic = models.FileField()
    ph_no = models.CharField(max_length=10)
    dob = models.DateField()
    fcm_token = models.TextField(default="")
    address = models.TextField()
    email = models.CharField(max_length=255)
    vote = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            Committees.objects.create(admin=instance, address="", profile_pic="", gender="", ph_no="",
                                      dob="2000-01-01", qualification="", blood_group="", committee_number="")

        if instance.user_type == 3:
            Voters.objects.create(admin=instance,
                                  address="", profile_pic="",
                                  gender="", ph_no="", dob="2000-01-01", blood_group="", voter_number="",
                                  voter_status="No")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.committees.save()
    if instance.user_type == 3:
        instance.voters.save()
