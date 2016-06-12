# --*-- coding: utf8 --*--
    <section>
        <templateId root="2.16.840.1.113883.2.23.11.3.2.54"/>
        <code code="11366-2" displayname="手术报告" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC"/>
        	<id root=${item['id']} extension="002"/>
        	<title>手术记录</title>
            <text>
                <content ID="raw_text">${item['rawtext']}</content>
                <content ID="level_one">
        	 <table border="1" width="100%" id=${the_Enzyme} type="PathologyReport">
                <thead>
                    <tr>
                        <th>${Xml_Creat_Time}</th>
                        <th>${the_Enzyme}</th>
                    </tr>
                </thead>
                <tbody>
                %for i in range(len(item['shoushumingcheng']['value'])):
                    <tr>
                    	<td>标本</td>
                        <td>${item['shoushumingcheng']['displayname']}</td>
                        <td>${item['shoushumingcheng']['value'][i]}</td>
                        <td>mapping</td>
                    </tr>
                    <tr>
                        <td>标本</td>
                        <td>${item['shoushuleixing']['displayname']}</td>
                        <td>${item['shoushuleixing']['value'][i]}</td>
                        <td>mapping</td>
                    </tr>
                    <tr>
                        <td>标本</td>
                        <td>${item['shoushubuwei']['displayname']}</td>
                        <td>${item['shoushubuwei']['value'][i]}</td>
                        <td>mapping</td>
                    </tr>
                %endfor
                </tbody>
        	</table>
        </text>
        <entry>
			<title>detailed information</title>

        	<act classCode='ACT' moodCode='EVN'>
				<entryRelationship typeCode="COMP">
                    <observation classCode="OBS" moodCode="EVN">
                        <code code="entity,feature,value" displayname=${item['ganyinghua']['displayname']}/>
                         <value type="boolean" code="true" displayname=${item['ganyinghua']['value']} codeSystem="'codeSystem'" codeSystemName="'codeSystemName' " codeConfidence=${item['ganyinghua']['confidence']}/> <!-- 0..100 100 highest confidence-->
                        <originalText>
                            <reference value="">${item['ganyinghua']['originalText']}</reference>
                        </originalText>
                    </observation>
                </entryRelationship>
				<entryRelationship typeCode="COMP">
                    <observation classCode="OBS" moodCode="EVN">
                        <code code=",,value" displayname=${item['zhongliushuliang']['displayname']}/>
                         <value type="PQ" value=${item['zhongliushuliang']['value']} unit="枚" codeConfidence=${item['zhongliushuliang']['confidence']}/> <!-- 0..100 100 highest confidence-->
                        <originalText>
                            <reference value="">${item['zhongliushuliang']['originalText']}</reference>
                        </originalText>
                    </observation>
                </entryRelationship>
			%for part in item['zhongliu']['value']:
				<entryRelationship>
				<observation classCode="OBS" moodCode="EVN">
				<code code=",,value" displayname=${part['zhongliuxinxi']['displayname']}/>
				<originalText>
					<reference value="">${part['zhongliuxinxi']['value']}</reference>
				</originalText>
				</entryRelationship>
				<entryrelationship>
					<observation classCode="OBS" moodCode="EVN">
					<code code="" displayname=${part['weizhi']['displayname']}/>
					<value type="CE" displayname=${part['weizhi']['value']}>
					</observation>
				</entryrelationship>
				<entryrelationship>
					<observation classCode="OBS" moodCode="EVN">
					<code code="" displayname=${part['zhongliudaxiao']['displayname']}/>
					<value type="CE" displayname=${part['zhongliudaxiao']['value']} unit="cm">
					</observation>
				</entryrelationship>
				<entryrelationship>
					<observation classCode="OBS" moodCode="EVN">
					<code code="" displayname=${part['zizaoshuliang']['displayname']}/>
					<value type="PQ" displayname=${part['zizaoshuliang']['value']} unit="个">
					</observation>
				</entryrelationship>
			%endfor
			</act>
		</entry>
		 %for j in range(len(item['shoushumingcheng']['value'])):
		<entry>
			<procedure classCode="FAULT" moodCode="EVN">
                <!--此段信息用于手术记录-->
                <effectiveTime value="201403070000"/>
                <text>${item['shoushumingcheng']['value'][j]}</text>
                <targetSiteCode code="E00XXX,EXXX;;" displayName=${item['shoushubuwei']['value'][j]} codeSystem="" codeSystemName=""/>
                <!--术者医师信息--> 
                  <performer> 
                        <assignedEntity> 
                          <!--术者工号--> 
                          <id /> 
                          <assignedPerson> 
                            <!--术者姓名--> 
                            <name codeConfidence=${item['shuzhe']['confidence']}>${item['shuzhe']['value']}</name> 
                          </assignedPerson> 
                        </assignedEntity>               
                    </performer> 
                <participant typeCode="FAULT">
                    <ParticipantRole classCode="FAULT">
                      <!--助手工号--> 
                      <id /> 
                      <playingEntity> 
                        <!--助手姓名--> 
                        <name codeConfidence=${item['zhushou']['confidence']}>${item['zhushou']['value']}</name> 
                      </playingEntity> 
                    </ParticipantRole>
                </participant>
				<entryRelationship typeCode="COMP">
					<observation classCode="OBS" moodCode="EVN">
						<code code="entity,feature,value" displayname="标本,${item['shoushuleixing']['displayname']},value"/>
						<value type="CD" code="" displayname=${item['shoushuleixing']['value'][j]} codeSystem="'codeSystem'" codeSystemName="'codeSystemName'"/>
						<originalText>
							<reference value="">${item['shoushuleixing']['originalText'][j]}</reference>
						</originalText>
					</observation>
				</entryRelationship>
				<entryRelationship typeCode="COMP">
					<observation classCode="OBS" moodCode="EVN">
						<code code="entity,feature,value" displayname="标本,${item['shoushubuwei']['displayname']},value"/>
						<value type="CD" code="" displayname=${item['shoushubuwei']['value'][j]} codeSystem="'codeSystem'" codeSystemName="'codeSystemName'"/>
						<originalText>
							<reference value="">${item['shoushubuwei']['value'][j]}</reference>
						</originalText>
					</observation>
				</entryRelationship>  
			</procedure>
        </entry>
        %endfor	
     </section>