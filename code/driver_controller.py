from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class MANAGER:
	def open_web(self):
		chrome_options = Options()
		"""chrome_options.add_argument('--headless')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--disable-dev-shm-usage')"""
		self.web = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

	def load_cookies(self):
		self.web.get("https://discord.com/")
		for c in self.cookies:
			self.web.add_cookie(c)

	def save_cookies(self):
		self.cookies = self.web.get_cookies()

	def load_account(self):
		if not self.logged:
			self.login()
			self.profile_info["discord"]["logged"] = True
		else:
			self.load_cookies()
			self.web.get("https://discord.com/channels/@me")
		sleep(10)
		self.save_cookies()

		return self.profile_info, self.cookies

	def send_message(self, message):
		input_ = self.web.find_element_by_xpath(self.chat_input)
		input_.send_keys(message)
		input_.send_keys(Keys.ENTER)


	def get_name_of_chat_element(self, element):
		try:
			return element.find_element_by_css_selector(self.chat_name_css_selector).get_attribute('innerHTML')
		except:
			return False

	def go_to_chat(self, chat_name):
		for c in self.get_chats_elements():
			if self.get_name_of_chat_element(c) == chat_name:
				c.click()
				return True
		return False

	def get_message_from_element(self, element):
		try:
			return element.find_element_by_css_selector(self.chat_message_content_css_selector).get_attribute('innerHTML')
		except:
			return False

	def get_messages_elements(self):
		return self.web.find_elements_by_css_selector(self.chat_message_css_selector)

	def get_messages(self):
		messages = []
		for c in self.get_messages_elements():
			messages.append(self.get_message_from_element(c))
		return messages

	def new_messages_label(self):
		if len(self.web.find_elements_by_css_selector(self.chat_new_messages_div_css_select)) > 2:
			return True
		else:
			return False

	def get_newest_message(self):
		messages = self.get_messages()
		return messages[len(messages)-1]

	def get_new_messages(self):
		if self.new_messages_label():
			message = self.get_newest_message()
			if message == "Hola":
				self.send_message("Hola")

	def get_chats_elements(self):
		chats = []
		for c in self.web.find_elements_by_css_selector(self.chat_container_css_selector):
			if not self.get_name_of_chat_element(c) in self.trash_chats:
				chats.append(c)
		return chats

	def get_chat_names(self):
		names = []
		for c in self.get_chats_elements():
			names.append(self.get_name_of_chat_element(c))
		return names


	def login(self):
		self.web.get("https://discord.com/login")
		email_input = self.web.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[1]/div/div[2]/input')
		password_input = self.web.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/div[2]/div/input')
		submit_input = self.web.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/div/form/div/div/div[1]/div[3]/button[2]')
		email_input.send_keys(self.email)
		password_input.send_keys(self.password)
		submit_input.click()


	def __init__(self, profile_info, cookies):
		self.profile_info = profile_info
		self.logged = self.profile_info["discord"]["logged"]
		self.cookies = cookies
		self.email = self.profile_info["discord"]["email"]
		self.password = self.profile_info["discord"]["password"]
		self.web = False




		self.trash_chats = ["Nitro", "Friends", False]


		#ccs selectors

		#container of chats
		self.chat_container_css_selector = '.layout-2DM8Md'


		#name
		self.chat_name_css_selector = '.overflow-WK9Ogt'


		#new messages div
		self.chat_new_messages_div_css_select = '.divider-3_HH5L'

		#message
		self.chat_message_css_selector = '.message-2qnXI6'

		#message content
		self.chat_message_content_css_selector = '.markup-2BOw-j'

		#xpaths elements

		#container of chats
		self.chat_container_xpath = '//*[@id="private-channels"]/div'

		#input text

		self.chat_input = '//*[@id="app-mount"]/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/main/form/div/div/div/div[3]/div[2]'