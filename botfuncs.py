from bs4 import BeautifulSoup
import requests, os, time
import socks, socket, ssl
import sys, random

def pega_pag(pagremota, paglocal):
	if( not os.path.exists(paglocal) or (time.time()-os.path.getmtime(paglocal) )/60>=30 ):
		print('Disparei requisicao!');
		headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/71.0'};
		proxy = {'socks5' : '127.0.0.1:9050'};
		r=requests.get(pagremota, headers=headers, proxies=proxy );
		arq = open(paglocal, 'w+');
		arq.write(r.text);
		arq.close();
	arq = open(paglocal, 'r');
	return( arq.read() );

def ctftime():
	arq = pega_pag("https://ctftime.org/event/list/upcoming/rss/",".ctftime.html");
	soup = BeautifulSoup( arq, 'lxml' );

	numEventos = len( soup.find_all('guid') );
	saida = "";
	for num in range(numEventos):
		ctfinfo =""
		ctfinfo+= soup.find_all('ctf_name')[num].text+" | ";
		data = soup.find_all('start_date')[num].text
		ctfinfo+= data[6:8]+"/"+data[4:6]+"/"+data[0:4]+" "+data[9:11]+":"+data[11:13]+":"+data[13:15]+" | ";
		ctfinfo+= "https://ctftime.org"+soup.find_all('ctftime_url')[num].text+ " | ";
		ctfinfo+= soup.find_all('url')[num].text;
		ctfinfo+="\n";
		saida+=ctfinfo;
		if(num+1>=3):
			break;

	return saida;

def thehackernews():
	pega_pag("https://feeds.feedburner.com/TheHackersNews", ".thehackernews.html");
	arq=open(".thehackernews.html", "r");
	soup = BeautifulSoup(arq.read(), "lxml");
	#print( soup.prettify() );

	k=1;
	saida="";
	for item in soup.find_all("item"):
		if( len(item.title.text)>60 ):
			saida+=str(item.title.text[:60])+"..."+" | ";
		else:
			saida+=str(item.title.text)+" | ";

		for linha in item.text.split('>'):
			if( linha.find("https://thehackernews.com")!=-1 ):
				saida+=linha+"\n";
		if(k>=5):
			break;
		k+=1;
	return saida;

# Agradecimentos ao pessoal da Collab no Riseup Pad pra criar essas expressões maravilhosas
def madlib():
    verbos={'dançar hip-hop', 'programar', 'cagar', 'fazer a dança do ventre', 'ouvir asmr', 'fazer o passinho do romano', 'fumar grama', 'correr pelado', 'assistir xvideos', 'fazer pudim', 'beber perfume', 'coçar o saco', 'imitar o lacraia', 'cantar Pabllo Vittar', 'fazer a paradinha', 'bater latinhas', 'tomar agua mineral', 'beber seu suco detox', 'ser espionado pela sua vó', 'assediar velhinhas na rua', 'mandar cantadas de pedreiro', 'assobiar faroeste caboclo', 'fazer pum com o suvaco', 'cortar os cabelos do saco', 'deixar so o bigodinho do Hittler', 'mandar o middle finger', 'codar', 'fazer exames proctologicos', 'cutucar o ouvido de mendigos', 'raspar a bunda'};
    adverbios={'com raiva', 'sonolento', 'gemendo sexualmente', 'de maneira intensa', 'intensamente', 'estranhamente', 'ferozmente', 'pacientemente', 'travestidamente', 'regularmente', 'aparentemente', 'sambando', 'descendo na boquinha da garrafa', 'freneticamente', 'fora de controle', 'bêbado', 'na sombra', 'pelado','carentemente'};
    substantivo={'copo da razer', 'pc da xuxa', 'exploit de Nokia tijolo', 'teclado gaymer', 'bigode', 'disquete de 1Mb', 'mouse de bolinha', 'modem 9600 da usrobotics', 'mullet', 'pochete', 'saia balonet', 'alpargatas', 'galochas pink', 'glitter', 'protetor de saco', 'vibrador', 'boneco Ken', 'Barbie nadadora', 'batom', 'clips', 'doritos picante', 'facão', 'absorvente', 'torradeira', 'gato caolho', 'objetivo de vida', 'OB tamanho GG' ,'escravo sexual da deep web', 'cadeira da DXRacer', 'caixinha de som da Multilaser', 'bicicleta da Baidu', 'avatar do Habbo', 'travesseiro da Nasa', 'skin de CSGO', 'chaveiro da Hello Kitty', 'cosplay de Sailor Moon', 'unha de Zé do Caixão', 'patinete', 'uber', 'taxi tunado', 'alien da Área51', 'iPhone', 'Xiaomi', 'mp3 player'};
    adjetivo={'escroto', 'fedorento', 'brilhante', 'hackudo', 'pré-histórico', 'gostoso', 'gordo', 'magrelo', 'peludo', 'depilado', 'morto', 'congelado', 'careca', 'tortão pra direita', 'selvagem', 'gigante', 'grudento', 'assustador', 'customizado', 'insano', 'atrevido', 'aoooo potencia', 'sideral', 'pica das galaxias', 'xoxo, capenga, manco, anêmico, frágil e inconsistente', 'pink', 'pintudo', 'sortudo', 'azarado', 'da mãe', 'do pai', 'da irmã'};
    gosta_nao_gosta={'adora', 'ama', 'odeia', 'teme', 'curte', 'deseja'};
    com_o_que={'com seu', 'segurando o seu', 'acariciando o seu', 'mamando o seu', 'sacodindo o seu', 'desentortando o seu', 'queimando o seu', 'vendendo o seu', 'procurando o seu', 'escondendo o seu', 'brincando com seu', 'consertando o seu'};
    frase=str(random.choice(list(gosta_nao_gosta)))+" "+str(random.choice(list(verbos)))+" "+str(random.choice(list(adverbios)))+" "+str(random.choice(list(com_o_que)))+" "+str(random.choice(list(substantivo)))+" "+str(random.choice(list(adjetivo)))
    return frase;

