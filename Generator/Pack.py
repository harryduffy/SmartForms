from Exceptions.exceptions import InvalidArgument
from Helpers.user_system import db
import pickle

class Pack(db.Model):

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    smartforms = db.Column(db.PickleType, nullable=False)
    user = db.Column(db.Integer, nullable=False)

    def add_to_pack(self, SmartForm):

        smartform_loaded = pickle.loads(self.smartforms)

        if type(SmartForm) == "SmartForm":
            smartform_loaded.append(SmartForm)
            self.smartforms = pickle.dumps(smartform_loaded)
        else:
            raise InvalidArgument("Error: invalid SmartForm argument")

        
