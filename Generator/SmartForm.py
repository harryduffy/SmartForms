from Helpers.user_system import db
from sqlalchemy import orm

class SmartForm(db.Model):

    __tablename__ = 'smartforms'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)

    content = db.Column(db.String(1500), nullable=False)
    question_count = db.Column(db.Integer)
    title = db.Column(db.String(50))

    def init_imitator(self):

        self.question_count = 0
        self.content = ""

    def set_SmartForm_title(self, title):

        self.title = title

    def add_short_question_input(self, question, inline):
        
        self.question_count += 1

        if inline:
            self.content += f'''

                <div id="smartform-inputs-div-{self.question_count}">
                    <h3>{self.question_count}. {question}</h3>
                    <input type="text" id="smartform-inputs" maxlength="250" name="inline-short-{self.question_count}" placeholder="Enter text...">
                </div>
            
            '''
        else:
            self.content += f'''

                <div id="smartform-inputs-div-{self.question_count}">
                    <h3>{self.question_count}. {question}</h3>
                    <input type="text" id="smartform-inputs" maxlength="250" name="break-short-{self.question_count}" placeholder="Enter text...">
                </div>
            
            '''

    def add_long_question_input(self, question):
        
        self.question_count += 1

        self.content += f'''

            <div id="textarea-inputs-div">
                <h3>{self.question_count}. {question}</h3>
                <textarea type="text" id="textarea-inputs" rows="10" cols="auto" name="long-{self.question_count}" placeholder="Enter text..."></textarea>
            </div>
        
        '''

    def add_list_question_input(self, question, values, amount, inline):
        
        self.question_count += 1

        options = ""
        for i in values:
            options += f'<option value="{i}">\n'

        if inline:
            self.content += f'''

                <div id="list-inputs-div">
                    <h3>{self.question_count}. {question}</h3>
                    <input list="datalistOptions" id="data-list-inputs" name="inline-lists-{self.question_count}" placeholder="Type to search...">
                    <datalist id="datalistOptions">
                        {options}
                    </datalist>
                </div>
            
            '''
        else:
            self.content += f'''

            <div id="list-inputs-div">
                <h3>{self.question_count}. {question}</h3>
                <input list="datalistOptions" id="data-list-inputs" name="break-lists-{self.question_count}" placeholder="Type to search...">
                <datalist id="datalistOptions">
                    {options}
                </datalist>
            </div>
        
        '''

    def add_date_input(self, question, inline):
        
        self.question_count += 1

        if inline:
            self.content += f'''

                <div class="smartform-inputs-div">
                    <h3>{self.question_count}. {question}</h3>
                    <input type="date" id="date-smartform-inputs" maxlength="250" name="inline-date-{self.question_count}">
                </div>
            
            '''

        else:
            self.content += f'''

                <div class="smartform-inputs-div">
                    <h3>{self.question_count}. {question}</h3>
                    <input type="date" id="date-smartform-inputs" maxlength="250" name="break-date-{self.question_count}">
                </div>
            
            '''

    def add_address_input(self, question, inline):
        
        self.question_count += 1

        if inline:
            self.content += f'''

                <div class="smartform-inputs-div">
                    <h3>{self.question_count}. {question}</h3>
                    <input type="text" id="address-smartform-inputs" maxlength="250" name="inline-address-{self.question_count}" placeholder="Enter address...">
                </div>
            
            '''
        else:
            self.content += f'''

            <div class="smartform-inputs-div">
                <h3>{self.question_count}. {question}</h3>
                <input type="text" id="address-smartform-inputs" maxlength="250" name="break-address-{self.question_count}" placeholder="Enter address...">
            </div>
        
        '''

    def add_boolean_input(self, question):
        
        self.question_count += 1

        self.content += f'''

            <h4>{self.question_count}. {question}</h4>
            <div>
                <input type="checkbox" name="{self.question_count}" value="True">
                <label>Yes</label>
            </div>
        
        '''

    def clear_content(self):

        self.question_count = 0
        self.content = ""