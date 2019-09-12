import requests

class MiloError(Exception):
	def __init__(self, msg):
		self.msg = msg

def validate(res):
	if not res['success']:
		raise MiloError(res['error'])

class MiloAPI:
	def __init__(self, base):
		self.base = base
		self.token = None

	def register(self, name, username, password):
		payload = {
			'name': name,
			'username': username,
			'key': password
		}
		data = self._post("register", payload)
		self.token = data['token']

	def login(self, username, password):
		payload = {
			'username': username,
			'key': password
		}
		data = self._post("login", payload)
		self.token = data['token']

	def logged_in():
		return self.token is not None

	def info(self):
		self._checktoken()
		return self._get("info")

	def history(self):
		self._checktoken()
		return self._get("history")

	def transfer(self, to, amount):
		self._checktoken()
		payload = {
			'to': to,
			'amount': amount
		}
		return self._post("transfer", payload)

	def withdraw(self, amount):
		self._checktoken()
		payload = {
			'amount': amount
		}
		return self._post("withdraw", payload)

	def admin_deposit(self, to, amount):
		self._checktoken()
		payload = {
			'username': to,
			'amount': amount
		}
		return self._post("admin/deposit", payload)

	def admin_withdraw(self, who, amount):
		self._checktoken()
		payload = {
			'username': who,
			'amount': amount
		}
		return self._post("admin/withdraw", payload)

	def _checktoken(self):
		if not self.token:
			raise MiloError("Not logged in")

	def _post(self, path, data):
		h = {}
		if self.token:
			h['Authorization'] = self.token
		res = requests.post(self.base + "/" + path, json=data, headers=h).json()
		validate(res)
		return res

	def _get(self, path):
		h = {}
		if self.token:
			h['Authorization'] = self.token
		res = requests.get(self.base + "/" + path, headers=h).json()
		validate(res)
		return res
