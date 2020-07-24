from src.models import UserModel, LectureModel, SubjectModel, AttendanceStatusModel
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from src.models.UserModel import UserModel
from src.models.LectureModel import LectureModel
from src import app
import datetime
executed = False

def send_notif(token, name):
    print(token)
    url = "https://fcm.googleapis.com/fcm/send"

    payload = "{\n    \"to\":\""+token+"\",\n      \"data\":{\"name\":\""+name+"\"}\n\n}"
    headers = {
    'Authorization': 'key=AAAA8OaMYk4:APA91bHWKNBxtPZ7nCwo1-p2ydPvnRgcgMer76Bzlh94B88I9R5cKpM4LCeJtkQx5qYCTs6Jxkv_74SWqH0h6AV9nhhOjNioKJdTlCnOyicFFkL3LOKDTExgvWG7X8FyrnygCfD-Nzo6',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))

def print_date_time():
    with app.app_context():
        weekday = datetime.datetime.today().weekday()
        lectures = LectureModel.query.filter_by(day=weekday).all()
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        # bf = now - datetime.timedelta(minutes=10)
        # af = now + datetime.timedelta(minutes=10)
        for lecture in lectures:
            st=datetime.datetime.strptime(lecture.start_time,'%H:%M:%S')
            lnow = st.hour
            lmin = st.minute
            if (lnow == hour and abs(lmin-minute) <= 10):
                user = UserModel.find_by_id(lecture.user_id)
                send_notif(user.token, lecture.name)
        # users = UserModel.query.all()
        # print(users)
    # for user in users:
    #     send_notif(user.token)

def execute():
    global executed
    if (executed == False):
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=print_date_time, trigger="interval", seconds=9)
        scheduler.start()
        executed = True