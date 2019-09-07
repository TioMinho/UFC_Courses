############################
##
##	TRABALHO DA DISCIPLINA DE SISTEMAS DISTRIBUÍDOS
##	TÍTULO: MQTT VS SOCKETS
##
##	Equipe:
##		Otacílio Bezerra Leite Neto - 385213
##		Saulo Mendes de Melo - 371868
##		Thiago Arruda Beppe e Silva - 385219
##
############################

## Instruções de Execução
# MQTT:
Para executar o sistema desenvolvido em MQTT, execute os scripts dos Sensores/Atuadores, e posteriormente o script do Controlador.
Os scripts, num sistema Linux, são executados na seguinte ordem (ignore o símbolo '$' e as linhas iniciadas com "#"):

	# Sensores/Atuadores
	$ python3 mqtt-arcond.py
	$ python3 mqtt-gelad.py
	$ python3 mqtt-porta.py
	$ python3 mqtt-temp_sensor.py
	$ python3 mqtt-subscriber-lampada.py

	# Controlador
	$ python3 tkinter_controller.py

# Sockets:
Para executar o sistema desenvolvido com Sockets, execute os scripts do Servidor Controlador, e posteriormente o script dos Sensores/Atuadores.
Os scripts, num sistema Linux, são executados na seguinte ordem (ignore o símbolo '$' e as linhas iniciadas com "#"):

	# Controlador
	$ python3 server.py

	# Sensores/Atuadores
	$ python3 client_sensors.py	
	$ python3 client_actuators.py
