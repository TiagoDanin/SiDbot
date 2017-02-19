#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from utils.database import *
from utils.help import *
from utils.methods import sendFalid
from utils.tools import add_log, regex
from config import plugins_list, debug, api_list, send_falid_plugin, dev_mode
from objectjson import ObjectJSON
from importlib import import_module as import_plugin
import threading

add_log('Bot....',
		'Bot Run!', True)

class run_plugin(threading.Thread):
	def __init__(self, msg_text, chat_id, bot_type):
		threading.Thread.__init__(self)
		self.msg_text    = msg_text
		self.chat_id 	 = chat_id
		self.bot_type    = bot_type
		if debug:
			#I need some privacy here ;-;
			self.debug = debug
		if send_falid_plugin:
			self.send_falid_plugin = send_falid_plugin
		if dev_mode:
			self.dev_mode = dev_mode

	def run(self):
		for plugin in plugins_list:
			res = import_plugin('plugins.{plugin}'.format(plugin=plugin))
			for patt in res.patterns:
				matches = regex(patt, self.msg_text)
				if matches:
					self.plugin = plugin
					self.matches = matches
					self.trigger = patt

					if self.debug:
						add_log('{cmd} - {plugin}: {text} '.format(
								cmd = patt,
								plugin = plugin,
								text = self.msg_text
							),
							'[TRIGGER]'
						)

					if self.dev_mode:
						res.run(self,  matches.group(1), matches)
					else:
						try:
							res.run(self,  matches.group(1), matches)
						except Exception as err:
							add_log('Failed run_plugin: {}'.format(err),
								'Error in bot!',
								True, True
							)
							if self.send_falid_plugin:
								sendFalid(self, title='BOT', reason='generic')

def start_plugin(msg_text, chat_id, bot_type):
	try:
		run_plugin(msg_text, chat_id, bot_type).start()
	except Exception as err:
		add_log('Failed start_plugin: {}'.format(err),
			'Error in bot!',
			True, True
		)

def start_bot():
	if 'cli' in api_list:
		while True:
			msg_text = input('Say: /')
			start_plugin(
				msg_text = '/' + msg_text,
				chat_id = 12345,
				bot_type = 'cli'
			)
try:
	start_bot()
except Exception as error:
	add_log('B O T: {}'.format(error), 'Stop Bot', True, True)
	exit()
