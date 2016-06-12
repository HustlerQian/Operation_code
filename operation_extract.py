#-*- coding:utf-8 -*-
import re
import os
import sys
import time
from mako.template import Template

ISOTIMEFORMAT='%Y-%m-%d %X'

#肝部位pattern
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

confident_level={
    u'0':u'未抽全，存疑',
    u'1':u'低',
    u'2':u'中',
    u'3':u'高'
}

count_cn2arab={
    u'二':u'2',u'2':u'2',
    u'三':u'3',u'3':u'3',
    u'四':u'4',u'4':u'4',
    u'五':u'5',u'5':u'5',
    u'六':u'6',u'6':u'6',
    u'七':u'7',u'7':u'7',
    u'八':u'8',u'8':u'8',
    u'九':u'9',u'9':u'9'
}

def _addSpace(matched):
    rawStr = matched.group()
    return ' '+rawStr

def _trans(rawStr, targetList = ['(', ')', '{', '}', '.']):
    #字符转义，避免re.compile报错
    newStr = rawStr
    for t in targetList:
        newStr = newStr.replace(t, '\\' + t)
    return newStr





#抽取手术名称
def extractOperationName(text):
    #手术名称pattern
    RE_PATTERN_OPERATION_NAME = u'手术名称\S*'
    RE_PATTERN_SECTION_NAME = u'([^\s\t\n　\d\w。）;；？,，]{,4})：\S'
    ######## 抽出u'手术日期', u'手术名称', u'术前诊断', u'术中诊断', u'麻醉方法', u'麻醉医师', u'助手姓名', u'手术经过', u'包括', u'探查'的list ########
    re_rlts_section_name = re.compile(RE_PATTERN_SECTION_NAME).findall(text)
    uniqSecNames = [i.strip() for i in list(set(re_rlts_section_name)) if len(i.strip())]
    newStr = text
    for secName in uniqSecNames:
        re_ex = u'[^\\s\\t\\n　]'+ _trans(secName)
        #print re_ex
        p = re.compile(re_ex)
        newStr = p.sub(_addSpace, newStr)
    #######手术名称
    re_rlts_operation_name = re.compile(RE_PATTERN_OPERATION_NAME).findall(newStr)

    return re_rlts_operation_name 

def type(rawText):
    #手术类型pattern
    pattern_dict={
    u'切除':[u'切除',u'ALPPS(II期)',u'切术',u'淋巴结清扫',u'开窗',u'根治'],
    u'结扎':[u'ALPPS(I期)'],
    u'RFA':[u'射频'],
    u'取栓':[u'取栓',u'癌栓取出'],
    u'PEI':[u'无水酒精注射'],
    u'活检':[u'活检']
    }
    #非手术类型pattern
    pattern_out={
    u'none liver':[u'VATS',u'胃',u'脾',u'DIXON',u'ERCP',u'病灶',u'膀胱']
    }
    typetext=''
    rawText=rawText.replace(u'术,',u'术+')
    rawText=rawText.replace(u'术，',u'术+')
    raw=rawText.split(u'+')
    #print raw
    for part in raw:
        #typetext += u'+'
        jump,findtype,findbuwei,leixing,flag,ganbuwei=0,0,0,0,0,u''
        ########如果是none liver 直接跳出 ##########
        for pattern in pattern_out[u'none liver']:
            if re.search(pattern,part):
                typetext += u'none liver:NA@3||'
                jump,findtype,findbuwei,flag=1,1,1,1   
        for key in pattern_dict:
            for pattern in pattern_dict[key]:
               if re.search(pattern,part) and jump==0:
                    findtype=1
                    for buwei in pattern_buwei:
                        if re.search(buwei,part):
                            ganbuwei=buwei 
                            findbuwei,flag=1,2
                    leixing=key
        if re.search(u'特殊肝',part):
            typetext += u'特殊肝'
            if flag!=2:flag=1
            if re.search(u'（[\s\S]+）',part):
                typetext += re.search(u'（[\s\S]+）',part).group(0)
                flag=3
            findbuwei=1
           
        if findbuwei==0 and re.search(u'肝',part):
            typetext += u'肝:'
        elif findbuwei==0:
            typetext += 'NA:'
        elif jump!=1:
            typetext += ganbuwei + u':' 
        if leixing!=0:
            typetext += leixing + '@' + str(flag) +'||'       
        if findtype==0:
            typetext += 'NA@'+ str(flag) + '||'
    typetext = rawText + '\t' +typetext
    return typetext[:-2]

