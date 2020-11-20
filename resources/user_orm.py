from flask_restful import Resource,reqparse
#處理使用者傳來參數(reqparse,ex:http method:post)
import pymysql
from flask import jsonify
#restful api resorrce
import traceback #印出錯誤訊息
from server import db
from models import UserModel



parser = reqparse.RequestParser()
#建立白名單，處理使用者傳來那些欄位
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

class User(Resource): #resource init 處理單一筆user 資料

    def get(self,id):
        user = UserModel.query.filter_by(id=id,deleted=None).first()
        return jsonify({'data':user.serialize()})
    def patch(self,id):#更新user 特定欄位
        arg = parser.parse_args()#使用者傳來參數 dic type
        user = UserModel.query.filter_by(id=id,deleted=None).first()
        if arg['name'] != None:
            user.name = arg['name']   
        if arg['gender'] != None:
            user.gender = arg['gender'] 
        if arg['birth'] != None:
            user.birth = arg['birth'] 
        if arg['note'] != None:
            user.note = arg['note']                
        response = {}    
        try:
            db.session.commit()
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'

        return jsonify(response)  

    def delete(self,id):
        user = UserModel.query.filter_by(id=id,deleted=None).first()
        response = {}    
        try:
            db.session.delete(user)
            db.session.commit()
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        return jsonify(response) 

class Users(Resource): #resource init
    
    def get(self,id):
        users = UserModel.query.filter(UserModel.deleted.isnot(True)).all()
        return jsonify({'data':list(map(lambda user:user.serialize(),users))})

    def post(self):
        arg = parser.parse_args()#使用者傳來參數 dic type
        user = {
            'name':arg['name'],
            'gender':arg['gender'] or 0,
            'birth':arg['birth'] or '1900-01-01', #給予初始值，非None
            'note':arg['note']
        } 
        response = {}    
        try:
            new_user = UserModel(name=user['name'],gender= user['gender'],birth=user['birth'],note=user['note'])
            db.session.add(new_user)
            db.session.commit()
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'

        return jsonify(response)        

