import requests
import pprint


def get_event_programs():
	url = 'http://84.252.132.43:8000/api/event-programs/'
	response = requests.get(url)
	response.raise_for_status()

	event_programs = response.json()
	return event_programs
	