#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# https://hexchat.readthedocs.io/en/latest/script_python.html

import hexchat
import subprocess
import os
import ConfigParser

__module_name__ = "hexchat-encrypt" 
__module_version__ = "1.0" 
__module_description__ = "hexchat symmetric encryption" 

COLORS = { 'GREEN': "\x0303", 'RED': "\x0304" }
PROCESSING = False
PASSFILE = None
CHANNELS = set()
DEBUG = False
MCHARSIZE = 330
			
def channelServer(ctxt):
	return (ctxt.get_info('channel'), ctxt.get_info('server'))

def textPos(message):
	return COLORS['GREEN'] + message

def textNeg(message):
	return COLORS['RED'] + message

def encrypt(plaintext):
	process = subprocess.Popen(
		["openssl","enc","-aes-256-cbc","-e","-a","-A","-pass","file:" + PASSFILE],
		stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	stdout,stderr = process.communicate(plaintext)      
	if process.returncode == 0: return stdout
	raise Exception(stderr)

def decrypt(cryptogram):
	process = subprocess.Popen(
		["openssl","enc","-aes-256-cbc","-d","-a","-A","-pass","file:" + PASSFILE],
		stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	stdout,stderr = process.communicate(cryptogram)
	if process.returncode == 0: return stdout
	raise Exception(stderr)
		
def send(word, word_eol, userdata):
	ctxt = hexchat.get_context()
	if channelServer(ctxt) in CHANNELS:
		message = word_eol[0]
		try:
			for x in range(0,len(message),MCHARSIZE): 
				hexchat.command('PRIVMSG %s :%s' % 
					(ctxt.get_info('channel'), "HEXCHATENC:" 
						+ encrypt(message[x:x+MCHARSIZE])))
			hexchat.emit_print('Your Message', 
				hexchat.get_info('nick'), textPos(message))
			return hexchat.EAT_HEXCHAT
		except Exception as e:
			ctxt.prnt(textNeg("Could not encrypt!"))
			if DEBUG: ctxt.prnt(str(e))
			return hexchat.EAT_ALL
	return hexchat.EAT_NONE

def receive(word, word_eol, userdata):
	global PROCESSING
	if PROCESSING:
		return hexchat.EAT_NONE
	sender,message = word[0],word[1]
	ctxt = hexchat.get_context()
	if message[:11] == "HEXCHATENC:":
		try:
			plaintext = decrypt(message[11:])
			PROCESSING = True
			ctxt.emit_print('Private Message to Dialog', 
				sender, textPos(plaintext))
			PROCESSING = False
			return hexchat.EAT_HEXCHAT
		except Exception as e:
			ctxt.prnt(textNeg("Could not decrypt!"))
			if DEBUG: ctxt.prnt(str(e))
			return hexchat.EAT_NONE
	return hexchat.EAT_NONE
			
def info(ctxt):
	if channelServer(ctxt) in CHANNELS:
		ctxt.prnt(textPos("Outgoing encryption enabled"))
	else:
		ctxt.prnt(textNeg("Outgoing encryption disabled"))
	return hexchat.EAT_ALL

def enable(ctxt):
	CHANNELS.add(channelServer(ctxt))
	ctxt.prnt(textPos("Encryption enabled"))
	return hexchat.EAT_ALL

def disable(ctxt):
	if channelServer(ctxt) in CHANNELS:
		CHANNELS.remove(channelServer(ctxt))
		ctxt.prnt(textNeg("Encryption disabled"))
	return hexchat.EAT_ALL

def debug(ctxt):
	global DEBUG
	if DEBUG:
		DEBUG = False
		ctxt.prnt("Debug disabled")
	else:
		DEBUG = True
		ctxt.prnt("Debug enabled")
	return hexchat.EAT_ALL

def readConf(section,option):
	confFilePath = hexchat.get_info('configdir') + '/enc.conf'
	if not os.path.isfile(confFilePath): 
		raise IOError(confFilePath)
	config = ConfigParser.ConfigParser()
	config.read(confFilePath)
	return config.get(section,option)

def enc(word,word_eol,userdata):
	ctxt = hexchat.get_context()
	try:
		arg = word[1]
		if arg == "enable":
			enable(ctxt)
		elif arg == "disable":
			disable(ctxt)
		elif arg == "info":
			info(ctxt)
		elif arg == "debug":
			debug(ctxt)
	except Exception:
		pass
	return hexchat.EAT_ALL

def init():
	try:
		filepath = readConf('PASSFILE','path')
		if os.path.isfile(filepath):
			global PASSFILE
			PASSFILE = filepath
			hexchat.prnt(textPos(PASSFILE + " loaded!"))
			hexchat.hook_command('', send)
			hexchat.hook_command('enc',enc)
			hexchat.hook_print('Private Message to Dialog', receive)	
		else:
			raise IOError(filepath)
	except IOError as e:
		hexchat.prnt(textNeg(str(e) + " could not be opened"))
	except Exception as e:
		hexchat.prnt(textNeg(str(e)))	

init()

