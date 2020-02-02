import requests, json
from thrift.transport.THttpClient import THttpClient
from thrift.protocol.TCompactProtocol import TCompactProtocol
from boteater_lib import BoteaterService
from boteater_lib.ttypes import *

my_token = None   ##CHROME HEADER TOKEN // NONE FOR QR LOGIN

def qrLogin():
    headers= {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
        "X-Line-Application": "CHROMEOS\t2.3.2\tChrome OS\t1",
        "x-lal": "en_ID",
        "X-Line-Carrier": "51010,1-0"
    }
    sys_name = "BE-Team"
    transport = THttpClient("https://ga2.line.naver.jp" + '/api/v4/TalkService.do')
    transport.setCustomHeaders(headers)
    protocol = TCompactProtocol(transport)
    talk = BoteaterService.Client(protocol)
    qr_code = talk.getAuthQrcode(keepLoggedIn=True, systemName=sys_name, returnCallbackUrl=True)
    transport.close()
    print(qr_code.callbackUrl)
    headers["X-Line-Access"] = qr_code.verifier
    transport = THttpClient("https://ga2.line.naver.jp" + '/api/v4p/rs')
    transport.setCustomHeaders(headers)
    protocol = TCompactProtocol(transport)
    auth = BoteaterService.Client(protocol)
    get_access = json.loads(requests.get("https://ga2.line.naver.jp" + '/Q', headers=headers).text)
    login_request = LoginRequestStruct()
    login_request.type = 1
    login_request.identityProvider = 1
    login_request.keepLoggedIn = True
    login_request.systemName = sys_name
    login_request.verifier = get_access['result']['verifier']
    result = auth.loginZ(login_request)
    transport.close()
    return result.authToken

def getMid(my_token):
    headers= {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
        "X-Line-Application": "CHROMEOS\t2.3.2\tChrome OS\t1",
        "x-lal": "en_ID",
        "X-Line-Carrier": "51010,1-0"
    }
    headers["X-Line-Access"] = my_token
    transport = THttpClient("https://ga2.line.naver.jp" + '/api/v4/TalkService.do')
    transport.setCustomHeaders(headers)
    protocol = TCompactProtocol(transport)
    talk = BoteaterService.Client(protocol)
    mid = talk.getProfile().mid
    transport.close()
    return mid
    
list_country = ['cn', 'es', 'hk', 'id', 'jp', 'kr', 'mx', 'my', 'sa', 'sg', 'th', 'us', 'vn', 'ph', 'in']
print("1. Download Free Region Sticker")
print("2. Download Paid Region Sticker")
print("3. Free Sticker List")
select = int(input("Select option: "))
if select in [1,2,3]:
    print("Region List : {}".format(list_country))
    region = input("Input region: ")
    if region in list_country:
        if select == 1:
            if my_token == None:
                my_token = qrLogin()
            my_mid = getMid(my_token)
            product_id = input("Sticker ID : ")
            data = {}
            data["to"] = my_mid
            data["token"] = my_token
            data["header"] = "chrome"
            data["type"] = "free"
            data["id"] =  product_id
            result = json.loads(requests.post("http://"+region+".line.boteater.us/get_sticker, data=data).text)
            print(result)
        if select == 2:
            if my_token == None:
                my_token = qrLogin()
            my_mid = input("Reciever MID : ")
            product_id = input("Sticker ID : ")
            data = {}
            data["to"] = my_mid
            data["token"] = my_token
            data["header"] = my_app
            data["type"] = "paid"
            data["id"] =  product_id
            result = json.loads(requests.post("http://"+region+".line.boteater.us/get_sticker, data=data).text)
            print(result)
        if select == 3:
            result = json.loads(requests.get("http://"+region+".line.boteater.us/list_sticker").text)
            for data in result["result"]:
                print("Name : " + data["name"])
                print("Author : " + data["author"])
                print("ID : " + data["id"])
                print("Link : https://store.line.me/officialaccount/event/sticker/" + data["id"])
                print("")
    else:
        raise Exception("[ Error ] Wrong region")
else:
    raise Exception("[ Error ] Wrong option")
