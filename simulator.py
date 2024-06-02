
	
	
"""Simulator class
An object that can be used to find numerical results of a second-order differential equation (the equation itself is second-order, in other words the state of the whole Simulator is a function of time and acceleration of the system is a function of position and velocity, and time.)
The Simulator does not hold any data about the current position or velocity.

The Simulator defines two separate Vectors, the particleVector and the parameterVector. The particleVector defines the part of the system that can be accelerated, usually a collection of particles with mass. The parameterVector defines every part of the system that changes the way the particles interact, such as the tension of a string, damping, or any other quality. A Sequence object can be defined that can change the parameters continuously in time; at every time creating a parameterVector, which can be given to the Simulator.

Since the ParameterVector is not added or scaled, it doesn't need to be an actual Vector, it can be a list of values.

description, implemented as a base class that need not be used in code
includes simple unit test test_anySimulator(s)
includes concrete class particleWithSpring

Simulators are time-invariant. The acceleration found by the Simulator is a function of the current position and velocity and nothing else.

The parameters of the Simulator, defined in the parameterVector, change in time according to the Sequence's whims, and of course these parameter values indirectly change how the particles will update.

A SoundGenerator object holds the Simulator and Sequence, and tracks the current position and velocity vectors.







'The Pythonic way to create a static class is simply to declare those methods outside of a class (Java uses classes both for objects and for grouping related functions, but Python modules are sufficient for grouping related functions that do not require any object instance).' - Michael Aaron Safyan, who is a user on stackoverflow who got more than a hundred upvotes so he prolly knows more than me

Only after long thought and modification did I come to the realization that the Simulator object should have only methods, not data fields.
But there are two considerations that make me wonder if I should  continue using them as objects:
1. There could be a wide variety of different objects with similar behavior, for example a spring with two particles, with three particles, or more likely ten or 100, or springs with different hysteresis qualities or random or noisy qualities in certain aspects. It seems reasonable to me to group the getting methods for default init position and velocity, getting acceleration, getting default Parameter vectors, etc, into an object simply to organize them. These would be STATIC classes with no instantiation, which I am assured is UNPYTHONIC and not worthy of consideration.
2. Perhaps we might want to create an interesting function, perhaps one with precisely set noise functions or modified functions for damping or spring acceleration, and then use these functions in the acceleration method. These functions could be modified as the human user is setting up the simulations.... this means the functions would be data members of a class intantiation... this would need instantiation and each instance will need to store the modified function....
3. I think of how many Simulator objects can be put together into a larger Simulator, so each individual Simulator will have qualities set..... also needs instantiation...

ugh, I think I need to just create something to see what is needed instead of endlessly theorizing. I think I'm going to go with 1. for now, and make the Simulator classes static with no instantiatioin. The qualities of individual Simulators if they are put into a larger simulator or use arbitrarily complicated methods, will need to be tracked by the SoundGenerators and Sequences, not the Simulators.

This means I need to modify the way the Simulators are written now, to remove the instantiation (self and __init__)

"""
	

	
import vector

	

class Simulator(object):
	#def __init__(self): raise NotImplementedError
	
	def getParticleZero(): raise NotImplementedError
	def getParameterZero(): raise NotImplementedError
	
	def getDefaultInitPos(): raise NotImplementedError
	def getDefaultInitVel(): raise NotImplementedError
	def getDefaultParameterVector(): raise NotImplementedError
	
	def getAccel(pos, vel, parameters): raise NotImplementedError
	
	
	
	

	

		
class particleWithSpring(Simulator):
	#256Hz = approximately middle C
	#44100Hz = common sampling frequency
		
	#particles: a single-dimension position for a mass on a spring
	#parameters: mass, spring constant, damping constant. Use a regular python list.
		
	#parameter[0] is mass
	#parameter[1] is spring constant
	#parameter[2] is damping constant
		
	def getParticleZero(): return vector.singleValueVector(0.0)
	def getParameterZero(): return [0.0, 0.0, 0.0] #hm, this probably doesn't have a reason to be used?
		
	def getDefaultInitPos(): return vector.singleValueVector(0.0)
	def getDefaultInitVel(): return vector.singleValueVector(0.0)
	def getDefaultParameterVector(): return [1.0, 65536.0, 0.5]
	def getAccel(pos, vel, parameters):

		
		force = particleWithSpring.getParticleZero()
		#force = getParticleZero()
		
		#spring force =  -displacement( which is x - x_0, ) * springConstant, x_0 == 0.
		force = force.add(pos.scale(-1.0*parameters[1]))
		#damping force = -velocity * dampingConstant
		force = force.add(vel.scale(-1.0*parameters[2]))
		#f=ma, a = f/m
		return force.scale(1.0/parameters[0])
		
		
		
#just checking that running the functions don't actually cause crashes, for now
def test_anySimulator(s):
	pos = s.getDefaultInitPos()
	vel = s.getDefaultInitVel()
	param = s.getDefaultParameterVector()
	acc = particleWithSpring.getAccel(pos,vel,param)
	acc = s.getAccel(pos,vel,param)
	
	s.getParticleZero()
	s.getParameterZero()



