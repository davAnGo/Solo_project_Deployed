from pydoc import render_doc
from flask_app import app
from flask_app.models import user, shift
from flask import render_template, redirect, request, session, flash
from datetime import datetime

@app.route("/count/shift/hours", methods = ['POST'])
def countHours():
    totalHours = {
        "numOfHours0":request.form['numOfHours0'],
        "numOfHours1":request.form['numOfHours1'],
        "numOfHours2":request.form['numOfHours2'],
        "numOfHours3":request.form['numOfHours3'],
        "numOfHours4":request.form['numOfHours4'],
        "numOfHours5":request.form['numOfHours5']
    }
    hoursFormData = totalHours
    if not shift.Shift.validate_hours(hoursFormData):
        return redirect('/dashboard')
    shift.Shift.countHours(totalHours)
    session['sessionedHours'] = totalHours
    sessionedHours = session['sessionedHours']
    print("i am the hours of the first input",sessionedHours['numOfHours0'])
    return redirect("/step/two")

@app.route("/step/two")
def inputMoney():
    if "user_id" not in session:
        return redirect("/")
    user_data = {
        'id':session['user_id']
    }
    sumOfHours = session['sumOfHours']
    
    return render_template("tipToolPt2.html",sumOfHours = sumOfHours) #homepage is dashboard for reference

@app.route("/count/shift/money", methods = ['POST'])
def countMoney():
    totalMoney = {
        "quarters":request.form['quarters'],
        "ones":request.form['ones'],
        "fives":request.form['fives'],
        "tens":request.form['tens'],
        "twenties":request.form['twenties'],
        "fifties":request.form['fifties'],
        "hundreds":request.form['hundreds']
    }
    shift.Shift.countMoney(totalMoney)
    return redirect("/loading")

@app.route("/loading")
def showLoading():
    return render_template("loading.html")

@app.route("/split/money", methods = ['POST'])
def divideMoney():
    sessionedHours = session['sessionedHours']
    print("fromfsplitmoney",sessionedHours)
    shift.Shift.divideMoney(sessionedHours)
    return redirect("/end/shift/results")




@app.route("/end/shift/results")
def displayTotals():
    sessionedHoursValues = session['sessionedHoursValues']
    totalWorkers = session['totalWorkers']
    collectiveCuts = session['collectiveCuts']
    print(totalWorkers)
    hourly = session['hourly']
    sumOfHours = session['sumOfHours']
    sumOfMoney = session['sumOfMoney']
    print("I am hourly",hourly)    
    return render_template("display.html", hourly = hourly, sumOfMoney = sumOfMoney, sumOfHours = sumOfHours, sessionedHoursValues = sessionedHoursValues,totalWorkers = totalWorkers, collectiveCuts = collectiveCuts)

@app.route("/save/shift", methods = ['POST'])
def saveShift():
    if "user_id" not in session:
        return redirect("/")
    user_data = {
        'id':session['user_id']
    }
    shiftData = {
        "shift_date":request.form['shift_date'],
        "tips":request.form['tips'],
        "user_id":session['user_id']
    }
    print(shiftData)
    shift.Shift.saveShift(shiftData)
    return redirect("/user/account")

@app.route("/delete/<id>")
def deleteShift(id):
    shiftID ={
        "id":id
    }
    shift.Shift.deleteShift(shiftID)
    print("THIS IS YOUR SHIFT ID",shiftID['id'])
    return redirect("/user/account")
    
@app.route("/edit/shift/<int:id>")
def shiftEditor(id):
    thisShiftID = {
        "id":id
    }
    return render_template("editShift.html", thisShiftID=thisShiftID)

@app.route("/edit/shift/<int:id>", methods=['POST'])
def editShift(id):
    if "user_id" not in session:
        return redirect("/")
        # dont forget to validate
    
    newShiftData ={
        "shift_date":request.form['shift_date'],
        "tips":request.form['tips'],
        "id":id
    }
    shift.Shift.editShift(newShiftData)
    return redirect('/user/account')