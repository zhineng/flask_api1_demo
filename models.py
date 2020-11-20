#資料庫模型，欄位
from server import db 
class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(45))
    gender = db.Column(db.Integer)
    birth = db.Column(db.DateTime)
    note = db.Column(db.Text)
    deleted = db.Column(db.Boolean)

    def __init__(self,name,gender,birth,note,deleted = None):
        self.name = name
        self.gender = gender
        self.birth = birth
        self.note = note
        self.deleted = deleted

    def serialize(self): #api 回傳json，sqlalcmey 獨有資料結構，需改成dic type
        return {
            "name" : self.name,
            "gender" : self.gender,
            "birth" : self.birth,
            "note" : self.note,
            "deleted" : self.deleted
        }

class AccountModel(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer,primary_key=True)
    balance = db.Column(db.String(45))
    account_number = db.Column(db.String(45))
    user_id = db.Column(db.String(45))
    deleted = db.Column(db.Boolean)

    def __init__(self,balance,account_number,user_id,deleted = None):
        self.balance = balance
        self.account_number = account_number
        self.user_id = user_id
        self.deleted = deleted

    def serialize(self): #api 回傳json，sqlalcmey 獨有資料結構，需改成dic type
        return {
            "balance" : self.balance,
            "account_number" : self.account_number,
            "user_id" : self.user_id,
            "deleted" : self.deleted
        }
