import json
import os

import dateutil.parser
from datetime import timezone

from dotenv import load_dotenv
from coned import Coned
from reading import Reading

import mysql.connector

load_dotenv()

CONED_USER = os.getenv("CONED_USER")
CONED_PASS = os.getenv("CONED_PASS")
CONED_TOTP = os.getenv("CONED_TOTP")
OPOWER_ACCOUNT_ID = os.getenv("OPOWER_ACCOUNT_ID")
OPOWER_METER = os.getenv("OPOWER_METER")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASS = os.getenv("MYSQL_PASS")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DB = os.getenv("MYSQL_DB")

coned = Coned(CONED_USER, CONED_PASS, CONED_TOTP, OPOWER_ACCOUNT_ID, OPOWER_METER)

try:
    coned.login()
    usage_json = coned.get_usage()
except Exception as e:
    coned.save_screenshot("error.png")
    raise e

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

cnx = mysql.connector.connect(user=MYSQL_USER,
        password=MYSQL_PASS,
        host=MYSQL_HOST,
        database=MYSQL_DB)
cursor = cnx.cursor()

for r in readings:
    add_reading = ("INSERT IGNORE INTO readings "
                  "(start, end, wh) "
                  "VALUES (%s, %s, %s)")
    data_reading = (r.start_time.astimezone(tz=timezone.utc), r.end_time.astimezone(tz=timezone.utc), r.wh)
    cursor.execute(add_reading, data_reading)

cnx.commit()
cursor.close()
cnx.close()
