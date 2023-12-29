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
run_mqtt_server:
	@echo "Running program.."
	python3 source/mqtt/server/mqtt-server.py
run_mqtt_client:
	@echo "Running mqtt client.."
	python3 source/mqtt/client/mqtt-speed-bench-client.py
run_mqtt_bench_tp:
	@echo "Running mqtt throughput benchmark"
	python3 source/mqtt/server/mqtt-throughput-benchmark-server.py
run_mqtt_bench_es:
	@echo "Running mqtt execution speed benchmark"
	python3 source/mqtt/server/mqtt-speed-benchmark-server.py
run_coap_server:
	@echo "Running coap server"
	python3 source/coap/server/coap_server.py
run_coap_bench_es:
	@echo "Running coap execution seeed bench"
	python3 source/coap/server/coap_speed_benchmark-server.py
run_coap_test_client:
	@echo "Running coap test client"
	python3 source/coap/client/test_client.py
generate:
	@echo "Creating files"
	touch file-{1..5}.txt
list:
	@echo "Listing files"
	ls
