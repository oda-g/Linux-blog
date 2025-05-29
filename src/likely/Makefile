all: a.s a-o3.s a_like.s a_like-o3.s a_unlike-o3.s

a.s: a.c
	gcc -S a.c

a-o3.s: a.c
	gcc -S -O3 -o a-o3.s a.c

a_like.s: a_like.c
	gcc -S a_like.c
       
a_like-o3.s: a_like.c
	gcc -S -O3 -o a_like-o3.s a_like.c

a_unlike-o3.s: a_unlike.c
	gcc -S -O3 -o a_unlike-o3.s a_unlike.c
