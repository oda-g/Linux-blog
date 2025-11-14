import random
import rbtree

root = rbtree.rb_root()
#keys = random.sample(range(15), k=15)
#keys = random.sample(range(20), k=20)
#keys = [0, 5, 6, 8, 18, 16, 12, 13, 3, 4, 19, 15, 2, 9, 7, 14, 17, 10, 1, 11]
keys = [14, 0, 1, 3, 11, 9, 6, 5, 2, 10, 8, 13, 7, 4, 12]
print(keys)
for key in keys:
    print("insert", key)
    node = rbtree.rb_node(key)
    rbtree.rb_add(node, root)
    rbtree.print_node(0, root.root)
    print()

#keys = random.sample(range(15), k=15)
keys = [2, 6, 13, 12, 3, 8, 7, 4, 9, 10, 11, 14, 0, 5, 1]
print(keys)
for key in keys:
    print("delete", key)
    node = rbtree.rb_find(key, root)
    if node is None:
        print("not found", key)
        break
    rbtree.rb_erase(node, root)
    rbtree.print_node(0, root.root)
    print()
    if key == 9:
        break
