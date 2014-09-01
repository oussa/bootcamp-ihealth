__author__ = 'oussama'

from django.conf.urls import patterns, include, url

urlpatterns = patterns('bootcamp.ihealth.views',
    url(r'^$', 'appointments', name='appointments'),
    url(r'^patients/$', 'patients', name='patients'),
    url(r'^prescriptions/$', 'prescriptions', name='prescriptions'),
)
