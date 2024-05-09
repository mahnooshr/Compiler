import anytree
from anytree import Node, RenderTree
import scanner

# while True:
#     first_token = scanner.get_next_token()

root = anytree.Node("root-node")

f = anytree.Node("first-child", parent=root)

def write_tree_to_file(node, indent=0):
    with open("tree_output.txt", "a") as f:
        f.write("  " * indent + node.name + "\n")
        for child in node.children:
            write_tree_to_file(child, indent + 1)

# Call the function with the root node
write_tree_to_file(root)


with open("parse_tree.txt", "w") as parse_tree:
    # for i, symbol in enumerate(parse_tree):
    #     parse_tree.write(str(i + 1) + ".\t" + symbol + "\n")
        for pre, fill, node in RenderTree(root):
            parse_tree.write("%s%s" % (pre, node.name))


