__author__ = 'oussama'

import httplib
import simplejson
import json
from classes import *
from django.contrib.sessions.backends.db import SessionStore
import datetime

SERVER = "localhost:8000"


############### Global utils ###############

def get_trytond_response(db_name, method, params, session=None):
    """
    :param db_name: Database name
    :param method: Method to call
    :param params: Parameters / Arguments of the called method
    :param session: Session got after login
    :return: Return JSON result of the query sent to trytond
    """
    if session:
        params = session + params
    conn = httplib.HTTPConnection(SERVER)
    # print simplejson.dumps(params)
    # print '{"method": "%s", "params":%s, "id": 1}' % (method, simplejson.dumps(params))
    conn.request("POST", "/%s" % db_name,
                 '{"method": "%s", "params":%s, "id": 1}' % (method, simplejson.dumps(params)))
    response = conn.getresponse()
    if not response.reason == 'OK':
        print 'WS Error'
        return response.read()
    return simplejson.loads(response.read())


def get_session(db_name, username, password):
    res = get_trytond_response(db_name, 'common.db.login', [username, password])
    if res:
        # print res
        return res["result"]


def parse_as(s, typo_class):
    return json.loads(str(s), object_hook=typo_class)


############### Specific utils ###############
# These methods return a dict that can be accessed using obj['id'] for example
# In order to get correct json text from them, you should apply on them:
# str(json.dumps(obj))

def model_search(db_name, session, method, domain=[]):
    """
    :rtype : list
    :param db_name: Database name
    :param session: Session got after login
    :param method: 'model.party.party.search' for example
    :param domain: domain = [(<field name>, <operator>, <operand>)]
    :return: Return a list of records that match the domain.
    """
    return get_trytond_response(db_name, method, [domain, {}], session)


def model_read(db_name, session, method, ids, fields={}):
    return get_trytond_response(db_name, method, [ids, fields], session)


def date_to_string(d):
    return str(d.month).zfill(2) + '/' + str(d.day).zfill(2) + '/' + str(d.year).zfill(4) + ' ' + str(d.hour).zfill(2) + ':' + str(d.minute).zfill(2) + ':' + str(d.second).zfill(2)


############### Appointment, Patient and Prescription utils ##############


def get_appointments(db_name, session):
    return model_search(db_name, session, "model.gnuhealth.appointment.search")


def get_appointments_details(db_name, session, ids, fields):
    return model_read(db_name, session, "model.gnuhealth.appointment.read", ids, fields)


def get_patients(db_name, session):
    return model_search(db_name, session, "model.party.party.search", [("is_patient", "=", True)])


def get_patients_details(db_name, session, ids, fields):
    return model_read(db_name, session, "model.party.party.read", ids, fields)


def get_prescriptions(db_name, session):
    return model_search(db_name, session, "model.gnuhealth.prescription.order.search")


def get_prescriptions_details(db_name, session, ids, fields):
    return model_read(db_name, session, "model.gnuhealth.prescription.order.read", ids, fields)


### Some sample code to help ###


# DB_NAME = "test"

# method = "model.party.party.read"
# method = "model.party.party.search"
# domain = [("name", "=", "Montassar")]

# username = "admin"
# password = "x"
# session = get_session(DB_NAME, username, password)
# model_search(DB_NAME, None, 'model.party.party.search', session)