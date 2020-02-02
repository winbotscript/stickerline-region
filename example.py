import requests, json


list_country = ['cn', 'es', 'hk', 'id', 'jp', 'kr', 'mx', 'my', 'sa', 'sg', 'th', 'us', 'vn', 'ph', 'in']
list_header = ["ios_ipad", "chrome", "ios", "android_lite"]
print("1. Download Free Region Sticker")
print("2. Download Paid Region Sticker")
print("3. Free Sticker List")
select = int(input("Select option: "))
if select in [1,2,3]:
    print("Region List : {}".format(list_country))
    region = input("Input region: ")
    if region in list_country:
        if select == 1:
            my_token = input("Your token : ")
            my_mid = input("Your MID : ")
            print("Header List : {}".format(list_header))
            my_app = input("Token header : ")
            product_id = input("Sticker ID : ")
            if my_app in list_header:
                data = {}
                data["to"] = my_mid
                data["token"] = my_token
                data["header"] = my_app
                data["type"] = "free"
                data["id"] =  product_id
                result = json.loads(requests.post("http://"+region+".line.boteater.us/get_sticker, data=data).text)
                print(result)
            else:
                raise Exception("[ Error ] Wrong header")
        if select == 2:
            my_token = input("Your token : ")
            my_mid = input("Reciever MID : ")
            print("Header List : {}".format(list_header))
            my_app = input("Token header : ")
            product_id = input("Sticker ID : ")
            if my_app in list_header:
                data = {}
                data["to"] = my_mid
                data["token"] = my_token
                data["header"] = my_app
                data["type"] = "paid"
                data["id"] =  product_id
                result = json.loads(requests.post("http://"+region+".line.boteater.us/get_sticker", data=data).text)
                print(result)
            else:
                raise Exception("[ Error ] Wrong header")
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
