# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 13:44:13 2016

@author: 310149083
"""
import re
import os
import string

RE_PATTERN_OPERATION_NAME = u'手术名称\S*'
RE_PATTERN_OPERATER_NAME = u'助手姓名[:：][\S ]*手术经过[：:]|手术医师[:：][\S ]*手术经过[：:]'
#u'肝硬化[重中轻]度|[重中轻]度肝硬化|无肝硬化|肝硬化'
RE_PATTERN_CIRRHOSIS = u'[，,。： ][^，,。]*肝[^ 。肝]*硬化[^，,。]*[，。, ]'
RE_PATTERN_SECTION_NAME = u'([^\s\t\n　\d\w。）;；？,，]{,4})：\S'

def _addSpace(matched):
    rawStr = matched.group()
    return ' '+rawStr

def _trans(rawStr, targetList = ['(', ')', '{', '}', '.']):
    #字符转义，避免re.compile报错
    newStr = rawStr
    for t in targetList:
        newStr = newStr.replace(t, '\\' + t)
        #print 21, newStr
    return newStr

def type(rawText):
    pattern_dict={
    u'切除':[u'切除',u'ALPPS(II期)',u'切术',u'淋巴结清扫',u'开窗',u'根治'],
    u'结扎':[u'ALPPS(I期)'],
    u'RFA':[u'射频'],
    u'取栓':[u'取栓',u'癌栓取出'],
    u'PEI':[u'无水酒精注射'],
    u'活检':[u'活检']
    }
    pattern_out={
    u'none liver':[u'VATS',u'胃',u'脾',u'DIXON',u'ERCP',u'病灶',u'膀胱']
    }
    pattern_buwei={
    u'肝左叶':[u'肝左叶',u'左肝'],
    u'肝右叶':[u'肝右叶',u'右肝'],
    u'肝中叶':[u'肝中叶'],
    u'胆囊':[u'胆囊'],
    u'肝左外叶':[u'肝?左外叶'],
    u'肝左内叶':[u'肝?左内叶'],
    u'肝右前叶':[u'肝?右前叶'],
    u'肝右后叶':[u'肝?右后叶'],
    u'肝左外叶上段':[u'肝?左外叶上段',u'Ⅱ段'],
    u'肝左外叶下段':[u'肝?左外叶下段',u'Ⅲ段'],
    u'肝左内叶上部':[u'肝?左内叶上[段部]',u'Ⅳa段'],
    u'肝左内叶下部':[u'肝?左内叶下[段部]',u'Ⅳb段'],
    u'肝右前叶下段':[u'肝?右前叶下段',u'Ⅴ段'],
    u'肝右前叶上段':[u'肝?右前叶上段',u'Ⅷ段'],
    u'肝右后叶下段':[u'肝?右后叶下段',u'Ⅵ段'],
    u'肝右后叶上段':[u'肝?右后叶上段',u'Ⅶ段'],
    u'肝尾状叶':[u'肝?尾状?叶'],
    }
    typetext=''
    rawText=rawText.replace(u'术,',u'术+')
    rawText=rawText.replace(u'术，',u'术+')
    raw=rawText.split(u'+')
    #print raw
    for part in raw:
        #typetext += u'+'
        jump,findtype,findbuwei,leixing,flag,ganbuwei=0,0,0,0,0,u''
        for pattern in pattern_out[u'none liver']:
            if re.search(pattern,part):
                typetext += u'none liver@3||'
                jump,findtype,findbuwei,flag=1,1,1,1   
        for key in pattern_dict:
            for pattern in pattern_dict[key]:
               if re.search(pattern,part) and jump==0:
                    findtype=1
                    for buwei in pattern_buwei:
                        if re.search(buwei,part):
                            #typetext += buwei + ':'
                            ganbuwei=buwei 
                            findbuwei,flag=1,2
                    leixing=key
                    #if typetext=='+':
                    #    typetext='+NA:'
                    #typetext += key+'||'
        if re.search(u'特殊肝',part):
            typetext += u'特殊肝'
            if flag!=2:flag=1
            if re.search(u'（[\s\S]+）',part):
                typetext += re.search(u'（[\s\S]+）',part).group(0)
                flag=3
            findbuwei=1
           
        if findbuwei==0 and findtype!=0 and re.search(u'肝',part):
            typetext += u'肝:'
        elif findbuwei==0:
            typetext += 'NA:'
        elif jump!=1:
            typetext += ganbuwei + u':' 
        if leixing!=0:
            typetext += leixing + '@' + str(flag) +'||'       
        if findtype==0:
            typetext += 'NA@'+ str(flag) + '||'
    #if typetext!='+':
    #    typetext=typetext[1:]
    #    if typetext[-1]==u'+':
    #        typetext+='NA'
    #    elif typetext[0]==u'+':
    #        typetext="NA"+typetext
    #else:
    #    typetext='NA'
    return typetext[:-2]

def shuzhe(rawText):
	shuzhetext=rawText.replace(u'手术经过：','')
	return shuzhetext
	
def shuzhedetail(rawText):
	shuzhetext=rawText.replace(u'手术经过：','')
	shuzhetext=shuzhetext.replace(u'手术医师：','')
	shuzhetext=shuzhetext.replace(u'助手姓名：','')
	shuzhetext=shuzhetext.replace(u'，',' ')
	shuzhetext=shuzhetext.replace(u'、',' ')
	shuzhetext=shuzhetext.replace(u'　',' ')
	shuzhetext=shuzhetext.replace(u'。',' ')
	shuzhetext=shuzhetext.replace(u'副教授',' ')
	shuzhetext=shuzhetext.replace(u'教授',' ')
	shuzhetext=shuzhetext.replace(u'主治医师',' ')
	shuzhetext=shuzhetext.replace(u'主任医师',' ')
	shuzhetext=shuzhetext.replace(u'住院医师',' ')
	shuzhetext=shuzhetext.replace(u'副主任医生',' ')
	shuzhetext=shuzhetext.replace(u'主任',' ')
	shuzhetext=shuzhetext.split(u' ')
	shuzhelist=[]
	for i in range(len(shuzhetext)):
		line=shuzhetext[i]
		if line!='':
			if len(line)>=4 or len(line)==1:
				line+='@'
			shuzhelist.append(line)
	shuzhedetailtext=''
	for i in range(len(shuzhelist)):
		if i==0:
			shuzhedetailtext += u'术者姓名：' + shuzhelist[i] + u'；'
		elif i==1:
			shuzhedetailtext += u'助手姓名：' + shuzhelist[i] + u'，'
		else:
			shuzhedetailtext += shuzhelist[i] + u'，'
	return shuzhedetailtext[:-1]
	
def extractOperationName(rawStr, outpath = None, mode = 'append'):
    uniqSecNames = getSecNames(rawStr, None)
    newStr = rawStr
    for secName in uniqSecNames:
        re_ex = u'[^\\s\\t\\n　]'+ _trans(secName)
        #print re_ex
        p = re.compile(re_ex)
        newStr = p.sub(_addSpace, newStr)
    re_rlts_operation_name = re.compile(RE_PATTERN_OPERATION_NAME).findall(newStr)
    if outpath is None:
        print re_rlts_operation_name
        pass
    else:
        if os.path.isfile(outpath):
            if mode == 'append':
                outfile = open(outpath, 'a')
            elif mode == 'overwrite':
                outfile = open(outpath, 'w')
        else:
            outfile = open(outpath, 'w')
        for rlt in re_rlts_operation_name:
            #txt = rawStr + '\t' + rlt + '\t' + type(rlt) + '\n'      
            txt = rlt + '\t' + type(rlt) + '\n'  
            outfile.write(txt.encode('utf8'))
        outfile.close()

def extractOperaterName(rawStr, outpath = None, mode = 'append'):
    uniqSecNames = getSecNames(rawStr, None)
    newStr = rawStr
    for secName in uniqSecNames:
        re_ex = u'[^\\s\\t\\n]'+ _trans(secName)
        #print re_ex
        p = re.compile(re_ex)
        newStr = p.sub(_addSpace, newStr)
    re_orts_operation_name = re.compile(RE_PATTERN_OPERATER_NAME).findall(newStr)
    if outpath is None:
        print re_orts_operation_name
        pass
    else:
        if os.path.isfile(outpath):
            if mode == 'append':
                outfile = open(outpath, 'a')
            elif mode == 'overwrite':
                outfile = open(outpath, 'w')
        else:
            outfile = open(outpath, 'w')
        for ort in re_orts_operation_name:
            txt = shuzhe(ort) + '\t' + shuzhedetail(ort) + '\n'  
            outfile.write(txt.encode('utf8'))
        outfile.close()		

def extractCirrhosis(rawStr, outpath = None, mode = 'append'):
    uniqSecNames = getSecNames(rawStr, None)
    newStr = rawStr
    for secName in uniqSecNames:
        re_ex = u'[^\\s\\t\\n　]'+ _trans(secName)
        #print re_ex
        p = re.compile(re_ex)
        newStr = p.sub(_addSpace, newStr)
    re_gyhts_operation_name = re.compile(RE_PATTERN_CIRRHOSIS).findall(newStr)
    if outpath is None:
        print re_rlts_operation_name
        pass
    else:
        if os.path.isfile(outpath):
            if mode == 'append':
                outfile = open(outpath, 'a')
            elif mode == 'overwrite':
                outfile = open(outpath, 'w')
        else:
            outfile = open(outpath, 'w')
        for gyht in re_gyhts_operation_name:
            #txt = rawStr + '\t' + rlt + '\t' + type(rlt) + '\n'      
            txt = gyht + '\n'  
            outfile.write(txt.encode('utf8'))
        outfile.close()		

def getSecNames(rawStr, outpath = None, mode = 'append'):
    re_rlts_section_name = re.compile(RE_PATTERN_SECTION_NAME).findall(rawStr)
    unique_secNames = [i.strip() for i in list(set(re_rlts_section_name)) if len(i.strip())]
    if outpath is None:
        #print re_rlts_section_name
        pass
    else:
        if os.path.isfile(outpath):
            if mode == 'append':
                outfile = open(outpath, 'a')
            elif mode == 'overwrite':
                outfile = open(outpath, 'w')
        else:
            outfile = open(outpath, 'w')
        for rlt in unique_secNames:
            txt = rlt + '\n'            
            outfile.write(txt.encode('utf8'))
        outfile.close()
    return unique_secNames
        
if __name__ == '__main__':
    infolder = r''
    infile = r'./operationData.txt'
    os.system('del operationName_gyhts.txt')
    os.system('del operationName_rlts.txt')
    os.system('del operationName_orts.txt')
    for line in open(infile, 'r'):
        line = line.strip().decode('utf8')
        extractCirrhosis(line, r'./operationName_gyhts.txt', 'append') 
        extractOperaterName(line, r'./operationName_orts.txt', 'append')        
        extractOperationName(line, r'./operationName_rlts.txt', 'append')
		