from datetime import timezone, datetime, date

dt = datetime(2015, 10, 19)
timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
print(dt)
print(timestamp)