# FUNCS DE CRIPTOGRAFIA
def encripta_cesar(entrada, cifra):
	saida = "> "
	i=0
	for c in entrada:
		if (ord(c)>=65 and ord(c)<=90): # maiúsculas
			saida += chr(((ord(c)-65+ cifra )%26 )+65)
			i+=1
		elif (ord(c)>=97 and ord(c)<=122): # minúsculas
			saida += chr(((ord(c)-97+ cifra )%26 )+97)
			i+=1
		else:
			saida += c;
	return saida;
def decripta_cesar(entrada, cifra):
	saida = "> "
	i=0
	for c in entrada:
		if (ord(c)>=65 and ord(c)<=90): # maiúsculas
			saida += chr(((ord(c)-65+26- cifra )%26 )+65)
			i+=1
		elif (ord(c)>=97 and ord(c)<=122): # minúsculas
			saida += chr(((ord(c)-97+26- cifra )%26 )+97)
			i+=1
		else:
			saida += c;
	return saida;
def encripta_vigenere(entrada, cifra):
	i=0
	cifra = cifra.upper()
	saida = "> "
	for c in entrada:
		if (ord(c)>=65 and ord(c)<=90): # maiúsculas
			saida += chr(((ord(c)-65+ (ord(cifra[i%len(cifra)])-65) )%26 )+65)
			i+=1
		elif (ord(c)>=97 and ord(c)<=122): # minúsculas
			saida += chr(((ord(c)-97+ (ord(cifra[i%len(cifra)])-65) )%26 )+97)
			i+=1
		else:
			saida += c;
	return saida;
def decripta_vigenere(entrada, cifra):
	i=0
	cifra = cifra.upper()
	saida = "> "
	for c in entrada:
		if (ord(c)>=65 and ord(c)<=90): # maiúsculas
			saida += chr(((ord(c)-65+26- (ord(cifra[i%len(cifra)])-65) )%26 )+65)
			i+=1
		elif (ord(c)>=97 and ord(c)<=122): # minúsculas
			saida += chr(((ord(c)-97+26- (ord(cifra[i%len(cifra)])-65) )%26 )+97)
			i+=1
		else:
			saida += c;
	return saida;
# FIM DAS FUNCS DE CRIPTOGRAFIA
