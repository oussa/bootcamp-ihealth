__author__ = 'oussama'


class Party(object):
    code = ""
    create_date = ""
    citizenship = ""
    photo = ""
    alternative_identification = ""
    sex = ""
    insurance_company_type = ""
    internal_user = ""
    activation_date = ""
    alternative_ids = []
    full_name = ""
    vat_number = ""
    insurance = []
    addresses = []
    create_uid = ""
    alias = ""
    code_readonly = ""
    id = ""
    is_patient = ""
    is_insurance_company = ""
    code_length = ""
    vat_code = ""
    ref = ""
    vat_country = ""
    website = ""
    lang = ""
    fax = ""
    write_uid = ""
    lastname = ""
    ethnic_group = ""
    contact_mechanisms = []
    write_date = ""
    insurance_plan_ids = []
    active = ""
    du = ""
    categories = []
    rec_name = ""
    unidentified = ""
    name = ""
    phone = ""
    mobile = ""
    is_institution = ""
    marital_status = ""
    is_healthprof = ""
    is_pharmacy = ""
    dob = ""
    residence = ""
    is_person = ""
    email = ""


class Appointment(object):
    rec_name = ""
    create_uid = ""
    consultations = ""
    create_date = ""
    name = ""
    appointment_date = ""
    healthprof = ""
    institution = ""
    state = ""
    comments = ""
    visit_type = ""
    appointment_type = ""
    write_date = ""
    patient = ""
    write_uid = ""
    id = ""
    urgency = ""
    speciality = ""


class Prescription(object):
    rec_name = ""
    create_uid = ""
    patient = ""
    healthprof = ""
    pregnancy_warning = ""
    notes = ""
    prescription_line = []
    pharmacy = ""
    prescription_date = ""
    prescription_warning_ack = ""
    write_date = ""
    user_id = ""
    create_date = ""
    write_uid = ""
    id = ""
    prescription_id = ""


def as_party(d):
    if isinstance(d, dict):
        p = Party()
        p.__dict__.update(d)
    elif isinstance(d, list):
        out = []
        for i in d:
            n = Party()
            n.__dict__.update(i)
            out.append(n)
        p = out
        print "out : ", out
    else:
        raise Exception('got non-dict value %s' % d)
    return p


def as_appointment(d):
    if isinstance(d, dict):
        p = Appointment()
        p.__dict__.update(d)
    elif isinstance(d, list):
        out = []
        for i in d:
            n = Appointment()
            n.__dict__.update(i)
            out.append(n)
        p = out
        print "out : ", out
    else:
        raise Exception('got non-dict value %s' % d)
    return p


def as_prescription(d):
    if isinstance(d, dict):
        p = Prescription()
        p.__dict__.update(d)
    elif isinstance(d, list):
        out = []
        for i in d:
            n = Prescription()
            n.__dict__.update(i)
            out.append(n)
        p = out
        print "out : ", out
    else:
        raise Exception('got non-dict value %s' % d)
    return p