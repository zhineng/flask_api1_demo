from flask_restful import Resource,reqparse
#處理使用者傳來參數(reqparse,ex:http method:post)
import pymysql
from flask import jsonify
#restful api resorrce
import traceback #印出錯誤訊息

parser = reqparse.RequestParser()
#建立白名單，處理使用者傳來那些欄位
parser.add_argument('balance')
parser.add_argument('account_number')
parser.add_argument('user_id')


class Account(Resource): #resource init 處理單一筆Account 資料
    def db_init(self):
        db = pymysql.connect('localhost','root','$ssmi119$','api1')
        cursor = db.cursor(pymysql.cursors.DictCursor) #Dic type
        return db,cursor
    
    def get(self,user_id,id):
        db,cursor = self.db_init()
        sql = """Select * From api1.accounts Where id = '{}' and deleted is not True """.format(id)
        cursor.execute(sql)
        db.commit()
        account = cursor.fetchone()
        db.close()

        return jsonify({'data':account})
        #input dic type change to josn type in web

    def patch(self,user_id,id):#更新account 特定欄位
        db,cursor = self.db_init()
        arg = parser.parse_args()#使用者傳來參數 dic type
        account = {
            'balance':arg['balance'],
            'account_number':arg['account_number'] ,
            'user_id':arg['user_id']  
                   }
        query = []
        for key,value in account.items():
            if value != None:
                query.append(key + " = " + "'{}'".format(value))
        query = ", ".join(query)
        sql = """
            UPDATE `api1`.`accounts` SET {} WHERE (`id` = {});
        """.format(query,id)

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

    def delete(self,user_id,id):
        db,cursor = self.db_init()
        sql = """
            UPDATE `api1`.`accounts` SET deleted = True WHERE (`id` = {});
        """.format(id)
        
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


class Accounts(Resource): #resource init
    def db_init(self):
        db = pymysql.connect('localhost','root','$ssmi119$','api1')
        cursor = db.cursor(pymysql.cursors.DictCursor) #Dic type
        return db,cursor
    
    def get(self,user_id):
        db,cursor = self.db_init()
        sql = 'Select * From api1.accounts where user_id = "{}" and deleted is not True'.format(user_id)
        cursor.execute(sql)
        db.commit()
        accounts = cursor.fetchall()
        db.close()

        return jsonify({'data':accounts})
        #input dic type change to josn type in web

    def post(self,user_id):
        db,cursor = self.db_init()
        arg = parser.parse_args()#使用者傳來參數 dic type
        accounts = {
            'balance':arg['balance'],
            'account_number':arg['account_number'] ,
            'user_id':arg['user_id']  
                   }
        sql = """
            INSERT INTO `api1`.`accounts` (`balance`, `account_number`, `user_id`) VALUES ('{}', '{}', '{}');
        """.format(accounts['balance'],accounts['account_number'],accounts['user_id'])


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