#抽取术者信息    
def extractOperaterName(text):
    RE_PATTERN_OPERATER_NAME = u'助手姓名[:：][\S ]*手术经过[：:]|手术医师[:：][\S ]*手术经过[：:]'
    RE_PATTERN_SECTION_NAME = u'([^\s\t\n　\d\w。）;；？,，]{,4})：\S'
    ######## 抽出u'手术日期', u'手术名称', u'术前诊断', u'术中诊断', u'麻醉方法', u'麻醉医师', u'助手姓名', u'手术经过', u'包括', u'探查'的list ########
    re_orts_section_name = re.compile(RE_PATTERN_SECTION_NAME).findall(text)
    uniqSecNames = [i.strip() for i in list(set(re_orts_section_name)) if len(i.strip())]
    newStr = text
    for secName in uniqSecNames:
        re_ex = u'[^\\s\\t\\n　]'+ _trans(secName)
        #print re_ex
        p = re.compile(re_ex)
        newStr = p.sub(_addSpace, newStr)
    #######手术名称
    re_orts_operation_name = re.compile(RE_PATTERN_OPERATER_NAME).findall(newStr)

    return re_orts_operation_name     
    
def shuzhedetail(rawText,item):

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
            item['shuzhe']['value']=shuzhelist[i]
            if shuzhelist[i][-1]==u'@':
                item['shuzhe']['confidence']+=-10
        else:
            if item['zhushou']['value']=='NA':
                item['zhushou']['value']=shuzhelist[i]
            else:
                item['zhushou']['value'] += u'，' + shuzhelist[i]
            if shuzhelist[i][-1]==u'@':
                item['zhushou']['confidence']+=-10
    return item    

#抽取肝硬化    
def extractcirrhosis(text,item):
    RE_PATTERN_CIRRHOSIS_NAME = u'[，,。： ][^，,。： ]*肝[^ 。]*硬化[^，,。: ]*[，。, ]'
    pattern_negative=u'无'
    if re.search(RE_PATTERN_CIRRHOSIS_NAME,text):
        linecirr=re.search(RE_PATTERN_CIRRHOSIS_NAME,text).group(0)
        if linecirr[0]==u'：':
            pattern = u'[^，,。：]*肝[^ 。]*硬化[^，,。: ]*'
            linecirr = re.search(pattern,linecirr).group(0)
        else:
            linecirr=linecirr[1:-1]
        if re.search(pattern_negative,linecirr):
            item['ganyinghua']['value']=u'否'
        else:
            item['ganyinghua']['value']=u'是'
        item['ganyinghua']['originalText']=linecirr
    return item

#抽取肿瘤数量（准备和抽提肿瘤信息相结合）    
def extracttumorcount(text,item):
    RE_PATTERN_tumor_count = u'肿瘤[2-9二三四五六七八九]*枚'
    if re.search(RE_PATTERN_tumor_count,text):
        item['zhongliushuliang']['originalText']=re.search(RE_PATTERN_tumor_count,text).group(0)
        line=''
        for i in range(len(item['zhongliushuliang']['originalText'][2:-1])):
            line+=count_cn2arab[item['zhongliushuliang']['originalText'][2:-1][i]]
        item['zhongliushuliang']['value']=line
    return item
    
