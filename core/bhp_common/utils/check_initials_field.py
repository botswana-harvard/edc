from django import forms


def check_initials_field(first_name, last_name, initials):
    """
        check that the first and last initials match what is expected based on
        first and last name
    """
    if initials and first_name:
        if first_name[:1].upper() != initials[:1].upper():
            raise forms.ValidationError("First initial does not match first name, expected '%s' but you wrote %s." % (first_name[:1], initials[:1]))
    if initials and last_name:
        if last_name[:1].upper() != initials[-1:].upper():
            raise forms.ValidationError("Last initial does not match last name, expected '%s' but you wrote %s." % (last_name[:1], initials[-1:]))
