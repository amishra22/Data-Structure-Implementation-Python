class SinglyLinkedNode(object):
    def __init__(self, item=None, next_link=None):
        super(SinglyLinkedNode, self).__init__()
        self._item = item
        self._next = next_link

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        self._item = item

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next):
        self._next = next

    def __repr__(self):
        return repr(self.item)


class DoublyLinkedNode(object):
    def __init__(self, key=None, value=None, next_link=None, prev_link=None):
        super(DoublyLinkedNode, self).__init__()
        self._key = key
        self._value = value
        self._next = next_link
        self._prev = prev_link

    @property
    def key(self):
        return self._key

    @key.setter
    def item(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, next):
        self._next = next

    @property
    def prev(self):
        return self._prev

    @prev.setter
    def prev(self, prev):
        self._prev = prev

    def __repr__(self):
        return repr(self.key)


class SinglyLinkedList(object):
    def __init__(self):
        super(SinglyLinkedList, self).__init__()
        self.head = None

    def __len__(self):
        """
        :return:
        returns the length of the linked list
        """
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.next
        return count

    def __iter__(self):
        current = self.head
        while current is not None:
            yield str(current.item)
            current = current.next

    def __contains__(self, item):
        """
        :param item:
         check if item is present in the linked list
        :return:
        returns True if item is present otherwise returns False
        """
        current = self.head
        found = False
        while current and found is False:
            if current.item == item:
                found = True
            else:
                current = current.next
        if current is None:
            raise ValueError("Item not found")
        return found

    def remove(self, item):
        """
        :param item:
         delete the item from the linked list
        :return:
        deletes the item from linked list \
        and return True otherwise return False
        """
        current = self.head
        previous = None
        found = False
        while current and found is False:
            if current.item == item:
                found = True
            else:
                previous = current
                current = current.next
        if current is None:
            return False
        if previous is None:
            self.head = current.next
            found = True
        else:
            previous.next = current.next
            found = True
        return found

    def prepend(self, item):
        """
        :param item:
        add the item at the head of the linked list
        :return:
        """
        new_node = SinglyLinkedNode(item, self.head)
        self.head = new_node

    def __repr__(self):
        s = "List:" + "->".join([item for item in self])
        return s


class ChainedHashDict(object):
    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        super(ChainedHashDict, self).__init__()

        self._bin_count = bin_count
        self._max_load = max_load
        self._load_factor = 0.0
        self.hash_slot = [DoublyLinkedNode(None, None, None, None)
                          for i in range(self._bin_count)]
        self.hash_func = hashfunc

    @property
    def load_factor(self):
        self._load_factor = self.__len__() / float(self._bin_count)
        return self._load_factor

    @property
    def bin_count(self):
        print self._bin_count

    def rebuild(self, bincount):
        self.hash_slot += \
            [DoublyLinkedNode(None, None, None, None) for i in range(bincount)]

    def __getitem__(self, key):
        """
        :param key:
        the key whose value is to be found
        :return:
        if the key is found it returns the \
        value associated with the key  otherwise raise exception
        """
        hash_value = self.hash_func(key)
        temp = self.hash_slot[hash_value]
        tvalue = None
        while temp and temp.key != key:
            temp = temp.next
        if temp and temp.key == key:
            tvalue = temp.value
        if tvalue:
            return tvalue
        else:
            raise ValueError("Value not found")

    def __setitem__(self, key, value):
        """
        :param key:
        find the slot in hash table based on the key \
        and add the value associated with the key
        :param value:
        the value to be inserted for the key
        :return:
        """
        if self._load_factor == self._max_load:
            self.rebuild(10)
            self._bin_count += 10
        hash_value = self.hash_func(key)
        new_node = DoublyLinkedNode(key, value, None, None)
        if self.hash_slot[hash_value].key is None:
            self.hash_slot[hash_value] = new_node
        else:
            temp = self.hash_slot[hash_value]
            self.hash_slot[hash_value] = new_node
            new_node.next = temp
            temp.prev = new_node

    def __delitem__(self, key):
        """
        :param key:
         delete the key-value pair from the hash table
        :return:
        raise exception if key was not found for deletion
        """
        hash_value = self.hash_func(key)
        temp = self.hash_slot[hash_value]
        while temp and temp.key != key:
            temp = temp.next
        if not temp:
            raise ValueError("Value not found")
        if temp == self.hash_slot[hash_value] and not temp.next:
            self.hash_slot[hash_value] = \
                DoublyLinkedNode(None, None, None, None)
        elif temp == self.hash_slot[hash_value] and temp.next:
            self.hash_slot[hash_value] = temp.next
        elif temp.key == key and temp.next:
            temp.prev.next = temp.next
            temp.next.prev = temp.prev
        elif temp.key == key:
            temp.prev.next = temp.next

    def __contains__(self, key):
        """
        :param key:
         check whether the hash table contains key
        :return:
        return True if the has table contains key else raise exception
        """
        hash_value = self.hash_func(key)
        temp = self.hash_slot[hash_value]
        found = False
        while temp and temp.key != key:
            temp = temp.next
        if temp and temp.key == key:
            found = True
        if found:
            return found
        else:
            raise ValueError("Value not found")

    def __len__(self):
        """
        :return:
        length of the hashtable
        """
        count = 0
        for i in range(len(self.hash_slot)):
            temp = self.hash_slot[i]
            while temp is not None:
                count += 1
                temp = temp.next
        return count

    def display(self):
        """
        :return:
        return all the key-value pair as a string
        """
        s = ""
        for i in range(len(self.hash_slot)):
            if self.hash_slot[i] is not None:
                temp = self.hash_slot[i]
                # print i, ":",
                s += str(i) + ":"
                while temp:
                    s = s + "(" + str(temp.key) + "," + str(temp.value) + ")->"
                    # print "(", temp.key, ",", temp.value, ")->",
                    temp = temp.next
                s += "NULL\n"
                i += 1
        return s


