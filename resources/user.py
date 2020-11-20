from flask_restful import Resource,reqparse
#處理使用者傳來參數(reqparse,ex:http method:post)
import pymysql
from flask import jsonify
#restful api resorrce
import traceback #印出錯誤訊息

parser = reqparse.RequestParser()
#建立白名單，處理使用者傳來那些欄位
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('note')

class User(Resource): #resource init 處理單一筆user 資料
    def db_init(self):
        db = pymysql.connect('localhost','root','$ssmi119$','api1')
        cursor = db.cursor(pymysql.cursors.DictCursor) #Dic type
        return db,cursor
    
    def get(self,id):
        db,cursor = self.db_init()
        sql = """Select * From api1.users Where id = '{}' and deleted is not True """.format(id)
        cursor.execute(sql)
        db.commit()
        user = cursor.fetchone()
        db.close()

        return jsonify({'data':user})
        #input dic type change to josn type in web

    def patch(self,id):#更新user 特定欄位
        db,cursor = self.db_init()
        arg = parser.parse_args()#使用者傳來參數 dic type
        user = {
            'name':arg['name'],
            'gender':arg['gender'] ,
            'birth':arg['birth'] , 
            'note':arg['note']
        }
        query = []
        for key,value in user.items():
            if value != None:
                query.append(key + " = " + "'{}'".format(value))
        query = ", ".join(query)
        sql = """
            UPDATE `api1`.`users` SET {} WHERE (`id` = {});
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

    def delete(self,id):
        db,cursor = self.db_init()
        sql = """
            UPDATE `api1`.`users` SET deleted = True WHERE (`id` = {});
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


class Users(Resource): #resource init
    def db_init(self):
        db = pymysql.connect('localhost','root','$ssmi119$','api1')
        cursor = db.cursor(pymysql.cursors.DictCursor) #Dic type
        return db,cursor
    
    def get(self):
        db,cursor = self.db_init()
        arg = parser.parse_args()
        sql = 'Select * From api1.users where deleted is not True'
        if arg['gender'] != None:
            sql += ' and gender = "{}"'.format(arg['gender'])
        cursor.execute(sql)
        db.commit()
        users = cursor.fetchall()
        db.close()

        return jsonify({'data':users})
        #input dic type change to josn type in web

    def post(self):
        db,cursor = self.db_init()
        arg = parser.parse_args()#使用者傳來參數 dic type
        user = {
            'name':arg['name'],
            'gender':arg['gender'] or 0,
            'birth':arg['birth'] or '1900-01-01', #給予初始值，非None
            'note':arg['note']
        }
        sql = """
            INSERT INTO `api1`.`users` (`name`, `gender`, `birth`, `note`) VALUES ('{}', '{}', '{}', '{}');
        """.format(user['name'],user['gender'],user['birth'],user['note'])


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

