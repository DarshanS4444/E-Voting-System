"""E_voting_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from E_voting_system_app import views, AdminViews, CommitteeViews, VoterViews

from E_voting_system import settings

urlpatterns = [
    # HOD url path
    path('demo', views.showDemoPage),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.ShowLoginPage, name="show_login"),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user, name="logout"),
    path('doLogin', views.doLogin, name="do_login"),
    path('admin_home', AdminViews.admin_home, name="admin_home"),
    path('add_committee', AdminViews.add_committee, name="add_committee"),
    path('add_committee_save', AdminViews.add_committee_save, name="add_committee_save"),
    path('add_candidate', AdminViews.add_candidate, name="add_candidate"),
    path('add_candidate_save', AdminViews.add_candidate_save, name="add_candidate_save"),
    path('add_voter', AdminViews.add_voter, name="add_voter"),
    path('add_voter_save', AdminViews.add_voter_save, name="add_voter_save"),
    path('manage_committee', AdminViews.manage_committee, name="manage_committee"),
    path('manage_voter', AdminViews.manage_voter, name="manage_voter"),
    path('manage_candidate', AdminViews.manage_candidate, name="manage_candidate"),
    path('committee_home', CommitteeViews.committee_home, name="committee_home"),
    path('committee_profile', CommitteeViews.committee_profile, name="committee_profile"),
    path('committee_profile_save', CommitteeViews.committee_profile_save, name="committee_profile_save"),
    path('results', CommitteeViews.results, name="results"),
    path('candidate_result/<str:candidate_id>', CommitteeViews.candidate_result, name="candidate_result"),
    path('candidate_result_save', CommitteeViews.candidate_result_save, name="candidate_result_save"),
    path('voter_home', VoterViews.voter_home, name="voter_home"),
    path('voting_panel', VoterViews.voting_panel, name="voting_panel"),
    path('voter_profile', VoterViews.voter_profile, name="voter_profile"),
    path('voter_profile_save', VoterViews.voter_profile_save, name="voter_profile_save"),
    path('admin_profile', AdminViews.admin_profile, name="admin_profile"),
    path('admin_profile_save', AdminViews.admin_profile_save, name="admin_profile_save"),
    path('view_candidate/<str:candidate_id>', VoterViews.view_candidate, name="view_candidate"),
    path('view_candidate_save', VoterViews.view_candidate_save, name="view_candidate_save"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
