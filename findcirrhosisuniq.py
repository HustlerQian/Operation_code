# -*- coding: utf-8 -*-
import re
infile = r'./operationData.txt'
outfile = open('./cirrhosisname_error.txt','w')
RE_PATTERN_CIRRHOSIS_NAME = u'[，,。： ][^，,。： ]*肝[^ 。]*硬化[^，,。: ]*[，。, ]'
i=0
for line in open(infile, 'r'):
	i+=1
	line = line.strip().decode('utf8')
	if not re.search(RE_PATTERN_CIRRHOSIS_NAME,line):
		#print i,line.encode('utf8')
		ort = str(i) + '@\t' + line + '\n'
	else:
		line=re.search(RE_PATTERN_CIRRHOSIS_NAME,line).group(0) 
		if line[0]==u'：':
			pattern = u'[^，,。：]*肝[^ 。]*硬化[^，,。: ]*'
			line = re.search(pattern,line).group(0)
		else:
			line=line[1:-1]
		ort =str(i) + '\t' + line + '\n'
	outfile.write(ort.encode('utf-8'))	