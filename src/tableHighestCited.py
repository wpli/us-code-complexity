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
import re
import sys
import zipfile


def initOutput():
	'''
	Setup the UTF-8 output.
	'''
	streamWriter = codecs.lookup('utf-8')[-1]
	sys.stdout = streamWriter(sys.stdout)
	
if __name__ == "__main__":
	'''
	Set the snapshot and load the file list.
	'''
	initOutput()
	
	edges = cPickle.load(open('data/citations.pickle'))
	sectionID = cPickle.load(open('data/sectionID.pickle'))
	nodes = set()
	map(nodes.update, zip(*edges))
	nodes = sorted(list(nodes))
	node_map = dict(zip(nodes, range(len(nodes))))
	edge_map = [(node_map[e[0]], node_map[e[1]]) for e in edges]
	g = igraph.Graph(edge_map, directed=True)
	g.vs['label'] = nodes
	indegree = g.indegree()
	outdegree = g.outdegree()

	output_file = csv.writer(open('results/table_section_degree.csv', 'w'))	
	for i in range(len(nodes)):
		if nodes[i] in sectionID:
			row = [nodes[i], indegree[i], outdegree[i]]
			output_file.writerow(row)
		else:
			print(nodes[i])
		
