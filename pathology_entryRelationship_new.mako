# --*-- coding: utf8 --*--
    <section>
        <templateId root="2.16.840.1.113883.2.23.11.3.2.54"/>
        <code code="11366-2" displayName="病理报告" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC"/>
        <text >
            <table border="1" width="100%" id="${the_Enzyme}" type="PathologyReport">
                <thead>
                    <tr>
                        <th>${Xml_Creat_Time}</th>
                        <th>${the_Enzyme}</th>
                    </tr>
                </thead>
                %for item_list in item_lists:
                <tbody>
                %for item in item_list:
                    %if item['type'] == 'boolean':
                    <tr>
                        <td>标本</td>
                        <td>${item['norName']}</td>
                        <td>${item['value']['value']}</td>
                        <td>mapping</td>
                    </tr>
                    %elif item['type'] == 'cd':
                    <tr>
                        <td>标本</td>
                        <td>${item['norName']}</td>
                        <td>${item['value']['displayName']}</td>
                        <td>mapping</td>
                    </tr>
                    %endif
                %endfor
                </tbody>
                %endfor
            </table>
        </text>
        <entry>
            <procedure classCode="FAULT" moodCode="EVN">
                <participant typeCode="FAULT">
                    <ParticipantRole classCode="FAULT">
                        <Device classCode="FAULT">
                            <softwareName>${the_Enzyme}</softwareName>
                            <originalText>
                        <reference value="">${item['originalText']['value']}</reference>
                    </originalText>
                        </Device>
                    </ParticipantRole>
                </participant>
            </procedure>
            %for item_list in item_lists:
            <act classCode='ACT' moodCode='EVN'>
            %for item in item_list:
                %if item['type'] == 'boolean':
                <entryRelationship typeCode="COMP">
                    <observation classCode="OBS" moodCode="EVN">
                        <code code="${item['code']['code']['entity']},${item['code']['code']['feature']},${item['code']['code']['value']}" displayName="${item['code']['displayName']['entity']},${item['code']['displayName']['feature']},${item['code']['displayName']['value']}" />
                        <value xsi:type="BL" value="${item['value']['value']}" />
                        <originalText>
                            <reference value="">${item['originalText']['value']}</reference>
                        </originalText>
                    </observation>
                </entryRelationship>
                %elif item['type'] == 'cd':
                <entryRelationship typeCode="COMP">
                    <observation classCode="OBS" moodCode="EVN">
                        <code code="${item['code']['code']['entity']},${item['code']['code']['feature']},${item['code']['code']['value']}" displayName="${item['code']['displayName']['entity']},${item['code']['displayName']['feature']},${item['code']['displayName']['value']}" />
                        <value xsi:type="CD" code="${item['value']['code']}" displayName="${item['value']['displayName']}" codeSystem="${item['value']['codeSystem']}" codeSystemName="${item['value']['codeSystemName']}"/>
                        <originalText>
                            <reference value="">${item['originalText']['value']}</reference>
                        </originalText>
                    </observation>
                </entryRelationship>
                %endif
            %endfor
            </act>
            %endfor
        </entry>
    </section>