
import quickrand
import simulator







#definition of the object "abstract class"
class SoundGenerator(object):
	"""A thing that can generate sounds, by returning a sound output sample by sample, and updating to the next time point."""
	def __init__(self):
		raise NotImplementedError
	#def getDescription(self): #use docstrings instead
		#raise NotImplementedError
	def setParam(strName, parameter): #sometimes float values, sometimes functions.
		raise NotImplementedError
	
	# def getDefaultInitPos(self):
		# raise NotImplementedError
	# def getDefaultInitVel(self):
		# raise NotImplementedError
	# def getDefaultInitTime(self):
		# raise NotImplementedError
		
	def useDefaultEnergyInput(self):
		raise NotImplementedError
	
	# def getAccel(self, pos, vel, time):
		# raise NotImplementedError
	def update(self, timeDel):
		raise NotImplementedError
	
	def getMonoSound(self, timeDelta):
		raise NotImplementedError
	def getStereoSound(self, timeDelta):
		raise NotImplementedError
		
def test_SoundGenerator(test_object):
	print(test_object.getDescription())
	# p = test_object.getDefaultInitPos()
	# v = test_object.getDefaultInitVel()
	# t = test_object.getDefaultInitTime()
	test_object.useDefaultEnergyInput()
	# test_object.getAccel(p,v,t)
	test_object.getMonoSound(self, 1.0/44100.0)
	test_object.getStereoSound(self, 1.0/44100.0)
	
	
#use rk4.singleValueVector instead
# class singleValueVector(object):
	# def __init__(self, val): self.val = val
	# def getZero(self): return singleValueVector(0.0)
	# def add(self,other): return singleValueVector(self.val + other.val)
	# def scale(self, scalar): return singleValueVector(self.val * scalar)
	# def getMagn(self): return self.val
	# def getMagnSq(self): return self.val * self.val
	
	
class SimpleSpringSG(object):
	"""Use docstring instead of a getDescription function"""
	

	
	def __init__(self, mass, spring, damp):
		"""initialize the simplest useful SoundGenerator, a single mass on a spring (with damping). Use the rk4.Simulator inside this SimpleSpringSG object."""
		
		if (mass==0.0): self.inv_mass = 1.0
		else: self.inv_mass = 1.0/mass
		self.neg_damp = -damp
		self.neg_k = -spring
		
		self.simulator = rk4.particleWithSpring
		
		self.pos = rk4.singleValueVector(0.0)
		self.vel = rk4.singleValueVector(0.0)
		self.time = 0.0
		
	def reset():
		self.pos = rk4.singleValueVector(0.0)
		self.vel = rk4.singleValueVector(0.0)
		self.time = 0.0
		
	def applyDefaultEnergyInput():
		self.vel = self.vel.add(rk4.singleValueVector(1.5))
		
		
	def _change_mass(self, mass):
		if(mass == 0.0): self.inv_mass = 1.0
		else: self.inv_mass = 1.0/mass
	def _change_spring(self, spring):
		self.neg_k = -spring
	def _change_damp(self, damp):
		self.neg_d = -damp
	paramDict = {"mass": SimpleSpringSG._change_mass, "spring": SimpleSpringSG._change_spring, "damp": SimpleSpringSG._change_damp}
	def param_set(self, paramName, value):
		SimpleSpringSG.paramDict[paramName](self, value)
		
	
	
	
	
	
	
	
def test_anySoundGenerator(s):
	
