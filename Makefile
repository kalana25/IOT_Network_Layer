all:say_hello generate
install_paho:
	@echo "Installing Paho"
	pip3 install paho-mqtt
install_aiocoap:
	@echo "Installing aiocap"
	pip3 install --upgrade "aiocoap"
run_mqtt_prot:
	@echo "Running program"
	python3 source/mqtt-protocol-lunch.py
run_coap_prot:
	@echo "Running coap server"
	python3 source/coap_server.py
generate:
	@echo "Creating files"
	touch file-{1..5}.txt
list:
	@echo "Listing files"
	ls