#抽取肿瘤信息（未完成）    
def extracttumorinfo(text,item):
    RE_PATTERN_tumor_info = u'病人安返病房.*|术毕送移植监护室.*送病理'
    pattern=u'肿瘤.*|血管瘤.*|胆囊癌.*|囊肿.*|肿块.*|肿物.*'
    pattern_size=u'\d.\d[×X*]\d.\d[×X*]\d.\dcm'
    line2,count='',0
    if re.search(RE_PATTERN_tumor_info,text):
        line=re.search(RE_PATTERN_tumor_info,text).group(0)
        if re.search(pattern,line):
            line=re.search(pattern,line).group(0)
        item['zhongliu']['originalText']=line
        if re.search(u'1枚',line):
            line2=line.split(u'1枚')
        if re.search(u'一枚',line):
            line2=line.split(u'一枚')
        if line2=='':
            line2,count=line,1
        for i in line2:
            part={
            'zhongliuxinxi':{'displayname':u'肿瘤信息','value':u'1枚位于肝右叶V段，大小约3.0×2.5×2.5cm，其旁子灶1枚，直径1.0cm，肿瘤界清，包膜完整，','originalText':u'1枚位于肝右叶V段，大小约3.0×2.5×2.5cm，其旁子灶1枚，直径1.0cm，肿瘤界清，包膜完整，','confidence':100},
            'weizhi':{'displayname':u'位置','value':u'NA','originalText':u'肝右叶V段','confidence':100},
            'zhongliudaxiao':{'displayname':u'肿瘤大小','value':u'NA','originalText':u'3.0×2.5×2.5cm','confidence':100},
            'zizaoshuliang':{'displayname':u'子灶数量','value':u'1','originalText':u'子灶1枚','confidence':100}
            }
            if count!=0:
                part['zhongliuxinxi']['value']=i
                for buwei in pattern_buwei:
                    if re.search(buwei,i):
                        part['weizhi']['value']=re.search(buwei,i).group(0)
                if re.search(pattern_size,i):
                    part['zhongliudaxiao']['value']=re.search(pattern_size,i).group(0)[:-2]
                item['zhongliu']['value'].append(part)
            count+=1
    #for i in item['zhongliu']['value']:
    #    print i['zhongliuxinxi']['value']
    return item

    
def process_operation(text):
    #每个肿瘤信息的字典
    part={
    'zhongliuxinxi':{'displayname':u'肿瘤信息','value':u'1枚位于肝右叶V段，大小约3.0×2.5×2.5cm，其旁子灶1枚，直径1.0cm，肿瘤界清，包膜完整，','originalText':u'1枚位于肝右叶V段，大小约3.0×2.5×2.5cm，其旁子灶1枚，直径1.0cm，肿瘤界清，包膜完整，','confidence':100},
    'weizhi':{'displayname':u'位置','value':u'肝右叶V段','originalText':u'肝右叶V段','confidence':100},
    'zhongliudaxiao':{'displayname':u'肿瘤大小','value':u'3.0*2.5*2.5','originalText':u'3.0×2.5×2.5cm','confidence':100},
    'zizaoshuliang':{'displayname':u'子灶数量','value':u'1','originalText':u'子灶1枚','confidence':100}
    }
    #每个病人的字典
    item={
    'id':u'1',
    'rawtext':text,
    'shoushumingcheng':{'displayname':u'手术名称','value':'','originalText':[],'confidence':[]},
    'shoushuleixing':{'displayname':u'手术类型','value':[],'originalText':[],'confidence':[]},
    'shoushubuwei':{'displayname':u'手术部位','value':[],'originalText':[],'confidence':[]},
    #'kexindu':{'displayname':u'可信度','value':[],'originalText':[]},
    'shuzhe':{'displayname':u'术者姓名','value':'NA','originalText':[],'confidence':100},
    'zhushou':{'displayname':u'助手姓名','value':'NA','originalText':[],'confidence':100},
    'ganyinghua':{'displayname':u'肝硬化','value':u'NA','originalText':'NA','confidence':100},
    'zhongliushuliang':{'displayname':u'患者；肿瘤，数量','value':u'1','originalText':u'NA','confidence':100},
    'zhongliu':{'displayname':u'肿瘤','value':[],'originalText':u'肿瘤3枚，1枚位于肝右叶V段，大小约3.0×2.5×2.5cm，其旁子灶1枚，直径1.0cm，肿瘤界清，包膜完整，另1枚位于左内叶，直径1.2cm，界清，无明显包膜。','confidence':100}
    }
    rlt_rawtext = extractOperationName(text)[0]
    ort_rawtext = extractOperaterName(text)[0]
    item = shuzhedetail(ort_rawtext,item)
    item = extractcirrhosis(text,item)
    item = extracttumorcount(text,item)
    item = extracttumorinfo(text,item)
    #print item['ganyinghua']['value']
    #item['shoushumingcheng']['value']=rlt
    mingchengtypeandpart=type(rlt_rawtext).split(u'\t')
    item['shoushumingcheng']['value']=mingchengtypeandpart[0].split(u'：')[1].split(u'+')
    item['shoushumingcheng']['originalText']=item['shoushumingcheng']['value']
    typeandpart=mingchengtypeandpart[1].split(u'||')

    for i in typeandpart:
        buwei=i.split(u':')[0]
        leixing=i.split(u':')[1].split(u'@')[0]
        flag=i.split(u':')[1].split(u'@')[1]
        flag_trans=confident_level[flag]
        item['shoushuleixing']['value'].append(leixing)
        item['shoushuleixing']['originalText'].append(leixing)
        item['shoushubuwei']['value'].append(buwei)
        item['shoushubuwei']['originalText'].append(buwei)
        #item['kexindu']['value'].append(flag_trans)
        #item['kexindu']['originalText'].append(flag)
    
    return item

