# red black tree

red black tree の理解のため、自分でもプログラムを書いて動かしてみた。

コードは、以下。

[rbtree.py](https://github.com/oda-g/Linux-blog/tree/main/src/rbtree/rbtree.py)

ロジックとしては、Linuxの実装と全く同じである。ただし、Linuxのコードから以下の改善を加えている。

- 親ポインタと色は、別メンバとする。
- 回転操作をメソッド化し使用するようにしている。
- case 間でコードを共有することによる分かりにくさを解消するため、case ごとでコードを分けている。  
(前項の改善のためか、ほとんど重複している感はない。)

簡単のため、キー(int)、比較関数もclassに入れている。

[rbtest.py](https://github.com/oda-g/Linux-blog/tree/main/src/rbtree/rbtest.py) は、動作確認のために使用したプログラム。適当に修正し、動作を試してみるとよい。