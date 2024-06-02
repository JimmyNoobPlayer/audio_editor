"""Mar 2024 """

import wave, struct, math, random
import winsound
import simulator
import soundgenerator


def trunc(val, maxVal=float("inf"), minVal=float("-inf")):
	"""Simple truncation, constrict a value to be between a minVal and maxVal."""
	if (val>maxVal): return maxVal
	if (val<minVal): return minVal
	return val


 # sampleRate = 44100.0
 # duration = 1.0
 # frequency = 220.0
 # loudness = 0.75





		

class RangeTracker(object):
	""" Observe any signal and track values of the signal, can do operations on the stored signal.
	This initial implementation just measures the max and min values of the signal, other variations are easy to imagine
	"""
	def __init__(self):
		self.min = 0.0
		self.max = 0.0
	def checkSignal(self, currentInputValue):
		if(currentInputValue < self.min): self.min=currentInputValue
		if(currentInputValue > self.max): self.max=currentInputValue
	def reset(self):
		self.min=0.0
		self.max=0.0
	def printFinalRange(self):
		print("RangeTracker, min value: " + str(self.min) + ", max value: " + str(self.max))



#change to use soundgenerator.SoundGenerator objects instead of Sounder objects.		
class BasicSGBank:
	#holds a collection of SoundGenerators, then sets up the total time duration and sampling frequency, and has the ability to execute the sounders and put the output in a file.
	def __init__(self, sgList=[]):
		self.sgList = sgList
	def addSG(self, s):
		self.sgList.append(s)
		return self
		

		

	def simpleRunDurationFile(self, filename, dur=1.0):
		"""Run each SoundGenerator in sgList for this duration, sum the mono outputs, and
		save that to a file, and play the file x3.
		"""
		
		#for every time sample, go through the list of every Sounder, add up the values, then round it into the right int value and write it to the file, then update the time value for all the Sounders, preparing for the next sample.
		magicSampleRate =  44100.0
		del_t = 1.0/magicSampleRate
		
		tracker = RangeTracker()
		tracker.reset()

		
		with wave.open(filename, mode='wb') as wf:
			wf.setnchannels(1)
			wf.setsampwidth(2)
			wf.setframerate(magicSampleRate)

			for i in range(round(magicSampleRate*dur)):
				value = 0.0
				for s in self.sgList:
					value += s.getMonoSound(del_t)
				
				tracker.checkSignal(value)
					
				#in this code block, change a float value from 0 to 1 into a value usable for a wave file, which is an integer between 0 and 2**15 - 1 inclusive, between zero and 32767. Little-endian form.
				
				#https://docs.python.org/3/library/wave.html
				
				intValue = int(round(32767.0*value*0.6)) #2**15 - 1
				cappedIntValue = trunc(intValue, 32766, -32766)
				#value = int(round(0.3*loudness*random.randint(-32767,32767)))
				#value = int(round( 32767.0*math.sin(math.pi*frequency*t) ))
				data = struct.pack('<h', cappedIntValue) #<h for little-endian, which is the incorrect way to eat an egg but what can you do. When in Liliput do as the Liliputians.
				
				#could be done using numpy rather than the struct module...
				
				wf.writeframesraw(data)
				for s in self.sgList:
					s.update(del_t)
		#end wavefile writing block
		
		#now play the sound from that file
		tracker.printFinalRange()
		repeat = 3
		for i in range(repeat):
			winsound.PlaySound(filename, winsound.SND_FILENAME)
		
	def simpleRunDurationList(self, dur=1.0):
		


	
	#I need to have a class that creates a simulator, and be able to change what ever qualities I need such as volume and frequency as a function of time, and also be able to define whatever functions I want as the spring and damping values, including being able to use the noise values.

	

def stuff():

	

	
	s = soundgenerator.SimpleSpringSG(1.0, 65536.0, 2.0) #the frequency is approximately the sqrt of the spring constant
	s.useDefaultEnergyInput()
	
	s2 = soundgenerator.SineWaveSG(256.0,0.7)
	
	b = BasicSGBank()
	b.addSG(s)
	#b.addSG(s2)
	b.simpleRunDurationFile("tryinout.wav")
	
	    