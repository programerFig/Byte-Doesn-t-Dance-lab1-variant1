from typing import Optional, List, Callable, Any


class UnrolledNode:
    def __init__(self, capacity: int) -> None:
        self.capacity: int = capacity
        self.values: List[int] = []
        self.next: Optional[UnrolledNode] = None  # refers to the next node


class UnrolledLinkedList:
    def __init__(self, node_capacity: int = 0) -> None:
        self.node_capacity: int = node_capacity
        self.head: Optional[UnrolledNode] = None

    def size(self) -> int:  # return the size of the Unrolled Linked List
        count: int = 0
        current_node: Optional[UnrolledNode] = self.head
        while current_node:
            count += len(current_node.values)
            current_node = current_node.next
        return count

    def add(self, value: int) -> None:
        if not self.head:  # if the head does not exist
            self.head = UnrolledNode(self.node_capacity)
            self.head.values.append(value)
            return

        current_node: UnrolledNode = self.head  # if the head does exist
        while current_node.next and len(current_node.values) == current_node.capacity:
            current_node = current_node.next

        if len(current_node.values) < current_node.capacity:
            current_node.values.append(value)
        else:
            new_node = UnrolledNode(self.node_capacity)
            new_node.values.append(value)
            current_node.next = new_node

    def get(self, index: int) -> int:
        current_node: Optional[UnrolledNode] = self.head
        while current_node:
            if index < len(current_node.values):
                return current_node.values[index]
            index -= len(current_node.values)
            current_node = current_node.next
        raise IndexError("Index out of range")

    def set(self, index: int, value: int) -> None:
        current_node: Optional[UnrolledNode] = self.head
        while current_node:
            if index < len(current_node.values):
                current_node.values[index] = value
                return
            index -= len(current_node.values)
            current_node = current_node.next
        raise IndexError("Index out of range")

    def remove(self, value: int) -> None:
        current_node: Optional[UnrolledNode] = self.head
        prev_node: Optional[UnrolledNode] = None
        removed: bool = False
        while current_node:
            if value in current_node.values:
                current_node.values = [v for v in current_node.values if v != value]
                removed = True
                if len(current_node.values) == 0:
                    if prev_node:
                        prev_node.next = current_node.next
                    else:
                        self.head = current_node.next
                    current_node = current_node.next
                    continue
            prev_node = current_node
            current_node = current_node.next
        if not removed:
            raise ValueError("Value not found in the list")

    def isMember(self, value: int) -> bool:
        current_node: Optional[UnrolledNode] = self.head
        while current_node:
            if value in current_node.values:
                return True
            current_node = current_node.next
        return False

    def reverse(self) -> None:
        current_node: Optional[UnrolledNode] = self.head
        prev_node: Optional[UnrolledNode] = None
        while current_node:
            current_node.values = current_node.values[::-1]
            next_node: Optional[UnrolledNode] = current_node.next
            current_node.next = prev_node
            prev_node = current_node
            current_node = next_node
        self.head = prev_node

    def filter(self, predicate: Callable[[int], bool]) -> None:
        current_node: Optional[UnrolledNode] = self.head
        prev_node: Optional[UnrolledNode] = None
        while current_node:
            current_node.values = [
                value for value in current_node.values if predicate(value)
            ]
            if len(current_node.values) == 0:
                if prev_node:
                    prev_node.next = current_node.next
                else:
                    self.head = current_node.next
            prev_node = current_node
            current_node = current_node.next

    def map(self, func: Callable[[int], Any]) -> None:
        current_node: Optional[UnrolledNode] = self.head
        while current_node:
            current_node.values = [func(value) for value in current_node.values]
            current_node = current_node.next

    def reduce(self, func: Callable[[Any, int], Any], init: Any) -> Any:
        if not self.head:
            raise ValueError("Empty list")
        res: Any = init
        current_node: Optional[UnrolledNode] = self.head
        while current_node:
            for value in current_node.values:
                if res is None:
                    res = value
                else:
                    res = func(res, value)
            current_node = current_node.next
        return res

    def from_list(self, lst: List[int]) -> None:
        for item in lst:
            self.add(item)

    def to_list(self) -> List[int]:
        result: List[int] = []
        current_node: Optional[UnrolledNode] = self.head
        while current_node:
            result.extend(current_node.values)
            current_node = current_node.next
        return result

    def __str__(self) -> str:
        elements: List[int] = []
        current_node: Optional[UnrolledNode] = self.head
        while current_node:
            elements.extend(current_node.values)
            current_node = current_node.next
        return " : ".join(map(str, elements))

    def __iter__(self) -> "UnrolledLinkedList":
        self.current_node: Optional[UnrolledNode] = self.head
        self.current_index: int = 0
        return self

    def __next__(self) -> int:  # return the value of next element
        if not self.current_node:
            raise StopIteration
        if self.current_index < len(self.current_node.values):
            value: int = self.current_node.values[self.current_index]
            self.current_index += 1
            return value
        else:
            self.current_node = self.current_node.next
            self.current_index = 0
            return self.__next__()

    def concat(self, other: "UnrolledLinkedList") -> "UnrolledLinkedList":
        if not other.head:
            return self

        new_linked_list = UnrolledLinkedList(self.node_capacity)

        # copy the lst1 to new lst
        if self.head:
            new_linked_list.head = UnrolledNode(self.node_capacity)
            new_linked_list.head.values.extend(self.head.values)
            current_node = new_linked_list.head
        else:
            # if lst1 is none
            current_node = None

        # check all the element in lst2
        other_node = other.head
        while other_node:
            if current_node is None:
                # if lst1 is none
                new_linked_list.head = UnrolledNode(self.node_capacity)
                new_linked_list.head.values.extend(other_node.values)
                current_node = new_linked_list.head
            elif (
                len(current_node.values) + len(other_node.values) <= current_node.capacity
            ):
                current_node.values.extend(other_node.values)
            else:
                # if current node is full
                new_node = UnrolledNode(self.node_capacity)
                new_node.values.extend(
                    other_node.values[
                        : current_node.capacity - len(current_node.values)
                    ]
                )
                other_node.values = other_node.values[
                    current_node.capacity - len(current_node.values) :
                ]
                current_node.next = new_node
                current_node = new_node

            if other_node and other_node.next:
                other_node = other_node.next
            elif not other_node.next:
                break
        return new_linked_list
