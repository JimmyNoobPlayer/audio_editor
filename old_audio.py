"""Feb 2024 """

import wave, struct, math, random
import winsound
import rk4
import soundgenerator


def trunc(val, maxVal=float("inf"), minVal=float("-inf")):
	"""Simple truncation, constrict a value to be between a minVal and maxVal."""
	if (val>maxVal): return maxVal
	if (val<minVal): return minVal
	return val

# class Sounder:
	# defaultSampleRate = 44100.0 #hertz
	# defaultDuration = 1.0 #seconds
	# defaultFrequency = 440.0 #hertz
	# def __init__(self, sampleRate=defaultSampleRate, duration=defaultDuration, frequency=defaultFrequency):
		# self.sampleRate = sampleRate
		# self.duration = duration
		# self.frequency = frequency
		# self.t=0.0
		# return self
	# def __iter__(self):
		# return self
	# def __next__(self):
		# return "nothing here"

 # sampleRate = 44100.0
 # duration = 1.0
 # frequency = 220.0
 # loudness = 0.75



# with wave.open("testwavefile.wav", mode='wb') as wf:
	# wf.setnchannels(1)
	# wf.setsampwidth(2)
	# wf.setframerate(sampleRate)
	# t=0.0
	# del_t = 1.0/sampleRate
	# for i in range(round(sampleRate*duration)):
		# #value = int(round(0.3*loudness*random.randint(-32767,32767)))
		# value = int(round( 32767.0*math.sin(math.pi*frequency*t) ))
		# t += del_t
		# data = struct.pack('<h', value)
		# wf.writeframesraw(data)
# #end wave file writing

#I want to do:
#define a Sounder to make a sound (which can be varied by frequency and loudness, and perhaps many other qualities) then play that Sounder in many ways in a music (wave) file with many sounds that can be put together into a musical track.

#with a Sounder that produces a sound of potentially infinite duration, there must be an envelope to limit the sound, which could be as simple as some kind of step or window function. This could be placed like a block of sound as a raw material, which can be modified and used in a digital workstation or music editing program.

#sounds can have filters placed on them, which have a simple flexible and comprehensive form as a rational discrete filter. Other functions of the output can be defined and used. (PID controller?)

#we should have a SounderBank that holds a bunch of Sounders, and can have filters placed on the sounders or groups of sounders. then the SounderBank can play and put all the sounds into a wave file.

#if they are used in SounderBanks, the Sounders themselves can be modified to be much more like physical simulations, not needing information about sampling frequency and so forth, because that info is only useful in the process of making that physical simulation a discrete-ized sequence of audio samples.




#rk4.Simulation is a useful class. It runs a physical simulation that defines a vector of all the moveable elements of that specific simulation, and for any position and velocity vector, the Simulation has a way to detect the sound produced by that position/velocity, and a way to define the acceleration experienced by every moveble element for that position/velocity. A stepping method like Runge-Kutta or Euler's method can be used to find the position/velocity value for a time step in the future.

#however this Simulation class isn't all I need, since I want the ability to use simply defined Sounders like a square wave or sine producer!

#simulators track the time of the simulation, in case I want to have some quality of the simulation that changes over time, so this can be relied on to make a simply defined sound producer into a Simulation. Simply define the acceleration as zero all the time, maybe even define a useless completely zero vector (by which I mean, the set of all possible vectors is just a single zero vector, which I beleive trivially satisfies all the vector axioms and definitions)



		#sin^3(x), or (sin(x))^3, = 1/4(3sin(x) - sin(3x))
		#sin(sin(x)) is a fairly complex waveform with a general sine-like shape.
		
		
#my favorite part was when August Moebius said "It's coordinatin' time" and then defined points as centers of mass of masses at the corners of an n-dimensional simplex all over the place

class Sounder:
#a physical simulation, so uses real values. Not able to move arbitrarily in time, it must be updated step by step.
	def __init__(self):
		self.t = 0.0
	def update(self, tdel):
		self.t += tdel
		return self
	def getCurrentT(self):
		return self.t
	def val(self):
		return 0.0
		