class OpenAddressHashDict(object):
    def __init__(self, bin_count=10, max_load=0.7, hashfunc=hash):
        super(OpenAddressHashDict, self).__init__()

        self._bin_count = bin_count
        self.max_load = max_load
        self.__load_factor = 0
        self.i = 1
        self.hash_slot = [None for i in range(self._bin_count)]
        self.hash_value = [None for i in range(self._bin_count)]
        self.hash_func = hashfunc

    @property
    def load_factor(self):
        length_hash = self.__len__()
        return length_hash / float(self._bin_count)

    @property
    def bin_count(self):
        print self._bin_count

    def rebuild(self, bincount):
        """
        :param bincount:
         rebuild the hash by this amount
        :return:
        returns the new rebuilt hash
        """
        new_hash_slot = [None for i in range(bincount)]
        new_hash_value = [None for i in range(bincount)]
        self.hash_slot = self.hash_slot + new_hash_slot
        self.hash_value = self.hash_value + new_hash_value

    def __getitem__(self, key):
        """
        :param key:
         the value associated with this key
        :return:
        returns the value associated with this key otherwise raise exception
        """
        hash_index = self.hash_func(key)
        value = None
        stop = False
        found = False
        pos = hash_index
        while self.hash_slot[pos] is not None and not stop and not found:
            if self.hash_slot[pos] == key:
                found = True
                value = self.hash_value[pos]
            else:
                pos = (pos + 1) % self._bin_count
                if pos == hash_index:
                    stop = True
        if value:
            return value
        else:
            raise ValueError("Value not found")

    def __setitem__(self, key, value):
        """
        :param key:
         the key value to be inserted
        :param value:
        the value associated with the key
        :return:
        """
        if self.load_factor == self.max_load:
            self.rebuild(10)
            self._bin_count += 10
        hash_index = self.hash_func(key)
        if self.hash_slot[hash_index] is None or \
                self.hash_slot[hash_index] is "del" or\
                self.hash_slot[hash_index] == key:
            self.hash_slot[hash_index] = key
            self.hash_value[hash_index] = value
        else:
            while self.hash_slot[hash_index] is not None and \
                    self.hash_slot[hash_index] is not "del" and \
                    self.hash_slot[hash_index] != key:
                hash_index = (hash_index + 1) % self._bin_count
            self.hash_slot[hash_index] = key
            self.hash_value[hash_index] = value

    def __delitem(self, key):
        """
        :param key:
         the key-value pair that has to be deleted
        :return:
        deletes the key-value pair if found otherwise raise exception
        """
        stop = False
        found = False
        start_index = self.hash_func(key)
        pos = start_index
        while self.hash_slot[pos] is not None and not stop and not found:
            if self.hash_slot[pos] == key:
                self.hash_slot[pos] = "del"
                self.hash_value[pos] = "del"
                found = True
            else:
                pos = (pos + 1) % self._bin_count
                if pos == start_index:
                    stop = True
        if not found:
            raise ValueError("Value not found")

    def __contains__(self, key):
        """
        :param key:
         the key which has to be checked in the hash table
        :return:
        return true if the key is present\
         in hash table otherwise raise exception
        """
        hash_index_start = self.hash_func(key)
        stop = False
        found = False
        pos = hash_index_start
        while self.hash_slot[pos] is not None and not stop and not found:
            if self.hash_slot[pos] == key:
                found = True
            else:
                pos = (pos + 1) % self._bin_count
                if pos == hash_index_start:
                    stop = True
        if found:
            return found
        else:
            raise ValueError("Value not found")

    def __len__(self):
        """
        :return:
        returns the length of hashtable
        """
        count = 0
        for i in range(len(self.hash_slot)):
            if self.hash_slot[i] is not None:
                count += 1
        return count

    def display(self):
        """
        :return:
        returns all the key-value pair of the hashtable as a string
        """
        s = ""
        s += "Key\t\tValue\n"
        for i in range(len(self.hash_slot)):
            s += str(self.hash_slot[i]) + "\t\t" + str(self.hash_value[i]) \
                + "\n"
        return s


