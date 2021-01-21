import datetime as dt


def shortdate():
    return dt.datetime.now().strftime('%d.%m.%y')

def localtime():
    return dt.datetime.now().strftime('%H:%M:%S')
