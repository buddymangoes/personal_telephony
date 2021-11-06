import os
from dotenv import load_dotenv
from twilio.rest import Client

# DEBUG: Should really be loaded onto the environment if app is running already
# load_dotenv()

sid = os.environ['TW_SID']
secret = os.environ['TW_SECRET']


def handle_recording_metadata(recording_sid):
	with Client(sid, secret) as client:
		recording_obj = client.recordings(recording_sid).fetch()


def handle_call_metadata(call_sid):
	with Client(sid, secret) as client:
		call_obj = client.calls(call_sid).fetch()


def delete_recording(recording_sid):
	try:
		with Client(sid, secret) as client:
			client.recordings(recording_sid).delete()
	except Exception as e:
		print(e)
		return False
	else:
		return True
