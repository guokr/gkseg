/*
 *      Wapiti - A linear-chain CRF tool
 *
 * Copyright (c) 2009-2011  CNRS
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#include <inttypes.h>
#include <limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#include "decoder.h"
#include "options.h"
#include "reader.h"
#include "tools.h"

#include "label.h"


/*******************************************************************************
 * Global structure
 ******************************************************************************/

const char  *shmdir = "/dev/shm/gkseg";
const char  *shmin = "/dev/shm/gkseg_in_";
const char  *shmout = "/dev/shm/gkseg_out_";

struct struct_paths *paths_in  = NULL;    /* important! initialize to NULL */
struct struct_paths *paths_out = NULL;    /* important! initialize to NULL */
struct struct_opts  *opts = NULL;    /* important! initialize to NULL */

mdl_t *ptr_mdl = NULL;
const opt_t label_opt_defaults =  {
    .mode    = 1,
    .input   = NULL,     .output  = NULL,
    .type    = "crf",
    .maxent  = false,
    .algo    = "l-bfgs", .pattern = NULL,  .model = NULL,   .devel  = NULL,
    .compact = false,    .sparse  = false,
    .nthread = 1,        .jobsize = 64,    .maxiter = INT_MAX,
    .rho1    = 0.5,      .rho2    = 0.0001,
    .objwin  = 5,        .stopwin = 5,     .stopeps = 0.02,
    .lbfgs = {.clip   = false, .histsz = 5, .maxls = 40},
    .sgdl1 = {.eta0   = 0.8,   .alpha  = 0.85},
    .bcd   = {.kappa  = 1.5},
    .rprop = {.stpmin = 1e-8, .stpmax = 50.0, .stpinc = 1.2, .stpdec = 0.5,
              .cutoff = false},
    .label   = false,    .check   = false, .outsc = false,
    .lblpost = false,    .nbest = 1
};
opt_t opt;

/*******************************************************************************
 * Labeling API
 ******************************************************************************/

void label_init(char *mpath) {
    opt = label_opt_defaults;
    ptr_mdl = mdl_new(rdr_new(opt.maxent));
    ptr_mdl->opt = &opt;

    // First, load the model provided by the user. This is mandatory to
    // label new datas ;-)
    if (mpath == NULL)
        fatal("you must specify a model");
    //info("* Load model\n");
    FILE *file = fopen(mpath, "r");
    if (file == NULL)
        pfatal("cannot open input model file");
    mdl_load(ptr_mdl, file);
    fclose(file);

    mkdir(shmdir, 0777);
    //int result = mkdir(shmdir, 0777);
    //if (result == -1)
    //    pfatal("cannot create data folder");
}

void label_paths(int key) {
    char path[512];
    struct struct_paths *i, *o;

    i = (struct struct_paths*)xmalloc(sizeof(struct struct_paths));
    i->id = key;
    sprintf(path, "%s%d", shmin, key);
    //printf("input file: %s\n", path);
    strcpy(i->name, path);
    HASH_ADD_INT(paths_in, id, i);  /* id: name of key field */

    o = (struct struct_paths*)xmalloc(sizeof(struct struct_paths));
    o->id = key;
    sprintf(path, "%s%d", shmout, key);
    //printf("output file: %s\n", path);
    strcpy(o->name, path);
    HASH_ADD_INT(paths_out, id, o);  /* id: name of key field */
}

char *get_in(int key) {
    struct struct_paths *s;
    HASH_FIND_INT(paths_in, &key, s);  /* s: output pointer */
    //printf("get input file: %s\n", s->name);
    return s->name;
}

char *get_out(int key) {
    struct struct_paths *s;
    HASH_FIND_INT(paths_out, &key, s);  /* s: output pointer */
    //printf("get out file: %s\n", s->name);
    return s->name;
}

void label_in(int key, const char* value) {
    FILE *fout = fopen(get_in(key), "w");
    fputs(value, fout);
    fclose(fout);
}

void label_do(int key) {
    FILE *fin = stdin, *fout = stdout;
    fin = fopen(get_in(key), "r");
    if (fin == NULL)
        pfatal("cannot open input data file");
    fout = fopen(get_out(key), "w");
    if (fout == NULL)
        pfatal("cannot open output data file");

    // Do the labelling
    //info("* Label sequences\n");
    tag_label(ptr_mdl, fin, fout);
    //info("* Done\n");

    // And close files
    fclose(fin);
    fclose(fout);
}

void label_out(int key, char *value) {
    FILE *fout = fopen(get_out(key), "r");
    if (fout == NULL)
        pfatal("cannot open output data file");

    int ind = 0;
    while (1) {
       char ch = fgetc (fout) ;
       if (ch == EOF)
           break;
       else
           value[ind] = ch;
       ind++;
    }

    fclose(fout);
}

void label_free(int key) {
    struct struct_paths *s;
    HASH_FIND_INT(paths_in, &key, s);
    remove(s->name);
    HASH_DEL(paths_in, s);
    free(s);
    HASH_FIND_INT(paths_out, &key, s);
    remove(s->name);
    HASH_DEL(paths_out, s);
    free(s);
}

void label_destroy() {
    mdl_free(ptr_mdl);
    free(paths_in);
    free(paths_out);

    rmdir(shmdir);
}

