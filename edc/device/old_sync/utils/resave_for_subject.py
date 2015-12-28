from django.db.models import get_models, get_model

from edc_appointment.models import Appointment
from edc_registration.models import RegisteredSubject


def resave_for_subject(subject_identifier, consent, visit, visit_key):

    """ resave all model instances for a given subject

    for example:

    resave_for_subject(
        '062-5511-0',
        ('maikalelo_maternal','maternalconsent'),
        ('maikalelo_maternal', 'maternalvisit'),
        'maternal_visit'
        )
    """

    APP_LABEL = 0
    MODEL_NAME = 1

    visit_model = get_model(visit[APP_LABEL], visit[MODEL_NAME])

    if consent:
        consent_model = get_model(consent[APP_LABEL], consent[MODEL_NAME])
    else:
        consent_model = None

    field_contains = '%s__appointment__registered_subject__subject_identifier' % (visit_key,)

    # registered_subject
    registered_subjects = RegisteredSubject.objects.filter(subject_identifier=subject_identifier)
    for rs in registered_subjects:
        rs.save()
        print "saved %s" % (rs,)

    # consent
    if consent_model:
        consents = consent_model.objects.filter(subject_identifier=subject_identifier)
        for consent in consents:
            consent.save()
            print "saved %s" % (consent,)

    #unscheduled and registration forms
    for model in get_models():
        try:
            if getattr(model, 'registered_subject'):
                m = model.objects.get(registered_subject__subject_identifier=subject_identifier)
                if m:
                    m.save()
                    print "saved %s" % (m,)
        except:
            pass

    #appointments
    appointments = Appointment.objects.filter(registered_subject__subject_identifier=subject_identifier)
    for appt in appointments:
        appt.save()
        print "saved %s" % (appt,)

    # visits
    visits = visit_model.objects.filter(appointment__registered_subject__subject_identifier=subject_identifier)
    for visit in visits:
        visit.save()
        print "saved %s" % (visit,)

    #scheduled forms, will also resave the audit record
    for model in get_models():
        try:
            if getattr(model, visit_key):
                models = model.objects.filter(**{field_contains: subject_identifier})
                for model in models:
                    model.save()
                    print "saved %s" % (model,)
        except:
            pass
