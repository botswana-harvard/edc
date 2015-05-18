from dateutil import parser

from django.utils.encoding import force_text


def datatype_to_string(value):
    """Converts a value of Boolean, Decimal, Integer, Date or datetime or other into a string."""
    string_value = None
    if value == True:  # store booleans, None as a text string
        string_value = 'True'
    if value == False:
        string_value = 'False'
    if value == None:
        string_value = 'None'
    else:
        try:
            string_value = value.strftime('%Y-%m-%d')
            if not parser.parse(string_value) == value:
                raise ValueError
        except ValueError:
            pass
        except AttributeError:
            pass
        try:
            string_value = value.strftime('%Y-%m-%d %H:%M')
            if not parser.parse(string_value) == value:
                raise ValueError
        except ValueError:
            pass
        except AttributeError:
            pass
    return string_value or force_text(value)
