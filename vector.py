"""Vector class
description, implemented as a base class that need not be used in code
including simple unit test, test_anyVector(v):
including concrete class singleValueVector
"""


#"abstract class"
#a mathematical vector, basically something that can be scaled, added, and has a magnitude. Also has a method to find a zero vector (which is required to meet the scaling and adding requirements, since you can scale anything by negative one and add) and a method to find the magnitude squared, which is often much more efficient to find.
#from those methods the vecDiff, vecAddList, vecPolynomial, and vecEquals functions can be defined.
#immutable.


#The Vectors used in the Simulation need not actually inherit Vector, they just need all this functionality.
#Use test_anyVector(non_zero_vector) to verify it has all the needed functionality.

class Vector(object):
	def __init__(self): raise NotImplementedError
	def getZero(self): raise NotImplementedError
	def add(self,other): raise NotImplementedError
	def scale(self, scalar): raise NotImplementedError
	def getMagn(self): raise NotImplementedError
	def getMagnSq(self): raise NotImplementedError



		
def vecDiff(a,b):
	return a.add(b.scale(-1.0))
def vecAddList(vectorList, scalarList):
	if (len(vectorList) == 0): return 0.0
	acc = vectorList[0].getZero() #accumulator, start at zero
	for i in range(len(vectorList)):
		acc = acc.add(vectorList[i].scale(scalarList[i]))
	return acc
def vecPolynomial(vectorList, scalarx):
	if (len(vectorList)==0): return 0.0
	acc = vectorList[0].getZero()
	for i in range(len(vectorList)):
		acc = acc.add(vectorList[i].scale(scalarx**i))
	return acc
def vecEquals(v1,v2,error=0.0):
	diff = vecDiff(v1,v2)
	return diff.getMagnSq()<=error*error
def vecLint(v1,v2,x):
	diff = vecDiff(v2,v1)
	return v1.add(diff.scale(x))

class singleValueVector(Vector):
	def __init__(self, value): self.value = value
	def __str__(self): return "singleValueVector, value " + str(self.value)
	def getZero(self): return singleValueVector(0.0)
	def add(self,b): return singleValueVector(self.value+b.value)
	def scale(self,scalar): return singleValueVector(self.value*scalar)
	def getMagn(self): return self.value
	def getMagnSq(self): return self.value * self.value

	
def test_singleValueVector():
	v1 = singleValueVector(1337.0)
	v2 = singleValueVector(420.0)
	v3 = singleValueVector(3.0)
	sList = [2.0,2.0]
	v4 = singleValueVector(3514.0)#1337*2 = 14+2660 = 2674, 2674+840 = 3514
	assert v3.getMagnSq() == 9.0
	test1 = v4
	test2 = vecAddList([v1,v2],sList)
	print(str(test1.getMagnSq()))
	print(str(test2.getMagnSq()))
	assert vecEquals(test1, test2, 0.0001)
	
	#getZero
	z = singleValueVector(0.0)
	assert v1.getZero().getMagn() == 0.0
	assert vecEquals(v2.getZero(), z, 0.00001)
	#add
	#scale
	#getMagn
	#getMagnSq
	#vecDiff
	#vecAddList
	#vecPolynomial
	#vecEquals
	
def test_anyVector(v):

	#getZero
	z = v.getZero()
	assert v.getZero().getMagn() == 0.0
	assert vecEquals(v.scale(0.0), v.getZero(), 0.00001)
	
	#add
	#scale
	#vecEquals
	assert vecEquals(v.scale(2.0), v.add(v), 0.0001)
	
	#getMagn
	assert v.getMagn()*14.5 == v.scale(14.5).getMagn()
	
	#getMagnSq
	assert v.getMagn()*v.getMagn() == v.getMagnSq()
	
	#vecDiff
	assert vecEquals(vecDiff(v.scale(3.2), v), v.scale(2.2), 0.0001)
	
	#vecAddList
	assert vecEquals(vecAddList([v,z,v], [2.0,2.0,2.0]), v.scale(4.0), 0.0001)
	
	#vecPolynomial
	assert vecEquals(vecPolynomial([v,v,v], 2.0), v.scale(7.0), 0.0001)
	
	#vecLint
	assert vecEquals(vecLint(v,v.getZero(),0.9), v.scale(0.1), 0.0001)
	
	print("If you see this with no assert or other errors, 'sall good.")
	
	