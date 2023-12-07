all:say_hello generate
install_paho:
	@echo "Installing Paho"
	pip3 install paho-mqtt
run:
	@echo "Running program"
	python3 source/mqtt-protocol-lunch.py
generate:
	@echo "Creating files"
	touch file-{1..5}.txt
list:
	@echo "Listing files"
	ls
