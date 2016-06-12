# --*-- coding: utf8 --*--
    <component>
        <section>
            <templateId root="2.16.840.1.113883.10.20.22.2.7.1" assigningAuthorityName="CCDA Procedures Section (Entries Required)" />
            <id root="b44edfed-9333-47f7-a6a0-baa23f439283" />
            <code code="47519-4" displayName="HISTORY OF PROCEDURES" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" />
            <title>Procedures and Surgical/Medical History</title>
            <text>
                <content ID="raw_text">${item['rawtext']}</content>
            </text>
            %for j in range(len(item['shoushumingcheng']['value'])):
            <entry typeCode="DRIV">
                <procedure classCode="PROC" moodCode="EVN">
                <templateId root="2.16.840.1.113883.10.20.22.4.14" assigningAuthorityName="CCDA Procedure Activity Procedure" />
                <id root="2.16.840.1.113883.3.140.1.0.6.10.17.2" extension="95" />
                <code code="81000" displayName="Urinalysis" codeSystem="2.16.840.1.113883.6.12" codeSystemName="CPT-4">
                    <originalText>
                        <reference value="#procedureDescriptionID1" />${item['shoushumingcheng']['value'][j]}</reference>
                    </originalText>
                </code>
                    <entryRelationship typeCode="SUBJ" inversionInd="false">
                        <observation classCode="OBS" moodCode="EVN" negationInd="false">
                            <templateId root="2.16.840.1.113883.10.20.22.4.4" assigningAuthorityName="CCDA Problem Observation" />
                            <id root="1b3afe34-965a-43c8-b036-2268e20d37e4" />
                            <code code="entity,feature,value" displayName="标本,${item['shoushuleixing']['displayname']},value" codeSystem="2.16.840.1.113883.6.96" codeSystemName="SNOMED CT" />
                            <text>
                                <reference value="#procedureDescription1" />
                            </text>
                            <statusCode code="completed" />
                            <effectiveTime>
                            <low value="20070903" />
                            </effectiveTime>
                            <value code="CD" displayName="${item['shoushuleixing']['value'][j]}" codeSystem="2.16.840.1.113883.6.103" codeSystemName="ICD9CM" xsi:type="CD">
                                <originalText>
                                    <reference value="#procedureDescription1" />${item['shoushuleixing']['originalText'][j]}</reference>
                                </originalText>
                            </value>
                        </observation>
                    </entryRelationship>
                    
                    <entryRelationship typeCode="SUBJ" inversionInd="false">
                        <observation classCode="OBS" moodCode="EVN" negationInd="false">
                            <templateId root="2.16.840.1.113883.10.20.22.4.4" assigningAuthorityName="CCDA Problem Observation" />
                            <id root="1b3afe34-965a-43c8-b036-2268e20d37e4" />
                            <code code="entity,feature,value" displayName="标本,${item['shoushubuwei']['displayname']},value" codeSystem="2.16.840.1.113883.6.96" codeSystemName="SNOMED CT" />
                            <text>
                                <reference value="#procedureDescription1" />
                            </text>
                            <statusCode code="completed" />
                            <effectiveTime>
                            <low value="20070903" />
                            </effectiveTime>
                            <value code="CD" displayName="${item['shoushubuwei']['value'][j]}" codeSystem="2.16.840.1.113883.6.103" codeSystemName="ICD9CM" xsi:type="CD">
                                <originalText>
                                    <reference value="#procedureDescription1" />${item['shoushubuwei']['originalText'][j]}</reference>
                                </originalText>
                            </value>
                        </observation>
                    </entryRelationship>
                </procedure>
            </entry>
            %endfor
        </section>
    </component>