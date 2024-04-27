import unittest
from typing import List

from hypothesis import given
from hypothesis import strategies as st
from list import UnrolledLinkedList


class Test(unittest.TestCase):

    @given(st.lists(st.integers(min_value=1, max_value=100)))
    def test_size(self, values: List[int]) -> None:
        # Test size of an empty list
        lst1: UnrolledLinkedList = UnrolledLinkedList()
        self.assertEqual(lst1.size(), 0)

        # Test size of a list with zero capacity
        lst2: UnrolledLinkedList = UnrolledLinkedList(0)
        self.assertEqual(lst2.size(), 0)

        # Test size of a list with one or more elements
        if values:
            lst3: UnrolledLinkedList = UnrolledLinkedList(3)
            for value in values:
                lst3.add(value)
            self.assertEqual(lst3.size(), len(values))

    @given(st.lists(st.integers()), st.integers())
    def test_add(self, initial_values: list[int], new_value: int) -> None:
        lst: UnrolledLinkedList = UnrolledLinkedList(3)
        lst.from_list(initial_values)
        lst.add(new_value)
        expected_result = initial_values + [new_value]
        self.assertEqual(lst.to_list(), expected_result)

    @given(st.lists(st.integers()))
    def test_get(self, values: List[int]) -> None:
        # Test getting elements from an empty list
        lst1: UnrolledLinkedList = UnrolledLinkedList(3)
        self.assertRaises(IndexError, lst1.get, 0)

        # Test getting elements from a list with one node
        lst2: UnrolledLinkedList = UnrolledLinkedList(3)
        if values:
            lst2.add(values[0])
            self.assertEqual(lst2.get(0), values[0])
            if len(values) > 1:
                self.assertRaises(IndexError, lst2.get, 1)

        # Test getting elements from a list with multiple nodes
        lst3: UnrolledLinkedList = UnrolledLinkedList(3)
        lst3.from_list(values)
        for i, value in enumerate(values):
            self.assertEqual(lst3.get(i), value)
        self.assertRaises(IndexError, lst3.get, len(values))

    @given(st.lists(st.integers(min_value=1, max_value=100)))
    def test_set(self, values: List[int]) -> None:
        # Test setting elements in an empty list
        lst1: UnrolledLinkedList = UnrolledLinkedList(3)
        self.assertRaises(IndexError, lst1.set, 0, 1)

        # Test setting elements in a list with multiple nodes
        if values:
            lst3: UnrolledLinkedList = UnrolledLinkedList(2)
            lst3.from_list(values)
            new_value = 5
            index = min(len(values) - 1, 1)  # ensure index is within bounds
            lst3.set(index, new_value)
            values[index] = new_value
            self.assertEqual(lst3.to_list(), values)
            self.assertRaises(IndexError, lst3.set, len(values), 4)

    @given(st.lists(st.integers(min_value=1, max_value=100)))
    def test_remove(self, values: List[int]) -> None:
        # Test removing elements from an empty list
        lst1: UnrolledLinkedList = UnrolledLinkedList(3)
        for value in values:
            self.assertRaises(ValueError, lst1.remove, value)

        # Test removing elements from a list
        if values:
            lst2: UnrolledLinkedList = UnrolledLinkedList(3)
            lst2.from_list(values)
            unique_values = list(set(values))
            for value in unique_values:
                lst2.remove(value)
            er = [value for value in values if value not in unique_values]
            self.assertEqual(lst2.to_list(), er)

        # Test automatic merging of nodes after removing elements
        if values:
            lst3: UnrolledLinkedList = UnrolledLinkedList(2)
            lst3.from_list(values)
            lst3_values = lst3.to_list()
            unique_values = list(set(lst3_values))
            for value in unique_values:
                lst3.remove(value)
            er = [value for value in lst3_values if value not in unique_values]
            self.assertEqual(lst3.to_list(), er)

    @given(st.lists(st.integers(min_value=1, max_value=100)))
    def test_is_member(self, values: List[int]) -> None:
        # Test whether an element exists in an empty list
        lst1: UnrolledLinkedList = UnrolledLinkedList(3)
        self.assertFalse(lst1.isMember(1))

        # Test whether an element exists in a single-node list
        if values:
            lst2: UnrolledLinkedList = UnrolledLinkedList(3)
            lst2.add(values[0])
            self.assertTrue(lst2.isMember(values[0]))
            self.assertFalse(lst2.isMember(values[0] + 1))

    @given(st.lists(st.integers(min_value=1, max_value=100)))
    def test_reverse(self, values: List[int]) -> None:
        # Test reversing an empty list
        lst1: UnrolledLinkedList = UnrolledLinkedList()
        lst1.reverse()
        self.assertEqual(lst1.to_list(), [])

        # Test reversing a single-node list
        if values:
            lst2: UnrolledLinkedList = UnrolledLinkedList(3)
            lst2.add(values[0])
            lst2.reverse()
            self.assertEqual(lst2.to_list(), [values[0]])

        # Test reversing a multi-node list
        if values:
            lst3: UnrolledLinkedList = UnrolledLinkedList(3)
            lst3.from_list(values)
            lst3.reverse()
            self.assertEqual(lst3.to_list(), list(reversed(values)))

    @given(st.lists(st.integers(min_value=1, max_value=100)))
    def test_filter(self, values: List[int]) -> None:
        # Test filtering an empty list
        lst1: UnrolledLinkedList = UnrolledLinkedList(0)
        lst1.filter(lambda x: x % 2 == 0)
        self.assertEqual(lst1.to_list(), [])

        # Test filtering a single-node list
        if values:
            lst2: UnrolledLinkedList = UnrolledLinkedList(3)
            lst2.add(values[0])
            lst2.filter(lambda x: x % 2 == 0)
            if values[0] % 2 == 0:
                self.assertEqual(lst2.to_list(), [values[0]])
            else:
                self.assertEqual(lst2.to_list(), [])

        # Test filtering a multi-node list
        if values:
            lst3: UnrolledLinkedList = UnrolledLinkedList(3)
            lst3.from_list(values)
            lst3.filter(lambda x: x % 2 == 0)
            filtered_values = [value for value in values if value % 2 == 0]
            self.assertEqual(lst3.to_list(), filtered_values)

    @given(st.lists(st.integers(min_value=1, max_value=100)))
    def test_map(self, values: List[int]) -> None:
        # Test mapping an empty list
        lst1: UnrolledLinkedList = UnrolledLinkedList()
        lst1.map(lambda x: x * 2)
        self.assertEqual(lst1.to_list(), [])

        # Test mapping a list with elements
        if values:
            lst2: UnrolledLinkedList = UnrolledLinkedList(3)
            lst2.from_list(values)
            lst2.map(str)
            self.assertEqual(lst2.to_list(), list(map(str, values)))

        # Test mapping a multi-node list
        if values:
            lst: UnrolledLinkedList = UnrolledLinkedList(3)
            lst.from_list(values)
            lst.map(lambda x: x * 2)
            self.assertEqual(lst.to_list(), list(map(lambda x: x * 2, values)))

    @given(st.lists(st.integers(min_value=1, max_value=100)))
    def test_reduce(self, values: List[int]) -> None:
        # Test reducing an empty list
        lst1: UnrolledLinkedList = UnrolledLinkedList()
        self.assertRaises(ValueError, lst1.reduce, lambda x, y: x + y, None)

        # Test reducing a single-node list
        if values:
            lst2: UnrolledLinkedList = UnrolledLinkedList(3)
            lst2.add(values[0])
            self.assertEqual(lst2.reduce(lambda x, y: x + y, 0), values[0])

        # Test reducing a multi-node list
        if values:
            lst3: UnrolledLinkedList = UnrolledLinkedList(3)
            lst3.from_list(values)
            self.assertEqual(lst3.reduce(lambda x, y: x + y, 0), sum(values))

    @given(st.lists(st.integers(min_value=1, max_value=100)),
           st.lists(st.integers(min_value=1, max_value=100)),
           st.lists(st.integers(min_value=1, max_value=100)))
    def monoid_test(self, values: List[int], values2: List[int], values3: List[int],) -> None:
        # Test concatenating three lists using the associative property (monoid law)

        # Creating three UnrolledLinkedList instances
        lst1: UnrolledLinkedList = UnrolledLinkedList(3)
        lst1.from_list(values)

        lst2: UnrolledLinkedList = UnrolledLinkedList(3)
        lst2.from_list(values2)

        lst3: UnrolledLinkedList = UnrolledLinkedList(3)
        lst3.from_list(values3)

        # Concatenating lst2 and lst3 first, then concatenating lst1 with the result
        lst4: UnrolledLinkedList = lst1.concat(lst2.concat(lst3))

        # Concatenating lst1 and lst2 first, then concatenating lst3 with the result
        lst5: UnrolledLinkedList = lst1.concat(lst2).concat(lst3)

        # Asserting that the two concatenated lists are equal
        self.assertEqual(lst4.to_list(), lst5.to_list())

    @given(st.lists(st.lists(st.integers(min_value=1, max_value=100))))
    def test_from_list(self, test_data: List[List[int]]) -> None:
        for e in test_data:
            lst: UnrolledLinkedList = UnrolledLinkedList(3)
            lst.from_list(e)
            self.assertEqual(lst.to_list(), e)

    @given(st.lists(st.integers(min_value=1, max_value=100)))
    def test_to_list(self, values: List[int]) -> None:
        # Test converting an empty list
        lst1: UnrolledLinkedList = UnrolledLinkedList(3)
        self.assertEqual(lst1.to_list(), [])

        # Test converting a list with one element
        if values:
            lst2: UnrolledLinkedList = UnrolledLinkedList(3)
            lst2.add(values[0])
            self.assertEqual(lst2.to_list(), [values[0]])

        # Test converting a list with multiple elements
        if values:
            lst3: UnrolledLinkedList = UnrolledLinkedList(3)
            lst3.from_list(values)
            self.assertEqual(lst3.to_list(), values)

    @given(st.lists(st.integers(min_value=1, max_value=100)))
    def test_str(self, values: List[int]) -> None:
        # Test string representation of an empty list
        lst1: UnrolledLinkedList = UnrolledLinkedList()
        self.assertEqual(str(lst1), "")

        # Test string representation of a single-node list
        if values:
            lst2: UnrolledLinkedList = UnrolledLinkedList(3)
            lst2.add(values[0])
            self.assertEqual(str(lst2), str(values[0]))

        # Test string representation of a multi-node list
        if values:
            lst3: UnrolledLinkedList = UnrolledLinkedList(3)
            lst3.from_list(values)
            self.assertEqual(str(lst3), " : ".join(map(str, values)))

    @given(st.lists(st.integers(min_value=1, max_value=100)))
    def test_iter(self, values: List[int]) -> None:
        # Test iteration over an empty list
        lst1: UnrolledLinkedList = UnrolledLinkedList(3)
        i = iter(lst1)
        self.assertRaises(StopIteration, lambda: next(i))

        # Test iteration over a non-empty list
        if values:
            lst2: UnrolledLinkedList = UnrolledLinkedList(3)
            lst2.from_list(values)
            tmp: list[int] = []
            for e in lst2:
                tmp.append(e)
            self.assertEqual(values, tmp)
            self.assertEqual(lst2.to_list(), tmp)
