import os
from xml.dom.minidom import Document
from xml.dom.minidom import parse
import xml.dom.minidom
import numpy as np
import csv
import cv2
import string

def WriterXMLFiles(filename, imagename, path, box_list, label_list, diff_list, w, h, d):
    doc = Document() 
    # dict_box[filename]=json_dict[filename]
    # doc = xml.dom.minidom.Document()
    root = doc.createElement('annotation')
    doc.appendChild(root)

    foldername = doc.createElement("folder")
    foldername.appendChild(doc.createTextNode("JPEGImages"))
    root.appendChild(foldername)

    nodeFilename = doc.createElement('filename')
    nodeFilename.appendChild(doc.createTextNode(imagename))
    root.appendChild(nodeFilename)

    pathname = doc.createElement("path")
    pathname.appendChild(doc.createTextNode("xxxx"))
    root.appendChild(pathname)

    sourcename=doc.createElement("source")

    databasename = doc.createElement("database")
    databasename.appendChild(doc.createTextNode("Unknown"))
    sourcename.appendChild(databasename)

    annotationname = doc.createElement("annotation")
    annotationname.appendChild(doc.createTextNode("xxx"))
    sourcename.appendChild(annotationname)

    imagename = doc.createElement("image")
    imagename.appendChild(doc.createTextNode("xxx"))
    sourcename.appendChild(imagename)

    flickridname = doc.createElement("flickrid")
    flickridname.appendChild(doc.createTextNode("0"))
    sourcename.appendChild(flickridname)

    root.appendChild(sourcename)

    nodeowner = doc.createElement('owner')
    nodeflickrid = doc.createElement("flickrid")
    nodeflickrid.appendChild(doc.createTextNode("xxxx"))
    nodeowner.appendChild(nodeflickrid)
    nodeownername = doc.createElement('name')
    nodeownername.appendChild(doc.createTextNode('504'))
    nodeowner.appendChild(nodeownername)
    root.appendChild(nodeowner)

    nodesize = doc.createElement('size')
    nodewidth = doc.createElement('width')
    nodewidth.appendChild(doc.createTextNode(str(w)))
    nodesize.appendChild(nodewidth)
    nodeheight = doc.createElement('height')
    nodeheight.appendChild(doc.createTextNode(str(h)))
    nodesize.appendChild(nodeheight)
    nodedepth = doc.createElement('depth')
    nodedepth.appendChild(doc.createTextNode(str(d)))
    nodesize.appendChild(nodedepth)
    root.appendChild(nodesize)

    segname = doc.createElement("segmented")
    segname.appendChild(doc.createTextNode("0"))
    root.appendChild(segname)

    for (box, label, difficulty) in zip(box_list, label_list, diff_list):

        nodeobject = doc.createElement('object')
        nodename = doc.createElement('name')
        nodename.appendChild(doc.createTextNode(str(label)))
        nodeobject.appendChild(nodename)
        nodename = doc.createElement('pose')
        nodename.appendChild(doc.createTextNode('Unknown'))
        nodeobject.appendChild(nodename)
        nodename = doc.createElement('truncated')
        nodename.appendChild(doc.createTextNode('1'))
        nodeobject.appendChild(nodename)
        nodename = doc.createElement('difficulty')
        nodename.appendChild(doc.createTextNode(str(difficulty)))
        nodeobject.appendChild(nodename)
        nodebndbox = doc.createElement('bndbox')
        nodex1 = doc.createElement('x1')
        nodex1.appendChild(doc.createTextNode(str(box[0])))
        nodebndbox.appendChild(nodex1)
        nodey1 = doc.createElement('y1')
        nodey1.appendChild(doc.createTextNode(str(box[1])))
        nodebndbox.appendChild(nodey1)
        nodex2 = doc.createElement('x2')
        nodex2.appendChild(doc.createTextNode(str(box[2])))
        nodebndbox.appendChild(nodex2)
        nodey2 = doc.createElement('y2')
        nodey2.appendChild(doc.createTextNode(str(box[3])))
        nodebndbox.appendChild(nodey2)
        nodex3 = doc.createElement('x3')
        nodex3.appendChild(doc.createTextNode(str(box[4])))
        nodebndbox.appendChild(nodex3)
        nodey3 = doc.createElement('y3')
        nodey3.appendChild(doc.createTextNode(str(box[5])))
        nodebndbox.appendChild(nodey3)
        nodex4 = doc.createElement('x4')
        nodex4.appendChild(doc.createTextNode(str(box[6])))
        nodebndbox.appendChild(nodex4)
        nodey4 = doc.createElement('y4')
        nodey4.appendChild(doc.createTextNode(str(box[7])))
        nodebndbox.appendChild(nodey4)

        # ang = doc.createElement('angle')
        # ang.appendChild(doc.createTextNode(str(angle)))
        # nodebndbox.appendChild(ang)
        nodeobject.appendChild(nodebndbox)
        root.appendChild(nodeobject)
    fp = open(path + filename, 'w')
    # fp.write(doc.toprettyxml(indent='\t', encoding='utf-8'))
    # doc.writexml(fp, indent='\t', addindent='\t', newl='\n')
    doc.writexml(fp, addindent='\t', newl='\n')
    fp.close()


def load_annoataion(p):
    '''
    load annotation from the text file
    :param p:
    :return:
    '''
    text_polys = []
    text_tags = []
    text_diff = []
    if not os.path.exists(p):
        return np.array(text_polys, dtype=np.float32)
    with open(p, 'r') as f:
        for line in f.readlines()[:]:
            label = 'txt'
            # strip BOM. \ufeff for python3,  \xef\xbb\bf for python2
            #line = [i.strip('\ufeff').strip('\xef\xbb\xbf') for i in line]
            print(line)
            line = line.replace('.0', '').replace('\n','')
            x1, y1, x2, y2, x3, y3, x4, y4 ,label, difficulty= line.split(' ')[0:10]
            #print(label)
            text_polys.append([x1, y1, x2, y2, x3, y3, x4, y4])
            text_tags.append(label)
            text_diff.append(difficulty)

        return np.array(text_polys, dtype=np.int32), np.array(text_tags, dtype=np.str), np.array(text_diff, dtype=np.str)

if __name__ == "__main__":
    txt_path = './txt/'
    xml_path = './Annotations/'
    img_path = './8bit_image/'
    print(os.path.exists(txt_path))
    txts = os.listdir(txt_path)
    for count, t in enumerate(txts):
        boxes, labels, difficulty = load_annoataion(os.path.join(txt_path, t))
        xml_name = t.replace('.txt', '.xml')
        img_name = t.replace('.txt', '')
        print(img_name)
        img = cv2.imread(os.path.join(img_path, img_name))
        h, w, d = img.shape
        #print(xml_name, xml_path, boxes, labels, w, h, d)
        WriterXMLFiles(xml_name, img_name, xml_path, boxes, labels, difficulty, w, h, d)

        if count % 1000 == 0:
            print(count)
