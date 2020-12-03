# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 20:48:58 2020

@author: Hamza
"""

from flask import Flask
from flask_restful import Resource, Api, reqparse
import DB_Connector as DB 
"""
http://localhost:5000/billets
http://localhost:5000/users
http://localhost:5000/info
http://127.0.0.1:5000/users?Nom=NOM_TEST&Prenom=Prenom_TEST
http://127.0.0.1:5000/billets?Nom=Prenom_TEST&Prenom=Prenom_TEST&Id_Vol=1

"""
    
    
class Billet(Resource):
    def get(self):#get billet dispo
        Connection = DB.DATABASE()
        data = Connection.Get_Billet_Dispo()
        data = data.to_dict()
        Connection.Close()
        return {'data': data}, 200
    def post(self):#Reservation
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('Nom', required=True)
        parser.add_argument('Prenom', required=True)
        parser.add_argument('Id_Vol', required=True)
        args = parser.parse_args()  # parse arguments to dictionary
        Connection = DB.DATABASE()
        if( Connection.Reservation_User_NP_ID_VOL(args['Nom'] ,  args['Prenom'] ,args['Id_Vol'] ) ==  -1 ):
            return {'Status':'Vol indisponible'},200
        Connection.Close()
        return {'Status':'Done'},200

class Info(Resource):
    def get(self):# get all users reservation 
        Connection = DB.DATABASE()
        data = Connection.Get_ALL_Users_Reservation()
        data = data.to_dict()
        Connection.Close()
        return {'data': data}, 200
        
class Users(Resource):
    def get(self):# get list users
        Connection = DB.DATABASE()
        data = Connection.Get_All_Users()
        data = data.to_dict()
        Connection.Close()
        return {'data': data}, 200
    def post(self):# create a user
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('Nom', required=True)
        parser.add_argument('Prenom', required=True)
        args = parser.parse_args()  # parse arguments to dictionary
        Connection = DB.DATABASE()
        Connection.Insert_New_User(args['Nom'] ,args['Prenom'] )
        Connection.Close()
        return {'Status':'Done'},200


app = Flask(__name__)
api = Api(app)    

api.add_resource(Users, '/users')  
api.add_resource(Billet, '/billets') 
api.add_resource(Info, '/info')  


app.run()
#Connection.Close()