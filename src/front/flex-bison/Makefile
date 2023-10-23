
main:
	$(MAKE) flex_part
	$(MAKE) bison_part
	gcc -o calc y.tab.c lex.yy.c

flex_part:
	flex calc.1

bison_part:
	bison -vdty calc.y

clean:
	rm calc lex* y*
