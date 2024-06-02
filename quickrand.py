"""
A hash object can quickly and consistently get a pseudorandom value from a sequence of byte index values. hash256.listHast(self, byteList) will return the same value every time for the same byteList (after the hash256 object is initialized) but will have a random appearance when comparing the result of different sequences. Values in the byteList should be between 0 and 255 inclusive, but of course can be any integer class, not just a byte.

The distributions used are simply python lists. The values are not necessarily random in the distribution lists, it could for example have values ordered from lowest to highest."""




import random as r
#import time
import math

#We could precompute both the hash and the distribution objects, but I generally don't care about speed when the editor is starting up, only when computing the values. So for now I'll just use random  and math module functions to initialize the objects.

#magic values
arraySize = 256







class hash256(object):
	def __init__(self):
		templist = list(range(256))
		r.shuffle(templist) 
		self.h = templist*2
	def listHash(self, byteList):
		current = 0
		for i in byteList:
			current = self.h[i+current]
		return current

		
		
		

		

	


#Because we're completely relying on the hash to find a random byte value, we can use the inverse of the cumulative distribution to evenly distribute 256 values.

# class uniformDistribution(object):
	# def __init__(self):
		# self.a = [float(i)/float(arraySize) for i in range(arraySize)]
uniformDistribution = [float(i)/float(arraySize) for i in range(arraySize)]
		
#this distribution is one component of a unit vector with a uniformly-distributed random angle orientation
#this is the distribution you would expect if this were one dimension of a two-dimensional Perlin Noise
# class cosAngleDistribution(object):
	# def __init__(self):
		# self.a = [math.cos(float(i)*math.pi/float(arraySize)) for i in range(arraySize)]
cosAngleDistribution = [math.cos(float(i)*math.pi/float(arraySize)) for i in range(arraySize)]

#requires a hash object and a noise distribution object. Everything is deterministic, so calling noise1 twice with the same values (and the same hash and distribution arrays) will give exactly the same results. startIndex and hashList should be lists of values from 0 to 255 (bytes, but in integer form). startIndex and extraHashList can be empty. startIndex is intended to be the index of an object that uses this noise function, so that multiple objects with different values in StartIndex will have different noise results. extraHashList is intended to be used as an extra shuffle to mix up the results a bit more.
#this function finds the integer part of x/featureWidth, and uses that as a part of a multistep hashing process, to find two values to linearly interpolate (with easing) between.
#find the hash of [startIndex, x/featureWidth] + hashlist, then use that value as the index of the distribution array.
#it's assumed that featureWidth won't be zero. it's assumed that all the values in startIndex and hashList will be integers between 0 and 255 inclusive.
def noise1(featureWidth, x, startIndex, extraHashList, h, d=uniformDistribution):
	normed = x/featureWidth
	intPart = math.floor(normed)
	t = normed - intPart
	#easing function is 6t^5 - 15t^4 + 10t^3, a function with both value and derivative equal to zero at t=0 and t=1
	# = ((6*t -15)*t + 10)*t^3
	eased = ((6.0*t - 15.0)*t + 10.0)*t*t*t
	lowValue = d[ h.listHash(startIndex + [intPart] + extraHashList) ]
	highValue = d[ h.listHash(startIndex + [intPart+1] + extraHashList) ]
	return lowValue + (highValue-lowValue)*eased
	
def noise1d(featureWidth, x, startIndex, extraHashlist, h, d=uniformDistribution):
	#find the derivative of the noise1 function (with respect to x)
	#stub
	return 0.0
	
def test_all():
	h = hash256()
	value = noise1(1.0, 1.0, [5,4], [6,7], h, cosAngleDistribution)
	assert value == noise1(1.0,1.0,[5,4],[6,7], h, cosAngleDistribution)
	
def test_time():
	import time
	listLength = 1000
	randomList = [r.randrange(256) for i in range(listLength)]
	repeatTimes = 1000
	N = nphash256() #actual values will be different, I'm not even looking at what they are, only looking at computing time.
	L = hash256() #L = listhash256()
	
	
	
	startN = time.time()
	for i in range(repeatTimes):
		N.gethash_unsafe(randomList)
	totalN = time.time() - startN
	print("time for the numpy hash function: " + str(totalN))
	
	startL = time.time()
	for i in range(repeatTimes):
		L.listHash(randomList) #oops I'm changing the name a bit
	totalL = time.time() - startL
	print("time for the python list hash function: " + str(totalL))
	
	
	print("calling noise1 this many times: " + str(repeatTimes))
	
	startNoiseTime = time.time()
	noiseRepeat = 100000
	for i in range(noiseRepeat):
		noise1(1.0, 1.0, [5,4], [6,7], L, cosAngleDistribution)
	totalNoiseTime = time.time() - startNoiseTime
	print("Noise time: " + str(totalNoiseTime))
	
	startNoiseTime = time.time()
	print("to compare, calling random.randbytes(1) this many times:" + str(noiseRepeat))
	for i in range(noiseRepeat):
		r.randbytes(1)
	totalNoiseTime = time.time()-startNoiseTime
	print("Random module time: " + str(totalNoiseTime))
	startNoiseTime = time.time()
	for i in range(noiseRepeat):
		L.listHash([0])
	totalNoiseTime = time.time()-startNoiseTime
	print("Using hash, which I hope to gosh sakes is faster: " + str(totalNoiseTime))
	
	#well seems random.randbytes is very close to the same speed as calling this hash, on my computer... it's so fast that an operation like a modulo doubles the time. Although being truly random is actually not the desired behavior (consistent repeatability is also important) so it might still be worth it.
	
	