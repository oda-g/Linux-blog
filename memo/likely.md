# likely

likely/unlikelyの効果を確かめるため、以下のような単純なコードを用意した。

src/likely/a.c
```
# define likely(x)      __builtin_expect(!!(x), 1)
# define unlikely(x)    __builtin_expect(!!(x), 0)

extern int x();
extern int y();

int f(int a, int b)
{
        int tmp;

        if (a > 0) {        ★
                tmp = x();
        } else {
                tmp = y();
        }

        return tmp + 1;     ※
}
```

この他に、★の部分を「if (likely(a > 0)) {」にした、a_like.c と 「if (unlikely(a > 0)) {」にした、a_unlike.cを用意してある。

これらをgccでコンパイルした結果も src/likely/ 配下に置いてある。x86_64 環境。

- a.s: a.c 最適化なし
- a-o3.s: a.c -O3
- a_like.s: a_like.c 最適化なし
- a_like-o3.s: a_like.c -O3
- a_unlike-o3.s: a_unlike.c -O3

a_like.s (likely付き、最適化なし)は、悲惨な結果になっている。「!!(x)」の部分がまともにコード化されていて、付けていない場合よりもステップが増えている上に分岐の数も減っていない。一方、最適化を施した結果を見ると、a-o.s(likelyなし)とa_like-o3.s(likely付き)は、全く同じコードになっており、likelyを付ける・付けないよりも最適化の方が重要であることが分かる。

likelyにした場合(a_like-o3.s)とunlikelyにした場合(a_unlike-o3.s)を較べて見ると、条件分岐の部分(★)が異なっている。

a_like-o3.s:
```
        testl   %edi, %edi
        jle     .L2        (a <= 0 の場合にジャンプ。a > 0 の場合は、ジャンプせずに次の命令を実行)
```

a_unlike-o3.s:
```
        testl   %edi, %edi
        jg      .L6        (a > 0 の場合にジャンプ。a <= 0 の場合は、ジャンプせずに次の命令を実行)
```

これは、a_unlike-o3 のコードは、あたかも Cコードが以下のようであったようにコンパイルされているということである。
```
        if (a <= 0) {
                tmp = y();
        } else {
                tmp = x();
        }
```
コンパイラはなかなか頑張っている。これに関しては、unlikelyを使わずとも、初めから、上記のようにコーディングしておけば良かったと言えなくもない。

なお、最適化した場合、※の部分が分岐しなかった部分と分岐した部分の双方に出現しており、余分な分岐をしないようになっている。(return tmp + 1 を一か所にしようとすると、どうしても分岐が発生してしまう。)

(あたかも、以下のようなCコードと同じ。)
```
        if (a > 0) {
                tmp = x();
                return tmp + 1;
        } else {
                tmp = y();
                return tmp + 1;
        }
```