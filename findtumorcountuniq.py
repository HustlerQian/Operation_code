# -*- coding: utf-8 -*-
import re
infile = r'./operationData.txt'
outfile = open('./tumorcount_error.txt','w')
RE_PATTERN_tumor_count = u'肿瘤[2-9二三四五六七八九]*枚'
i=0
for line in open(infile, 'r'):
	i+=1
	line = line.strip().decode('utf8')
	if not re.search(RE_PATTERN_tumor_count,line):
		#print i,line.encode('utf8')
		ort = str(i) + '@\t' + line + '\n'
	else:
		line=re.search(RE_PATTERN_tumor_count,line).group(0) 
		ort =str(i) + '\t' + line + '\n'
	outfile.write(ort.encode('utf-8'))	