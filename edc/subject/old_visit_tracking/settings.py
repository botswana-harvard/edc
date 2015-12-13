from edc_constants.constants import (
    MISSED_VISIT, SCHEDULED, UNSCHEDULED, DEATH_VISIT, OFF_STUDY, DEFERRED_VISIT, LOST_VISIT)

VISIT_REASON_NO_FOLLOW_UP_CHOICES = [MISSED_VISIT, DEATH_VISIT, LOST_VISIT, DEFERRED_VISIT]
VISIT_REASON_FOLLOW_UP_CHOICES = [SCHEDULED, UNSCHEDULED, OFF_STUDY]
VISIT_REASON_REQUIRED_CHOICES = VISIT_REASON_FOLLOW_UP_CHOICES + VISIT_REASON_NO_FOLLOW_UP_CHOICES