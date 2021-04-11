import os
from tqdm import tqdm
import shutil
import random


def get_args():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--images', help="images path",
                        type=str, default='./images/100k')
    parser.add_argument('-t', '--type', help="type of dataset",
                        choices=['train', 'val'], default='train')
    parser.add_argument('-p', '--percent', help='sample percent',
                        type=float, default=0.1)

    parser.add_argument('-r', '--random', help='random sample',
                        type=bool, choices=[True, False], default=False)

    return parser.parse_args()


def getFileList(dir, extract):
    fileList = []
    filenames = os.listdir(dir)
    for filename in filenames:
        ext = os.path.splitext(filename)[-1]
        if ext == extract:
            fileList.append(filename)
    return fileList


def copyFile(imageNameLists, imageRootPath, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    for imageName in tqdm(imageNameLists):
        imageName = os.path.join(imageRootPath, imageName)
        labelName = imageName.replace('.jpg', '.txt')
        shutil.copy(imageName, dst)
        shutil.copy(labelName, dst)


if __name__ == '__main__':
    args = get_args()

    imageRootPath = args.images
    per = args.percent

    if args.type == 'train':
        imageRootPath = os.path.join(args.images, 'train')
    else:
        imageRootPath = os.path.join(args.images, 'val')

    imageList = getFileList(imageRootPath, '.jpg')

    listLen = len(imageList)
    index = int(listLen*per)

    if args.random:
        imageList = random.sample(imageList, index)
    else:
        imageList = imageList[:index]

    print('copying file')
    copyFile(imageList, imageRootPath, args.type)
