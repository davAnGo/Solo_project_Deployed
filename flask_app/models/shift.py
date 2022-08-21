from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash, session
from datetime import datetime



class Shift:
    def __init__(self,data):
        self.id = data['id']
        self.numOfWorkers = ['numOfWorkers']
        self.shift_date = data['shift']
        self.tips = data['tips']
        self.created_at  = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @staticmethod  #validation set, can be used for editing as well
    def validate_hours(hoursFormData):
        is_valid = True
        print(hoursFormData)
        for x in range(6):          
            if len(hoursFormData['numOfHours'+str(x)])<1:
                is_valid = False
                flash("No inputs may be left empty")

        return is_valid

    @classmethod
    def countHours(cls, totalHours):
        sumOfHours = 0
        totalWorkers = 0

        for key in totalHours:
            convertedValue = float(totalHours[key])
            if convertedValue!=0:
                totalWorkers= totalWorkers+1
            print(totalHours[key])
            sumOfHours = sumOfHours + convertedValue
            print("this many workers",totalWorkers)
            print(sumOfHours)        
            session['sumOfHours'] = sumOfHours
            session['totalWorkers'] = totalWorkers
        sumOfHours = session['sumOfHours']
        totalWorkers = session['totalWorkers']
        return sumOfHours, totalWorkers

    @classmethod
    def countMoney(cls, totalMoney):
        sumOfMoney = 0
        convQ = float(totalMoney["quarters"])*.25
        convO = float(totalMoney["ones"])*1
        convF = float(totalMoney["fives"])*5
        convT = float(totalMoney["tens"])*10
        convTw = float(totalMoney["twenties"])*20
        convFif = float(totalMoney["fifties"])*50
        convHun = float(totalMoney["hundreds"])*100
        sumOfMoney = convQ + convO + convF + convT + convTw + convFif + convHun
        session['sumOfMoney'] = sumOfMoney
        sumOfMoney = session['sumOfMoney']
        return(sumOfMoney)

    @classmethod
    def divideMoney(cls,sessionedHours):
        sumOfMoney=session['sumOfMoney']
        sumOfHours=session['sumOfHours']
        totalWorkers=session['totalWorkers']
        session['hourly'] = round(sumOfMoney/sumOfHours,2)
        hourly = session['hourly']
        collectiveCuts = []
        sessionedHoursValues = []

        for workers in sessionedHours:
            sessionedHoursValues.append(sessionedHours[workers])
            eachCut = round(float(sessionedHours[workers])*hourly,2)
            collectiveCuts.append(eachCut)
        print(collectiveCuts)
        print(sessionedHoursValues)
        session['collectiveCuts'] = collectiveCuts
        collectiveCuts = session['collectiveCuts']
        session['sessionedHoursValues'] = sessionedHoursValues
        sessionedHoursValues = session['sessionedHoursValues']

        return hourly, collectiveCuts, sessionedHoursValues

    @classmethod
    def saveShift(cls, shiftData):
        query ="INSERT INTO shifts(shift_date, tips,created_at, updated_at, user_id) VALUES(%(shift_date)s,%(tips)s, NOW(),NOW(),%(user_id)s);"
        print("your shift has been saved")
        return connectToMySQL("tipToolDB").query_db(query, shiftData)
    @classmethod
    def editShift(cls, newShiftData):
        query = "UPDATE shifts SET shift_date = %(shift_date)s, tips = %(tips)s WHERE id = %(id)s;"
        return connectToMySQL("tipToolDB").query_db(query,newShiftData)

    @classmethod
    def deleteShift(cls,shiftID):
        query ="DELETE FROM shifts WHERE id = %(id)s;"
        return connectToMySQL("tipToolDB").query_db(query,shiftID)