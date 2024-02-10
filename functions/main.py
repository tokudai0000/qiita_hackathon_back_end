import datetime
import zoneinfo
import google.cloud.firestore
import firebase_admin
from firebase_admin import firestore, initialize_app
from firebase_functions import firestore_fn, https_fn

# Firebase Admin SDKの初期化
app = initialize_app()

# Firestoreクライアントの取得
db = firestore.client()

collection = "userdata"

@https_fn.on_request()
def UserJoin(request):
    # リクエストボディからJSONを取得
    request_json = request.get_json()

    # JSONをPythonの配列に変換
    data_array = []
    for item in request_json:
        data_array.append({ 
            "UUID": item["UUID"],
            "lang": item["lang"],
        }
    )

    # Firestoreにデータを格納
    collection_ref = db.collection(collection)
    document_ref = collection_ref.document(data_array["UUID"])
    document_ref.set({"data": data_array})

    # レスポンスを返す
    return "OK"