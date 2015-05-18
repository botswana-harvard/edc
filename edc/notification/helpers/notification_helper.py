from datetime import datetime

import json

from ..models import NotificationPlan, Notification


class NotificationHelper(object):

    def update_plan(self, notification_plan_setup):
        """Creates or updates the notification plan model instance using a given notification_plan_setup dictionary."""
        for notification_plan_name, notification_plan in notification_plan_setup.iteritems():
            try:
                notification_plan_instance = NotificationPlan.objects.get(name=notification_plan_name)
                notification_plan_instance.name = notification_plan.get('name')
                notification_plan_instance.friendly_name = notification_plan.get('friendly_name')
                notification_plan_instance.subject_format = notification_plan.get('subject_format')
                notification_plan_instance.body_format = notification_plan.get('body_format')
                notification_plan_instance.recipient_list = json.dumps(notification_plan.get('recipient_list'))
                notification_plan_instance.cc_list = json.dumps(notification_plan.get('cc_list'))
                notification_plan_instance.save()
            except NotificationPlan.DoesNotExist:
                NotificationPlan.objects.create(
                    name=notification_plan.get('name'),
                    friendly_name=notification_plan.get('friendly_name'),
                    subject_format=notification_plan.get('subject_format'),
                    body_format=notification_plan.get('body_format'),
                    cc_list=json.dumps(notification_plan.get('cc_list')),
                    )

    def queue_notification(self, plan_name, export_filename, exit_status, export_datetime=None, transaction_count=None):
        """Queues a notification by writing a NotificationPlan model instance.

        Returns the notification plan model instance"""
        export_datetime = export_datetime or datetime.today()
        transaction_count = transaction_count or 0
        notification_plan = NotificationPlan.objects.get(name=plan_name)
        exit_status_word = 'Success' if (exit_status[0] == 0) else 'Failed'
        return Notification.objects.create(
            notification_datetime=export_datetime,
            notification_plan_name=notification_plan.name,
            subject=notification_plan.subject_format.format(
                exit_status=exit_status_word, timestamp=export_datetime.strftime('%Y-%m-%d'), ),
            body=notification_plan.body_format.format(
                notification_plan_name=notification_plan.friendly_name,
                exit_status=exit_status_word,
                exit_status_message=exit_status[1],
                file_name=export_filename,
                tx_count=transaction_count,
                export_datetime=export_datetime.strftime('%d %B %Y')),
            recipient_list=notification_plan.recipient_list,
            cc_list=notification_plan.cc_list,
            )
