MPY_DIR ?= ../../../micropython/micropython
ARCH ?= xtensawin
MOD = _stage
SRC = _stage.c

CFLAGS += \
	-I$(MPY_DIR)/ports/esp32/ \
	-I$(MPY_DIR)/ports/esp32/build \
	-I../../../micropython/esp-idf/components/freertos/include \
	-I../../../micropython/esp-idf/components/esp32/include \
	-I../../../micropython/esp-idf/components/driver/include \
	-I../../../micropython/esp-idf/components/soc/include \
	-I../../../micropython/esp-idf/components/soc/esp32/include \
	-I../../../micropython/esp-idf/components/heap/include \


include $(MPY_DIR)/py/dynruntime.mk
