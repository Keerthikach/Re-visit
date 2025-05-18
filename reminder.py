import time
from database import fetch_for_rev
from win10toast import ToastNotifier 

def show_notifications():
    vals=fetch_for_rev()
    print(vals)

    toaster=ToastNotifier()
    for _,q,d,_ in vals:
        toaster.show_toast(
            "Revision Reminder",
            f"{q}:{d}",
            duration=10,
            threaded=False
        )
    
show_notifications() 
