


#"abstract class"
#a mathematical vector, basically something that can be scaled, added, and has a magnitude. Also has a method to find a zero vector (which is required to meet the scaling and adding requirements, since you can scale anything by negative one and add) and a method to find the magnitude squared, which is often much more efficient to find.
#from those methods the vecDiff, vecAddList, vecPolynomial, and vecEquals functions can be defined.
#immutable.


#The Vectors used in the Simulation need not actually inherit Vector, they just need all this functionality.
#Use test_anyVector(non_zero_vector) to verify it has all the needed functionality.

class Vector(object):
	def __init__(self):
		raise NotImplementedError
	def getZero(self):
		raise NotImplementedError
	def add(self,other):
		raise NotImplementedError
	def scale(self, scalar):
		raise NotImplementedError
	def getMagn(self):
		raise NotImplementedError
	def getMagnSq(self):
		raise NotImplementedError
		

		
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
def vecEquals(v1,v2,error=0):
	diff = vecDiff(v1,v2)
	return diff.getMagnSq()<=error*error



class singleValueVector(Vector):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return "singleValueVector, value " + str(self.value)
	def getZero(self):
		return singleValueVector(0.0)
	def add(self,b):
		return singleValueVector(self.value+b.value)
	def scale(self,scalar):
		return singleValueVector(self.value*scalar)
	def getMagn(self):
		return self.value
	def getMagnSq(self):
		return self.value * self.value
	# def equal(a,b,error):
		# diff = a.value-b.value
		# return diff<=error and diff>= -error
	# def addList(vlist, slist):
		# acc = singleValueVector.getZero()
		# for i in range(len(vlist)):
			# acc = singleValueVector.add(acc, singleValueVector.scale(vlist[i],slist[i]))
		# return acc
	
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
	
#just checking that running the functions don't actually cause crashes, for now
def test_anySimulator(s):
	pos = s.getDefaultInitPos()
	vel = s.getDefaultInitVel()
	t = s.getDefaultInitTime()
	acc = s.getAccel(pos,vel,0.0)
	s.getOutputValue(pos,vel,0.0)
	

	
	
	
	
	

	

		
class particleWithSpring(object):
	# class vec(Vector):
		# def __init__(self, x,y,z):
			# self.x=x
			# self.y=y
			# self.z=z
		# def getZero(self):
			# return particleWithSpring.vec(0.0,0.0,0.0)
		# def getMagnSq(self):
			# return self.x*self.x + self.y*self.y + self.z*self.z
		# def getMagn(self):
			# return math.sqrt(self.getMagnSq())
		# def add(self, other):
			# return particleWithSpring.vec(self.x+other.x, self.y+other.y, self.z+other.z)
		# def scale(self, scalar):
			# return particleWithSpring.vec(self.x*scalar, self.y*scalar, self.z*scalar)
		#end particleWithSpring.vec subclass
		
		#256Hz = approximately middle C
		#44100Hz = common sampling frequency
		
	def __init__(self, mass, spring, damp): #spring_zero_point=singleValueVector(0.0)):
		if (mass==0.0): self.inv_mass = 1.0
		else: self.inv_mass = 1.0/mass
		self.szero = singleValueVector(0.0)
		self.neg_s = -spring
		self.neg_d = -damp
		
	def getDefaultInitPos(self):
		return singleValueVector(0.02)
		
	def getDefaultInitVel(self):
		return singleValueVector(2.0)
		
	def getDefaultInitTime(self):
		print("debugging, running particleWithSpring.getDefaultInitTime() here")
		return 0.0
		
		
	def getAccel(self, posVector, velVector, time):
	
		timeShift = 1.0 - 0.9*time

		force = posVector.getZero()
		#spring force =  -displacement(x - x_0) * springConstant
		displacement = vecDiff(posVector, self.szero)
		force = force.add(displacement.scale(self.neg_s * timeShift))
		#damping force = -velocity * dampingConstant
		force = force.add(velVector.scale(self.neg_d))
		#f=ma, a = f/m
		return force.scale(self.inv_mass)
		
	def getOutputValue(self, posVector, velVector, time):
		return velVector.getMagn()
		
		




		
		

