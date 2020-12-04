from abc import ABC, abstractmethod

class Package(ABC):
	def __init__(self, name, weight, distance, sender):
		self._name = name
		self._weight = weight
		self._distance = distance
		self._owner = sender
		
	def __repr__(self):
		return '{}'.format((self._name, self._weight, self._distance))
	@abstractmethod
	def costs(self):
		pass

class Parcel(Package):
	def costs(self):
		self._costs = self._weight * (self._distance / 100)
		# apply discount for large objects
		if self._costs >= 100000:
			self._costs = 100000
		return self._costs

class Letter(Package):
	def costs(self):
		self._costs = self._distance / 100
		return self._costs
	
class TruckingCompany:
	def __init__(self, trucks, parcel):
		self._trucks = trucks
		self._parcel = parcel
		self._loc = 'Base'
	
	def load_parcel_to_truck(self):
		for tr in self._trucks:
			for pr in self._parcel[:]:
				if tr._range >= pr._distance and (tr._cur_weight + pr._weight) <= tr._max_weight and tr._cur_loc == self._loc:
					tr.load_cargo(pr)
					self._parcel.remove(pr)
		if len(self._parcel) > 0:
			return 'the following parcel cannot be delivered: {}'.format(self._parcel)
		return 'All parcels could be delivered'
		
class Truck:
	def __init__(self, max_weight, range, cur_loc):
		self._max_weight = max_weight
		self._range = range
		self._cur_loc = cur_loc
		self._cur_weight = 0
		self._cargo = []
		
	def load_cargo(self,cargo):
		self._cargo.append(cargo)
		self._cur_weight += cargo._weight
	
	def current_cargo(self):
		return self._cargo[:]
	
	def deliver(self):
		if len(self._cargo) > 0:
			max = self._cargo[0]._distance
		else:
			return 'Nothing to deliver'
		for pr in self._cargo:
			if pr._distance >= max:
				max = pr._distance
		self._range -= max

if __name__ == '__main__':
	veh = [
		Truck(1000,1000, 'Base'),
		Truck(100000,10000, 'Washington')
	]
	packages = [
		Letter('Exams',100,40, 'Prof. Dr. Python'),
		Parcel('Gandalf Weed', 300,100, 'Gandalf'),
		Parcel('Gandalf Weed', 300,100, 'Gandalf'),
		Parcel('Gandalf Weed', 300,100, 'Gandalf'),
		Parcel('Gandalf Weed', 300,100, 'Gandalf'),
		Parcel('Gandalf Weed', 300,100, 'Gandalf'),
		Parcel('Haggrid and friends',10000,100000, 'Haggrid')
	]
	
	t = TruckingCompany(veh, packages)
	print(t.load_parcel_to_truck())
	print(veh[0].current_cargo())
	print(veh[0]._cur_weight)
	
	veh[0].deliver()
	print(veh[0]._range)