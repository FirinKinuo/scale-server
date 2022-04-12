PYTHON_PATH := /usr/bin/python3
ROOT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
SCALE_SERVER_PATH := /usr/bin/scale-server
EXTERNAL_FILES_DIR := /etc/scale-server
CONFIG_FILE_PATH := $(EXTERNAL_FILES_DIR)/config.yaml
LOGS_DIR := /var/log/scale-server


ifeq (, $(shell which $(PYTHON_PATH) ))
  $(error "PYTHON=$(PYTHON_PATH) not found")
endif

PYTHON_VERSION_MIN=3.8
PYTHON_VERSION=$(shell $(PYTHON_PATH) -c 'import sys; print("%d.%d"% sys.version_info[0:2])' )
PYTHON_VERSION_OK=$(shell $(PYTHON_PATH) -c 'print(int(float($(PYTHON_VERSION)) >= float($(PYTHON_VERSION_MIN))))')

ifeq ($(PYTHON_VERSION_OK),0)
  $(error "Need python $(PYTHON_VERSION) >= $(PYTHON_VERSION_MIN)")
endif

clear:
	-rm -r "$(ROOT_DIR)/venvScaleServer"
	-rm $(SCALE_SERVER_PATH)

clear-dirs:
	-rm -r $(EXTERNAL_FILES_DIR)
	-rm -r $(LOGS_DIR)

install:
	make clear

	virtualenv --python=$(PYTHON_PATH) "$(ROOT_DIR)/venvScaleServer"
	"$(ROOT_DIR)/venvScaleServer/bin/python3" "$(ROOT_DIR)/setup.py" install

	-mkdir $(EXTERNAL_FILES_DIR)
	-mkdir $(LOGS_DIR)

	if ! [ -f $(CONFIG_FILE_PATH) ]; then cp "$(ROOT_DIR)/config.yaml.sample" $(CONFIG_FILE_PATH); fi

	-ln -s "$(ROOT_DIR)/venvScaleServer/bin/scale_server" $(SCALE_SERVER_PATH)

clear-install:
	make clear
	make clear-dirs
	make install
