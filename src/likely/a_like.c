# define likely(x)	__builtin_expect(!!(x), 1)
# define unlikely(x)	__builtin_expect(!!(x), 0)

extern int x();
extern int y();

int f(int a, int b)
{
	int tmp;

	if (likely(a > 0)) {
		tmp = x();
	} else {
		tmp = y();
	}

	return tmp + 1;
}
