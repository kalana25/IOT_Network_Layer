all:say_hello generate
install_paho:
	@echo "Installing Paho"
	pip3 install paho-mqtt
copy_files:
	@echo "File are being copied"
	mkdir ../run
	cp source/mqtt-template-lab3.py ../run
generate:
	@echo "Creating files"
	touch file-{1..5}.txt
list:
	@echo "Listing files"
	ls