#use soundgenerator.SoundGenerator


class SqWaveSounder(Sounder):
	def __init__(self, freq, maxVal, minVal):
		super().__init__()
		self.half_period = 0.5/freq
		self.maxVal = maxVal
		self.minVal = minVal
	#def update(self, tdel)
	#def getCurrentT(self)
	def val(self):
		count = math.floor(self.t/self.half_period)
		if (count%2==0): return self.maxVal
		else: return self.minVal
		
class SimSounder(Sounder):
	def __init__(self, inSim, stepfunction):
		self.sim = inSim	
		self.pos = inSim.getDefaultInitPos()
		self.vel = inSim.getDefaultInitVel()
		self.time = inSim.getDefaultInitTime()	
		self.stepfunc = stepfunction
	
	def update(self, tdel):
		(self.pos, self.vel) = self.stepfunc(self.sim, tdel, self.pos, self.vel, self.time)
	def getCurrentT(self):
		return self.time
	def val(self):
		return self.sim.getOutputValue(self.pos,self.vel,self.time)
		


	
class BasicSounderBank:
	#holds a collection of Sounders, then sets up the total time duration and sampling frequency, and has the ability to execute the sounders and put the output in a file.
	def __init__(self, sounderList=[]):
		self.sounderList = sounderList
	def addSounder(self, s):
		self.sounderList.append(s)
		return self
		

		
	#is temp memory large enough to hold the whole thing in something like a list?
	#even if it is, I can save it to a file, then play that file, probably don't need to tho.
	def runDurationFile(self, filename, dur=1.0):
		#for every time sample, go through the list of every Sounder, add up the values, then round it into the right int value and write it to the file, then update the time value for all the Sounders, preparing for the next sample.
		magicSampleRate =  44100.0
		del_t = 1.0/magicSampleRate
		
		largestValue = 0.0
		smallestValue = 0.0

		
		with wave.open(filename, mode='wb') as wf:
			wf.setnchannels(1)
			wf.setsampwidth(2)
			wf.setframerate(magicSampleRate)

			for i in range(round(magicSampleRate*dur)):
				value = 0.0
				for s in self.sounderList:
					value += s.val()
				
				if (value>largestValue): largestValue = value
				if (value<smallestValue): smallestValue = value
					
				intValue = int(round(32767.0*value*0.015))
				cappedIntValue = trunc(intValue, 32766, -32766)
				#value = int(round(0.3*loudness*random.randint(-32767,32767)))
				#value = int(round( 32767.0*math.sin(math.pi*frequency*t) ))
				data = struct.pack('<h', cappedIntValue)
				wf.writeframesraw(data)
				for s in self.sounderList:
					s.update(del_t)
		#end wavefile writing block
		
		#now play the sound from that file
		print("range of values from the full list of Sounders: " + str(smallestValue) + " to " + str(largestValue))
		repeat = 3
		for i in range(repeat):
			winsound.PlaySound(filename, winsound.SND_FILENAME)
		
	


	
	#I need to have a class that creates a simulator, and be able to change what ever qualities I need such as volume and frequency as a function of time, and also be able to define whatever functions I want as the spring and damping values, including being able to use the noise values.

	

def stuff():
	loudness = 0.1
	s = SqWaveSounder(256.0, 1.0*loudness, -1.0*loudness) #set to 1.0, the volume is quite loud, and it seems to set intensity, not decibels, which are put in a logarithmic scale.
	
	sim = rk4.particleWithSpring(1.0, 69000.0, 0.5)  #(self, mass, spring, damp, spring_zero_point)
	ss = SimSounder(sim, rk4.rungekuttastep)
	
	b = BasicSounderBank()
	#b.addSounder(s)
	b.addSounder(ss)
	b.runDurationFile("tryinout.wav")
	
	    