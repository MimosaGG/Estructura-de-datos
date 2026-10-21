from abc import ABC, abstractmethod
from typing import Any, Optional


class Order:

  def __init__(self, customer, qtty):
    self.customer = customer
    self.qtty = qtty

  def impresion(self):
    
    print(f"Customer: {self.customer}")
    print(f"Quantity: {self.qtty}")
    print("------------------------")

  def getqtty(self):
    return self.qtty

  def getcustomer(self):
    return self.customer


class Node:

  def __init__(self, info: Any):
    self.info = info  
    self.next: Optional["Node"] = None


class QueueInterface(ABC):
  

  @abstractmethod
  def size(self) -> int:
    pass

  @abstractmethod
  def isEmpty(self) -> bool:
    pass

  @abstractmethod
  def front(self) -> Optional[Any]:
    pass

  @abstractmethod
  def enqueue(self, info: Any) -> None:
    pass

  @abstractmethod
  def dequeue(self) -> Optional[Any]:
    pass

  @abstractmethod
  def printInfo(self) -> None:
    pass


class Queue(QueueInterface):

  def __init__(self):
    self.head: Optional[Node] = None
    self.tail: Optional[Node] = None
    self._size: int = 0

  def size(self) -> int:
    return self._size

  def isEmpty(self) -> bool:
    return self.head is None

  def front(self) -> Optional[Any]:
    if self.isEmpty():
      return None
    return self.head.info

  def enqueue(self, info: Any) -> None:
    new_node = Node(info)
    if self.isEmpty():
      self.head = new_node
      self.tail = new_node
    else:
      self.tail.next = new_node
      self.tail = new_node
    self._size += 1  

  def dequeue(self) -> Optional[Any]:
    if self.isEmpty():
      return None
    temp = self.head
    self.head = self.head.next
    self._size -= 1
    if self.head is None:
      self.tail = None
    return temp.info

  def printInfo(self) -> None:
    
    current = self.head
    print(f"\n--- Queue Info (Tamaño: {self.size()}) ---")
    if self.isEmpty():
      print("Cola Vacía")

    while current is not None:
      if isinstance(current.info, Order):
        current.info.impresion()
      else:
        print(current.info)
      current = current.next
    print("------------------------------------------\n")



if __name__ == "__main__":
  mi_cola = Queue()


  mi_cola.enqueue(Order("Monica Jimena",9))
  mi_cola.enqueue(Order("Ana Pérez", 6))
  mi_cola.enqueue(Order("Antonio Galvez", 8))
  

  mi_cola.printInfo()