class BinaryTreeNode(object):
    def __init__(self, data=None, left=None, right=None, parent=None):
        super(BinaryTreeNode, self).__init__()
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent


class BinarySearchTreeDict(object):
    def __init__(self):
        super(BinarySearchTreeDict, self).__init__()
        self.root = None
        self.parent = None
        self._height = None
        self.length = 0
        pass

    @property
    def height(self):
        """
        :return:
        returns the height of the tree
        """
        return self.height_rec(self.root)

    def height_rec(self, node):
        if not node:
            return 0
        return max(self.height_rec(node.left), self.height_rec(node.right)) + 1

    def inorder_keys_rec(self, node):
        if node:
            for data in self.inorder_keys_rec(node.left):
                yield data
            yield node.data
            for data in self.inorder_keys_rec(node.right):
                yield data

    def inorder_keys(self):
        """
        :return:
        returns the inorder traversal of the tree
        """
        return [n for n in self.inorder_keys_rec(self.root)]

    def postorder_keys_rec(self, node):
        if node:
            for data in self.postorder_keys_rec(node.left):
                yield data
            for data in self.postorder_keys_rec(node.right):
                yield data
            yield node.data

    def postorder_keys(self):
        """
        :return:
        returns the postorder traversal of the tree
        """
        return [n for n in self.postorder_keys_rec(self.root)]

    def preorder_keys_rec(self, node):
        if node:
            yield node.data
            for data in self.preorder_keys_rec(node.left):
                yield data
            for data in self.preorder_keys_rec(node.right):
                yield data

    def preorder_keys(self):
        """
        :return:
        return the preorder traversal of the key
        """
        return [n for n in self.preorder_keys_rec(self.root)]

    def items(self):
        """
        :return:
        return the in-order traversal of the key
        """
        tree_in = [n for n in self.inorder_keys()]
        return tree_in

    def getitem_rec(self, node, key):
        if None == node:
            return None
        elif node.data[0] == key:
            return node.data[1]
        elif key < node.data[0]:
            return self.contain_recursive(node.left, key)
        else:
            return self.contain_recursive(node.right, key)

    def __getitem__(self, key):
        """
        :param key:
         get the value associated with the key
        :return:
        return tha value found at that particular key
        """
        return self.getitem_rec(self.root, key)

    def contain_recursive(self, node, key):
        if None == node:
            return None
        elif node.data[0] == key:
            return node.data[1]
        elif key < node.data[0]:
            return self.contain_recursive(node.left, key)
        else:
            return self.contain_recursive(node.right, key)

    def __contains__(self, key):
        """
        :param key:
         the key which has to be checked if it exist
        :return:
        return True is found otherwise raise exception
        """
        val = self.contain_recursive(self.root, key)
        if val:
            return True
        else:
            raise ValueError("Key not found")

    def __setitem__(self, key, value):
        """
        :param key:
         the key that has to be inserted in the tree
        :param value:
        the value that has to be associated with the key
        :return:
        """
        y = None
        x = self.root
        z = BinaryTreeNode([key, value], None, None, None)
        while x is not None:
            y = x
            if z.data[0] < x.data[0]:
                x = x.left
            elif z.data[0] > x.data[0]:
                x = x.right
            else:
                break
        if x and (x.data[0] == z.data[0]):
            x.data[1] = z.data[1]
        else:
            z.parent = y
            if y is None:
                self.root = z
            elif z.data[0] < y.data[0]:
                y.left = z
            else:
                y.right = z
            self.length += 1

    def __delitem(self, key):
        """
        :param key:
         the key which has to be deleted from tree
        :return:
        if key is found it is deleted otherwise raise exception
        """
        if self.root is None:
            print "Tree is empty"
        else:
            temp = self.root
            while temp is not None and temp.data[0] != key:
                if temp.data[0] < key:
                    temp = temp.right
                else:
                    temp = temp.left
            if temp is not None:
                print "Key found: ", key, " value = ", \
                    temp.data[1], " and deleted"
                if temp.left is None:
                    self.transplant(temp, temp.right)
                elif temp.right is None:
                    self.transplant(temp, temp.left)
                else:
                    y = self.treeminimum(temp.right)
                    if y.parent != temp:
                        self.transplant(y, y.right)
                        y.right = temp.right
                        y.right.parent = y
                    self.transplant(temp, y)
                    y.left = temp.left
                    y.left.parent = y
                self.length -= 1
            else:
                raise ValueError("Value not found")

    def treeminimum(self, x):
        """
        :param x:
        find min element rooted at node x
        :return:
        return the min element rooted at x
        """
        while x.left is not None:
            x = x.left
        return x

    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent

    def __len__(self):
        """
        :return:
        return the length of the tree
        """
        return self.length

    def display(self):
        """
        :return:
        return the inorder and preorder traversal of the tree
        """
        tree_in = [n for n in self.inorder_keys()]
        tree_pre = [n for n in self.preorder_keys()]
        return tree_in, tree_pre

