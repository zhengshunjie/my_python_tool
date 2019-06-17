import cv2
import os
def file_name(file_dir):
    L = []
    for root ,dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                L.append(os.path.join(root,file))
    L.sort()
    return L

if __name__ == '__main__':
    imgs = file_name('.')
    for i in range(len(imgs)):
        img = cv2.imread(imgs[i])
        # cv2.imshow('123',img)
        # cv2.waitKey()
        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        cv2.imwrite(imgs[i],img)
        # cv2.imshow('456',img)
        # cv2.waitKey()