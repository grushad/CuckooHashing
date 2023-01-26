# explanations for member functions are provided in requirements.py
# each file that uses a cuckoo hash should import it from this file.
import random as rand
from typing import List

class CuckooHash:
	def __init__(self, init_size: int):
		self.__num_rehashes = 0
		self.CYCLE_THRESHOLD = 10

		self.table_size = init_size
		self.tables = [[None]*init_size for _ in range(2)]		

	def hash_func(self, key: int, table_id: int) -> int:
		key = int(str(key) + str(self.__num_rehashes) + str(table_id))
		rand.seed(key)
		return rand.randint(0, self.table_size-1)

	def get_table_contents(self) -> List[List[int]]:
		return self.tables

	# you should *NOT* change any of the existing code above this line
	# you may however define additional instance variables inside the __init__ method.

	def insert(self, key: int) -> bool:
		# TODO
		if self.lookup(key):
			return True
		cnt = 0
		tableId = 0		
		while True:
			val = self.hash_func(key, tableId)
			keyToEvict = self.tables[tableId][val]	
			self.tables[tableId][val] = key
			if keyToEvict is None:
				return True
			else:
				if cnt == self.CYCLE_THRESHOLD:
					return False
				tableId = 1 - tableId
				key = keyToEvict
				cnt += 1
		
		
	def lookup(self, key: int) -> bool:
		# TODO
		val0 = self.tables[0][self.hash_func(key, 0)]
		val1 = self.tables[1][self.hash_func(key, 1)]
		return True if val0 == key or val1 == key else False
		

	def delete(self, key: int) -> None:
		# TODO
		if(not self.lookup(key)):			
			return
		h0 = self.hash_func(key, 0)
		h1 = self.hash_func(key, 1)
		if self.tables[0][h0] == key:
			self.tables[0][h0] = None
		elif self.tables[1][h1] == key:
			self.tables[1][h1] = None

	def rehash(self, new_table_size: int) -> None:
		
		old_size = self.table_size
		self.__num_rehashes += 1; self.table_size = new_table_size # do not modify this line	
		oldTable = self.tables	 
		self.tables = [[None]*new_table_size for _ in range(2)]
		for i in range(old_size):									
			if oldTable[0][i] is not None:				
				if not self.insert(oldTable[0][i]):
					return
		for i in range(old_size):
			if oldTable[1][i] is not None:				
				if not self.insert(oldTable[1][i]):
					return
		