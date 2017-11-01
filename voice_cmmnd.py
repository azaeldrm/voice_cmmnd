#==========LOADING==========
import speech_recognition as sr
import os
import time
from mutagen.mp3 import MP3
from gtts import gTTS
import threading


print ('Loading: ...')

path = '' # Insert your path here
start_dir = os.getcwd()
path_list = os.listdir(path)
for i in range(len(path_list)):
	path_list[i] = path_list[i].lower()
f_range = range(len(path_list))
commands = {1:'open ',2:'stop'}

open_r = 'Opening '
text_file = 'text_speech.mp3'
soundfile = path + text_file
r = sr.Recognizer()
r.energy_threshold = 4000


#========FUNCTIONS========
def substring_after(sentence, delimiter):
	return sentence.partition(delimiter)[2]

def execute_prog():
	global execute
	return os.system('"' + execute + '"')

def get_speech(sentence):
	tts = gTTS(sentence, lang='en')
	tts.save(text_file)
	os.system(text_file)
	audio = MP3(soundfile)
	print (sentence)
	time.sleep(audio.info.length+0.25)

def appending(p):
	global path_list, execute, response
	execute = path_list[p]
	response = execute[:execute.rfind(".")]
	response_list.append(response)
	execute_list.append(execute)

def catch_voice():
	global text_input
	with sr.Microphone() as source:
		try:
			print ()
			print ('Speak now.')
			audio = r.listen(source, phrase_time_limit = 5)
			print ('Done!')
			text_input = r.recognize_google(audio).lower()
			if text_input != '':
				print ("You've said: ")
				print (text_input)
				print ()
		except sr.WaitTimeoutError:
			print ('Timeout error. Will try again.')
			pass
		except sr.UnknownValueError:
			print ('Unknown value error. Will try again.')
			pass

def sorting_results():
	global text_output_list, text_output, path_list, execute_list, response_list
	f_range = range(len(path_list))
	o_range = range(len(text_output_list))
	execute_list = []
	response_list = []

	if len(text_output_list) > 1:
		for f in f_range:
			for o in o_range[1:]:
				text_output = text_output_list[o-1] + ' ' + text_output_list[o]
				if text_output in path_list[f]:
					appending(f)
					print (True)

		if len(execute_list) == 0:
			for f in f_range:
				for o in o_range:
					text_output = text_output_list[o]
					if text_output in path_list[f]:
						appending(f)
						print (True)

	elif len(text_output_list) == 1:
		for f in f_range:
			if text_output in path_list[f]:
				appending(f)
				print (True)


#==========STARTING CODE==========
print ()
print ("============PROGRAM BEGINS====================")
print ()

if path == '':
	print ('Verify that you''ve set up a path for this program to run.')
	input()
	break

os.chdir(path)

while True:

	text_input = ''

	catch_voice()

	if text_input != '':

		path_list = os.listdir(path)
		for i in range(len(path_list)):
			path_list[i] = path_list[i].lower()

		try:

			if commands[1] in text_input:

				#Splits string input into different words to be analyzed (after commands[1])
				text_output = substring_after(text_input,commands[1])
				text_output_list = text_output.split()


				print ("============INFORMATION====================")
				print ("Output list: ")
				print (text_output_list)
				print ()		
				print ("Range of output list: ")
				print (range(len(text_output_list)))
				print ()
				print ("Length of output list: ")
				print (len(text_output_list))
				print ()
				print ("Range of directory: ")
				print (range(len(path_list)))
				print ()


				#Executing output analysis
				sorting_results()


				print ()
				print ('Programs to open:')
				print ('\n'.join(response_list))
				print ()


				if len(execute_list) > 1:

					text_output = 'Which program do I open?'

					#Converts text_output to sound
					get_speech(text_output)

					#Listens to user input and converts to string
					catch_voice()

					#Splits string input into different words to be analyzed
					text_output = text_input
					text_output_list = text_output.split()


					print ("============INFORMATION====================")
					print ("Output list: ")
					print (text_output_list)
					print ()		
					print ("Range of output list: ")
					print (range(len(text_output_list)))
					print ()
					print ("Length of output list: ")
					print (len(text_output_list))
					print ()
					print ("Range of response list: ")
					print (range(len(execute_list)))
					print ()

					
					#Redefines 'path_list' with results from 'execute_list'
					path_list = []
					path_list.extend(execute_list)


					#Executing output analysis
					sorting_results()


					o_range = range(len(text_output_list))
					l_range = range(len(execute_list))

					for l in l_range:
						for o in o_range:
							if text_output_list[o] in execute_list[l]:
								execute = execute_list[l]


				if len(execute_list) == 0:
					text_output = "This file does not exist."
				elif len(execute_list) == 1:
					text_output = open_r + response_list[0] + '.'
							
	
				if len(execute_list) > 0:
					threading.Thread(target=execute_prog).start()
				get_speech(text_output)


			elif commands[2] in text_input:
				get_speech('Closing program.')
				break

		except sr.WaitTimeoutError:
			print ('Timeout error. Will try again.')
			pass

		except sr.UnknownValueError:
			pass