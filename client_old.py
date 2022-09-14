import socket
import json
import random
import sys

HOST = "proj1.3700.network"  # The server's hostname or IP address
PORT = 27993  # The port used by the server
NORTHEASTERN_USERNAME = "mantri.an"

def remove_empty_spaces(word_list):
	result = []
	for word in word_list:
		if word.strip():
			result.append(word)

	return result



# if the letter is not present in the secret word, remove all words
# in the word_list with that letter in them (mark = 0)
def remove_words_with_letter(word_list, letter):
	for word in word_list:
		if (letter in word):
			word_list.remove(word)

	#word_list = remove_empty_spaces(word_list)

	return word_list
	
# receives messages from the server and determines the course of action 
# depending on the type of the message
def server_message_receiver(word_list):
	while True:
		received_data = s.recv(1024).decode()

		while not received_data.endswith('\n'):
			received_data += s.recv(1024).decode()

		message_dict = json.loads(received_data)
		message_type = message_dict.get("type")

		GAME_ID = message_dict.get("id")

		if (message_type == "bye"):
			secret_flag = message_dict.get("flag")
			print(secret_flag)
			s.close()
			break

		elif (message_type == "error"):
			print(message_dict.get("message"))
			s.close()
			sys.exit(1)

		else:
			#filter word list
			word_list = filter_word_list(word_list, message_dict)
			guess_words(GAME_ID, word_list)



def filter_word_list(word_list, message_dict):
	previous_guesses = message_dict.get("guesses")
	letters_not_present = find_letters_not_present(previous_guesses)
	print(type(letters_not_present))

	if (len(letters_not_present) > 0):
		for word in word_list:
			for letter in letters_not_present:
				if (letter in word):
					word_list.remove(word)

	return word_list	


def find_letters_not_present(previous_guesses):
	letters_not_present = []

	if (len(previous_guesses) > 0):
		for guess in previous_guesses:
			for i in range(len(guess.get("marks"))): # iterating over array of marks in the this word
				if ((guess.get("marks")[i]) == 0): # if the letter is not present in the Wordle word
					current_word = message_dict.get("word")
					letters_not_present.append(current_word[i])

	return letters_not_present


def guess_words(GAME_ID, word_list):
		# send guesses
		# filter out words with letters that are 0 (not in the word)
		# if error, print message
		# if bye, print secret flag

		#if message_type == "error":
		#	print()

	guess_dict = { 
		"type": "guess", 
		"id": GAME_ID, 
		"word": random.choice(word_list)
	} 	

	guess = (json.dumps(guess_dict)) + "\n"
	s.sendall(guess.encode())
	server_message_receiver(word_list)



# main function
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))

	hello_message_dict = { 
	"type": "hello", 
	"northeastern_username": NORTHEASTERN_USERNAME, 
	} 	


	with open('project1-words.txt') as file:
		word_list = file.read().split('\n')
	print(type(word_list))


	first_hello_message = (json.dumps(hello_message_dict)) + "\n"
	s.sendall(first_hello_message.encode())

	server_message_receiver(word_list)







