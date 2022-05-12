try:
    import requests,uuid,os,ctypes
except Exception as ex:
    print(ex)
    input()
    exit(0)


class Login():
    def __init__(self):
        self.username = input("Username : ")
        self.password = input("Password : ")
        self.req = requests.session()
        self.login()

    def login(self):
        head = {"User-Agent":"Instagram 152.0.0.1.60 Android (28/9; 380dpi; 1080x2147; OnePlus; HWEVA; OnePlus6T; qcom; en_US; 146536611)","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
        
        data = "signed_body=SIGNATURE.{\"jazoest\":\"22283\",\"country_codes\":\"[{\\\"country_code\\\":\\\"1\\\",\\\"source\\\":[\\\"default\\\"]},{\\\"country_code\\\":\\\"966\\\",\\\"source\\\":[\\\"sim\\\"]}]\",\"phone_id\":\"" + str(uuid.uuid4()) + "\",\"enc_password\":\"#PWD_INSTAGRAM:0:0:" + self.password + "\",\"username\":\"" + self.username + "\",\"adid\":\"" + str(uuid.uuid4()) + "\",\"guid\":\"" + str(uuid.uuid4()) + "\",\"device_id\":\"" + str(uuid.uuid4()) + "\",\"google_tokens\":\"[]\",\"login_attempt_count\":\"3\"}"
        
        res = self.req.post("https://i.instagram.com/api/v1/accounts/login/",data=data,headers=head)
        if "logged_in_user" in res.text:
            print("sucssfully login")
            input("sessionid : "+ res.cookies['sessionid'])
            exit(0)
        elif "bad_password" in res.text:
            input("bad password")
            exit(0)

        elif "challenge_required" in res.text:
            api_path = res.json()['challenge']['api_path']
            self.api_challenge(api_path)
        else:
            input(res.text)
            exit(0)
    
    def api_challenge(self,api_path):
        try:
            head = {"User-Agent":"Instagram 152.0.0.1.60 Android (28/9; 380dpi; 1080x2147; OnePlus; HWEVA; OnePlus6T; qcom; en_US; 146536611)","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
                
            res = self.req.get("https://i.instagram.com/api/v1"+api_path,headers=head)
            if "phone_number" in res.text:
                print("0 - "+res.json()['step_data']['phone_number'])
            if 'email' in res.text:
                print("1 - "+res.json()['step_data']['email'])
            if res.text.__contains__("phone_number") and res.text.__contains__("email") == False:
                input("unknown verification method !!")
                exit(0)
            self.api_send_choice(api_path)
        except Exception as ex:pass
    
    def api_send_choice(self,path):
        try:
            head = {"User-Agent":"Instagram 152.0.0.1.60 Android (28/9; 380dpi; 1080x2147; OnePlus; HWEVA; OnePlus6T; qcom; en_US; 146536611)","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
            
            choice = input("Choice : ")
            data = "choice="+choice    
            res = self.req.post("https://i.instagram.com/api/v1"+path,data=data,headers=head)
            if (res.text.__contains__("contact_point")) or (res.text.__contains__("\"resend_delay\":60")):
                print("code Sent To "+res.json()['step_data']['contact_point'])
                self.api_send_code(path)
            else:
                input(res.text)
                exit(0)
        except:pass
    
    def api_send_code(self,path):
        try:
            head = {"User-Agent":"Instagram 152.0.0.1.60 Android (28/9; 380dpi; 1080x2147; OnePlus; HWEVA; OnePlus6T; qcom; en_US; 146536611)","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
            
            code = input("code : ")
            data = "security_code="+code
            res = self.req.post("https://i.instagram.com/api/v1"+path,data=data,headers=head)
            if "logged_in_user" in res.text:
                print("sucssfully login")
                input("sessionid : "+ res.cookies['sessionid'])
                exit(0)
            else:
                input(res.text)
                exit(0)
        except:pass


def main():
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW("Instagram login By RiOS")
        os.system("mode con:cols=74 lines=17")

    Login()

if __name__ == "__main__":
    main()