def terrible_hash(bin):
    """A terrible hash function that can be used for testing.

    A hash function should produce unpredictable results,
    but it is useful to see what happens to a hash table when
    you use the worst-possible hash function.  The function
    returned from this factory function will always return
    the same number, regardless of the key.

    :param bin:
        The result of the hash function, regardless of which
        item is used.

    :return:
        A python function that can be passes into the constructor
        of a hash table to use for hashing objects.
    """

    def hashfunc(item):
        return bin

    return hashfunc


def main():
    # Thoroughly test your program and produce useful out.
    #
    # Do at least these kinds of tests:
    #  (1)  Check the boundary conditions (empty containers,
    #       full containers, etc)
    #  (2)  Test your hash tables for terrible hash functions
    #       that map to keys in the middle or ends of your
    #       table
    #  (3)  Check your table on 100s or randomly generated
    #       sets of keys to make sure they function
    #
    #  (4)  Make sure that no keys / items are lost, especially
    #       as a result of deleting another key

    print "---------------------LINKED LIST OPERATIONS--------------------\n"

    L = SinglyLinkedList()
    for i in range(0, 50, 5):
        L.prepend(i)
    print "\nPrinting Linked List-> ", L
    print ("\nDeleting 115 if found:")
    isfound = L.remove(115)
    if isfound:
        print "Value found and deleted\n"
    else:
        print "Value not found\n"
    L.remove(25)
    print "After removing 25 list is:\n", L

    H = OpenAddressHashDict(10, 0.7, lambda x: x % 10)
    H1 = OpenAddressHashDict(hashfunc=terrible_hash(5))
    for i in range(12):
        H1[i] = i + 10
    print "\n-------------------------Terrible Hash operations\
    ----------------\n"
    s1 = H1.display()
    print s1
    print "\n"
    print "\n------------ OpenAddressHash operation-----------------\n"

    for i in range(100):
        H[i] = i + 10
    s = H.display()
    print s
    print "\nLength of hash is:", len(H)

    H._OpenAddressHashDict__delitem(21)
    print "\nAfter deleting 21 the Hash table is"
    s = H.display()
    print s

    print "\n------------ ChainedHash operation-----------------\n"
    D = ChainedHashDict(10, 0.7, lambda x: x % 10)
    for i in range(100):
        D[i] = i + 10
    s = D.display()
    print s
    length = len(D)
    print "\nLength of chained hash is : ", length
    for i in range(0, 100, 7):
        del D[i]
    print "\nAfter deleting values in multiple of 7 the hash is\n"
    s = D.display()
    print s

    print "\n--------------Binary Tree Operations-----------\n"
    B = BinarySearchTreeDict()
    B[2] = 3
    B[3] = "PQR"
    B[4] = 5
    B[5] = "STL"
    B[7] = "ABC"
    B[1] = "ASU"
    B[6] = "MNO"
    B[-2] = "XYZ"
    B[-1] = "GHI"
    print "Length of tree is :", len(B)

    print "\nUsing Tree Display function : "
    tree_in1, tree_pre1 = [n for n in B.display()]
    print "Inorder Tree Traversal: ", tree_in1
    print "Preorder Tree Traversal: ", tree_pre1

    print "\nUsing Tree items functions:"
    tree_in = B.items()
    print "Inorder Tree Traversal: ", tree_in

    print "\nHeight of B-tree is:", B.height
    tree_in = [n for n in B.inorder_keys()]
    print "\nInorder Tree Traversal: ", tree_in
    tree_post = [n for n in B.postorder_keys()]
    print "\nPostorder Tree Traversal: ", tree_post
    tree_pre = [n for n in B.preorder_keys()]
    print "\nPreorder Tree Traversal: ", tree_pre

    B._BinarySearchTreeDict__delitem(2)
    print "\nAfter deleting 2 the binary tree is :\n"
    tree = B.items()
    print "Inorder traversal of tree after deleting node 2 is: ", tree


if __name__ == '__main__':
    import doctest

    doctest.testfile("ds_assignment.txt")
    main()