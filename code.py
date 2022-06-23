import cv2
import numpy as np
import os
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--location', default='/Users/Keatshao/Desktop/test', help='The folder containing the imgs sequence.')
    parser.add_argument('-sp', '--start_point', default=(210,300), help='This denotes the start point (the upper left point).')
    parser.add_argument('-sz', '--size', default=(90,80), help='The size tuple must be compatible with the original img size')
    return parser.parse_args()

def get_imgs(args):
    folder_path = args.location
    details_folder = args.location+'_details'
    redline_folder = args.location+'_redline'
    files = os.listdir(folder_path)
    if not os.path.exists(details_folder):
        os.makedirs(details_folder)
        print('%s has been made!'%details_folder)
    if not os.path.exists(redline_folder):
        os.makedirs(redline_folder)
        print('%s has been made!'%redline_folder)
    for file in files:
        file_path = os.path.join(folder_path,file)
        img = cv2.imread(file_path)
        h, w, c = img.shape
        ratio = min(h//args.size[0], w//args.size[1])
        row_place = args.start_point[0]
        col_place = args.start_point[1]
        if row_place+args.size[0]>h or col_place+args.size[1]>w:
            return print('Input size or start_point is wrong!')
        img_detail = img[row_place:row_place+args.size[0], col_place:col_place+args.size[1],:]
        img_detail_zoom = img_detail.repeat(ratio,axis=0).repeat(ratio,axis=1)
        h_list = [i for i in range(col_place-3, col_place+3+args.size[1])]
        v_list = [i for i in range(row_place-3, row_place+3+args.size[0])]
        #Draw horizontal red line:
        for i in h_list:
            for j in range(1,4):  #Width of the line
                img[row_place-j, i]=[0, 0, 255]
            for j in range(1,4):
                img[row_place+j+args.size[0]-1, i]=[0, 0, 255]
        for i in v_list:
            for j in range(1,4):
                img[i, col_place-j]=[0, 0, 255]
            for j in range(1,4):
                img[i, col_place+j+args.size[1]-1]=[0, 0, 255]
        cv2.imwrite(os.path.join(details_folder, file), img_detail_zoom, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
        cv2.imwrite(os.path.join(redline_folder, file), img, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
        print('Successfully process image %s, and the ratio is %d'%(file_path,ratio))


if __name__ == '__main__':
    args = get_args()
    get_imgs(args)