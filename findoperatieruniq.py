# -*- coding: utf-8 -*-
import re
infile = r'./operationData.txt'
outfile = open('./operatername_error.txt','w')
RE_PATTERN_OPERATER_NAME = u'助手姓名[:：][\S ]*手术经过[：:]|手术医师[:：][\S ]*手术经过[：:]'
i=0
for line in open(infile, 'r'):
	i+=1
	line = line.strip().decode('utf8')
	if not re.search(RE_PATTERN_OPERATER_NAME,line):
		#print i,line.encode('utf8')
		ort = str(i) + '\t' + line + '\n'
		outfile.write(ort.encode('utf-8'))
		