import os
import pickle
import sys

from dotenv import load_dotenv
from coned import Coned

load_dotenv()

CONED_USER = os.getenv("CONED_USER")
CONED_PASS = os.getenv("CONED_PASS")
CONED_TOTP = os.getenv("CONED_TOTP")
OPOWER_ACCOUNT_ID = os.getenv("OPOWER_ACCOUNT_ID")
OPOWER_METER = os.getenv("OPOWER_METER")

coned = Coned(CONED_USER, CONED_PASS, CONED_TOTP, OPOWER_ACCOUNT_ID, OPOWER_METER)

coned.init()
coned.login()
usage = coned.get_usage()
print(usage)

# Save cookies for use next time
# cookies = driver.get_cookies()
# pickle.dump(cookies, open("cookies.dat","wb"))
