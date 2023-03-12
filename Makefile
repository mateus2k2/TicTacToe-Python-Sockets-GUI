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