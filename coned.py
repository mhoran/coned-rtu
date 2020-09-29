import json
import mechanize
import pyotp


class Coned:
    def __init__(self, user, password, totp, account_id, meter):
        self.user = user
        self.password = password
        self.totp = totp
        self.account_id = account_id
        self.meter = meter

        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)

    def opower_usage_url(self):
        return f"https://cned.opower.com/ei/edge/apis/cws-real-time-ami-v1/cws/cned/accounts/{self.account_id}/meters/{self.meter}/usage"  # noqa

    def login(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.coned.com/',
            'Content-Type': 'application/json',
            'Origin': 'https://www.coned.com'}
        data = json.dumps({
            "LoginEmail": self.user,
            "LoginPassword": self.password,
            "LoginRememberMe": False,
            "ReturnUrl": "",
            "OpenIdRelayState": ""})
        request = mechanize.Request(
            "https://www.coned.com/sitecore/api/ssc/ConEd-Cms-Services-Controllers-Okta/User/0/Login", data, headers)
        self.browser.open(request)

        totp = pyotp.TOTP(self.totp)
        thing = json.dumps({
            "MFACode": totp.now(),
            "ReturnUrl": "",
            "OpenIdRelayState": ""})
        request = mechanize.Request(
            'https://www.coned.com/sitecore/api/ssc/ConEd-Cms-Services-Controllers-Okta/User/0/VerifyFactor', thing, headers)
        response = self.browser.open(request)
        redirect_url = json.loads(response.read())["authRedirectUrl"]
        response = self.browser.open(redirect_url)

    def get_usage(self):
        response = self.browser.open(
            "https://cned.opower.com/ei/x/e/usage-export?utilityCustomerId=b6f0dd6b12999567636a5db8d79d7538c73706096ee72c5320735813249743cd")
        self.browser.select_form(id="appForm")
        response = self.browser.submit()

        # Get the usage from opower
        response = self.browser.open(self.opower_usage_url())
        return response.read()
