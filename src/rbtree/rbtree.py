RED = 0
BLACK = 1

class rb_node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.parent = None
        self.color = RED
        self.key = key

    def cmp(self, key):
        if key < self.key:
            return -1
        elif key > self.key:
            return 1
        return 0


class rb_root:
    def __init__(self):
        self.root = None


def node_color(node):
    if node is None:
        return " - "
    if node.color == RED:
        return "(" + str(node.key) + ")"
    return " " + str(node.key) + " "


def print_node(level, node):
    if node is None:
        return
    if level > 4:
        return

    print(level, ":", node_color(node), "parent:", node_color(node.parent),
          "left:", node_color(node.left), "right:", node_color(node.right))

    if node.left is not None:
        print_node(level + 1, node.left)
    if node.right is not None:
        print_node(level + 1, node.right)


def _rb_change_child(old, new, parent, root):
    # parentの子old(左右どちらか分からないが)をnewに変える。
    if parent is not None:
        if parent.left == old:
            parent.left = new
        else:
            parent.right = new
    else:
        root.root = new


def _rb_left_rotate(node, root):
    '''
    左回転。nodeの右子をnodeの上に変える。(色の処理はなし。位置の移動のみ。)
     n           r
      \         /
       r  =>   n
      /         \
    rl           rl
    '''
    n = node
    r = n.right  # must not be None
    p = n.parent
    rl = r.left

    r.parent = p
    n.parent = r
    n.right = rl
    if rl is not None:
        rl.parent = n
    r.left = n
    _rb_change_child(n, r, p, root)


def _rb_right_rotate(node, root):
    '''
    右回転。nodeの左子をnodeの上に変える。(色の処理はなし。位置の移動のみ。)
      n         l
     /           \
    l     =>      n
     \           /
      lr       lr
    '''
    n = node
    l = n.left  # must not be None
    p = n.parent
    lr = l.right

    l.parent = p
    n.parent = l
    n.left = lr
    if lr is not None:
        lr.parent = n
    l.right = n
    _rb_change_child(n, l, p, root)


# 補足: 以降、コード中のコメントでは、Linuxのコードのコメントにならい、大文字を黒、小文字を赤、どちらでもよい場合を括弧付きで表している。
#
def _rb_insert(node, root):
    n = node
    p = n.parent
    while True:
        # ループ不変条件: nは赤
        if p is None:
            # 一番最初のノードだったか、case 1で先送りされた結果、ルートまでたどり着いた(nはルート)。
            print("case 0")
            n.color = BLACK
            return
        if p.color == BLACK:
            # ノードのつなぎ先が黒であれば問題なし。
            print("case 0'")
            return

        # pは赤。したがって、p.parentは存在し、黒。
        gp = p.parent  # gp: grand parent
        if p == gp.left:
            u = gp.right  # u: uncle
            if u is not None and u.color == RED:
                print("case 1")
                '''
				 case 1 - uは赤。gpとp、uの色を取り換える。
				         G            g
				        / \          / \
				       p   u  -->   P   U
				      /            /
				     n            n
                '''
                p.color = BLACK
                u.color = BLACK
                gp.color = RED
                # gpを赤に変え、問題を先送りした。gpを対象(新たなn)にして、ループを回る。
                n = gp
                p = n.parent
                continue
            # u は、None か、BLACK
            if n == p.right:
                print("case 2")
                '''
				 case 2 - まず、nとpの位置を入れ替え(pで左回転)、次にnとgpの位置を入れ替え(gpで右回転)、nとgpの色を変える。
				        G             G            N
				       / \           / \          / \
				      p   U  -->    n   U  -->   p   g
				       \           /                  \
				        n         p                    U

                 (補足: 図のUがないケース(u == None)も問題ないことに注意)
                '''
                _rb_left_rotate(p, root)
                _rb_right_rotate(gp, root)
                gp.color = RED
                n.color = BLACK
                # 問題解消
                return
            else:  # n == p.left
                print("case 3")
                '''
			    case 3 - case 2の後半と(nとpの位置が違っているが)操作は、同じ。
			            G           P
			           / \         / \
			          p   U  -->  n   g
			         /                 \
			        n                   U
                '''
                _rb_right_rotate(gp, root)
                gp.color = RED
                p.color = BLACK
                # 問題解消
                return
        else:  # p == gp.right
            # if節と左右対称。left と right の単語を入れ替えただけ。
            u = gp.left
            if u is not None and u.color == RED:
                print("case 1'")
                p.color = BLACK
                u.color = BLACK
                gp.color = RED
                n = gp
                p = n.parent
                continue
            if n == p.left:
                print("case 2'")
                _rb_right_rotate(p, root)
                _rb_left_rotate(gp, root)
                gp.color = RED
                n.color = BLACK
                return
            else:
                print("case 3'")
                _rb_left_rotate(gp, root)
                gp.color = RED
                p.color = BLACK


