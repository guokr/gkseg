CFLAGS =-std=c99 -fPIC -W -Wall -Wextra -O3
LIBS   =-lm -lpthread

DESTDIR=
PREFIX =/usr/local

INSTALL= install -p
INSTALL_EXEC= $(INSTALL) -m 0755
INSTALL_DATA= $(INSTALL) -m 0644

SRC=src/*.c
HDR=src/*.h

wapiti: $(SRC) $(HDR)
	@$(CC) -DNDEBUG  -c -o bcd.o src/bcd.c           $(CFLAGS) $(LIBS) 
	@$(CC) -DNDEBUG  -c -o lbfgs.o src/lbfgs.c       $(CFLAGS) $(LIBS) 
	@$(CC) -DNDEBUG  -c -o pattern.o src/pattern.c   $(CFLAGS) $(LIBS) 
	@$(CC) -DNDEBUG  -c -o reader.o src/reader.c     $(CFLAGS) $(LIBS) 
	@$(CC) -DNDEBUG  -c -o thread.o src/thread.c     $(CFLAGS) $(LIBS) 
	@$(CC) -DNDEBUG  -c -o decoder.o src/decoder.c   $(CFLAGS) $(LIBS) 
	@$(CC) -DNDEBUG  -c -o model.o src/model.c       $(CFLAGS) $(LIBS) 
	@$(CC) -DNDEBUG  -c -o progress.o src/progress.c $(CFLAGS) $(LIBS) 
	@$(CC) -DNDEBUG  -c -o rprop.o src/rprop.c       $(CFLAGS) $(LIBS) 
	@$(CC) -DNDEBUG  -c -o tools.o src/tools.c       $(CFLAGS) $(LIBS) 
	@$(CC) -DNDEBUG  -c -o gradient.o src/gradient.c $(CFLAGS) $(LIBS) 
	@$(CC) -DNDEBUG  -c -o options.o src/options.c   $(CFLAGS) $(LIBS) 
	@$(CC) -DNDEBUG  -c -o quark.o src/quark.c       $(CFLAGS) $(LIBS) 
	@$(CC) -DNDEBUG  -c -o sgdl1.o src/sgdl1.c       $(CFLAGS) $(LIBS) 
	@$(CC) -DNDEBUG  -c -o vmath.o src/vmath.c       $(CFLAGS) $(LIBS) 
	@$(CC) -DNDEBUG  -c -o label.o src/label.c       $(CFLAGS) $(LIBS) 
	@$(CC) -DNDEBUG  -c -o wapiti.o src/wapiti.c     $(CFLAGS) $(LIBS) 
	@$(CC) -shared -Wl -o libwapiti.so bcd.o lbfgs.o pattern.o reader.o thread.o wapiti.o decoder.o model.o progress.o rprop.o tools.o gradient.o  options.o quark.o sgdl1.o vmath.o label.o -lc
	@echo "CC: wapiti.c --> wapiti"
	@$(CC) -DNDEBUG $(CFLAGS) -o wapiti $(SRC) $(LIBS)

debug: $(SRC) $(HDR)
	@echo "CC: wapiti.c --> wapiti"
	@$(CC) -g $(CFLAGS) -o wapiti $(SRC) $(LIBS)

install: wapiti
	@echo "CP: wapiti   --> $(DESTDIR)$(PREFIX)/bin"
	@mkdir -p $(DESTDIR)$(PREFIX)/bin
	@mkdir -p $(DESTDIR)$(PREFIX)/share/man/man1
	@$(INSTALL_EXEC) wapiti       $(DESTDIR)$(PREFIX)/bin
	@$(INSTALL_DATA) doc/wapiti.1 $(DESTDIR)$(PREFIX)/share/man/man1

clean:
	@echo "RM: wapiti"
	@rm -f wapiti
	@rm -f *.o
	@rm -f *.so

.PHONY: clean install
