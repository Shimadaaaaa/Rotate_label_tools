"""
功能介绍：
修改 img_path = '代标注图片所在路径'  txt_path = '标签文件存储路径' 
    labeled_path = '存储标记照片所在路径' img_format = '图片格式'
    category = ['类别一', '类别二'] （现仅支持两类，可拓展）

左键画点，四个点生成一个旋转标注框， 右键删除上一个框， 滚轮缩放图片   
D键下一张，A键上一张，ESC退出，下方滑条更换类别
work()传参可选择保存带框图片

生成标签类型为DOTA数据集

"""

import cv2
import os
import numpy as np

class Label():
    def __init__(self, img_path, txt_path, labeled_path, img_format, category):
        self.img_path = img_path
        self.txt_path = txt_path
        self.labeled_path = labeled_path
        self.img_format = img_format
        self.category = category
        self.cate_ind = 0
        self.switch = f'left: {self.category[0]}\nright: {self.category[1]}'
        

    def work(self, save = False):
        with open('progress.txt', "r+") as p:
            line = p.readline()
            if line :
                ind = int(line)
                print(ind)
            else :
                ind = 0
            img_list = os.listdir(self.img_path)
            while(ind < len(img_list) and ind >= 0):
                img_name = img_list[ind]
                if img_name.endswith(self.img_format):
                    print(img_name)
                    self.img_true_path = self.img_path + '/' + img_name
                    txt_name = img_name.replace(self.img_format, '.txt')
                    self.txt_true_path = self.txt_path + '/' + txt_name
                    self.img = cv2.imread(self.img_true_path)
                    self.reload_bboxes()
                    k = self.show_img()
                    self.write_bboxes()
                    if save:
                        save_name = img_name.replace(self.img_format, '.jpg')
                        cv2.imwrite(self.labeled_path + '/' + save_name, self.img)
                    ind += 1
                    p.seek(0)
                    p.truncate()
                    p.write(str(ind))
                    if k == 97:
                        ind -= 2
                    elif k == 27:
                        break
            p.seek(0)
            p.truncate()
            if ind > 0:
                p.write(str(ind-1))
            else :
                p.write('0')

    def reload_bboxes(self):
        if os.path.exists(self.txt_true_path):
            f=open(self.txt_true_path)
            line=f.readline()
            while line :
                line=line.replace('.0','')
                cate = line.split(' ')[8]
                line=np.array(line.split(' ')[:8])
                box=line.reshape((4,2))
                box = np.int0(box)
                if cate == self.category[0]:
                    cv2.drawContours(self.img, [box], 0, (255, 255, 0), 3)
                else :
                    cv2.drawContours(self.img, [box], 0, (0, 0, 255), 3)
                line=f.readline()

    def show_img(self):
        self.cnt = 0
        self.bboxes = []
        self.points = []
        cv2.namedWindow("image",0)
        # cv2.resizeWindow("image", 640, 640)
        cv2.setWindowProperty("image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        # cv2.moveWindow("image",20,20)
        cv2.imshow('image', self.img)
        cv2.createTrackbar(self.switch, 'image',0,1,self.nothing)
        cv2.setMouseCallback('image', self.click_event)
        k = cv2.waitKey()
        if k == 100 or k == 27 or k == 97:
            cv2.destroyAllWindows()
            return k
    
    def click_event(self, event, x, y, flags, param):
        cate_ind = cv2.getTrackbarPos(self.switch,'image')
        if event == cv2.EVENT_LBUTTONDOWN:
            xy = "%d,%d" % (x, y)
            cv2.circle(self.img, (x, y), 3, (0, 0, 255), -1)
            cv2.putText(self.img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                        1.0, (0, 0, 0), thickness=2)
            self.points.append([x,y])
            self.cnt+=1
            if(self.cnt == 4):
                temp = np.array(self.points)
                rect = cv2.minAreaRect(temp)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                if cate_ind == 0:	
                    cv2.drawContours(self.img, [box], 0, (255, 255, 0), 3)
                else :
                    cv2.drawContours(self.img, [box], 0, (0, 0, 255), 3)
                box = box.tolist()
                save_word = '{}.0 {}.0 {}.0 {}.0 {}.0 {}.0 {}.0 {}.0 {} 0'.format(box[0][0],
                    box[0][1], box[1][0], box[1][1], box[2][0], box[2][1], box[3][0], box[3][1], category[cate_ind])
                self.bboxes.append(save_word)
                self.cnt = 0
                self.points=[]
            cv2.imshow('image', self.img)
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.delet_bboxes()
            cv2.imshow('image', self.img)

    def write_bboxes(self):
        if self.bboxes:
            with open(self.txt_true_path, 'a+') as f:
                for bbox in self.bboxes:
                    line = repr(bbox).replace("\'","") + '\n'
                    f.write(line)
        self.bboxes = []
        print("write sucess")

    def delet_bboxes(self):
        if self.bboxes:
            self.write_bboxes()
            self.bboxes = []
        if os.path.exists(self.txt_true_path):
            file_old = open(self.txt_true_path, 'r')
            lines = [i for i in file_old]
            del lines[-1]
            file_old.close()
            if len(lines)>0:
                # 再覆盖写入
                file_new = open(self.txt_true_path, 'w')
                file_new .write(''.join(lines))
                file_new .close()
                self.img = cv2.imread(self.img_true_path)
                self.reload_bboxes()
            else:
                os.remove(self.txt_true_path)
                self.img = cv2.imread(self.img_true_path)
                self.reload_bboxes()
            print('delete success')


    def nothing(self,x):
        pass

if __name__ == "__main__":
    img_path = './8bit_image'
    txt_path = './txt'
    labeled_path = './labeled_image'
    img_format = '.png'
    category = ['shp', 'other']
    data = Label(img_path, txt_path, labeled_path, img_format, category)
    data.work(True)

