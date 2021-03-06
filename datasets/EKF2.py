# This code defines a customized dataset and can generate an instance of it
from torch.utils.data.dataset import *
import torch
import os
import numpy as np
import utils.transforms as t

class myDataset(Dataset):
	def __init__(self, info, opt, split):
		self.split = split
		self.dataInfo = info[split]
		self.numEntry = len(self.dataInfo['xml'])
		self.opt = opt
		self.dir = info['basedir']

	def __getitem__(self, index):
		path = self.dataInfo['dataPath'][index]
		data = torch.load(os.path.join(self.dir, path, 'merged.pth'))
		xml = self.dataInfo['xml'][index]
		startLp = data[0][0][0]
		for i in range(21):
			data[0][0][i] -= startLp
		xml -= startLp
		xmlLen = self.dataInfo['xmlLen'][index] # may not be useful
		return self.preprocessData(data), self.preprocessXml(xml)

	def __len__(self):
		return self.numEntry

	def preprocessData(self, ipt):
		if self.split == 'train':
			processed = t.thAddNoise(ipt, 0, 0.001)
			return processed
		elif self.split == 'val':
			processed = ipt
			return processed

	def preprocessXml(self, ipt):
		processed = torch.zeros(self.opt.outputSize)
		processed[0] = ipt[0]
		processed[1] = ipt[1]
		processed[2] = ipt[2]
		processed[3] = ipt[3]
		return processed

	def postprocessData(self):
		def process(ipt):
			processed = ipt
			return processed
		return process

	def postprocessXml(self):
		def process(ipt):
			processed = ipt / 2 * (self.opt.lpMax - self.opt.lpMin) + (self.opt.lpMax + self.opt.lpMin)/2
			return processed
		return process

def getInstance(info, opt, split):
	if split == 'test':
		return myDataset(info, opt, 'val')
	myInstance = myDataset(info, opt, split)
	return myInstance