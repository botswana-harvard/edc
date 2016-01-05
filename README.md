#edc

this is the PY2 / Django 1.6 Edc set of modules.

Edc is a clinical research data management system

Project `microbiome` is the most current Edc project.

In the develop branch, most of the functionality is being moved out to separate packages. So far:
* `edc.apps.app_configuration`: `edc_configuration`
* `edc.audit`: `edc_audit` (Note: import through `edc_base.audit` instead of directly directly)
* `edc.core.bhp_birt_reports`: `edc_birt_reports` but not used
* `edc.core.bhp_content_type_map: `edc_content_type_map`
* `edc.core.bhp_using`: dropped
* `edc.core.bhp_variables`: dropped
* `edc.core.crypto_fields`: `edc_crypto_fields` (Note: import through `edc_base.encrypted_fields` instead of directly)
* `edc.core.identifier`: `edc_identifier` (except for `Identifier` class still used by `edc_lab`)
* `edc.dashboard`: `edc_dashboard`
* `edc.data_dictionary`: `edc_data_dictionary`
* `edc.data_manager`: still active but timpoint_status classes moved to `edc_appointment`
* `edc.device.sync`: `edc_sync`
* `edc.lab`: `edc_lab`
* `edc.map`: `edc_map`
* `edc.subject.rule_groups`: `edc_rule_groups`
* `edc.subject.adverse_event`: `edc_death_report`
* `edc.subject.appointment`:  `edc_appointment`
* `edc.subject.appointment_helper`:  merged into `edc_appointment`
* `edc.subject.locator`: `edc_locator`
* `edc.subject.off_study`: `edc_offstudy`
* `edc.subject.registration`: `edc_registration`
* `edc.subject.subject_config`: merged into `edc_appointment`
* `edc.subject.visit_schedule`: `edc_visit_schedule`
* `edc.subject.visit_tracking`: `edc_visit_tracking`
* `edc.testing`: `edc_testing`


Features
--------

- full audit trail
- master patient record
- allocation of unique study identifiers
- informed consent
- visit schedule
- visit tracking (timepoint tracking)
- customizable rules for required and optional forms for each visit / timepoint
- allocation of unique specimen identifiers
- specimen requisitioning, reception, processing and labelling
- data synchronization to central server for offline data collection clients
- ... and much more
