import requests
from requests.auth import HTTPBasicAuth


class Services:
    def __init__(self, base_url, headers=None, auth=None):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth = auth
        if headers:
            self.session.headers.update(headers)

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, params=params, auth=self.auth)

    def post(self, endpoint, data=None, json=None):
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, data=data, json=json, auth=self.auth)


class WhatsAppServices(Services):
    def __init__(self, host, username, password):
        super().__init__(host, auth=HTTPBasicAuth(username, password))

    def checkExists(self, phone, session='default'):
        return self.get('/contacts/check-exists', dict(phone=phone, session=session))

    def startTyping(self, phone, session='default'):
        return self.post("/startTyping", dict(chatId=phone, session=session))

    def stopTyping(self, phone, session='default'):
        return self.post("/stopTyping", dict(chatId=phone, session=session))

    def sendMessage(self, phone, message, session='default'):
        return self.post('/sendText', data={
            "chatId": phone,
            "reply_to": None,
            "text": message,
            "linkPreview": True,
            "session": session,
        })


class SMSServices(Services):
    def __init__(self, host, apikey):
        super().__init__(host)
        self.apikey = apikey

    def sendMessage(self, message: str, number: str):
        return self.post('/send', dict(apikey=self.apikey, message=message, number=number))

    def getBalance(self):
        return self.get('/get/balance', dict(apikey=self.apikey))