def main():
    #测试的文本
    text = u' 手术日期：2014-3-7 手术名称：特殊肝段切除术（V、IV段）+胆囊切除术 术前诊断：原发性肝癌 术中诊断：原发性肝癌 麻醉方法：全身麻醉+连续硬膜外麻醉 麻醉医师：葛宁花 手术者及助手姓名：叶青海教授 高强 何梦江 张博  手术经过：（包括：手术经过、术中出现的情况、处理等）    麻醉成功后，患者平卧位，术野皮肤常规消毒铺巾，右侧肋缘下弧形切口逐层切开进腹。探查：腹腔无腹水，胃、肠、胰、脾及盆腔脏器无异常，胆囊肿大，壁厚，肝门淋巴结无肿大，门静脉主干及左右分支内无癌栓。重度肝硬化，硬化结节0.5-0.8cm，无腹水，肿瘤3枚，1枚位于肝右叶V段，大小约3.0×2.5×2.5cm，其旁子灶1枚，直径1.0cm，肿瘤界清，包膜完整，另1枚位于左内叶，直径1.2cm，界清，无明显包膜。术中诊断为原发性肝癌，遂决定行特殊肝段切除术（V、IV段）+胆囊切除术。 上肝拉钩，切断肝圆韧带，断端结扎＋缝扎，切断肝镰状韧带，离断右三角韧带，部分冠状韧带、肝肾韧带韧带。解剖肝十二指肠韧带，距胆总管0.5cm切断胆囊管，断端予以结扎+缝扎，于其后上方胆囊三角切断胆囊动脉，断端予以双重结扎，游离胆囊床，顺行切除胆囊。距肿瘤边缘2.0cm电刀标记预切线，两侧缝扎牵引线。沿切线血管钳法分离肝组织，断面所遇一切管道均予切断、结扎必要时缝扎，逐渐深入直至将肿瘤及部分肝右叶完整切除。缝扎肝断面出血点，冲洗，检查肝断面无胆漏，涂抹生物胶水，覆盖止血材料。同法切除左内叶肿瘤。清理腹腔无活动性出血，敷料器械完整无缺少，于右膈下放置乳胶管引流一枚于腹壁另口引出，逐层关腹术终。   手术顺利踔谐鲅?00ml，术中无输血，术中肝门阻断1次，9分钟，病人安返病房，切除组织送病理检查。 胆囊肿大，壁厚，重度肝硬化，硬化结节0.5-0.8cm，无腹水，肿瘤3枚，1枚位于肝右叶V段，大小约3.0×2.5×2.5cm，其旁子灶1枚，直径1.0cm，肿瘤界清，包膜完整，另1枚位于左内叶，直径1.2cm，界清，无明显包膜，肝门淋巴结无肿大，门脉主干及左、右分支无癌栓。术中顺利，出血100ml，未输血，阻断肝门1次，9分钟。'
    text = u'姓名：孙志海 性别：男 科别：病区：十六病区 床位号：19 住院号：603930 手术日期：2013-12-03   手术名称：同种异体原位肝移植术 术前诊断：原发性肝癌综合治疗后　　　　 术中诊断：原发性肝癌综合治疗后 麻醉方法：全麻  麻醉医师：详见手术记录单 手术医师：樊嘉 周俭 史颖弘　王征　施国明　杨欣荣　丁振斌　付修涛　王智超 手术经过：脑死亡病人，常规消毒铺巾，腹部大“十”字切口，逐层进腹，钝性分离腹主动脉，套二道7＃丝线，远端结扎封闭，近端剪开1/3圆周破口，插入导管至膈肌上主动脉水平并充满35ml气囊，局部7＃丝线固定2道。迅速从导管内快速灌注UW液（100毫升/min），共2000毫升。同法分离下腔静脉并插入引流导管。找出肠系膜上静脉，插入门静脉灌流管约2cm，从导管内快速灌注UW液（100毫升/min），共2000毫升。在紧贴十二指肠上方处，找出胆总管并剪断，从破口处用林格氏液体冲洗，直至胆总管端无胆汁样液体流出。冲洗的同时，大量冰屑覆盖肝脏表面。钝性分离肝下下腔静脉，在左肾静脉水平稍上方剪断，钝性或锐性分离肝周韧带。沿胃小弯从肝十二指肠韧带处剪开小网膜至贲门部；剪开胃结肠韧带，左侧至脾门处，右侧至幽门处。剪开膈肌，近右心房处剪断膈上下腔静脉。剪断胸主动脉，紧贴脊柱上方，向腹部方向剪开胸主动脉后方之疏松组织至腹腔干水平，同法提起腹主动脉，紧贴脊柱上方，向上剪开腹主动脉后方之疏松组织至腹腔干水平。在胰腺体颈交界处剪断胰腺；钝性分离kochen切口腹膜，游离十二指肠及十二指肠与胰腺钝性粘连；至此，供肝游离基本完毕，主刀者手托肝脏，助手剪开肝脏后方之疏松组织，将整个肝脏连同十二指肠韧带、腹腔干、肝总动脉及部分胰腺组织一并切取。迅速置入1000毫升UW保存液中，3道包扎袋包扎后置入冷冻冰箱中保存。 供肝修整：逐层打开肝脏包扎袋，置无菌手术台。取肝左右叶各－1厘米3肝脏组织送病理检查。先钝性分离肝上、肝下下腔静脉及肝脏周围结缔组织，遇有管道结扎加缝扎，剪除多余膈肌及结缔组织。沿肠系膜上静脉、脾静脉钝性分离，剪开周围胰腺组织，在门静脉起始处剪断；沿腹腔干钝性分离，从腹腔干开始分离胃左动脉、脾动脉，肠系膜上动脉分出肝总动脉、肝固有动脉，胃十二指肠动脉，注射肝素水见肝动脉通畅无渗漏。切除胆囊。门静脉及下腔静脉均注水及打气，查无渗漏。修整髂总及髂内外动脉，剪除多余结缔组织，小分支动脉结扎或缝扎，查无渗漏后保存备用。 受体：麻醉成功后，平卧位，术野皮肤常规消毒铺巾，留置导尿。取双侧肋缘下切口逐层进腹。探查：腹腔重度粘连，腹水1300ml，重度肝硬化，肿瘤四枚，最大一枚位于IVb段近V段处，约5×5×4cm，多结节融合型，界清，有包膜，包膜完整，切面50%坏死，一枚位于IVa与IVb段交界处，约3×3×3cm，单结节型，界清，包膜完整，一枚位于肝右叶V段与VIII段交界处，直径1cm，界清，无包膜，另一枚位于IVa段，直径1cm，界清，薨ぃ蚊帕馨徒嵛拗状螅怕鲋鞲杉白蟆⒂曳种薨┧ā?BR>　　上肝拉钩，解剖分离第一肝门，分离肝左、肝右动脉，予以离断后结扎。分离胆总管，在胆囊管开口上方离断肝总管。细致游离门静脉主干至骨骼化。离断肝周韧带，分离IVC后组织，逐支离断侧枝血管，游离整段肝后IVC后壁。解剖游离肝上和肝下下腔静脉。门静脉内化疗导管予以取出。　　待供肝修剪完毕，确认供肝质量满意后，钳夹离断门静脉主干、肝上及肝下下腔静脉，离断肝脏与周围组织粘连，移除病肝。创面严密止血、修整腔静脉吻合口。经门静脉灌注含白蛋白的冷乳酸林格式液（25g/500ml），分别以4-0 血管缝线端端吻合供肝的肝上、肝下下腔静脉和受体的肝上、肝下下腔静脉。以5-0 血管缝线端端吻合门静脉，留置1cm growth factor。开放门静脉，收紧缝线，肝脏迅速均匀充盈，顺次开放肝上、肝下下腔静脉吻合口，检查各吻合口通畅，无狭窄与渗漏。分离、修剪肝总动脉，行受体肝总动脉-胃十二指肠动脉patch与供体肝总动脉端端吻合，动脉内径约0.3cm，开放血流见动脉远心端搏动良好。?┨宓ü芸诳?mm，受体胆管宽13mm，以6-0 Prolen行供、受体胆管前、后壁连续缝合。于左、右膈下及肝门分别放置引流1根，另戳创引出腹外，清点器械纱布无误后关腹。术毕送移植监护室。　　病肝重660g。书页状切开病肝，重度肝硬化，肿瘤四枚，最大一枚位于IVb段近V段处，约5×5×4cm，多结节融合型，界清，有包膜，包膜完整，切面50%坏死，一枚位于IVa与IVb段交界处，约3×3×3cm，单结节型，界清，包膜完整，一枚位于肝右叶V段与VIII段交界处，直径1cm，界清，无包膜，另一枚位于IVa段，直径1cm，界清，无包膜，肝门淋巴结无肿大，门脉主干及左、右分支无癌栓。术中共计出血出血4000ml，输RBC悬液15u，血浆1000ml，Plt单采10U，PPSB 800IU，Fib 2g。给家属过目后送病理。'
    text = u'手术日期：2014-6-10 手术名称：肝中叶特殊肝段切除术（III段，IVb段） 术前诊断：肝中叶原发性肝癌术中诊断：肝中叶原发性肝癌 麻醉方法：全身麻醉+连续硬膜外麻醉 麻醉医师：庄小凤 手术者及助手姓名：叶青海 杨国欢 马源  手术经过：（包括：手术经过、术中出现的情况、处理等）    麻醉成功后，患者取右侧抬高45度卧位，术野皮肤常规消毒铺巾，右侧肋缘下弧形切口逐层切开进腹。探查腹腔无腹水，胃、肠、胆囊、胰、脾及盆腔脏器无异常，肝门淋巴结无肿大，门静脉主干无栓子。肝硬化中度，硬化结节0.3cm，肿瘤位于左内外叶交界处，直径约2.5cm，术中诊断为肝中叶原发性肝癌，遂决定行肝中叶特殊肝段切除术（III段、IVb段）。 上肝拉钩，切断肝圆韧带，断端结扎＋缝扎，切断肝镰状韧带，充分显露肿瘤，沿肿瘤边缘2cm电刀标记预切线，两侧缝扎牵引线。沿切线血管钳法分离肝组织，断面所遇一切管道均予切断、钳夹、结扎必要时缝扎，逐渐深入直至将肿瘤及部分肝中叶（III段、IVb段）完整切除。 缝扎肝断面出血点，冲洗，检查肝断面无胆漏，涂抹止血纱布及生物胶水。清理腹腔无活动性出血，敷料器械完整无缺少，于右膈下放置乳胶管引流一枚于腹壁另口引出，逐层关腹术终。   手术顺利，术中出血50ml，术中无输血，术中肝门阻断1次，历时15分钟，病人安返病房，切除组织送病理检查。 肿瘤位于左内外叶交界处，大小2.5*2.3*2.0cm，界清，包膜完整。肝硬化中度，硬化结节0.3cm。门脉主干无癌栓,肝门未见肿大淋巴结，阻断肝门1次，历时15分钟。 '
    item = process_operation(text)
    the_Enzyme = u'手术报告'
    ###模板位置
    mytemplate = Template(filename='./operation_name.mako')
    #mytemplate = Template(filename='./operation_entryRelationship_new.mako')
    write1=open('test1.xml','w')
    write1.write(mytemplate.render(item=item,the_Enzyme=the_Enzyme,Xml_Creat_Time=time.strftime(ISOTIMEFORMAT,time.localtime())).encode('utf8'))

# -----------------------------------
# Program Running
# -----------------------------------
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write(">_< User interrupt me, see you! ^.^\n")
        sys.exit(0)
