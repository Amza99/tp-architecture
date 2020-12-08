# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 20:48:58 2020

@author: Hamza
"""

from flask import Flask
from flask_restful import Resource, Api, reqparse
from DB_Connector import DATABASE as DB 
"""
http://localhost:5000/billets
http://localhost:5000/users
http://localhost:5000/info
http://127.0.0.1:5000/users?Nom=Boukhriss&Prenom=Hamza
http://127.0.0.1:5000/billets?Nom=Bouyahy&Prenom=oumaima&Id_Vol=4

"""
    
    
class Billet(Resource):
    def get(self):#get billet dispo
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('User', required=True)
        Connection = DB()
        Connection = DB()
        data = Connection.Get_Billet_Dispo()
        data = data.to_dict()
        Connection.Close()
        return {'data': data}, 200
    def post(self):#Reservation
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('Mode', required=True)
        parser.add_argument('Id_User', required=True)
        parser.add_argument('Id_Vol', required=True)
        args = parser.parse_args()  # parse arguments to dictionary
        Connection = DB()
        if( args['Mode'] == "Delete" ):
            Connection.Delete_Reservation(args['Id_User'],args['Id_Vol'])
        if( args['Mode'] == "Reserve"):
            Connection.Reservation(args['Id_User'],args['Id_Vol'])
        Connection.Close()
        return {'Status': "Done"}, 200

class Info(Resource):
    def get(self):# get all users reservation 
        Connection = DB()
        data = Connection.Get_ALL_Users_Reservation()
        data = data.to_dict()
        Connection.Close()
        return {'data': data}, 200
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('Id_User', required=True)
        args = parser.parse_args()  # parse arguments to dictionary
        Connection = DB()
        data =  Connection.Get_Reservation_User(args['Id_User'] )
        Connection.Close()
        try:
            data += 1
            return {'Status': "Aucune Reservatio n'est trouver "}, 401
        except:
            data = data.to_dict()
            return {'data': data}, 200
        
class Users(Resource):
    def get(self):# get list users
        Connection = DB()
        data = Connection.Get_All_Users()
        data = data.to_dict()
        Connection.Close()
        return {'data': data}, 200
    def post(self):# create a user
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('Nom', required=True)
        parser.add_argument('Prenom', required=True)
        args = parser.parse_args()  # parse arguments to dictionary
        Connection = DB()
        INDX = Connection.Return_INDX_User_Creat_user_if_not_existe(args['Nom'] ,args['Prenom'] )
        Connection.Close()
        return {'Index': INDX },200


app = Flask(__name__)
api = Api(app)    

api.add_resource(Users, '/users')  
api.add_resource(Billet, '/billets') 
api.add_resource(Info, '/info')  


app.run()
#Connection.Close()