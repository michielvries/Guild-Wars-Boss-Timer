import time
import datetime
from constants import boss_info


def get_message():
    current_unix = int(time.time())
    year = datetime.datetime.utcnow().year
    month = datetime.datetime.utcnow().month
    day = datetime.datetime.utcnow().day

    message = ""

    for i in boss_info:
        boss_hour = int(i[1][0:2])
        boss_minute = int(i[1][3:5])
        boss_unix = int(datetime.datetime(year, month, day, boss_hour, boss_minute).timestamp() + 3600)
        if boss_unix < current_unix - 900:
            boss_unix = int(datetime.datetime(year, month, day + 1, boss_hour, boss_minute).timestamp() + 3600)

        if not current_unix - 900 < boss_unix < current_unix + 3600:
            continue

        if boss_unix < current_unix:
            time_string = "`Active`"
        else:
            time_string = f"<t:{boss_unix}:R> (<t:{boss_unix}:t>)"

        message += f"> **{i[0]}**\n> Time: {time_string}\n> Location: *{i[2]}*, *{i[3]}*\n> Waypoint link: `{i[4]}`\n\n"

    return message.strip()
