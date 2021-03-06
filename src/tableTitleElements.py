# -*- coding: utf-8 -*-
'''
@author mjbommar
@date Jan 30, 2009
'''


import csv
import codecs
import cPickle
import glob
import htmlentitydefs
import igraph
import lxml.etree
import multiprocessing
import os.path
import pylab
import re
import sys
import zipfile

def initOutput():
	'''
	Setup the UTF-8 output.
	'''
	streamWriter = codecs.lookup('utf-8')[-1]
	sys.stdout = streamWriter(sys.stdout)

def loadTitle(titleN, elements):
	nodes = set()
	edges = set()
	
	titleString = 'TITLE {0} -'.format(titleN)
	titleAppendixString = 'TITLE {0} - APPENDIX'.format(titleN)
	
	for e in elements:
		if not e.startswith(titleString) or e.startswith(titleAppendixString):
			continue
		
		p = e.split('_')
		
		for i in range(1, len(p)):
			eA = '_'.join(p[0:i])
			eB = '_'.join(p[0:i+1])
			nodes.update([eA,eB])
			edges.add((eA,eB))
	
	nodes = sorted(list(nodes))
	nodeMap = dict(zip(nodes, range(len(nodes))))
	edges = sorted(list(edges))
	edges = [(nodeMap[e[0]], nodeMap[e[1]]) for e in edges]
	
	g = igraph.Graph(edges, directed = True)
	for i,v in enumerate(g.vs):
		v['label'] = nodes[i]
	
	return g

if __name__ == "__main__":
	initOutput()	
	
	elements = cPickle.load(open('data/elements.pickle'))
	titles = range(1,51)
	titles.remove(34)
	
	output_rows = []
	for t in titles:
		g = loadTitle(t, elements)
		numAbove = len([v['label'] for v in g.vs if u"§" not in v['label']])
		numSection = len([v['label'] for v in g.vs if u"§" in v['label'].split('_').pop()])
		numBelow = len([v['label'] for v in g.vs if u"§" in v['label'] and u"§" not in v['label'].split('_').pop()])

		row = map(str, [t, g.vcount(), numAbove, numSection, numBelow])
		output_rows.append([t, g.vcount(), numAbove, numSection, numBelow])
		print ' & '.join(row) + "\\\\"

	output_file = csv.writer(open('results/table_title_elements.csv', 'w'))
	output_file.writerows(output_rows)
	
	
