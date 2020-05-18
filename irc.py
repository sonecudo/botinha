from colorama import Fore,Back,Style
import socket, ssl, time
import sys
import socks

class IRC:
	def __init__(self):
		#define o socket
		s = socks.socksocket();
		s.set_proxy(socks.SOCKS5, "127.0.0.1", 9050);
		self.irc = ssl.wrap_socket(s);

	def send(self, chan, msg):
		msg = msg.split("\n");
		for linha in msg:
			data = "PRIVMSG " + chan + " :" + linha + "\n";
			self.irc.send( data.encode() );
			print( Back.BLUE+"[>]"+Style.RESET_ALL+" PRIVMSG " + chan + " :" + linha + "\n" );

	def who(self, chan):
		data="WHO "+chan+"\n";
		print(data)
		self.irc.send( data.encode() );
		return self.get_text();

	def connect(self, server, port, channel, botnick):
		print( "Conectando com "+server+"/"+str(port) );
		self.irc.connect((server, port))

		data = "NICK " + botnick + "\n";
		self.irc.send( data.encode() );

		data = "USER " + botnick + " 0 * :" + botnick + "\n";
		self.irc.send( data.encode() );

		time.sleep(2);
		data = "PRIVMSG NickServ :identify senha_do_bot\n";
		self.irc.send( data.encode() );
		time.sleep(2);

		data = "JOIN " + channel + "\n";
		self.irc.send( data.encode() );
		time.sleep(2);

		data = "MODE " + botnick + " +i\n";
		self.irc.send( data.encode() );
		print( Back.GREEN+"[>]"+Style.RESET_ALL+" "+data );

	def get_text(self):
		text=self.irc.recv(2040);
		text=text.decode('utf-8');
		if text.find('PING') != -1:
			data = "PONG "+text.split()[1]+"\r\n";
			self.irc.send(data.encode());
		return text

	def getout(self):
		self.irc.send("QUIT :Foi dancar conga\n".encode());
		self.irc.close();
		exit();
