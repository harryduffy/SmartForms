from sqlalchemy import orm
from Helpers.user_system import db

class PDF(db.Model):

    __tablename__ = 'pdfs'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)

    content = db.Column(db.String(1500), nullable=False)
    title = db.Column(db.String(1500))

    def init_imitator(self):

        self.checkbox_answers = {}
        self.content = ""

    def set_title(self, smartform_name):

        self.title = smartform_name

    def add_text(self, content):
        
        self.content += content

    def add_boolean_text(self, text_on, text_off):
        
        self.checkbox_answers[text_on] = text_off

    def clear_content(self):

        self.content = ""

    def add_text_answer_holder(self, inline):

        if inline:
            self.content += " <div id='text-question-answer' style='color: #808080; display: inline;'><i>->text question answer<-</i></div> "
        else:
            self.content += " <div id='text-question-answer' style='color: #808080; display: block;'><i>->text question answer<-</i></div> "

    def add_list_answer_holder(self, inline):

        if inline:
            self.content += " <div id='lists-question-answer' style='color: #808080; display: inline;'><i>->list answer<-</i></div> "
        else:
            self.content += " <div id='lists-question-answer' style='color: #808080; display: block;'><i>->list answer<-</i></div> "

    def add_date_holder(self, inline):

        if inline:
            self.content += " <div id='date-question-answer' style='color: #808080; display: inline;'><i>->date answer<-</i></div> "
        else:
            self.content += " <div id='date-question-answer' style='color: #808080; display: block;'><i>->date answer<-</i></div> "

    def add_address_holder(self, inline):

        if inline:
            self.content += " <div id='address-question-answer' style='color: #808080; display: inline;'><i>->address answer<-</i></div> "
        else:
            self.content += " <div id='address-question-answer' style='color: #808080; display: block;'><i>->address answer<-</i></div> "

    def add_checkbox_holder(self):

        self.content += " <div style='color: #808080'><i>->checkbox answer<-</i></div> "