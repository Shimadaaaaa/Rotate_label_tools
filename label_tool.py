"""
功能介绍：
修改 path = '代标注图片所在路径'  save_txt_path = '标签文件存储路径' 
    save_image_path = '存储标记照片所在路径'

左键画点，四个点生成一个旋转标注框， 右键删除上一个框   
D键下一张，A键上一张，ESC退出  

生成标签类型为DOTA数据集

"""
import cv2
import os
import numpy as np

def click_event(event, x, y, flags, param):
    global cnt, points, bboxes, txt_path, image_path
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=2)
        points.append([x,y])
        cnt+=1
        if(cnt == 4):
            temp = np.array(points)
            print(temp)
            rect = cv2.minAreaRect(temp)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            print(box)	
            cv2.drawContours(img, [box], 0, (255, 255, 0), 3)
            box = box.tolist()
            save_word = '{}.0 {}.0 {}.0 {}.0 {}.0 {}.0 {}.0 {}.0 ship 0'.format(box[0][0],
                box[0][1], box[1][0], box[1][1], box[2][0], box[2][1], box[3][0], box[3][1])
            bboxes.append(save_word)
            cnt = 0
            points=[]
            print(bboxes)
        cv2.imshow('image', img)
    if event == cv2.EVENT_RBUTTONDOWN:
        delet_bboxes(txt_path, image_path)
        cv2.imshow('image', img)

def show_img(img):
    global points, cnt, bboxes
    cnt = 0
    bboxes = []
    points = []
    cv2.namedWindow("image",0)
    cv2.resizeWindow("image", 640, 640)
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    k = cv2.waitKey()
    if k == 100 or k == 27 or k == 97:
        cv2.destroyAllWindows()
        return bboxes, k

def write_bboxes(filepath, bboxes):
    if bboxes:
        with open(filepath, 'a+') as f:
            for bbox in bboxes:
                line = repr(bbox).replace("\'","") + '\n'
                f.write(line)
    # elif os.path.exists(filepath):
    #     os.remove(filepath)
    bboxes = []

def delet_bboxes(filepath, image_path):
    global img, bboxes
    if bboxes:
        write_bboxes(filepath, bboxes)
        bboxes = []
    if os.path.exists(filepath):
        file_old = open(filepath, 'r')
        lines = [i for i in file_old]
        del lines[-1]
        file_old.close()
        if len(lines)>0:
            # 再覆盖写入
            file_new = open(filepath, 'w')
            file_new .write(''.join(lines))
            file_new .close()
            img = cv2.imread(image_path)
            img = reload_bboxes(filepath, img)
        else:
            os.remove(filepath)
            img = cv2.imread(image_path)
            img = reload_bboxes(filepath, img)
        
        print('delete success')
    else:
        pass


def reload_bboxes(filepath, img):
    if os.path.exists(filepath):
        f=open(filepath)
        line=f.readline()
        while line :
            line=line.replace('.0','')
            line=np.array(line.split(' ')[:8])
            box=line.reshape((4,2))
            box = np.int0(box)
            cv2.drawContours(img, [box], 0, (255, 255, 0), 3)
            print(box)
            line=f.readline()
        return img
    return img
        

if __name__ == "__main__":
    path = './demo/'
    save_txt_path = 'txt/'
    save_image_path = 'labeled_image/'
    work_progress = 'progress.txt'
    with open(work_progress, 'r+') as p:
        line = p.readline()
        if line:
            i = int(line)
            print(i)
        else :
            i = 0
        imagelist = os.listdir(path)
        while (i < (len(imagelist)) and i >= 0):
            imgname = imagelist[i] 
            if(imgname.endswith(".bmp")):
                print(imgname)
                image_path = path+'/'+imgname
                img = cv2.imread(image_path)
                txt_path = (save_txt_path + imgname + '.txt')
                img = reload_bboxes(txt_path, img)
                bboxes, k = show_img(img)
                write_bboxes(txt_path,bboxes)
                cv2.imwrite(save_image_path+imgname, img)
                i+=1
                p.seek(0)
                p.truncate()
                p.write(str(i))
                if k == 97:
                    i -= 2 
                elif k == 27:
                    break
        p.seek(0)
        p.truncate()
        p.write(str(i-1))
