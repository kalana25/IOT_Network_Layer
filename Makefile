all:say_hello generate
install_paho:
	@echo "Installing Paho"
	pip3 install paho-mqtt
install_proxi_lib:
	sudo pip3 install adafruit-circuitpython-vcnl4010
install_aiocoap:
	@echo "Installing aiocoap"
	pip3 install --upgrade "aiocoap"
install_slixmpp:
	@echo "Installing slixmpp"
	pip3 install slixmpp
run_mqtt_prot:
	@echo "Running program"
	python3 source/mqtt/server/mqtt-protocol-lunch.py
run_coap_server:
	@echo "Running coap server"
	python3 source/coap/server/coap_server.py
run_coap_test_client:
	@echo "Running coap test client"
	python3 source/coap/client/test_client.py
generate:
	@echo "Creating files"
	touch file-{1..5}.txt
list:
	@echo "Listing files"
	ls
