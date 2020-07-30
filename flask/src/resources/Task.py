from src.models import UserModel, LectureModel, SubjectModel, AttendanceStatusModel
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from src.models.UserModel import UserModel
from src.models.LectureModel import LectureModel
from src.models.AttendanceStatusModel import AttendanceStatusModel
from src import app
import datetime
executed = False

def send_notif(token, name, color, start_time, end_time, id, a_for):
    print(token)
    url = "https://fcm.googleapis.com/fcm/send"

    payload = "{\n    \"to\":\""+token+"\",\n       \"data\":{\n        \"name\":\""+name+"\",\n  \"a_for\":\""+str(a_for)+"\",\n       \"color\":\""+str(color)+"\",\n        \"start_time\":\""+start_time+"\",\n        \"end_time\":\""+end_time+"\",\n        \"id\":\""+str(id)+"\"\n        }\n\n}"
    headers = {
    'Authorization': 'key=AAAA8OaMYk4:APA91bHWKNBxtPZ7nCwo1-p2ydPvnRgcgMer76Bzlh94B88I9R5cKpM4LCeJtkQx5qYCTs6Jxkv_74SWqH0h6AV9nhhOjNioKJdTlCnOyicFFkL3LOKDTExgvWG7X8FyrnygCfD-Nzo6',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))

def print_date_time():
    with app.app_context():
        weekday = datetime.datetime.utcnow().date().weekday()
        now = datetime.datetime.utcnow()
        date = now.date()
        datestring = date.strftime("%d/%m/%Y")
        lectures = LectureModel.query.filter(((LectureModel.last_marked == None) | (LectureModel.last_marked != date)) & ((LectureModel.sent == False) |  (LectureModel.last_sent < (datetime.datetime.utcnow() - datetime.timedelta(hours=24)))) & (LectureModel.day == weekday)).all()
        print("got lectures" + str(len(lectures)))
        hour = now.hour
        minute = now.minute
        # bf = now - datetime.timedelta(minutes=10)
        # af = now + datetime.timedelta(minutes=10)
        for lecture in lectures:
            print(lecture.start_time)
            st=datetime.datetime.strptime(lecture.start_time,'%H:%M')
            lnow = st.hour
            lmin = st.minute
            if (lnow == hour and abs(lmin-minute) <= 10):
                user = UserModel.find_by_id(lecture.user_id)
                if user.login:
                    lecture.sent = True
                    lecture.last_sent = datetime.datetime.utcnow()
                    lecture.save_to_db()
                    status = AttendanceStatusModel(status="cancel", a_for=datestring)
                    status.lect_id = lecture.id
                    status.sub_id = lecture.sub_id
                    status.save_to_db()
                    send_notif(user.token, lecture.name, lecture.color, lecture.start_time, lecture.end_time, lecture.id, status.id)
        # users = UserModel.query.all()
        # print(users)
    # for user in users:
    #     send_notif(user.token)

def execute():
    global executed
    if (executed == False):
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=print_date_time, trigger="interval", seconds=10)
        scheduler.start()
        executed = True