import util
import SimBlock.node.Block
import SimBlock.node.Node
from SimBlock.simulator.Timer import *


class Simulator:
	def __init__():
		self.simulatedNodes = list()
		self.targetInterval = 1000*60*10 #msec
		self.averageDifficulty = None
		self.observedBlocks = list()
		self.observedPropagations = list()

		self.network = Network()
	
	def getSimulatedNodes(self): 
		return self.simulatedNodes 

	def getAverageDifficulty(self): 
		return self.averageDifficulty 

	def setTargetInterval(self, interval): 
		self.targetInterval = interval 
	
	def addNode(self, node):
		self.simulatedNodes.append(node)
		self.setAverageDifficulty()
	
	
	def removeNode(self, node):
		self.simulatedNodes.remove(node)
		self.setAverageDifficulty()
	
	
	def addNodeWithConnection(self, node):
		node.joinNetwork()
		self.addNode(node)
		for existingNode in self.simulatedNodes:
			existingNode.addNeighbor(node)
		
	# calculate averageDifficulty from totalMiningPower
	def setAverageDifficulty(self):
		totalMiningPower = 0
		for node in self.simulatedNodes:
			totalMiningPower += node.getMiningPower()
		if(totalMiningPower != 0):
			self.averageDifficulty =  totalMiningPower * self.targetInterval
		

	
	#
	#Record block propagation time
	#For saving memory, Record only the latest 10 Blocks
	# 
	
	
	def arriveBlock(self, block, node):
		if block in self.observedBlocks:
			Propagation = self.observedPropagations.get(observedBlocks.indexOf(block))
			Propagation.put(node.getNodeID(), getCurrentTime() - block.getTime())
		else:
			if(observedBlocks.size() > 10):
				printPropagation(observedBlocks.get(0),observedPropagations.get(0))
				observedBlocks.remove(0)
				observedPropagations.remove(0)
			
			propagation = dict()
			propagation[node.getNodeID()] = getCurrentTime() - block.getTime()
			self.observedBlocks.add(block)
			self.observedPropagations.add(propagation)
		
	
	
	def printPropagation(self, sblock, propagation):
		print(block + ":" + block.getHeight())
		for timeEntry in propagation.entrySet():
			print(timeEntry.getKey() + "," + timeEntry.getValue())	
		print()
	
	
	def printAllPropagation(self):
		for i in range(self.observedBlocks.size()):
			printPropagation(self.observedBlocks.get(i), self.observedPropagations.get(i))

