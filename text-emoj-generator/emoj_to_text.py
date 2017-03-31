from PIL import Image
from numpy import array
from matplotlib import pyplot

textHight = 30
hight = textHight * 2
orTL = 0b1000
orTR = 0b0100
orBL = 0b0010
orBR = 0b0001
textArr = {}
textArr[0b0000] = "  "
textArr[0b1000] = "' "
textArr[0b0100] = " '"
textArr[0b0010] = ", "
textArr[0b0001] = " ,"
textArr[0b1010] = "( "
textArr[0b0101] = " )"
textArr[0b1100] = "**"
textArr[0b0011] = "=="
textArr[0b1111] = "@@"
textArr[0b1001] = "',"
textArr[0b0110] = ",'"
textArr[0b1110] = "|'"
textArr[0b1101] = "'|"
textArr[0b1011] = "|,"
textArr[0b0111] = ",|"

multi_text_arr = ["@", "?", "*", " "]
bucket_size = 256 / len(multi_text_arr)

whiteH = 200
blackL = 180

def draw_text(text, textHight, textWidth):
    for x in xrange(textHight):
        printText = ""
        for y in xrange(textWidth):
            printText += text[x][y]
        printText = printText.replace("\t", "").replace("\r","").replace("\n","")
        print printText

def draw_pix(pix, pixHight, pixWidth):
    for x in range(pixHight):
        for y in range(pixWidth):
            print pix[y,x],

def draw_pix_dist(pix, pixHight, pixWidth):
    arr = []
    for x in range(pixHight):
        for y in range(pixWidth):
            arr.append(pix[y,x])
    arr = array(arr)
    pyplot.hist(arr,100)

    pyplot.xlabel('pix')
    pyplot.xlim(0,256)
    pyplot.ylabel('Frequency')
    pyplot.title('distribute of pix')
    pyplot.show()
    return arr

def to_text(pic = "wohuabizhi.jpg", dt = True, dpd = False, wh = whiteH):
    im = Image.open(pic)
    pixHight = hight
    pixWidth = im.size[0] * hight / im.size[1] * 2
    if pixWidth % 2 == 1:
        pixWidth += 1
    textWidth = pixWidth / 2
    im = im.resize((pixWidth, pixHight))
    im = im.convert("L")
    pix = im.load()
    print "text w: "+str(textWidth),
    print "text h: "+str(textHight)
    print "pix w: "+str(pixWidth),
    print "pix h: "+str(pixHight)
    text = [["" for x in xrange(textWidth)] for y in xrange(textHight)]
    
#    for x in range(pixHight):
#        for y in range(pixWidth):
#            if pix[y, x] == 0:
#                text[x/2][y/2] = " "
#            else:
#                text[x/2][y/2] = "@"
#    for x in range(0, pixHight, 2):
#        for y in range(0, pixWidth, 2):
#            bit = 0b0000
#            # print "set("+str(x)+","+str(y)+")"
#            if pix[y, x] > whiteH:
#                pix[y, x] = 255
#            if pix[y+1, x] > whiteH:
#                pix[y+1, x] = 255
#            if pix[y, x+1] > whiteH:
#                pix[y, x+1] = 255
#            if pix[y+1, x+1] > whiteH:
#                pix[y+1, x+1] = 255
#            if pix[y, x] < blackL:
#                bit |= orTL
#            if pix[y+1, x] < blackL:
#                bit |= orTR
#            if pix[y, x+1] < blackL:
#                bit |= orBL
#            if pix[y+1, x+1] < blackL:
#                bit |= orBR
#            if textArr.get(bit) == None:
#                text[x/2][y/2] = " "
#            else:
#                text[x/2][y/2] = textArr[bit]
    for x in xrange(0, pixHight, 2):
        for y in xrange(0, pixWidth, 1):
            if pix[y, x] > wh:
                pix[y, x] = 255
            if pix[y, x+1] > wh:
                pix[y, x+1] = 255
            gray = (pix[y, x] + pix[y, x+1]) / 2
            print "set("+str(x/2)+", "+str(y/2)+")"
            text[x/2][y/2] = multi_text_arr[gray / bucket_size]
    if dt:
        draw_text(text, textHight, textWidth)
    if dpd:
        draw_pix_dist(pix, pixHight, pixWidth)
    return (im,text)
