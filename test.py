import datetime

iso_str = "2005-07-28T20:43:13+02:00"

dt = datetime.datetime.fromisoformat(iso_str)

print(dt)