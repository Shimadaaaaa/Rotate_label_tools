"""
功能：将单通道16bit tiff遥感图像裁剪并保存成 800*800 8bit 三通道的jpg图片

"""
# -*- coding: utf-8 -*-
import os
import numpy as np
import cv2
from osgeo import gdal

def matrix2uint8(matrix):
    ''' 
matrix must be a numpy array NXN
Returns uint8 version
    '''
    m_min= np.min(matrix)
    m_max= np.max(matrix)
    matrix = matrix-m_min
    return(np.array(np.rint( (matrix-m_min)/float(m_max-m_min) * 255.0),dtype=np.uint8))
    #np.rint, Round elements of the array to the nearest integer.

def readTif(fileName, id):
	
	merge_img = 0
	driver = gdal.GetDriverByName('GTiff')
	driver.Register()
 
	dataset = gdal.Open(fileName)
	if dataset == None:
		print(fileName+ "掩膜失败，文件无法打开")
		return
	im_width = dataset.RasterXSize #栅格矩阵的列数
	print('im_width:', im_width) 
	im_height = dataset.RasterYSize #栅格矩阵的行数
	print('im_height:', im_height) 
	print(fileName)
	im_bands = dataset.RasterCount #波段数
    #print(im_bands)
	im_geotrans = dataset.GetGeoTransform()#获取仿射矩阵信息
	im_proj = dataset.GetProjection()#获取投影信息
	
 
	if im_bands == 1:
		band = dataset.GetRasterBand(1)
		im_data = dataset.ReadAsArray(0,0,im_width,im_height) #获取数据
		cdata = (im_data.astype(np.uint8))
		ndata = matrix2uint8(im_data)
		height, width = ndata.shape
		print(width, height)
		for i in range(width//800):
			for j in range(height//800):
				cur_image = ndata[i*800:(i+1)*800, j*800:(j+1)*800]
				#if(i==0 and j==0):print(type(cur_image), cur_image.shape)
				merge_img = cv2.merge([cur_image, cur_image, cur_image])
				cv2.imwrite('16bit/new/{}_{}_{}.jpg'.format(id, i, j), merge_img)
		cv2.imwrite('16bit/b.jpg', ndata)
# 
	elif im_bands == 4:
	# 	# im_data = dataset.ReadAsArray(0,0,im_width,im_height)#获取数据
	# 	# im_blueBand = im_data[0,0:im_width,0:im_height] #获取蓝波段
	# 	# im_greenBand = im_data[1,0:im_width,0:im_height] #获取绿波段
	# 	# im_redBand = im_data[2,0:im_width,0:im_height] #获取红波段
	# 	# # im_nirBand = im_data[3,0:im_width,0:im_height] #获取近红外波段
	# 	# merge_img=cv2.merge([im_redBand,im_greenBand,im_blueBand])
 
	# 	# zeros = np.zeros([im_height,im_width],dtype = "uint8")
 
	# 	# data1 = im_redBand.ReadAsArray
 
	# 	band1=dataset.GetRasterBand(1)
	# 	band2=dataset.GetRasterBand(2)
	# 	band3=dataset.GetRasterBand(3)
	# 	band4=dataset.GetRasterBand(4)
	
		data1=band1.ReadAsArray(0,0,im_width,im_height).astype(np.uint16) #r #获取数据
		data2=band2.ReadAsArray(0,0,im_width,im_height).astype(np.uint16) #g #获取数据
		data3=band3.ReadAsArray(0,0,im_width,im_height).astype(np.uint16) #b #获取数据
		data4=band4.ReadAsArray(0,0,im_width,im_height).astype(np.uint16) #R #获取数据
	# 	print(data1[1][45])
	# 	output1= cv2.convertScaleAbs(data1, alpha=(255.0/65535.0))
	# 	print(output1[1][45])
	# 	output2= cv2.convertScaleAbs(data2, alpha=(255.0/65535.0))
	# 	output3= cv2.convertScaleAbs(data3, alpha=(255.0/65535.0))
 
		merge_img1 = cv2.merge([output3,output2,output1]) #B G R
		
		cv2.imwrite('16bit/1.jpg', merge_img1)

if __name__ == "__main__":
    readTif('16bit_image/1.tiff', 1) #输入tiff图像文件名，id每次一定要改
    pass