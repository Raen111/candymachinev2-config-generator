import sys
import json


class UploadConfig:
	def __init__(self, output_file):
		self.output_file = output_file

		self.price = 0.01
		self.number = None
		self.gatekeeper = None
		self.gatekeeperNetwork = None
		self.gatekeeperExpireOnUse = False
		self.solTreasuryAccount = None
		self.splTokenAccount = None
		self.splToken = None
		self.goLiveDate = None
		self.endSettings = None
		self.whitelistMintSettings = None
		self.hiddenSettings = None
		self.storage = "arweave"
		self.ipfsInfuraProjectId = None
		self.ipfsInfuraSecret = None
		self.awsS3Bucket = None
		self.noRetainAuthority = False
		self.noMutable = False

	def generate_json(self):
		res = {}
		res["price"] = self.price
		res["number"] = self.number
		if self.gatekeeper:
			res["gatekeeper"] = {
				"gatekeeperNetwork": self.gatekeeperNetwork,
				"expireOnUse": self.gatekeeperExpireOnUse
			}
		else:
			res["gatekeeper"] = None
		res["solTreasuryAccount"] = self.solTreasuryAccount
		res["splTokenAccount"] = self.splTokenAccount
		res["splToken"] = self.splToken
		res["goLiveDate"] = self.goLiveDate
		res["endSettings"] = self.endSettings
		res["whitelistMintSettings"] = self.whitelistMintSettings
		res["hiddenSettings"] = self.hiddenSettings
		res["storage"] = self.storage
		res["ipfsInfuraProjectId"] = self.ipfsInfuraProjectId
		res["ipfsInfuraSecret"] = self.ipfsInfuraSecret
		res["awsS3Bucket"] = self.awsS3Bucket
		res["noRetainAuthority"] = self.noRetainAuthority
		res["noMutable"] = self.noMutable

		return json.dumps(res)

	def generate_file_config(self):
		with open(self.output_file, 'w') as f:
			f.write(self.generate_json())


# Class that manages the user inputs in a secure way
class SecureInput:
	def int_number_input(self, prompt):
		got_input = False
		while not got_input:
			try:
				res = int(input(prompt))
				got_input = True
			except ValueError:
				print("Only integers are allowed.")
		return res

	def float_number_input(self, prompt):
		got_input = False
		while not got_input:
			try:
				res = float(input(prompt))
				got_input = True
			except ValueError:
				print("Only numbers are allowed.")
		return res

	def boolean_input(self, prompt, default=""):
		got_input = False
		if default != "":
			prompt += ("(Y/n) " if default else "(y/N) ")
		while not got_input:
			res = input(prompt).upper()

			if (res == "Y" or res == "N"):
				got_input = True
			elif res == "" and default != "":
				return default
			else:
				print("Y for Yes, N for No")
		return True if res == "Y" else False

	def input_among_choices(self, prompt, choices):
		got_input = False
		n = len(choices)
		while not got_input:
			print(prompt)
			for i, choice in enumerate(choices):
				print(f"{i+1}- {choice}")
			res = int(input(f"Select the option between 1 and {n}: "))

			if (res >= 1 and res <= n):
				got_input = True
			else:
				print("\n")
		return choices[res-1]

	def string_input(self, prompt, default):
		got_input = False
		if default != "":
			prompt += f' (Enter for default value "{default}")'
		while not got_input:
			try:
				res = input(prompt)
				got_input = True
			except ValueError:
				print("Please enter a string.")
		return res if res != "" else default

	# TODO secure the input of a date
	def date_input():
		got_input = False
		while not got_input:
			try:
				res = float(input(prompt))
				got_input = True
			except ValueError:
				print("Only numbers are allowed.")
		return res


### Main Part of the Program
if __name__ == "__main__":
	# Display the help for usage
	if (len(sys.argv[1:]) != 0):
		print("help")
		sys.exit(2)

	uploadConfig = UploadConfig("config.json")
	secureInput = SecureInput()

	uploadConfig.number = secureInput.int_number_input(
		"How many items do you have in your collection? ")
	uploadConfig.price = secureInput.float_number_input(
		"At what price do you want to sell an item (in SOL)? ")
	uploadConfig.gatekeeper = secureInput.boolean_input(
		"Do you want Captcha Settings? ", True)
	if (uploadConfig.gatekeeper):
		uploadConfig.gatekeeperNetwork = secureInput.string_input(
			"Gatekeeper Network address :", "ignREusXmGrscGNUesoU9mxfds9AiYTezUKex2PsZV6")
		uploadConfig.gatekeeperExpireOnUse = secureInput.boolean_input(
			"Do you want the Captcha to expire on use? ", True)

	uploadConfig.storage = secureInput.input_among_choices("phrase: ", ["arweave", "AWSBucket", "IPFS"])

	uploadConfig.noMutable=not secureInput.boolean_input("Do you want your NFTs mutable? ", True)

	# Generate the config file
	uploadConfig.generate_file_config()