import time
from database import fetch_for_rev
from plyer import notification 

def send_reminder():
    my_ques=fetch_for_rev()
    if my_ques:
        #For system notifications using plyer 
        message="\n".join([f"- {q}" for _,q,_ in my_ques]) 

        notification.notify(
            title="Time For Revision",
            message=message,
            timeout=10
        )
        #For displaying the message in the terminal aswell

        print("Time For Revision")
        for q,d in my_ques:
            print(f"-{q}")
            print(f"{d}")

def start_rem():
    while True:
        send_reminder()            
        print("Next reminder in 24 hrs")

        time.sleep(86400)

if __name__=="__main__":
    start_rem()
    
