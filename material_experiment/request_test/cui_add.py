import requests
from urllib3 import encode_multipart_formdata


def test_add():
    api_url = "http://10.2.153.129:7001/test_add"
    headers = {
        "content-type": "application/x-www-form-urlencoded"
        #"content-type": "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"
    }
    data = {
        "name": "name"
    }
    fields = {
        "name": "name1",
        "name2": "name2",
       # "file": open("/Users/heming/Desktop/论文意见.docx", "rb").read()
        # "file": open("report.xls", "rb")
    }
    m = encode_multipart_formdata(fields)
    print(m)
    print(type(m))
    print(m[0])
    print(m[1])

    response = requests.post(api_url, data=m[0], headers=headers)
    print(response)

test_add()