def _rb_erase(node, root):
    n = node
    l = n.left
    r = n.right
    rebalance = None

    if l is None and r is None:
        # nの子がいないケース
        print("case 0")
        _rb_change_child(n, None, n.parent, root)
        if n.color == BLACK:
            rebalance = n.parent
    elif l is None:
        print("case 1")
        '''
        case 1: nの子が一つ(r)。rは赤、nは黒。
           (p)           (p)
             \             \
              N    -->      R
               \
                r
        '''
        _rb_change_child(n, r, n.parent, root)
        r.color = n.color  # RED -> BLACK
        r.parent = n.parent
    elif r is None:
        # nの子が一つ(l)。図は略。
        print("case 1'")
        _rb_change_child(n, l, n.parent, root)
        l.color = n.color  # RED -> BLACK
        l.parent = node.parent
    else:
        # nの子が両方いる場合。
        # s: successor (nに置き換わる、nの次に大きいノード)
        # c: s.right (s.leftはNone)
        if r.left is None:
            print("case 2")
            '''
			case 2: s == r
			      (n)          (s)
			      / \          / \
			    (l) (s)  ->  (l) (c)
			          \
			          (c)
            '''
            s = r
            s.left = l
            l.parent = s
            s.parent = n.parent
            if s.right is not None:
                # cがあれば、cは赤、sは黒である。cを黒に変えれば、数は合う。
                s.right.color = BLACK
            else:
                # cがない場合。sは赤でも黒でもあり得る。黒の場合、数が合わなくなる。(sの色はnに合わせる)
                if s.color == BLACK:
                    rebalance = s
            s.color = n.color
            _rb_change_child(n, s, n.parent, root)
        else:
            print("case 3")
            '''
			case 3: s は、rのleftを追っていった一番先。
			      (n)          (s)
			      / \          / \
			    (l) (r)  ->  (l) (r)
                    ...          ...
			        /            /
			      (sp)         (sp)
			      /            /
			    (s)          (c)
			      \
			      (c)
            '''
            s = r.left
            while True:
                if s.left is None:
                    break
                s = s.left
            c = s.right
            s.parent.left = c
            if c is not None:
                c.parent = s.parent
                # cがあれば、cは赤、sは黒である。cを黒に変えれば、数は合う。
                c.color = BLACK
            else:
                # cがない場合。sは赤でも黒でもあり得る。黒の場合、数が合わなくなる。(sの色はnに合わせる)
                if s.color == BLACK:
                    rebalance = s.parent
            s.right = r
            r.parent = s
            s.left = l
            l.parent = s
            s.parent = n.parent
            s.color = n.color
            _rb_change_child(n, s, n.parent, root)

    return rebalance


