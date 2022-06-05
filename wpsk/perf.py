import datetime

"""
Simple perfromance tools.
"""

def start() -> datetime:
	return datetime.datetime.now()

def check(dt_start: datetime, info: str = ""):
	dt_end = datetime.datetime.now()
	print (dt_end - dt_start, info)
