from datetime import datetime
from firebase_admin import initialize_app, firestore
from firebase_functions import https_fn, firestore_fn
import google.cloud.firestore
import json

# Firebase Admin SDKの初期化
app = initialize_app()

@https_fn.on_request()
def Update(request):
    firestore_client: google.cloud.firestore.Client = firestore.client()
    userdata = []
    userdatum = firestore_client.collection("userdata").stream()
    for datum in userdatum:
        userdata.append(datum.to_dict())

    return json.dumps(userdata)

@https_fn.on_request()
def UserRegist(request):
    # リクエストボディからJSONを取得
    reqjson = request.get_json()

    firestore_client: google.cloud.firestore.Client = firestore.client()
    userdata = []
    userdatum = firestore_client.collection("userdata").stream()
    for datum in userdatum:
        userdata.append(datum.to_dict())

    # JSONをPythonの辞書に変換
    data = {
        "id": reqjson['id'],
        "iconImage": reqjson['iconImage'],
        "userName": reqjson['userName'],
        "companionDrink": reqjson['companionDrink'],
        "totalTime": reqjson['totalTime'],
        "snsLink" : reqjson['snsLink'],
        "entryTime": reqjson['entryTime'],
        "lang": reqjson['lang']
    }
    index = -1
    for i in userdata:
        if (i['id'] == reqjson['id']):
            index = userdata.index(i)
    
    try:
        userdata[index].update(
            iconImage = data['iconImage'],
            userName = data['userName'],
            companionDrink = data['companionDrink'],
            totalTime = data['totalTime'],
            snsLink = data['snsLink'],
            entryTime = data['entryTime'],
            lang = data['lang']
        )
    except:
        userdata.append(data)
    # レスポンスを返す
    try:
        firestore_client.collection("userdata").document(data['id']).update(userdata[index])
    except:
        firestore_client.collection("userdata").document(data['id']).set(userdata[index])
    return "OK"


@https_fn.on_request()
def UserJoin(request):
    # リクエストボディからJSONを取得
    reqjson = request.get_json()

    firestore_client: google.cloud.firestore.Client = firestore.client()
    userdata = []
    userdatum = firestore_client.collection("userdata").stream()
    for datum in userdatum:
        userdata.append(datum.to_dict())

    # JSONをPythonの辞書に変換
    data = {
        "id" : reqjson['id'],
        "entryTime" : format(datetime.now(),'%Y%m%d%H%M%S'),
    }

    index = -1
    for i in userdata:
        if (i['id'] == reqjson['id']):
            index = userdata.index(i)
    try:
        userdata[index].update(
            entryTime=data['entryTime'],
            )
    except:
        userdata.append(data)
    # レスポンスを返す
    firestore_client.collection("userdata").document(data['id']).update(userdata[index])
    return json.dumps(userdata)

@https_fn.on_request()
def UserLeave(request):
    # リクエストボディからJSONを取得
    reqjson = request.get_json()

    firestore_client: google.cloud.firestore.Client = firestore.client()
    userdata = []
    userdatum = firestore_client.collection("userdata").stream()
    for datum in userdatum:
        userdata.append(datum.to_dict())
    
    index = -1
    for i in userdata:
        if (i['id'] == reqjson['id']):
            index = userdata.index(i)
    
    JoinTime = datetime.strptime(userdata[index]['entryTime'], '%Y%m%d%H%M%S')
    time = datetime.now() - JoinTime
    try:
        totalTime = format(datetime.strptime(userdata[index]['totalTime'], '%H%M%S') + time, '%H%M%S')
    except:
        totalTime = format(datetime.strptime("000000", '%H%M%S') + time, '%H%M%S')
    
    # JSONをPythonの辞書に変換
    data = {
        "id"  : reqjson['id'],
        "totalTime": totalTime
    }

    try:
        userdata[index].update(
            totalTime = totalTime,
            entryTime = ""
        )
    except:
        userdata.append(data)
    # レスポンスを返す
    firestore_client.collection("userdata").document(data['id']).update(data)
    return "OK"