import os
from dotenv import load_dotenv
from twilio.rest import Client

# DEBUG: Should really be loaded onto the environment if app is running already
# load_dotenv()

sid = os.environ['TW_SID']
secret = os.environ['TW_SECRET']


def handle_recording_metadata(recording_sid):

	# TODO -> Obtain and process:
	#  - Price (of the recording)
	#  - Price Unit of recording (USD/GBP)
	#  - Recording SID
	#  - Call SID
	#  - Date/Time captured
	#  - Duration
	#  - Recording status
	#  - Error Code (of the recording) -> May end up null/None

	with Client(sid, secret) as client:
		recording_obj = client.recordings(recording_sid).fetch()


def handle_call_metadata(call_sid):

	# TODO -> Obtain and process:
	#  - call_sid
	#  - Caller Number
	#  - Caller Name
	#  - direction
	#  - from
	#       * from_formatted
	#  - to
	#       * to_formatted
	#  - phone_number_sid
	#  - start_time
	#  - end_time
	#  - status
	#  - Duration (of the call)
	#             -> Length of call in seconds (Value is empty if busy, failed, unanswered or if the call is ongoing)
	#  - Price (of the call)
	#  - Price unit (of the call)
	
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
