#!/usr/bin/env python3
from irc import *
from botfuncs import *
from colorama import Fore,Back,Style
import os, sys, random

links = {
	'site' : 'link',
	'underDir' : 'http://underdj5ziov3ic7.onion/'
	'thenter' : '(off) http://pzqcmpphmomfvih2.onion/',
}

text="::start::";
nickname="apelido_do_bot";
dono="apelido_do_dono"; # quem vai ter privilégios

if( len(sys.argv)==2 ):
	esc_canal = int(sys.argv[1]);
else:
	esc_canal = 1;

# seus canais alternativos para o bot entrar
if esc_canal==1:
	channel = "#consulado";
	server = "irc.autistici.org";
	port = 9999;
elif esc_canal==2:
	channel = "#conlapso";
	server = "irc.autistici.org";
	port = 9999;
else:
	print("Nenhum canal escolhido!");
	exit();

irc = IRC();
irc.connect(server, port, channel, nickname);

while 1:
	text = irc.get_text();
	text = text[:-2] # retira \r\n no fim
	print( Back.CYAN+"[<]"+Style.RESET_ALL+" "+text );
	text = text.split(" ");

	#ALGUÉM ENTROU
	if(text[1]=="JOIN"):
		if(text[0][1:8]==nickname):
			irc.send(channel, "Saudações, "+nickname+" chegando.")
		else:
			num = random.randint(1,4)
			if num==1:
				irc.send(channel, "Que bom te ler por aqui.")
			if num==2:
				irc.send(channel, "Vish, ele voltou...")
			if num==3:
				irc.send(channel, "Quem ta vivo sempre conecta.")
			if num==4:
				irc.send(channel, "Deixaram a porta aberta, ta entrando ate mendigo!")

	#ALGUÉM SAIU/PARTIU
	if(text[1]=="PART" or text[1]=="QUIT" ):
		num = random.randint(1,5)
		if num==1:
			irc.send(channel, "Hasta la vista.")
		if num==2:
			irc.send(channel, "Iiih. Nao pagou a conta da internet.")
		if num==3:
			irc.send(channel, "Que a porta bata onde o sol nao bate!")
		if num==4:
			irc.send(channel, "Ja vai tarde.")
		if num==5:
			irc.send(channel, "Olha o efeito Neymar acontecendo")

	#PRIVMSG NO CANAL
	if(text[1]=="PRIVMSG" and text[2]==channel and text[3][1::]=="!"+nickname and len(text)>4 ):
		if( text[4]=="help" and len(text)==5 ):
			irc.send(channel, "!botinha [comando]");
			irc.send(channel, "~ oi|help|link|madlib|cesar|vigenere - ctf|news ~");
		elif( text[4]=="help" and len(text)==6 ):
			if(text[5]=="cesar"):
				irc.send(channel, "!botinha cesar [e/d] [1-25] texto");
			elif(text[5]=="vigenere"):
				 irc.send(channel, "!botinha vigenere [e/d] cifra texto");
			elif(text[5]=="link"):
				 irc.send(channel, "!botinha link siteDesejado");
			else:
				irc.send(channel, "Nao tem.");
		elif( text[4]=="link" ):
			if(len(text)!=6):
				irc.send(channel, "Uso incorreto! Tente: !botinha help link");
				continue;
			if text[5] in links: # se o text[5] é um link conhecido que está no dicionário 'links'
				irc.send(channel, links[ text[5] ])
			else:
				irc.send(channel, "Nao tenho esse link!");
		elif( text[4]=="oi" and len(text)==5 ):
			num = random.randint(1,5)
			if num==1:
				irc.send(channel, "Ola")
			elif num==2:
				irc.send(channel, "Oi")
			elif num==3:
				irc.send(channel, "Fala")
			elif num==4:
				irc.send(channel, "Como vai")
			elif num==5:
				irc.send(channel, "Diga")
		elif( text[4]=="cesar" ):
			if(len(text)!=8):
				irc.send(channel, "Uso incorreto! Tente: !botinha help cesar");
				continue;

			op = text[5];
			try:
				cifra = int(text[6])
			except:
				irc.send(channel, "Utilizacao incorreta!");
				continue;
			texto = text[7]
			if op=="e": #encripta
				saida = encripta_cesar(texto, cifra)
				irc.send(channel, saida)
			elif op=="d": #decripta
				saida = decripta_cesar(texto, cifra)
				irc.send(channel, saida)
			else:
				irc.send(channel, "Utilizacao incorreta!");
				continue;
		elif( text[4]=="vigenere" ):
			if(len(text)!=8):
				irc.send(channel, "Uso incorreto! Tente: !botinha help vigenere");
				continue;
			#!botinha vigenere enc senha mensagem
			op = text[5]
			cifra = text[6]
			text = text[7]
			if op=="e": #encripta
				saida = encripta_vigenere(text, cifra)
				irc.send(channel, saida)
			elif op=="d": #decripta
				saida = decripta_vigenere(text, cifra)
				irc.send(channel, saida)
		elif( text[4]=="ctf"):
			ctfs = ctftime();
			for linha in ctfs.strip().split('\n'):
				irc.send(channel, linha.replace('—', '|'));
		elif( text[4]=="news"):
			news = thehackernews();
			for linha in news.strip().split('\n'):
				irc.send(channel, linha);
		elif(text[4]=="madlib"):
			nicks=[];
			texto = irc.who(channel); # pede os apelidos do pessoal no canal
			for linha in texto.split("\r\n"):
				if( len(linha.split(" ")) >=7 ):
					nick=linha.split(" ")[7];
				if(len(nick)>0 and nick!="botinha" and nick!="list."):
					nicks.append(nick);
			irc.send(channel, random.choice(nicks)+" "+madlib());
		else:
			irc.send(channel, "Tente: !botinha help");

	#MENSAGENS DIRETAS
	if(text[0][1:7:]==dono and text[1]=="PRIVMSG" and text[2]==nickname):
		if(text[3][1::]=="sair"):
			irc.send(channel, "Ate mais");
			irc.getout();
		elif(text[3][1::]=="falar"):
			irc.send(channel, ' '.join(text[4:]));
	else:
		pass;