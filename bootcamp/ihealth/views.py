from django.shortcuts import render, redirect, get_object_or_404
from bootcamp.feeds.views import feeds
from django.contrib.auth.models import User
from bootcamp.feeds.models import Feed
from bootcamp.feeds.views import FEEDS_NUM_PAGES
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from bootcamp.ihealth.forms import ProfileForm, ChangePasswordForm
from django.contrib import messages
from django.conf import settings as django_settings
from PIL import Image
import os
import datetime

from utils import *

DB_NAME = "test"


def home(request):
    if request.user.is_authenticated():
        return feeds(request)
    else:
        return render(request, 'core/cover.html')


@login_required
def appointments(request):
    user = request.user
    session = get_session(DB_NAME, "admin", "x")
    # TODO : Include session value in Django session using cookies and stop generating it in every request
    appointments_ids = get_appointments(DB_NAME, session)['result']
    fields = {}
    appointments_details = get_appointments_details(DB_NAME, session, appointments_ids, fields)['result']
    # print appointments_details
    appointments_list = parse_as(str(json.dumps(appointments_details)), as_appointment)
    # Modifications on the parameters
    for appointment in appointments_list:
        # urgency
        if appointment.urgency == 'a':
            appointment.urgency = 'Normal'
        elif appointment.urgency == 'b':
            appointment.urgency = 'Urgent'
        elif appointment.urgency == 'c':
            appointment.urgency = 'Medical Emergency'
        else:
            appointment.urgency = ""
        # type
        appointment.appointment_type = appointment.appointment_type.capitalize()
        # specialty
        if appointment.speciality is None:
            appointment.speciality = ""
        # institution
        if appointment.institution is None:
            appointment.institution = ""
        # state
        if appointment.state == "free":
            appointment.state = "Free"
        elif appointment.state == "confirmed":
            appointment.state = "Confirmed"
        elif appointment.state == "done":
            appointment.state = "Done"
        elif appointment.state == "user_cancelled":
            appointment.state = "Cancelled by patient"
        elif appointment.state == "center_cancelled":
            appointment.state = "Cancelled by Health Center"
        elif appointment.state == "no_show":
            appointment.state = "No show"
        else:  # appointment.state is None:
            appointment.state = ""
        # appointment date
        appointment.appointment_date = date_to_string(appointment.appointment_date)
        # TODO : Show 'Patient', 'Specialty', 'Health Prof' and 'Institution' by name (in place of their ids)
    return render(request, 'ihealth.html', {
        'appointments': appointments_list,
    })


@login_required
def patients(request):
    user = request.user
    session = get_session(DB_NAME, "admin", "x")
    patients_ids = get_patients(DB_NAME, session)['result']
    fields = {}
    patients_details = get_patients_details(DB_NAME, session, patients_ids, fields)['result']
    # print patients_details
    patients_list = parse_as(str(json.dumps(patients_details)), as_party)
    # Modifications on the parameters
    for patient in patients_list:
        # date of birth
        if patient.dob is None:
            patient.dob = ""
        else:
            patient.dob = date_to_string(patient.dob)
    return render(request, 'patients.html', {
        'patients': patients_list,
    })


@login_required
def prescriptions(request):
    user = request.user
    session = get_session(DB_NAME, "admin", "x")
    prescriptions_ids = get_prescriptions(DB_NAME, session)['result']
    fields = {}
    prescriptions_details = get_prescriptions_details(DB_NAME, session, prescriptions_ids, fields)['result']
    prescriptions_list = parse_as(str(json.dumps(prescriptions_details)), as_prescription)
    # Modifications on the parameters
    for prescription in prescriptions_list:
        # date of birth
        if prescription.prescription_date is None:
            prescription.prescription_date = ""
        else:
            prescription.prescription_date = date_to_string(prescription.prescription_date)
    # TODO : Show 'Patient' and 'Prescribed by' name (in place of their ids)
    return render(request, 'prescriptions.html', {
        'prescriptions': prescriptions_list
    })


# @login_required
# def network(request):
#     users = User.objects.filter(is_active=True).order_by('username')
#     return render(request, 'core/network.html', {'users': users})

# @login_required
# def profile(request, username):
#     page_user = get_object_or_404(User, username=username)
#     all_feeds = Feed.get_feeds().filter(user=page_user)
#     paginator = Paginator(all_feeds, FEEDS_NUM_PAGES)
#     feeds = paginator.page(1)
#     from_feed = -1
#     if feeds:
#         from_feed = feeds[0].id
#     return render(request, 'core/profile.html', {
#         'page_user': page_user,
#         'feeds': feeds,
#         'from_feed': from_feed,
#         'page': 1
#         })