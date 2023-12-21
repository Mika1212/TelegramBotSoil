import math


def process_photo(photo):
    im = photo
    pix = photo.load()

    x = im.size[0] / 2 - 50
    y = im.size[1] / 2 - 50
    r = 0
    print("size = ", im.size)

    for i in range(100):
        for j in range(100):
            r += pix[x + i, y + j][0]
            # print(pix[x + i, y + j])
    r = r / 10000
    print("R = ", r)

    ans = (math.log(r / 216.39, math.e)) / -0.184
    print("ans = ", ans)

    return ans

