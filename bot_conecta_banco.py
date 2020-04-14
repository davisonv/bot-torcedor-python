#-- coding: utf-8 --
import requests
import telebot
from telebot import types
import pymysql #biblioteca de conexão com o mysql

conn = pymysql.connect(host='127.0.0.1', #indica o servidor
	unix_socket='/opt/lampp/var/mysql/mysql.sock', #indica em qual base ele deve se conectar já que uma conexão lampp
	user='root', #indica o usuario que o python usará para se conectar com o banco
	passwd='R7UZ8R59ylvjVD5R', #senha do usuário
	db='usuarios_telegram') # banco de dados
	#127.0.0.1 é igual ao localhost

cur = conn.cursor() #faz a conexão com o lampp

#Aqui inicia o bot

API_TOKEN = '902784469:AAHeaAWh1Aa9wkmgdIDwmXCHZFTxC3qIVRU' #Chave da api do telegram

bot = telebot.TeleBot(API_TOKEN) #telebot-sumário e TeleBot(comando) aplica o token

user_dict = {} #variavel unica

class User:
	def __init__(self,name):
		self.name = name
		self.age = None
		self.team = None
		self.mail = None

@bot.message_handler(commands=['start'])
def send_welcome(message):
	msg = bot.reply_to(message,"Oi, tudo certo? Este o bot de noticias do torcedor!")
	cid = message.chat.id
	bot.send_message(cid,"Nosso ID é: " + str(cid) + " este bot lhe enviará noticias do seu clube do coração! \n Qual é o seu nome?")
	bot.register_next_step_handler(msg,process_name_step)

def process_name_step(message):
	try:
		chat_id = message.chat.id
		name = message.text #atribui o nome digitado a variavel name
		user = User(name) #aloca o nome na variavel user
		user_dict[chat_id] = user #armazena chat_id da conversa
		msg = bot.reply_to(message, "Qual a sua idade?")
		bot.register_next_step_handler(msg,process_age_step)
	except Exception as e:
		bot.reply_to(message,e)
		
def process_age_step(message):
	try:
		chat_id = message.chat.id
		age = message.text
		if not age.isdigit():
			msg = bot.reply_to(message, "Você precisa digitar números!")
			bot.register_next_step_handler(msg, process_age_step)
			return
		user = user_dict[chat_id]
		user.age = age
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True) #Cria as opções visuais
		markup.add('Flamengo','Vasco') #Adciona opções
		msg = bot.reply_to(message,"Qual o seu time do coração?",reply_markup=markup) #Mostra as opções
		bot.register_next_step_handler(msg,process_team_step)
	except Exception as e:
		bot.reply_to(message, 'Oops, algo deu errado!')
		print(e)

def process_team_step(message):
	try:
		chat_id = message.chat.id
		team = message.text #atribui o nome digitado a variavel team
		user = user_dict[chat_id]
		if (team == u'Flamengo') or (team == u'Vasco'):
			user.team = team
		else:
			raise Exception()
		msg = bot.reply_to(message, "Qual o seu e-mail?")
		bot.register_next_step_handler(msg,process_mail_step)
	except Exception as e:
		bot.reply_to(message,e)


def process_mail_step(message):
	try:
		chat_id = message.chat.id
		mail = message.text 
		user =  user_dict[chat_id]
		cur.execute("USE usuarios_telegram") #seleciona a base a ser usada
		sql = "INSERT INTO USARIO(NOME_USUARIO, CHATID_USUARIO, CATEGORIA_USUARIO, EMAIL_USUARIO, idade_usuario) VALUES(%s,%s,%s,%s,%s)"
		val = (user.name,str(chat_id),user.team,mail,str(user.age))
		cur.execute(sql,val) #insert e valores
		print(val)
		conn.commit() #executa o insert
		cur.close()
		conn.close()
		msg = bot.reply_to(message, "Obrigado por se cadastrar!")
	except Exception as e:
		bot.reply_to(message,e)

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

bot.polling()
