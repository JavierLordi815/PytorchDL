import os
import torch
from torch.nn.parallel.data_parallel import DataParallel
import torch.nn as nn
import subprocess

def latest(opt):
	print('=> Loading the latest checkpoint')
	latestPath = os.path.join(opt.resume, 'latest.pth')
	assert os.path.exists(latestPath), opt.resume + '/latest.pth does not exist.'
	return torch.load(latestPath)

def best(opt):
	print('=> Loading the best checkpoint')
	bestPath = os.path.join(opt.resume, 'best.pth')
	assert os.path.exists(bestPath), opt.resume + '/best.pth does not exist.'
	return torch.load(bestPath)	

def load(opt):
	epoch = opt.epochNum
	if epoch == 0:
		return None
	elif epoch == -1:
		return latest(opt)
	elif epoch == -2:
		return best(opt)
	else:
		modelFile = 'model_' + str(epoch) + '.pth'
		criterionFile = 'criterion_' + str(epoch) + '.pth'
		optimFile = 'optimState_' + str(epoch) +'.pth'
		loaded = {'epoch':epoch, 'modelFile':modelFile, 'criterionFile':criterionFile, 'optimFile':optimFile}
		return loaded

def save(epoch, model, criterion, optimState, bestModel, loss, opt):
	if isinstance(model, nn.DataParallel):
		model = model.get(0)

	if bestModel or (epoch % opt.saveEpoch == 0):
		if opt.saveOne:
			subprocess.call('rm ' + opt.resume + '/*.pth', shell=True)
			
		modelFile = 'model_' + str(epoch) + '.pth'
		criterionFile = 'criterion_' + str(epoch) + '.pth'
		optimFile = 'optimState_' + str(epoch) +'.pth'
		torch.save(model, os.path.join(opt.resume, modelFile))
		torch.save(criterion, os.path.join(opt.resume, criterionFile))
		torch.save(optimState, os.path.join(opt.resume, optimFile))
		info = {'epoch':epoch, 'modelFile':modelFile, 'criterionFile':criterionFile, 'optimFile':optimFile, 'loss':loss}
		torch.save(info, os.path.join(opt.resume, 'latest.pth'))

	if bestModel:
		info = {'epoch':epoch, 'modelFile':modelFile, 'criterionFile':criterionFile, 'optimFile':optimFile, 'loss':loss}
		torch.save(info, os.path.join(opt.resume, 'best.pth'))
		torch.save(model, os.path.join(opt.resume, 'model_best.pth'))	