#requires a simluator, which defines vectors that can define all the positional, velocity, or acceleration data of the simulated physics object, and defines a function that can determine the acceleration vector from any complete position, velocity, and time value. (getAccel(), and getZero() #a zero value of the vector type/shape used for position, velocity, acceleration)

#simulator is the object which defines the initial position, velocity (and time), 
#timeStep is the real amount of time for a step in the physical simulation
#stepNum is the number of samples to get for the outputList
#extraSteps is the number of steps between the output samples
#stepfunc is the function used to update, which can be any of the huge variety of available numerical approximations

def getSimList(simulator, timeStep, stepNum, extraSteps, stepfunc):
	currentPos = simulator.getDefaultInitPos()
	currentVel = simulator.getDefaultInitVel()
	currentTime = simlator.getDefaultInitTime()
	outputList = [simulator.getOutputValue(currentPos, currentVel, currentTime)]
	for i in range(stepNum):
		(currentPos,currentVel) = stepfunc(simulator, timeStep, currentPos, currentVel, currentTime)
		currentTime += timeStep
		outputList.append(simulator.getOutputValue(currentPos,currentVel,currentTime))
		for i in range(extraSteps):
			(currentPos,currentVel) = stepfunc(simulator, timeStep, currentPos, currentVel, currentTime)
			currentTime += timeStep

	return outputList
		

#second-order partial derivative, so acceleration is found by the simulator and position and velocity is calculated
def rungekuttastep(simulator, step, posVector, velVector, time):
	#RK4, the most commonly used Runge Kutta approximation. Requires a lot of precalculated values.
	sixth = 0.16666666666666666
	
	k1 = simulator.getAccel(posVector, velVector, time)
	
	k2_vel = velVector.add(k1.scale(0.5*step))
	k2 = simulator.getAccel(posVector.add(velVector.scale(0.5*step)), k2_vel, time + 0.5*step)
	
	k3_vel = velVector.add(k2.scale(0.5*step))
	k3 = simulator.getAccel(posVector.add(k2_vel.scale(0.5*step)), k3_vel, time + 0.5*step)
	
	k4_vel = velVector.add(k3.scale(step))
	k4 = simulator.getAccel(posVector.add(k3_vel.scale(step)), k4_vel, time+step)
	

	next_pos = vecAddList([velVector,k1,k2,k3,posVector],[step, sixth*step*step, sixth*step*step, sixth*step*step, 1.0])
	next_vel = vecAddList([k1,k2,k3,k4,velVector], [sixth*step, 2.0*sixth*step, 2.0*sixth*step, sixth*step, 1.0])
	return (next_pos, next_vel)
	
#second-order partial derivative
def eulerstep(simulator, step, posVector, velVector, time):

	next_vel = velVector.add(simulator.getAccel(posVector,velVector, time).scale(step))
	next_pos = posVector.add(velVector.scale(step))
	return (next_pos, next_vel)
	
def nullstep(simulator, step, posVector, velVector, time):
	return (posVector, velVector)

	
def test_getSimList():

	test_anyVector(singleValueVector(3.3))


	p = particleWithSpring(1.0, 1.0, 1.0, singleValueVector(0.0))
	test_anySimulator(p)
	
	sp = p.getDefaultInitPos()
	sv = p.getDefaultInitVel()
	print("starting position and velocity")
	print(str(sp) + ' ' + str(sv))
	
	
	
	
	listNull = getSimList(p, 0.01, 10, nullstep, sp, sv, 0.0)
	listEuler = getSimList(p, 0.01, 10, eulerstep, sp, sv, 0.0)
	listRK = getSimList(p, 0.01, 10, rungekuttastep, sp, sv, 0.0)
	
	print(listNull)
	print(listEuler)
	print(listRK)