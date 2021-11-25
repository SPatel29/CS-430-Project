class Heap:
    def __init__(self):
        self.heap = []
        self.size = 0

    def insert(self, value):
        self.size += 1
        self.heap.append(value)

    def build_min_heap(self):
        for i in range((self.size // 2) - 1, -1, -1):  # Start from parent of leaf and work way up to root
            self.min_heapify(i)

    def min_heapify(self, index):  # Go from parent to leaf, switching values when necessary
        left = leftChild(index)
        right = rightChild(index)

        # If left is in heap and it is smaller than its parent
        if left <= self.size - 1 and self.heap[left].data[1] < self.heap[index].data[1]:
            smallest = left
        else:
            smallest = index
        # If right is in heap and it is smaller than the current smallest node:
        if right <= self.size - 1 and self.heap[right].data[1] < self.heap[smallest].data[1]:
            smallest = right
        if smallest != index:  # Swap if original element is not the smallest between its children
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self.min_heapify(smallest)

    def extract_min(self):
        if self.size > 0:
            min_value = self.heap[0]
            self.heap[0] = self.heap[-1]
            self.size -= 1
            del self.heap[-1]
            self.min_heapify(0)  # Start from root and work all the way down to leaf
            return min_value


class Tree:
    class Node:
        def __init__(self, data=None, left=None, right=None, bit=None, traverse=False):
            self.data = data
            self.left = left
            self.right = right
            self.bit = bit
            self.traverse = traverse

    def __init__(self):
        self.root = None


def parent(index):
    return (index - 1) // 2


def rightChild(index):
    return (2 * index) + 2


def leftChild(index):
    return (2 * index) + 1


# Huffman algorithm:
def huffman(heap, tree):  # O(Nlog(N))
    if heap.size > 1:  # (N)
        first_min_value = heap.extract_min()
        second_min_value = heap.extract_min()
        merge_nodes(first_min_value, second_min_value, heap, tree)  # log(N). merge_nodes calls build_min_heap
        huffman(heap, tree)


def merge_nodes(node1, node2, heap, tree):  # Takes a heap, tree and 2 node objects as parameter
    node1.bit = '0'
    node2.bit = '1'
    value = (node1.data[0] + node2.data[0], node1.data[1] + node2.data[1])
    heap.insert(tree.Node(data=value, left=node1, right=node2, bit=None, traverse=False))  # Insert new node to heap
    heap.build_min_heap()  # log(N). build_min_heap takes log(N) time


def traverse_tree(root):  # Post-Order Traversal. Takes in a node object as parameter
    if root:
        traverse_tree(root.left)
        traverse_tree(root.right)
        print(root.data, 'data', root.bit, 'bit')


# bit_traversal function maps letter to code to and inserts it to bit_dictionary
# The bits parameter is an array with all the bits leading up to a leaf node.
def bit_traversal(node, bits, tree, bit_dictionary):
    if node and node is tree.root:  # Since the root does not have a bit, we make a separate if clause
        bit_traversal(node.left, bits, tree, bit_dictionary)
        bit_traversal(node.right, bits, tree, bit_dictionary)
    if node and node.bit and node is not tree.root:  # Every node but the root
        bits.append(node.bit)
        bit_traversal(node.left, bits, tree, bit_dictionary)
        bit_traversal(node.right, bits, tree, bit_dictionary)
        if not node.left and not node.right:  # If it's a leaf node
            bit_dictionary[node.data[0]] = "".join(bits)  # maps the letter to code. (letter: code)
            del bits[-1]  # Delete most recent added bit, for when we recurse back to parent and go to next child
            node.traverse = True
        if node.left and node.right:  # If it's a parent node
            if node.left.traverse and node.right.traverse:  # Means we have visited both subtrees of a node
                node.traverse = True  # Mark the parent if all children subtrees have been traversed
                if len(bits) >= 1:
                    del bits[-1]  # Delete the parent node bit for when we recurse back


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


# Takes the bit dictionary, which maps letter to code and writes the code aspect to a user requested file
# bit_dictionary has the letter to code dictionary
# r is the original file user wanted encoded
# w is the output file user wants to redirect output of encoding process to. W later used for decoding
def second_file_read(bit_dictionary, r, w):
    while True:
        character = r.read(1)
        if not character:
            break
        else:
            if bit_dictionary[character]:
                w.write(str(bit_dictionary[character]))


# decoder function decodes the output of the encoding process
# input file is the w file from second_file_read
# tree consists of the root node only. Uses pointers to traverse nodes
# output_file is the desired user file
# decoder recursively iterates through heap, until we hit a leaf node, which we know is a character
# then it recurses back to root when we hit a leaf and write character to output file,
# since we don't know where the next character of the input file is located on the tree

def decoder(node, input_file, tree, output_file):
    if node and not node.right and not node.left:
        output_file.write(node.data[0])  # write the character the user output file
        decoder(tree.root, input_file, tree, output_file)  # recurse back to root
    elif node:
        character = input_file.read(1)  # we read the encoded file and determine if it is a '0' or a '1'
        if character:
            if character == "0":
                decoder(node.left, input_file, tree, output_file)  # recall nodes with bit 0 are placed on left side
            elif character == "1":
                decoder(node.right, input_file, tree, output_file)  # recall nodes with bit 1 are placed on right side


def printTree(node, tree, level=0):  # Uses the idea of inorder traversal to print out tree. Prints tree horizontally
    if node:
        string = 'root:'
        if node is not tree.root:
            string = '---{'
        printTree(node.left, tree, level + 1)
        print('')
        print(' ' * 5 * level + string, node.data)  # Adds spacing depending on what level node is
        print('')
        printTree(node.right, tree, level + 1)


def menu_print():
    print("Welcome to the Huffman Tree Encoder and Decoder!")
    print("-------------------------------------------------")
    print("The option menu is:")
    print("1. Encode and Decode")
    print("2. Help")
    print("3. Quit")
    option = input("What would you like to do?\n")
    return option


def help_menu():
    print("\n")
    print("                     HELP MENU:                          ")
    print("---------------------------------------------------------")
    print("This program takes a text file and encodes that file\n")
    print("The program then immediately decodes that encoded file\n")
    print("To input a file, a user can:")
    print("-------> Enter an absolute location of the file")
    print("-------> Enter the name of file, given it is in the same directory as this program file")
    print("\n")
    while True:
        print("--Type 1 to start encoding and decoding\n")
        print("--Type quit to exit out of the program\n")
        choice = input("What would you like to do?\n")
        choice = choice.strip("'")
        choice = choice.lower()
        if choice == "1" or choice == "start encoding and decoding":
            choice = "1"
            return choice
        elif choice == "quit" or choice == "exit":
            choice = "3"
            return choice
        else:
            print("Please Type a valid option")


def main():
    choice = menu_print()
    if choice == "2" or choice.lower() == "help":
        choice = help_menu()
    if choice == "3" or choice.lower() == "quit":
        print("Goodbye!")
    if choice == "1" or choice.lower() == "encode and decode":
        print("Starting Encoding and Decoding Process\n")
        hash_map = {}
        heap = Heap()
        tree = Tree()
        bits = []
        bit_dictionary = {}
        try:
            file_path = input("Enter relative or absolute path of INPUT file for ENCODING:")
            if file_path.find('""'):
                file_path = file_path.strip('"')  # Safety measure in case user types path with quotes
            file = open(file_path, "r")
            file_read(file, hash_map)
            print("\n")
            print("Enter relative or absolute path to redirect OUTPUT from ENCODING")
            encode_output_file = input("I would like to redirect output from ENCODING to: ")
            encode_output_file = encode_output_file.strip('"')
            print("\n")
            print("Enter relative or absolute path file to redirect OUTPUT from DECODING")
            decode_output_file = input("I would like to redirect output from DECODING to: ")
            decode_output_file = decode_output_file.strip('"')
            unsorted_lst = list(hash_map.items())
            for i in unsorted_lst:
                heap.insert(tree.Node(data=i, left=None, right=None, bit=None, traverse=False))
            heap.build_min_heap()
            huffman(heap, tree)
            tree.root = heap.heap[0]  # Make the only item in heap the root node
            bit_traversal(tree.root, bits, tree, bit_dictionary)
            r = open(file_path, "r")
            w = open(encode_output_file, "w+")
            second_file_read(bit_dictionary, r, w)
            r.close()
            w.close()
            r2 = open(encode_output_file, "r")
            w = open(decode_output_file, "w+")
            decoder(tree.root, r2, tree, w)
            w.close()
            r2.close()
            print("")
            print("")
            print("TREE PRINT:")
            print("---------------------------------------------------------------------------")
            print("READ IN HORIZONTAL DIRECTION, LEFTMOST IS THE ROOT, RIGHTMOST IS LEAF\n"
                  "EVERYTHING BELOW 'root:' IS THE LEFT-HAND SUBTREE OF ROOT\n"
                  "EVERYTHING ABOVE 'root:' IS THE RIGHT-HAND SUBTREE OF ROOT"
                  )
            print("")
            printTree(tree.root, tree)
            print("")
            print("SCROLL UP FOR TREE PRINT UNTIL YOU REACH 'root:' \n"
                  "READ IN HORIZONTAL DIRECTION, LEFTMOST IS THE ROOT, RIGHTMOST IS LEAF\n"
                  "EVERYTHING BELOW 'root:' IS THE LEFT-HAND SUBTREE OF ROOT\n"
                  "EVERYTHING ABOVE 'root:' IS THE RIGHT-HAND SUBTREE OF ROOT")
            print("")
            print("")
            print("PRINTED DICTIONARY OF CODE WORDS")
            print("------------------------------------")
            print("Your dictionary of codewords (letter to code) in NO PARTICULAR ORDER, is: \n")
            print(bit_dictionary)
            print("")
            print("")

            print("SCROLL UP FOR TREE PRINT")

        except FileNotFoundError:
            msg = "Sorry, cannot find file. Please check your path to file and try again!"
            print(msg)
    else:
        print("Try again and enter valid option")


if __name__ == "__main__":
    main()
