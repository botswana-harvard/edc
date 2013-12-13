from datetime import date


class OperatationalReportUtilities():

    def date_format_utility(self, date_string, default):
        if date_string == 'YYYY/MM/DD' or date_string == '':
            date_string = default

        if date_string.find('/') != -1:
            date_string = date_string.split('/')
            if int(date_string[0]) > 1950:  # format must be YYYY-MM-DD
                date_value = date(int(date_string[0]), int(date_string[1]), int(date_string[2]))
            else:
                date_value = date(int(date_string[2]), int(date_string[1]), int(date_string[0]))  # format must be DD-MM-YYYY
        elif date_string.find('-') != -1:
            date_string = date_string.split('-')
            if int(date_string[0]) > 1950:  # format must be YYYY-MM-DD
                date_value = date(int(date_string[0]), int(date_string[1]), int(date_string[2]))
            else:
                date_value = date(int(date_string[2]), int(date_string[1]), int(date_string[0]))  # format must be DD-MM-YYYY
        else:
            raise TypeError('Unrecognised date format. Please use either Mozilla Firefox, Google Chrome or Safari.')

        return date_value
