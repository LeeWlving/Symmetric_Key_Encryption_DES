from PIL import Image
import io
import numpy as np
from Des import DECRYPT, Des, ENCRYPT, IP, nsplit, IP_1, P, E

colorimg = "4.1.04.tiff"
grayimg = "7.1.02.tiff"


def data2array(data):
    i = 0
    array = [0] * 64
    while True:
        s = data // 2
        y = data % 2
        array[i] = y
        i = i + 1
        if (s == 0).all():
            break
        data = s
    return array


def array2data(array):
    n = 0
    for i, j in enumerate(array):
        n = j * pow(2, i) + n
    return n


class ColorImgDes(Des):
    def __init__(self):
        super().__init__()
        self.password = None
        self.img = None
        self.keys = list()

    def imgRun(self, key, img, action):
        if len(key) < 8:
            raise Exception("Key Should be 8 bytes long")
        elif len(key) > 8:
            key = key[:8]
        self.password = key
        self.img = np.int32(img)

        self.generatekeys()
        if action == ENCRYPT:
            print("Encrypting color imges")
        else:
            print("Decrypting color imges")
        for i, pixel in enumerate(self.img):
            for j, x in enumerate(pixel):
                for k, data in enumerate(x):
                    block = data2array(data)
                    data = self.permut(block, IP)
                    g, d = nsplit(data, 32)
                    tmp = None
                    for i in range(16):
                        d_e = self.expand(d, E)
                        if action == ENCRYPT:
                            tmp = self.xor(self.keys[i], d_e)
                        else:
                            tmp = self.xor(self.keys[15 - i], d_e)
                        tmp = self.substitute(tmp)
                        tmp = self.permut(tmp, P)
                        tmp = self.xor(g, tmp)
                        g = d
                        d = tmp
                        data = array2data(self.permut(d + g, IP_1))
        return self.img
        # print("The {}th round result:".format(j+1),bit_array_to_string(result))

    def encrypt(self, key, img):
        return self.imgRun(key, img, ENCRYPT)

    def decrypt(self, key, img):
        return self.imgRun(key, img, DECRYPT)


class GrayImgDes(Des):
    def __init__(self):
        super().__init__()
        self.password = None
        self.img = None
        self.keys = list()

    def imgRun(self, key, img, action):
        if len(key) < 8:
            raise Exception("Key Should be 8 bytes long")
        elif len(key) > 8:
            key = key[:8]
        self.password = key
        self.img = np.int32(img)

        self.generatekeys()
        if action == ENCRYPT:
            print("Encrypting color imges")
        else:
            print("Decrypting color imges")
        for i, pixel in enumerate(self.img):
            for j, data in enumerate(pixel):
                block = data2array(data)
                data = self.permut(block, IP)
                g, d = nsplit(data, 32)
                tmp = None
                for i in range(16):
                    d_e = self.expand(d, E)
                    if action == ENCRYPT:
                        tmp = self.xor(self.keys[i], d_e)
                    else:
                        tmp = self.xor(self.keys[15 - i], d_e)
                    tmp = self.substitute(tmp)
                    tmp = self.permut(tmp, P)
                    tmp = self.xor(g, tmp)
                    g = d
                    d = tmp
                    data = array2data(self.permut(d + g, IP_1))
        return self.img
        # print("The {}th round result:".format(j+1),bit_array_to_string(result))

    def encrypt(self, key, img):
        return self.imgRun(key, img, ENCRYPT)

    def decrypt(self, key, img):
        return self.imgRun(key, img, DECRYPT)


if __name__ == '__main__':
    key = "CISC7015"
    img = Image.open(colorimg)
    grayImg = Image.open(grayimg)
    print("The Image showed as:")
    img.show()
    print(np.int32(img))
    D = GrayImgDes()
    C = D.encrypt(key=key, img=grayImg)
    P = D.decrypt(key, C)
    print(P)
    print("The Image showed as:")
    P = Image.fromarray(P)
    P.show()
    D_1=ColorImgDes()
    C_1=D_1.encrypt(key=key,img=img)
    P_1=D_1.decrypt(key,C_1)
    print(P_1)
