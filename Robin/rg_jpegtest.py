from pdf2image import convert_from_path
from rg_pdftest import *






images = convert_from_path("Prüfbericht.pdf", 500,poppler_path=r'C:\Users\robin_\Pictures\Round1\poppler-0.68.0\bin')
for i, image in enumerate(images):
    fname = 'image'+str(i)+'.jpeg'
    image.save(fname, "JPEG")



