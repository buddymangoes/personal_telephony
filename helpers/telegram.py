import os
from dotenv import load_dotenv
from helpers.twilio import delete_recording
from telegram import Bot
from telegram.constants import PARSEMODE_MARKDOWN_V2
from telegram.error import (BadRequest, NetworkError,   InvalidToken,   Unauthorized,
                            TimedOut,   Conflict,       RetryAfter,     TelegramError)

load_dotenv()

DEV = os.environ['DEVELOPER_CHAT_TOKEN']
bot_token = os.environ['TELEGRAM_BOT_TOKEN']
bot = Bot(token=bot_token)


def upload_vm(recording_sid, call_sid, recording_url):
	
	# TODO: Lookup after completing issue: #12
	name = None
	number = None
	timestamp = None
	
	try:
		# Docs: https://python-telegram-bot.readthedocs.io/en/stable/telegram.bot.html#telegram.Bot.send_voice
		msg = bot.send_voice(voice=recording_url, filename=recording_sid, chat_id=DEV, parse_mode=PARSEMODE_MARKDOWN_V2,
								timeout=60,  # Timeout in seconds
								caption=f'New recording - {timestamp}'
										f'Name: {name}\n'
										f'Number: {number}\n')
	
	except BadRequest as e:
		# Raised when Telegram could not process the request correctly
		print(e)
	except TimedOut as e:
		# Raised when a request took too long to finish
		print(e)
	except NetworkError as e:
		# Base class for exceptions due to networking errors
		print(e)
	except Conflict as e:
		# Raised when a long poll or webhook conflicts with another one
		print(e)
	except InvalidToken as e:
		# Raised when the token is invalid
		print(e)
	except RetryAfter as e:
		# Raised when flood limits where exceeded
		print(e)
	except Unauthorized as e:
		# Raised when the bot has not enough rights to perform the requested action
		print(e)
	except TelegramError as e:
		# Base class for Telegram errors
		print(e)
	except Exception as e:
		print(e)
		raise
	
	else:
		# Post was successful
		# DEBUG
		# delete_recording(recording_sid)
		file_id = msg.voice.file_id


def left_vm():
	bot.send_message(parse_mode=PARSEMODE_MARKDOWN_V2, chat_id=DEV, text=f'*A caller has just left a voicemail*\n'
																		 f'expect a voicemail soon')
