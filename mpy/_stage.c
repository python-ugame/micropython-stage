/*
 * The MIT License (MIT)
 *
 * Copyright (c) 2018 Radomir Dopieralski
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#define MICROPY_ENABLE_DYNRUNTIME (1)


#include "py/dynruntime.h"
#include "../modules/stage/mod_stage.c"


mp_obj_type_t mp_type_text;
mp_map_elem_t text_locals_dict_table[1];
STATIC MP_DEFINE_CONST_DICT(text_locals_dict, text_locals_dict_table);

mp_obj_type_t mp_type_layer;
mp_map_elem_t layer_locals_dict_table[2];
STATIC MP_DEFINE_CONST_DICT(layer_locals_dict, layer_locals_dict_table);


mp_obj_t mpy_init(mp_obj_fun_bc_t *self, size_t n_args, size_t n_kw,
                mp_obj_t *args) {
    MP_DYNRUNTIME_INIT_ENTRY

    mp_type_text.base.type = (void*)&mp_type_type;
    mp_type_text.name = MP_QSTR_Text;
    mp_type_text.make_new = text_make_new;
    text_locals_dict_table[0] = (mp_map_elem_t){
        MP_OBJ_NEW_QSTR(MP_QSTR_move), MP_OBJ_FROM_PTR(&text_move_obj)
    };
    mp_type_text.locals_dict = (void*)&text_locals_dict;
    mp_store_global(MP_QSTR_Text, MP_OBJ_FROM_PTR(&mp_type_text));

    mp_type_layer.base.type = (void*)&mp_type_type;
    mp_type_layer.name = MP_QSTR_Layer;
    mp_type_layer.make_new = layer_make_new;
    layer_locals_dict_table[0] = (mp_map_elem_t){
        MP_OBJ_NEW_QSTR(MP_QSTR_move), MP_OBJ_FROM_PTR(&layer_move_obj)
    };
    layer_locals_dict_table[1] = (mp_map_elem_t){
        MP_OBJ_NEW_QSTR(MP_QSTR_frame), MP_OBJ_FROM_PTR(&layer_frame_obj)
    };
    mp_type_layer.locals_dict = (void*)&layer_locals_dict;
    mp_store_global(MP_QSTR_Layer, MP_OBJ_FROM_PTR(&mp_type_layer));

    mp_store_global(MP_QSTR_render, MP_OBJ_FROM_PTR(&stage_render_obj));

    MP_DYNRUNTIME_INIT_EXIT
}
