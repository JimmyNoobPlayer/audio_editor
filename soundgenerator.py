
import quickrand
import simulator

import math







#definition of the object "abstract class"
class SoundGenerator(object):
	"""A thing that can generate sounds, by returning a sound output sample by sample, and updating to the next time point."""
	def __init__(self):
		raise NotImplementedError
	def setParam(self, paramName, value): #sometimes float values, sometimes functions.
		raise NotImplementedError
	def reset(self):
		raise NotImplementedError
	def useDefaultEnergyInput(self):
		raise NotImplementedError
	def update(self, timeDel):
		raise NotImplementedError
	def getMonoSound(self, timeDelta):
		raise NotImplementedError
	def getStereoSound(self, timeDelta):
		raise NotImplementedError
		
def test_SoundGenerator(test_object):
	# p = test_object.getDefaultInitPos()
	# v = test_object.getDefaultInitVel()
	# t = test_object.getDefaultInitTime()
	test_object.reset()
	test_object.useDefaultEnergyInput()
	test_object.update(0.0025)
	# test_object.getAccel(p,v,t)
	test_object.getMonoSound(1.0/44100.0)
	test_object.getStereoSound(1.0/44100.0)
	
	
#use simulator.singleValueVector instead
# class singleValueVector(object):
	# def __init__(self, val): self.val = val
	# def getZero(self): return singleValueVector(0.0)
	# def add(self,other): return singleValueVector(self.val + other.val)
	# def scale(self, scalar): return singleValueVector(self.val * scalar)
	# def getMagn(self): return self.val
	# def getMagnSq(self): return self.val * self.val
	
	
class SineWaveSG(SoundGenerator):
	def __init__(self, freq=256.0, amp=1.0):
		self.freq = freq
		self.amp = amp
		self.time = 0.0
	def reset(self):
		self.time = 0.0
	def useDefaultEnergyInput(self):
		#dis do nufting
		unusedVariable = 123
	def update(self, timeDel):
		self.time += timeDel
	def getMonoSound(self, timeDelta):
		return self.amp * math.sin(self.time*2.0*math.pi/self.freq)	
	def getStereoSound(self, timeDelta):
		#timeDelta not used
		return (self.getMonoSound(timeDelta), self.getMonoSound(timeDelta))
	
class SimpleSpringSG(SoundGenerator):
	"""Use docstring instead of a getDescription function"""
	
	def __init__(self, mass, spring, damp, timeScale=1.0, outputScale=1.0):
		"""initialize the simplest useful SoundGenerator, a single mass on a spring (with damping). Use the simulator.particleWithSpring inside this SimpleSpringSG object. The scaling values self.timeScale and self.outputScale will modify the output of the simulator from the SoundGenerator's perspective, without modifying any internal values of the Simulator. When time is changed by t from the SoundGenerator's perspective, in other words the time of the SoundGenerator is updated by t, the time for the Simulator will change by timeScale*t. The SoundGenerator will track its own time, and the time used by the internal Simulator will always be timeScale*SoundGenerator.time. """
		
		self.timeScale = timeScale
		self.outputScale = outputScale
		
		# if (mass==0.0): self.inv_mass = 1.0
		# else: self.inv_mass = 1.0/mass
		# self.neg_d = -damp
		# self.neg_s = -spring
		
		self.sim = simulator.particleWithSpring(mass, spring, damp)
		
		self.pos = simulator.singleValueVector(0.0)
		self.vel = simulator.singleValueVector(0.0)
		self.time = 0.0
		
	def reset(self):
		self.pos = simulator.singleValueVector(0.0)
		self.vel = simulator.singleValueVector(0.0)
		self.time = 0.0
		
	def useDefaultEnergyInput(self):
		self.vel = self.vel.add(simulator.singleValueVector(1.5))
		

		
	def _change_mass(self, mass):
		if(mass == 0.0): self.sim.inv_mass = 1.0
		else: self.sim.inv_mass = 1.0/mass
	def _change_spring(self, spring):
		self.sim.neg_s = -spring
	def _change_damp(self, damp):
		self.sim.neg_d = -damp
	paramDict = {"mass": _change_mass, "spring": _change_spring, "damp": _change_damp}
	def setParam(self, paramName, value):
		paramDict[paramName](self, value)
		
	def update(self, timeDel):
		"""There is a choice of how many times to run the updating function over that time interval. This update method just runs once, which could lead to inaccuracies if the time interval is too long. The actual time interval used, from the simulator's perspective, will be timeDel*self.timeScale"""
		
		simulatorScaledTimeDel = timeDel*self.timeScale
		(self.pos,self.vel) = simulator.rungekuttastep(self.sim, simulatorScaledTimeDel, self.pos, self.vel, self.time)
		self.time += timeDel
	
	def getMonoSound(self, timeDelta):
		return self.outputScale*self.vel.getMagn()
	def getStereoSound(self, timeDelta):
		return (self.getMonoSound(timeDelta), self.getMonoSound(timeDelta))
