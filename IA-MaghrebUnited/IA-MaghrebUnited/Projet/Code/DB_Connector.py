# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 14:49:21 2020

@author: Hamza
"""
import sqlite3 , pandas 
class DATABASE:
    def __init__(self):
        self.connection = sqlite3.connect('DATABASE.db')
        self.cursor = self.connection.cursor()
    def Get_All_Users(self):
        self.cursor.execute("SELECT * FROM Users ;")
        data = pandas.DataFrame(self.cursor.fetchall(),columns =["Id_Users","Nom","Prenom"]) 
        return data
    def Get_All_Billet(self):
        self.cursor.execute("SELECT * FROM Billet ;")
        return self.cursor.fetchall()
    def Get_Number_of_Users(self):
        self.cursor.execute("SELECT COUNT(Id_Users) from Users;")
        return self.cursor.fetchall()[0][0]
    def Reservation(self , Indx_Users , Indx_Vol ):
        query = " INSERT INTO User_Reservation VALUES("+str(Indx_Users)+","+str(Indx_Vol)+")"
        self.Run_Query(query)
    def Insert_New_User(self,Nom,Prenom):
        New_Index = self.Get_Number_of_Users()+1
        query = "INSERT INTO Users VALUES ("+str(New_Index)+", '"+Nom+"','"+Prenom+"')"
        self.Run_Query(query)
    def Get_Billet_Dispo(self):
        query = """
        SELECT Id_Billet , AA.Nom_Airoport as Fromm , A.Nom_Airoport as too , Prix , Date(_Date_)  , NB_Billet_Dispo  FROM Billet as B
        INNER JOIN Airoport_ID as A on A.Id_Airoport = B.ID_Destination
        INNER JOIN Airoport_ID as AA on AA.Id_Airoport = B.ID_Provenance
        where NB_Billet_Dispo != 0
        """
        self.cursor.execute(query)
        data = pandas.DataFrame(self.cursor.fetchall(),columns =["Id_Billet","From","To","Price","Date","Billet_Dispo"]) 
        return data
    def Get_ALL_Users_Reservation(self):
        query = """
        SELECT Id_Billet ,U.Nom as NOM , U.Prenom as Prenom , AA.Nom_Airoport as Fromm , A.Nom_Airoport as too , Date(_Date_) FROM Billet as B
        INNER JOIN Airoport_ID as A on A.Id_Airoport = B.ID_Destination
        INNER JOIN Airoport_ID as AA on AA.Id_Airoport = B.ID_Provenance
        INNER JOIN User_Reservation as UR on UR.Id_Vol = B.Id_Billet
        INNER JOIN Users as U on U.Id_Users = UR.Id_User
        """
        self.cursor.execute(query)
        data = pandas.DataFrame(self.cursor.fetchall(),columns =["Id_Billet","Nom","Prenom","From","To","Date"]) 
        return data
    def Get_ID_User(self,Nom,Prenom):
        self.cursor.execute("SELECT Id_Users FROM Users as U where Nom like '"+Nom+"' and Prenom like '"+Prenom+"' ")
        out  = self.cursor.fetchall()
        if len( out ) == 0 :
            return None
        return out[0][0]
    def Reservation_User_NP_ID_VOL(self,Nom,Prenom,Id_Vol):
        # on test si le billet existe ou n'est pas dispo 
        self.cursor.execute("SELECT * FROM Billet as B where NB_Billet_Dispo != 0 and Id_Billet like "+str(Id_Vol))
        if len(self.cursor.fetchall()) == 0 :
            return -1
        if( self.Get_ID_User(Nom,Prenom) == None ):# si l'utilisateur n'existe pas on le creer 
            self.Insert_New_User(Nom,Prenom)
        Indx_User = self.Get_ID_User(Nom,Prenom)# on recupere son ID 
        self.Reservation(Indx_User,Id_Vol)
        #on decremente le nombre de billet 
        self.Run_Query("Update Billet Set NB_Billet_Dispo=NB_Billet_Dispo-1 where Id_Billet like "+str(Id_Vol))
    def Run_Query(self , query):
        self.cursor.execute( query )
        self.connection.commit()
    def Close(self):
        self.cursor.close()
        self.connection.close()
                
        
    