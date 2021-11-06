import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, send_from_directory, redirect, url_for, session
from twilio.twiml.voice_response import VoiceResponse
from helpers import telegram

load_dotenv()

# Used as currently being developed/tested on home PC, soon to be deployed onto a VPS
server_url = os.environ['SERVER_URL']

app = Flask(__name__)

# DEBUG: Redirects for testing
REDIRECT_RR = False
REDIRECT_VM = True


@app.route('/answer', methods=['POST', 'GET'])
def voice_answer():
	# Could be used to perform advanced call flow
	call_sid = request.values['CallSid']
	caller = request.values['Caller']  # TODO: Perform call flow
	
	resp = VoiceResponse()
	resp.play(url_for('wait_connected'))
	
	if REDIRECT_RR:
		# Rick Roll test
		resp.play('https://demo.twilio.com/docs/classic.mp3')
	
	
	if REDIRECT_VM:
		# DEBUG
		# resp.hangup()
		return redirect(url_for('voicemail'))
	else:
		return str(resp)
		
	


@app.route('/voicemail', methods=['GET', 'POST'])
def voicemail():
	resp_vm = VoiceResponse()
	resp_vm.play(url_for('vm_greeting'))
	
	resp_vm.record(action=url_for('recording_complete'), method='POST', play_beep=True,
						recording_status_callback=url_for('process_recording'),
						recording_status_callback_method='POST', recordingStatusCallbackEvent=['completed'],
						max_length=30, trim='trim-silence', timeout=5)
	
	# Should only occur if there was an issue trying to catch the recording
	resp_vm.say("Sorry, but it seems the voice message was not recorded.")
	
	return str(resp_vm)


@app.route('/process_recording', methods=['GET', 'POST'])
def process_recording():
	call_sid = request.values['CallSid']
	recording_sid = request.values['RecordingSid']
	recording_status = request.values['RecordingStatus']  # Could be 'failed' or 'completed'
	duration = request.values['RecordingDuration']  # Duration in seconds
	url = request.values['RecordingUrl']
	
	if recording_status == 'completed':
		telegram.upload_vm(recording_sid, call_sid, url)
	elif recording_status == 'failed':
		pass
	else:
		# This shouldn't happen
		pass


@app.route('/wait')
def wait_connected():
	try:
		return send_from_directory(os.getcwd() + '\\assets\\audio\\', 'Wait_1.mp3', as_attachment=True)
	except Exception as e:
		print(e)
		return str(e)


@app.route('/vm_greeting')
def vm_greeting():
	try:
		return send_from_directory(os.getcwd() + '\\assets\\audio\\', 'Unavailable_1.mp3', as_attachment=True)
	except Exception as e:
		print(e)
		return str(e)


@app.route('/recording_complete', methods=['GET', 'POST'])
def recording_complete():
	duration = request.values['RecordingDuration']
	print(f'Recording Duration: {duration}')
	telegram.left_vm()
	return None


if __name__ == '__main__':
	app.run(debug=True)
