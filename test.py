from treelib import Tree, Node
import pickle

# 文件数据类型
class File:
    def __init__(self, data):
        self.data = data

# 创建一个空树
tree = Tree()

# 创建一个根节点
root_node = Node(identifier="root", data=File(1))
tree.add_node(root_node)

# 创建一个子节点，并将其添加到根节点下
child_node = Node(identifier="child", data=File(666))
tree.add_node(child_node, parent="root")

# 创建一个孙子节点，并将其添加到子节点下
grandchild_node = Node(identifier="grandchild", data=File("Grandchild"))
tree.add_node(grandchild_node, parent="child")

with open('test.pkl', 'wb') as file:
    pickle.dump(tree, file)

with open('test.pkl', 'rb') as file:
    new = pickle.load(file)

# 打印整棵树
new.show()
# 获取children
print(tree.children('root'))
# 获取parent
print(tree.get_node(tree.ancestor('grandchild')))


