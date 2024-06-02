		
"""Numeric methods
The step methods, for example rungekuttastep(simulator, step, posVector, velVector, time), find a numeric approximation of the system defined by simulator starting at the state defined by posVector, velVector, and t=time, at the time t=time+step.
"""	

import vector
import simulator
	

def getDefaultOutput(pos,vel): return vel.getMagn()

def getSimListInAnyState(simulator, timeStep, stepNum, inbetweenSteps, stepfunc, initPos, initVel):

	"""requires a simluator, which defines vectors that can define all the positional, velocity, or acceleration data of the simulated physics object, and defines a function that can determine the acceleration vector from any complete position and velocity. (getAccel(), and getZero() #a zero value of the vector type/shape used for position, velocity, acceleration)

	simulator is the object which defines the initial position, velocity, but we can set another state with the initPos,initVel values
	timeStep is the real amount of time for a step in the physical simulation
	stepNum is the number of samples to get for the outputList
	inbetweenSteps is the number of steps between the output samples
	stepfunc is the function used to update, which can be any of the huge variety of available numerical approximations
	"""

	currentPos = initPos
	currentVel = initVel
	outputList = [getDefaultOutput(currentPos, currentVel)]
	for i in range(stepNum):
		(currentPos,currentVel) = stepfunc(simulator, timeStep, currentPos, currentVel)
		outputList.append(getDefaultOutput(currentPos, currentVel))
		for i in range(inbetweenSteps):
			(currentPos,currentVel) = stepfunc(simulator, timeStep, currentPos, currentVel)

	return outputList
		

def getSimListDefaultState(simulator, timeStep, stepNum, inbetweenSteps, stepfunc):
	return getSimListInAnyState(simulator, timeStep, stepNum, inbetweenSteps, stepfunc, simulator.getDefaultInitPos(), simulator.getDefaultInitVel())
		
#second-order partial derivative, so acceleration is found by the simulator and position and velocity is calculated
def rungekuttastep(accelFunc, startTime, stepTime, posVector, velVector):
	"""RK4, the most commonly used Runge Kutta approximation. Requires a lot of precalculated values and formulas.
	
	Any step function should take as inputs an accelFunc (some function that takes the current position vector, velocity vector, and the current time, and gives the acceleration the particles experience for that orientation), a time step value, and position and veloctiy vectors. It will return an approximation of the postion and velocity vectors after the given time step value, using some approximation method."""
	
	sixth = 0.16666666666666666
	
	halfTime = startTime + 0.5*stepTime
	endTime = startTime + stepTime
	
	k1 = accelFunc(posVector, velVector, startTime)
	
	k2_vel = velVector.add(k1.scale(0.5*stepTime))
	k2 = accelFunc(posVector.add(velVector.scale(0.5*step)), k2_vel, halfTime)
	
	k3_vel = velVector.add(k2.scale(0.5*stepTime))
	k3 = accelFunc(posVector.add(k2_vel.scale(0.5*step)), k3_vel, halfTime)
	
	k4_vel = velVector.add(k3.scale(step))
	k4 = accelFunc(posVector.add(k3_vel.scale(step)), k4_vel, endTime)
	

	next_pos = vecAddList([velVector,k1,k2,k3,posVector],[stepTime, sixth*stepTime*stepTime, sixth*stepTime*stepTime, sixth*stepTime*stepTime, 1.0])
	next_vel = vecAddList([k1,k2,k3,k4,velVector], [sixth*stepTime, 2.0*sixth*stepTime, 2.0*sixth*stepTime, sixth*stepTime, 1.0])
	return (next_pos, next_vel)
	
#second-order partial derivative
def eulerstep(accelFunc, startTime, stepTime, posVector, velVector):

	next_vel = velVector.add(accelFunc(posVector,velVector,startTime).scale(stepTime))
	next_pos = posVector.add(velVector.scale(stepTime))
	return (next_pos, next_vel)
	
def nullstep(accelFunc, startTime, stepTime, posVector, velVector):
	return (posVector, velVector)


def simulator_accel(posVector, velVector, time):
	params = simulator.particleWithSpring.getDefaultParameterVector()
	
	return simulator.particleWithSpring.getAccel(self, posVector, velVector, params):
	
	
def test_getSimList():

	vector.test_anyVector(vector.singleValueVector(3.3))

	p = simulator.particleWithSpring(1.0, 1.0, 1.0)
	test_anySimulator(p)
	
	sp = p.getDefaultInitPos()
	sv = p.getDefaultInitVel()
	print("starting position and velocity")
	print(str(sp) + ' ' + str(sv))

	listNull = getSimListDefaultState(p, 0.01, 10, 2, nullstep) # sp, sv, 0.0)
	listEuler = getSimListDefaultState(p, 0.01, 10, 2, eulerstep) # sp, sv, 0.0)
	listRK = getSimListDefaultState(p, 0.01, 10, 2, rungekuttastep) #sp, sv, 0.0)
	
	print(listNull)
	print(listEuler)
	print(listRK)