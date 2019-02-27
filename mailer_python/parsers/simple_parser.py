import os
from mailer import settings
from mailer.handlers import SimpleCsvHandler


class SimpleCsvEmailParser:
    csv_file=os.path.join(settings.BASE_DIR,"parsers/simple_csv.csv")
    def __init__(self):
        pass

    def parse_csv_file(self,sender,subject):
        data=[
            # {"to":"to_email","from":"senders_email","subject":"subject","message":"message"}
        ]
        csv_data=SimpleCsvHandler().read(self.csv_file)
        for d in csv_data:
            m=self.create_message({"name":d["name"],"score":int(d["score"])/24*100})
            data.append(
                {"sender":sender,"to":d["email"],"subject":subject,"message_text":m}
            )
        return data

    def create_message(self,d):
        return\
        '''
        Hi {},
        Your final score is {}
        Good luck.
        '''\
        .format(d["name"],d["score"])

