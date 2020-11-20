from flask_restful import Resource,reqparse
#處理使用者傳來參數(reqparse,ex:http method:post)
import pymysql
from flask import jsonify
#restful api resorrce
import traceback #印出錯誤訊息
from server import db 
from models import AccountModel

parser = reqparse.RequestParser()
#建立白名單，處理使用者傳來那些欄位
parser.add_argument('balance')
parser.add_argument('account_number')
parser.add_argument('user_id')


class Account(Resource): #resource init 處理單一筆Account 資料 
    def get(self,user_id,id):
        account = AccountModel.query.filter_by(id=id,deleted=None).first()
        return jsonify({'data':account.serialize()})

    def patch(self,user_id,id):#更新account 特定欄位
        arg = parser.parse_args()#使用者傳來參數 dic type
        account = AccountModel.query.filter_by(id=id,deleted=None).first()
        if arg['balance'] != None:
            account.balance = arg['balance']   
        if arg['account_number'] != None:
            account.account_number = arg['account_number'] 
        if arg['user_id'] != None:
            account.user_id = arg['user_id'] 
        response = {}    
        try:
            db.session.commit()
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        return jsonify(response)  

    def delete(self,user_id,id):
        account = AccountModel.query.filter_by(id=id,deleted=None).first()
        response = {}    
        try:
            db.session.delete(account)
            db.session.commit()
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        return jsonify(response) 


class Accounts(Resource): #resource init  
    def get(self,user_id):
        accounts = AccountModel.query.filter(AccountModel.user_id == user_id).filter(AccountModel.deleted.isnot(True)).all()
        return jsonify({'data':list(map(lambda account:account.serialize(),accounts))})

    def post(self,user_id):
        arg = parser.parse_args()#使用者傳來參數 dic type
        accounts = {
            'balance':arg['balance'],
            'account_number':arg['account_number'] ,
            'user_id':arg['user_id']  
                   }
        response = {}    
        try:
            new_account = AccountModel(balance = accounts['balance'],account_number = accounts['account_number'],user_id = accounts['user_id'] )
            db.session.add(new_account)
            db.session.commit()
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        return jsonify(response)        

