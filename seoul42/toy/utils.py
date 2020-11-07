from datetime import datetime, timedelta
import re


def get_weekday_list(selected=None):
	first_weekday = datetime.today() - timedelta(days=datetime.today().weekday())
	weekdays_kr = ["월", "화", "수", "목", "금", "토", "일"]
	weekday_list = {}
	if selected is None:
		selected = range(7)
	for i in selected:
		temp_day = first_weekday + timedelta(days=i)
		weekday_list[i] = {
			'head': f'{temp_day.strftime("%Y%m%d")}({weekdays_kr[i]})',
			'body': f'{temp_day.strftime("%Y-%m-%d")}({weekdays_kr[i]})',
		}
	weekday_numbers = selected
	return weekday_list, weekday_numbers


def change_report_date(content, head, body):
	content = re.sub('[0-9]{2,4}[0-9]{1,2}[0-9]{1,2} {0,1}\([월화수목금토일]\)', head, str(content))
	content = re.sub('[0-9]{2,4}-[0-9]{1,2}-[0-9]{1,2} {0,1}\([월화수목금토일]\)', body, str(content))
	return content
