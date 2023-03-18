clientGUI:
	@clear && cd ./src/GUI && python clientGUI.py

serverGUI:
	@clear && cd ./src/GUI && python serverGUI.py

1:
	@clear && cd ./src/GUI && python clientGUI.py

2:
	@clear && cd ./src/GUI && python serverGUI.py

server:
	@clear && cd ./src && python server.py

db:
	@clear && cd ./testes && python db.py

requirements:
	@clear && pip install -r requirements.txt


pulse:
	@clear && cd "C:\Users\mateu\Downloads\FACULDADE\1-COMP\4-Periodo\REDES\TPs\TP1\pulseaudio\bin" && ./pulseaudio.exe

audioVideo:
	@clear && bash 
	@export DISPLAY="$(grep nameserver /etc/resolv.conf | sed 's/nameserver //'):0" 
	@export PULSE_SERVER=tcp:$(grep nameserver /etc/resolv.conf | awk '{print $2}');