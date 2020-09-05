import json
import os

# import pickle
import dateutil.parser

from dotenv import load_dotenv
from coned import Coned
from reading import Reading

load_dotenv()

CONED_USER = os.getenv("CONED_USER")
CONED_PASS = os.getenv("CONED_PASS")
CONED_TOTP = os.getenv("CONED_TOTP")
OPOWER_ACCOUNT_ID = os.getenv("OPOWER_ACCOUNT_ID")
OPOWER_METER = os.getenv("OPOWER_METER")

coned = Coned(CONED_USER, CONED_PASS, CONED_TOTP, OPOWER_ACCOUNT_ID, OPOWER_METER)

try:
    coned.login()
    usage_json = coned.get_usage()
except Exception as e:
    coned.save_screenshot("error.png")
    raise e

# Save cookies for use next time
# cookies = driver.get_cookies()
# pickle.dump(cookies, open("cookies.dat","wb"))

usage = json.loads(usage_json)

readings = []
for read in usage["reads"]:
    # Opower gives readings with null value for intervals that don't have data
    # yet, so skip them.
    if read["value"] is None:
        continue

    reading = Reading(
        dateutil.parser.isoparse(read["startTime"]),
        dateutil.parser.isoparse(read["endTime"]),
        usage["unit"],
        read["value"],
    )
    readings.append(reading)

for r in readings:
    print(f"Start: {r.start_time}\tDuration: {r.duration()}\tWh: {r.wh}")
