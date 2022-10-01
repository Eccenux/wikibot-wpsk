import datetime
import logging

"""
Simple perfromance tools.
"""

def start() -> datetime:
	return datetime.datetime.now()

def check(dt_start: datetime, info: str = ""):
	dt_end = datetime.datetime.now()
	logging.info(f'perf: {dt_end - dt_start} {info}')
