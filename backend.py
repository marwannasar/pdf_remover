import PyPDF2
import fitz
from PIL import Image
import os

performanceData = {0:1, 1:5}

def process(fileName, uploadPath, downloadPath, imagePath, threshold, performance):

    dirname = os.path.dirname(__file__)
 
    file = open(os.path.join(dirname, uploadPath + fileName), 'rb')

    reader = PyPDF2.PdfFileReader(file)

    n = reader.numPages

    step = performanceData[performance]

    doc = fitz.open(uploadPath + fileName)

    pagesToKeep = list(range(n))
     
    for i in range (n):
        deletePage = True
       
        
        
        page = doc.loadPage(i)
        pix = page.getPixmap()
        output = imagePath + "img%d.png" % (i) 
        pix.writePNG(output)


        img = Image.open(imagePath + "img%d.png" % (i)) 
        size = img.size


        width, height = size
        totalPixels = width * height

        #sr,sg,sb = img.getpixel((1,1))
        


        maxPixels = (threshold * totalPixels) / step

        pixelCounter = 0

    
        
        for x in range (0,width,step):
            for y in range (0,height,step):
    
                r,g,b = img.getpixel((x,y))
                if (not((abs(r-b) <= 5) and (abs(r-g) <= 5) and (abs(b-g) <=5) and (min(r,g,b) > 235))):
                    pixelCounter +=1
                    if pixelCounter > maxPixels:
                        deletePage = False
                          

        if deletePage:
            pagesToKeep.remove(i)
            #print("DELETED PAGE" , i)


        os.remove(imagePath + "img%d.png" % (i))     
                        

    if len(pagesToKeep) == 0:
        return -1
    else:
        writer1 = PyPDF2.PdfFileWriter()
        
        for i in pagesToKeep:
            x = reader.getPage(i)
            writer1.addPage(x)

        with open (downloadPath + 'fixed_' + fileName, 'wb') as f:
            writer1.write(f)
    


    
#process('SPCOM.pdf', 'uploads\\', 'downloads\\', 'images\\', 0.01, 1)
    
    

    















