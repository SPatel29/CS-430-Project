class Tree:
    class Node:
        def __init__(self, data=None, left=None, right=None, bit=None):
            self.data = data
            self.left = left
            self.right = right
            self.bit = bit

        def change_bit(self, bit):
            self.bit = bit

    def __init__(self):
        self.root = None

    def make_root(self, node):
        self.root = node


def huffman(prio_queue):
    if len(prio_queue) > 1:
        min_value = prio_queue[-1]
        del prio_queue[-1]
        max_value = prio_queue[-1]
        del prio_queue[-1]
        merge_nodes(min_value, max_value, prio_queue)
        huffman(prio_queue)


def merge_nodes(node1, node2, prio_queue):
    node1.change_bit("0")
    node2.change_bit("1")
    value = (node1.data[0] + node2.data[0], node1.data[1] + node2.data[1])
    prio_queue.append(Tree.Node(data=value, left=node1, right=node2, bit=None))
    prio_queue.sort(key=lambda x: x.data[1], reverse= True)  # Sort the node objects inside the prio queue by frequency


def traverse_tree(root):  # Post-Order Traversal.
    if root:
        traverse_tree(root.left)
        traverse_tree(root.right)
        print(root.data, 'data', root.bit, 'bit')


def bit_traversal(node, array, tree, bit_dictionary):
    if node and node is tree.root:  # Since the root does not have a bit, we make a separate if clause
        bit_traversal(node.left, array, tree, bit_dictionary)
        bit_traversal(node.right, array, tree, bit_dictionary)
    if node and node.bit and node is not tree.root:  # Every node but the root
        array.append(node.bit)
        bit_traversal(node.left, array, tree, bit_dictionary)
        bit_traversal(node.right, array, tree, bit_dictionary)
        if not node.left and not node.right:  # If it's a leaf node
            bit_dictionary[node.data[0]] = "".join(array)
            del array[-1]
            node.bit = "2"
        if node.left and node.right:  # If it's a parent node
            if node.left.bit == "2" and node.right.bit == "2":  # Means we have visited both subtrees of a node
                node.bit = "2"  # Mark the parent of both subtrees as 2
                if len(array) >= 1:
                    del array[-1]


def file_read(file, hash_map):
    while True:
        character = file.read(1)
        if not character:
            break
        elif character not in hash_map:
            hash_map[character] = 1
        else:
            hash_map[character] += 1
    file.close()


def second_file_read(bit_dictionary, r, w):
    while True:
        character = r.read(1)
        if not character:
            break
        else:
            if bit_dictionary[character]:
                w.write(str(bit_dictionary[character]))


def decoder(node, input_file, tree, output_file):
    if node and not node.right and not node.left:
        output_file.write(node.data[0])
        decoder(tree.root, input_file, tree, output_file)
    elif node:
        character = input_file.read(1)
        if character:
            if character == "0":
                decoder(node.left, input_file, tree, output_file)
            elif character == "1":
                decoder(node.right, input_file, tree, output_file)


def printTree(node, level=0):
    if node:
        printTree(node.left, level + 1)
        print('')
        print(' ' * 6 * level + '->', node.data)
        print('')
        printTree(node.right, level + 1)


def main():
    prio_queue = []
    hash_map = {}
    bit_mapping = []
    bit_dictionary = {}
    tree = Tree()
    file_path = ""
    try:
        file_path = input("Enter path:")
        if file_path.find('""'):
            file_path = file_path.strip('"')  # Safety measure in case user types path with quotes
        file = open(file_path, "r")
        file_read(file, hash_map)
    except FileNotFoundError:
        msg = "Sorry, cannot find file. Please check if correct path of file"
        print(msg)
    unsorted_lst = list(hash_map.items())
    sorted_lst = sorted(unsorted_lst, key=lambda x: x[1],
                        reverse=True)  # Sort by the second item (index 1) from the tuple
    print(sorted_lst)
    for i in sorted_lst:
        prio_queue.append(Tree().Node(i))
    huffman(prio_queue)
    tree.root = prio_queue[0]  # Set the root of the tree to be the only element left in the prio queue
    root_node = tree.root
    traverse_tree(root_node)
    bit_traversal(root_node, bit_mapping, tree, bit_dictionary)
    print(bit_dictionary)
    print(root_node.right.bit)
    printTree(root_node)
    r = open(file_path, "r")
    w = open("encode.txt", "w+")
    second_file_read(bit_dictionary, r, w)
    r.close()
    w.close()
    r2 = open("encode.txt", "r")
    w = open("a-out.txt", "w+")
    decoder(root_node, r2, tree, w)
    w.close()
    r2.close()


if __name__ == "__main__":
    main()
