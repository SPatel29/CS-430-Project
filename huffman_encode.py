prio_queue = []
hash_map = {}


class Tree:
    class Node:
        def __init__(self, data=None, left=None, right=None):
            self.data = data
            self.left = left
            self.right = right

    def __init__(self):
        self.root = None

    def make_root(self, node):
        self.root = node


def huffman():
    while len(prio_queue) > 1:
        min_value = prio_queue[0]
        max_value = prio_queue[1]
        del prio_queue[0]
        del prio_queue[0]
        merge_nodes(min_value, max_value)


def merge_nodes(node1, node2):
    node1.bit = 0
    node2.bit = 1
    value = (node1.data[0] + node2.data[0], node1.data[1] + node2.data[1])
    # print(value)
    prio_queue.append(Tree.Node(data=value, left=node1, right=node2))
    prio_queue.sort(key=lambda x: x.data[1])  # Sort the node objects inside the prio queue
    # for x in prio_queue:
    #    print(x.data, 'sorted prio again')
    # print(prio_queue[-1].left.bit, prio_queue[-1].right.bit)


def file_read(file):
    while True:
        character = file.read(1)
        if not character:
            break
        elif character not in hash_map:
            hash_map[character] = 1
        else:
            hash_map[character] += 1
    file.close()


def main():
    tree = Tree()
    try:
        file_path = input("Enter path:")
        file = open(file_path, "r")
        file_read(file)
    except FileNotFoundError:
        msg = "Sorry, cannot find file. Please check if correct path of file"
        print(msg)
    unsorted_lst = list(hash_map.items())
    sorted_lst = sorted(unsorted_lst, key=lambda x: x[1],
                        reverse=False)  # Sort by the second item (index 1) from the tuple
    #print(sorted_lst)
    for i in sorted_lst:
        prio_queue.append(Tree().Node(i))
    huffman()
    #print(len(prio_queue))
    #for i in prio_queue:
    #    print(i.data, i.left.data, i.right.data)
    tree.make_root(prio_queue[0])
    #print(tree.root.data, 'data')
    #if tree.root.left:
    #    print(tree.root.left.data, 'left')
    #if tree.root.right:
    #    print(tree.root.right.data, 'right')


if __name__ == "__main__":
    main()
