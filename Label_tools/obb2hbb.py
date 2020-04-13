# coding=utf-8
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import os
 
 
# 批量修改整个文件夹所有的xml文件
def change_all_xml(xml_path):
    filelist = os.listdir(xml_path)
    #print(filelist)
    # 打开xml文档
    cnt=0
    for xmlfile in filelist:
        doc = ET.parse(xml_path + xmlfile)
        #print(xmlfile)
        root = doc.getroot()
        sub0 = root.findall('object')  # 找到filename标签，
        #print(sub0)
        for subs in sub0:
            #if subs.find('difficulty'):
                
                #a=subs.find('difficulty')
                #a.text=0
            #else:
                #model=Element('difficulty')
                #model.text=0
                #subs.append(model)          
            sub=subs.find('bndbox')

            sub1 = sub.find('x1')
            sub.remove(sub1)   
            sub2 = sub.find('x2')
            sub.remove(sub2)
            sub3 = sub.find('x3')
            sub.remove(sub3)
            sub4 = sub.find('x4')
            sub.remove(sub4)
            suy1 = sub.find('y1')
            sub.remove(suy1)
            suy2 = sub.find('y2')
            sub.remove(suy2)
            suy3 = sub.find('y3')
            sub.remove(suy3)
            suy4 = sub.find('y4')
            sub.remove(suy4)
            xmax,ymax=str(max(int(sub1.text),int(sub2.text),int(sub3.text),int(sub4.text))),str(max(int(suy1.text),int(suy2.text),int(suy3.text),int(suy4.text)))
            xmin,ymin=str(min(int(sub1.text),int(sub2.text),int(sub3.text),int(sub4.text))),str(min(int(suy1.text),int(suy2.text),int(suy3.text),int(suy4.text)))
            xmi=Element('xmin')
            xmi.text=xmin
            xma=Element('xmax')
            xma.text=xmax
            ymi=Element('ymin')
            ymi.text=ymin
            yma=Element('ymax')
            yma.text=ymax
            for i in (xmi,ymi,xma,yma):
                sub.append(i)
        doc.write(xml_path + xmlfile)  # 保存修改
        cnt+=1
        print(cnt)
xml_path ='./Annotation/'
change_all_xml(xml_path)

