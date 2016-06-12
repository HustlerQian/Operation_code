# -*- coding: utf-8 -*-
import re
import sys
import yaml
reload(sys)
sys.setdefaultencoding('utf-8')

#判断该句属于simple还是complex
def DecideCEorSE(text):
    decision=u'SE'
    
    #complex的模式，（总结的话）
    CEpattern=u'肿瘤\d+枚|均|分别|所有|肿瘤[两二三四五六七八九]枚'
    if re.search(CEpattern,text):
        decision=u'CE'
    
    return decision
    
#将中文数字转化为阿拉伯数字
def transCNtoabrb(text):
    output=re.sub(u'一',u'1',text)
    output=re.sub(u'二|两',u'2',output)
    output=re.sub(u'三',u'3',output)
    output=re.sub(u'四',u'4',output)
    output=re.sub(u'五',u'5',output)
    output=re.sub(u'六',u'6',output)
    output=re.sub(u'七',u'7',output)
    output=re.sub(u'八',u'8',output)
    output=re.sub(u'九',u'9',output)
    output=re.search(u'[0-9]+',output).group(0)
    return int(output.encode('utf-8'))

infile = r'./operationData.txt'
outfile = open('./tumorinfo_error.txt','w')
out_dict = open('./tumorinfo_dict.txt','w')
#总结的那句话的各种写法
RE_PATTERN_tumor_info = u'病人安返病房.*|术毕送移植监护室.*送病理'
line_no=0
tumor_infor={}
#肿瘤的各类写法
pattern=u'肿瘤.*|血管瘤.*|胆囊癌.*|胆囊肿.*|肿块.*|肿物.*|囊肿.*'
for line in open(infile, 'r'):
    line_no+=1
    line_raw=line
    line = line.strip().decode('utf8')
    part=''
    tumor_infor[line_no]={}
    if not re.search(RE_PATTERN_tumor_info,line):
        #print i,line.encode('utf8')
        ort = '@\t' + line + '\n'
    else:
        line=re.search(RE_PATTERN_tumor_info,line).group(0) 
        part=''
        #判断总结那句话里是否有肿瘤的信息
        if re.search(pattern,line):
            line=re.search(pattern,line).group(0)
            line=re.sub(u',',u'，',line)
            line=re.sub(u'；',u'，',line)
            line=re.sub(u'。',u'，',line)
            #按照逗号分句
            line=line.split(u'，')
            former='SE'
            former_index=''
            tumor_index=0
            for index in range(len(line)):
                #part+=line[index]+','
                part+=str(index)+DecideCEorSE(line[index])+':'+line[index]+u'|'
                
                #'术中输血'等信息不需要直接跳出,已‘术’开头
                break_pattern=u'^术中|^手术'
                #设置一个从单个肿瘤信息跳回SE的pattern,都是非单个肿瘤的信息
                refresh_pattern=u'^肝|^门静脉'
                
                if re.search(break_pattern,line[index]):
                    break
                
                #不属于CE底下的SE
                if DecideCEorSE(line[index])=='SE' and former!='CE':
                    outfile.write('%s\n'%(line[index]))
                #引出一串SE的CE    
                elif DecideCEorSE(line[index])=='CE':
                    outfile.write('%s\n'%(line[index]))
                    former='CE'
                #CE带出来的SE，                
                elif DecideCEorSE(line[index])=='SE' and not re.search(refresh_pattern,line[index]):
                    #单个肿瘤信息引出的模式
                    tumor_index_pattern=u'^最大一枚|^最大1枚|^另一枚|^另1枚|^一枚|^1枚'
                    if re.search(tumor_index_pattern,line[index]):
                        outfile.write('\t%s\n'%(line[index]))
                    else:    
                        outfile.write('\t\t%s\n'%(line[index]))
                elif DecideCEorSE(line[index])=='SE' and re.search(refresh_pattern,line[index]):
                    outfile.write('%s\n'%(line[index]))
                    former='SE'
                    
                    
        
                #判别语境前是se还是ce
                #if DecideCEorSE(line[index])=='SE':
                #    if former=='SE':
                #        tumor_infor[line_no][index]=line[index]
                #    else:
                #        #if  line[index][0]=='肝':
                #        if re.search(u'^肝',line[index]):
                #            tumor_infor[line_no][index]=line[index]
                #            former='SE'
                #        elif former=='CE肿瘤':
                #            tumor_index_pattern=u'^最大一枚|^最大1枚|^另一枚|^另1枚|^一枚|^1枚'
                #            #分别对应之前的几枚
                #            if re.search(tumor_index_pattern,line[index]):
                #                tumor_index+=1
                #                tumor_infor[line_no][former_index][tumor_index]=[line[index]]
                #            elif tumor_index!=0:
                #                tumor_infor[line_no][former_index][tumor_index].append(line[index])
                #            else:
                #                try:
                #                    print line[index]
                #                except:
                #                    pass
                #        else:
                #            tumor_infor[line_no][former_index]['SE'].append(line[index])
                #else:
                #    #根据肿瘤的数量制定字典中SE的个数
                #    tumor_count_pattern=u'肿瘤\d+枚|肿瘤[二三四五六七八九]枚'
                #    if re.search(tumor_count_pattern,line[index]):
                #        tumor_count=transCNtoabrb(line[index])
                #        tumor_infor[line_no][index]={'CE':line[index]}
                #        for i in range(tumor_count):
                #            tumor_infor[line_no][index][i+1]=[]
                #        former='CE肿瘤'
                #    else:
                #        tumor_infor[line_no][index]={'CE':line[index],'SE':[]}
                #        former='CE'
                #    former_index=index
                #print former_index
                
                
        #for sample in tumor_infor[line_no]:
        #    #print sample
        #    if type(tumor_infor[line_no][sample])!=dict:
        #        out_dict.write('%s\t%s\n'%(sample,tumor_infor[line_no][sample].encode('utf-8')))
        #    else:
        #        out_dict.write('%s\t%s\n'%(sample,tumor_infor[line_no][sample]['CE'].encode('utf-8')))
        #        if tumor_infor[line_no][sample].has_key('SE'):
        #            SE_item=';'.join(tumor_infor[line_no][sample]['SE'])
        #            out_dict.write('%s\t%s\n'%('\t',SE_item.encode('utf-8')))
        #        else:
        #            tumor_count=transCNtoabrb(tumor_infor[line_no][sample]['CE'])
        #            print tumor_count
        #            for tumor_count_index in range(tumor_count):
        #                tumor_count_index+=1
        #                SE_item=';'.join(tumor_infor[line_no][sample][tumor_count_index])
        #                out_dict.write('%s\t%s\n'%('\t',SE_item.encode('utf-8')))
        #out_dict.write('==================我是分割线=====================\n')            
        #yaml输出
        #yaml.dump(tumor_infor[line_no],out_dict)
        #print tumor_infor
        if part=='':
            part=line
        ort = '\t' + part + '\n'
    outfile.write('\n处理文本：%s'%(ort.encode('utf-8')))
    outfile.write('\n原文本：%s\n'%(line_raw))
    outfile.write('======================================================================================\n\n')
    #break

outfile.close()	