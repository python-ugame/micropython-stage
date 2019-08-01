Stage – a Tile and Sprite Engine
********************************

Stage is a library that lets you display tile grids and sprites on SPI-based
RGB displays in MicroPython. It is mostly made with video games in mind, but it
can be useful in making any kind of graphical user interface too.

For performance reasons, a part of this library has been written in C and has
to be compiled as part of the MicroPython firmware as the ``_stage`` module.
For memory saving reasons, it's best if the Python library is also included in
the firmware, as a frozen module.


API Reference
*************

The API reference is available at `<http://circuitpython-stage.readthedocs.io>`_.


Compiling
*********

Please refer to the official guide on compiling external modules available
at `<http://docs.micropython.org/en/latest/develop/cmodules.html>`_.

The sub-directories contain example library initialization files for different
platforms. You should freeze the files for the platform you target into your
firmware.

Example::
    make USER_C_MODULES=../../../micropython-stage/modules CFLAGS_EXTRA=-DMODULE_STAGE_ENABLE FROZEN_MPY_DIR=../../../micropython-stage/m5stack
