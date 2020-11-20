from flask import Flask,request,jsonify
from flask_restful import Api
from resources.user_orm import  Users,User
from resources.account_orm import Accounts,Account 
import pymysql
import traceback
from server import app

api = Api(app) # change to api
api.add_resource(Users,'/users') #route,obect:Users,route /users
api.add_resource(User,'/user/<id>') #動態，輸入id
api.add_resource(Accounts,'/user/<user_id>/accounts') 
api.add_resource(Account,'/user/<user_id>/account/<id>')


@app.route('/')
def index():
    return 'My first Flask Website!!'

@app.route('/user/<user_id>/account/<id>/deposit',methods=['POST'])
def deposit(user_id,id):
    db,cursor,account = get_account(id)
    money = request.get_json()['money']
    balance = account['balance'] + int(money)
    sql = 'Update api1.accounts Set balance = {} Where id = {} and deleted is not True'.format(balance,id)

    response = {}    
    try:
        cursor.execute(sql)
        response['msg'] = 'success'
    except:
        traceback.print_exc()
        response['msg'] = 'failed'

    db.commit()
    db.close()
    return jsonify(response)  

@app.route('/user/<user_id>/account/<id>/withdraw',methods=['POST'])
def withdraw(user_id,id):
    db,cursor,account = get_account(id)
    money = request.get_json()['money']
    balance = account['balance'] - int(money)

    response = {} 

    if balance < 0:
        response['msg'] = 'money not enough'
        return jsonify(response)  
    else:
        sql = 'Update api1.accounts Set balance = {} Where id = {} and deleted is not True'.format(balance,id)  
        try:
            cursor.execute(sql)
            response['msg'] = 'success'
        except:
            traceback.print_exc()
            response['msg'] = 'failed'
        db.commit()
        db.close()
        return jsonify(response)



def get_account(id):
    db = pymysql.connect('localhost','root','$ssmi119$','api1')
    cursor = db.cursor(pymysql.cursors.DictCursor) #Dic type
    sql = 'Select * From api1.accounts where id = "{}" and deleted is not True'.format(id)
    cursor.execute(sql)
    return db,cursor,cursor.fetchone()

if __name__ == '__main__':
    app.debug = False
    app.run(host='127.0.0.1',port=5000)