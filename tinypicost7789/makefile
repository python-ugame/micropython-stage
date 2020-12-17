ESPIDF=../../../esp-idf
PORT=/dev/ttyUSB0
FLASH_MODE = dio
FLASH_SIZE = 4MB
FLASH_FREQ = 80m
CROSS_COMPILE = ../../../xtensa-esp32-elf/bin/xtensa-esp32-elf-

BOARD=TINYPICO
USER_C_MODULES=../../../micropython-stage/modules
CFLAGS_EXTRA=-DMODULE_STAGE_ENABLED=1
FROZEN_MANIFEST=../../../micropython-stage/tinypicost7789/manifest.py

include Makefile
