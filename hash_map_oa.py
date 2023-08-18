# Name: Catherine Martens
# Email: potgietc@oregonstate.edu
# Description: This file contains an implementation of a hash map. Given a skeleton code file I, the student, completed
# the following methods - put(), get(), remove(), contains_key(), clear(), empty_buckets(), resize_table(), table_load()
# and get_keys()


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not change the underlying hash
        table capacity.
        """
        for index in range(0, self.capacity):
            if self.buckets[index] is not None:
                self.buckets[index] = None
        self.size = 0

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key. If the key is not in the hash
        map, the method returns None.

        implemented with quadratic probing
        """

        if self.size == 0:
            return None

        fresh_hash = self.hash_function(key)
        index = fresh_hash % self.capacity
        j = 1
        i = (index + (j ** 2)) % self.capacity

        if self.buckets[index] is None:
            return None

        if self.buckets[index].key == key and self.buckets[index].is_tombstone is False:
            return self.buckets[index].value


        while self.buckets[i] is not None:
            if self.buckets[i].key == key and self.buckets[i].is_tombstone is False:
                return self.buckets[i].value
            j = j + 1
            i = (index + (j**2)) % self.capacity

        return None

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key / value pair in the hash map. If the given key already exists in
        the hash map, its associated value is replaced with the new value. If the given key is
        not in the hash map, a key / value pair is added.

        For this hash map implementation, when this method is called and the current load factor of the table is
        greater than or equal to 0.5, the table is resized to double its current capacity.
        """

        if self.table_load() >= 0.5:
            new_cap = self.capacity * 2
            self.resize_table(new_cap)

        fresh_hash = self.hash_function(key)
        index = fresh_hash % self.capacity
        new_node = HashEntry(key, value)
        j = 1

    # If there is a matching key for a key-value pair, we update the value
        if self.buckets[index] is not None and self.buckets[index].key == key \
                and self.buckets[index].is_tombstone is False:
            self.buckets[index].value = value
            return
    # If there is an item at the hash index (not a tombstone), we apply quad probing
        if self.buckets[index] is not None and self.buckets[index].is_tombstone is False:
            i = (index + (j**2)) % self.capacity
            while self.buckets[i] is not None and self.buckets[i].is_tombstone is False:
                if self.buckets[i].key == key:
                    self.buckets[i].value = value
                    self.buckets[i].is_tombstone = False
                    return
                j = j + 1
                i = (index + (j**2)) % self.capacity

            self.buckets.set_at_index(i, new_node)
            self.size = self.size + 1
            return

    # Either the spot is empty or it's a tombstone
        self.buckets.set_at_index(index, new_node)
        self.size = self.size + 1

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method does nothing (no exception needs to be raised).

        quadratic probing is implemented
        """
        if self.size == 0:
            return

        key_hash = self.hash_function(key)
        index = key_hash % self.capacity
        j = 1
        i = (index + (j ** 2)) % self.capacity

        if self.buckets[index] is None:
            return

        if self.buckets[index].key == key and self.buckets[index].is_tombstone is False:
            self.buckets[index].is_tombstone = True
            self.size = self.size - 1
            return

        for item in range(0, self.capacity):
            while self.buckets[i] is not None:
                if self.buckets[i].key == key and self.buckets[i].is_tombstone is False:
                    self.buckets[i].is_tombstone = True
                    self.size = self.size - 1
                    return
                j = j + 1
                i = (index + (j ** 2)) % self.capacity

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False. An
        empty hash map does not contain any keys.

        quadratic probing is implemented
        """
        if self.size == 0:
            return False

        key_hash = self.hash_function(key)
        index = key_hash % self.capacity
        j = 1

        if self.buckets[index] is None:
            return False

        if self.buckets[index].key == key and self.buckets[index].is_tombstone is False:
            return True

        for item in range(0, self.capacity):
            i = (index + (j**2)) % self.capacity
            if self.buckets[i] is None:
                return False
            if self.buckets[i].key == key:
                return True
            else:
                j = j + 1
        return False

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.
        """
        return self.capacity - self.size

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.
        """
        return self.size/self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table. All existing key / value pairs
        remain in the new hash map, and all hash table links are rehashed. If new_capacity is less than 1
        or less than the current number of elements in the map, the method does nothing.
        """
        if new_capacity < 1 or new_capacity < self.size:
            return

        old_buckets = self.buckets
        old_cap = self.capacity

        self.buckets = DynamicArray()
        self.capacity = new_capacity
        buckaroo = self.buckets

        for i in range(new_capacity):
            buckaroo.append(None)

        self.size = 0
        for i in range(old_cap):
            curr = old_buckets[i]
            if curr and not curr.is_tombstone:
                self.put(curr.key, curr.value)

    def get_keys(self) -> DynamicArray:
        """
        This method returns a DynamicArray that contains all the keys stored in the hash map. The
        order of the keys in the DA does not matter.
        """
        key_array = DynamicArray()
        for index in range(0, self.capacity):
            if self.buckets[index] is not None:
                if self.buckets[index].is_tombstone is False:
                    key_array.append(self.buckets[index].key)

        return key_array


if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