def _rb_erase_color(parent, root):
    p = parent
    n = None
    # s: sibling
    while True:
        s = p.right
        if n != s:  # n == p.left
            if s.color == RED:
                print("case 1")
                '''
			    case 1 - left rotate at parent. parent => RED
			        P               S
			       / \             / \
			      N   s    -->    p   Sr
			         / \         / \
			        Sl  Sr      N   Sl
			    '''
                _rb_left_rotate(p, root)
                p.color = RED
                s = s.left
                # fall through
            sr = s.right
            sl = s.left
            if sr is None or sr.color == BLACK:
                if sl is None or sl.color == BLACK:
                    print("case 2")
                    '''
                    case 2 - s => RED
					      (p)           (p)
					      / \           / \
					     N   S    -->  N   s
					        / \           / \
					       Sl  Sr        Sl  Sr
                    '''
                    s.color = RED
                    if p.color == RED:
                        p.color = BLACK
                        # OK. done.
                        return
                    elif p.parent is None:  # p is root. done.
                        return
                    # loop back
                    n = p
                    p = p.parent
                    continue
                    # not reach here
                # sl is RED
                print("case 3")
                '''
				 case 3 - right rotate at sibling and left rotate at parent. sl => p.color, p => BLACK
				     (p)           (p)             (sl)
				     / \           / \             /  \
				    N   S    -->  N   sl   -->    P    S
				       / \             \         /      \
				      sl  Sr            S       N        Sr
				                         \
				                          Sr
                '''
                _rb_right_rotate(s, root)
                _rb_left_rotate(p, root)
                # slの色は元々のpの色に、pの色は黒にする。(図にはないが)1回目のrotate後は、slの左パスの数が1少なくなってしまっているが、
                # 2回目のrotateで、(Pの右パスにつながり)つじつまが合う、ということが裏で起こっている。
                sl.color = p.color
                p.color = BLACK
                # これで数が合った。
                return
            else:  # sr is RED
                print("case 4")
                '''
                case 4 - left rotate at parent. sr => BLACK, s => p.color, p => BLACK
			        (p)             (s)
			        / \             / \
			       N   S     -->   P   Sr
			          / \         / \
			        (sl) sr      N  (sl)
                '''
                _rb_left_rotate(p, root)
                sr.color = BLACK
                s.color = p.color
                p.color = BLACK  # 元々黒かもしれない
                # これで数が合った。
                return
        else:  # n == p.right
            # if 節と左右対称
            s = p.left
            if s.color == RED:
                print("case 1'")
                # case 1
                _rb_right_rotate(p, root)
                p.color = RED
                s = s.right
                # fall through
            sl = s.left
            sr = s.right
            if sl is None or sl.color == BLACK:
                if sr is None or sr.color == BLACK:
                    print("case 2'")
                    # case 2
                    s.color = RED
                    if p.color == RED:
                        p.color = BLACK
                        # OK. done.
                        return
                    elif p.parent is None:  # p is root. done.
                        return
                    # loop back
                    n = p
                    p = p.parent
                    continue
                    # not reach here
                # sr is RED
                print("case 3'")
                # case 3
                _rb_left_rotate(s, root)
                _rb_right_rotate(p, root)
                sr.color = p.color
                p.color = BLACK
                # これで数が合った。
                return
            else:  # sl is RED
                print("case 4'")
                # case 4
                _rb_right_rotate(p, root)
                sl.color = BLACK
                s.color = p.color
                p.color = BLACK  # 元々黒かもしれない
                # これで数が合った。
                return           


def rb_add(node, root):
    parent = root.root
    while parent is not None:
        if parent.cmp(node.key) < 0:
            if parent.left is None:
                parent.left = node
                node.parent = parent
                break;
            else:
                parent = parent.left
        else:
            if parent.right is None:
                parent.right = node
                node.parent = parent
                break
            else:
                parent = parent.right
    if node.parent is None:
        root.root = node
    _rb_insert(node, root)


def rb_find(key, root):
    node = root.root
    while node is not None:
        c = node.cmp(key)
        if c < 0:
            node = node.left
        elif c > 0:
            node = node.right
        else:
            break
    
    return node


def rb_erase(node, root):
    rebalence = _rb_erase(node, root)
    if rebalence is not None:
        print("rebalence")
        _rb_erase_color(rebalence, root)