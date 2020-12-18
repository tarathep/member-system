from bottle import Bottle, Route, run,response,request
import json
import db

app = Bottle()

#INIT LOAD DATA
members = db.members

@app.route('/')
def hello():
    print("----> GET Hello Member System")
    return 'Hello Member System'

@app.route('/members', method='GET')
def getMember():
    
    print("----> GET MEMBER(S)")
    
    response.content_type="application/json"
    return json.dumps({'members':members})

@app.route('/members/<id>' ,method='GET')
def getMemberById(id):
    response.content_type="application/json"
    
    print("----> GET MEMBER BY ID = "+id)
    
    for inx,i in enumerate(members):
        if(i["id"]==id):
            return json.dumps({'members':members[inx]})
    return json.dumps({'id':None,'name':None,'role':None})

@app.route('/members/<id>' ,method='DELETE')
def deleteMemberById(id):
    response.content_type="application/json"
    
    print("----> DELETE MEMBER BY ID = "+id)
    
    for inx,i in enumerate(members):
        if(i["id"]==id):
            members.remove(i)
            return json.dumps({'id':id,'status':'delete','message':'success'})
    return json.dumps({'id':None,'status':'delete','message':'error'})


@app.route('/members' ,method='POST')
def addMember():
    reqBody = request.body.getvalue().decode('utf-8')
    addData = json.loads(reqBody)

    print("----> ADD MEMBER DATA = ",addData)

    # FIND ID FOR IS DUPLICATE?
    for i in members:
        if(i["id"]==addData["id"]):
            return json.dumps({'id':addData["id"],'status':'add','message':'duplicate id'})
    members.append(addData)
    return json.dumps({'id':addData["id"],'status':'added','message':'success'})
  
@app.route('/members' ,method='PUT')
def editMember():
    reqBody = request.body.getvalue().decode('utf-8')
    updateData = json.loads(reqBody)

    print("----> UPDATE MEMBER DATA = ",updateData)

    # FIND ID FOR UPDATE
    for inx,i in enumerate(members):
        if(i["id"]==updateData["id"]):
            members.remove(i)
            members.append(updateData)
            return json.dumps({'id':updateData["id"],'status':'updated','message':'success'})
    return json.dumps({'id':id,'status':'update','message':'error'})

@app.route('/login', method='POST')
def auth():
    reqBody = request.body.getvalue().decode('utf-8')
    authData = json.loads(reqBody)

    print("----> AUTH MEMBER  = ",authData)

    for inx,i in enumerate(members):
        if(i["email"]==authData["username"] and i["password"]==authData["password"]):
            return json.dumps({'id':i["id"],'name':i["firstName"],'role':i["role"]})
    return json.dumps({'id':None,'name':None,'role':None})


if __name__ == '__main__':
    run(app, host='localhost', port=8080)