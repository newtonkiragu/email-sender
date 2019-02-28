import os
from mailer import settings
from mailer.handlers import SimpleCsvHandler


def create_message(d):
    # IP1 /31,IP2 /28,IP3 /22,IP4 /22
    student_name=d["Name"]
    status="on" if d['First Recommendation'] == 'Yes' else "not on"
    attendance=d["Attendance /100"]
    ip1,ip2,ip3,ip4=d["IP1 /31"],d["IP2 /28"],d["IP3 /22"],d["IP4 /22"]
    return f'''
    Hello {student_name}.

    To give you an update on how you are doing in class, you are currently {status} track to move forward to the next module.
        
    As you know, Moringa School looks at 3 major aspects of your learning in considering whether you proceed to the next module:
    Attendance and punctuality.
    Completion and quality of your IPs.
    Positive contributions to the classroom environment; are you working well with others, and interpersonal skills.
        
    As it stands:
    Your attendance out of 100 is {attendance}.
        
    As for your IPs:
    Angular
    IP1 out of 31 you have {ip1}.
    IP2 out of 28 you have {ip2}.
    Python
    IP1 out of 21 you have {ip3}.
    IP2 out of 22 you have {ip4}.
        
    Based on the above scores we recommend that you spend the rest of the module working on keeping up with your attendance, IP submissions and quality, and your interpersonal dynamics. Your work has been good so far, and we want to encourage you to keep the momentum going.
        
    This is an automatic email. Please do not reply to it. Follow up with your TM if you have any questions and fill out this form.
    https://goo.gl/forms/0IirlKjvqZ7Qwyt72

    Best,
    -Classroom Team.
    '''

class StudentReviewParser:
    csv_file=os.path.join(settings.BASE_DIR,"parsers/students_review.csv")
    subject="Student Review"
    def __init__(self):
        pass

    def parse_csv_file(self,sender):
        data=[
            # {"to":"to_email","from":"senders_email","subject":"subject","message":"message"}
        ]
        csv_data=SimpleCsvHandler().read(self.csv_file)
        for d in csv_data:
            m=create_message(d)
            data.append(
                {"sender":sender,"to":d["Email"],"subject":self.subject,"message_text":m}
            )
        return data