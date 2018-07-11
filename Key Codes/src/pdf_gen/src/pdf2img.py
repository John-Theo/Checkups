from pdf2image import convert_from_bytes
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import os
from os.path import dirname, join, abspath
import sys

input_file = join(dirname(__file__)[:-3], 'report.pdf').replace('\\', '/')

inp = PdfFileReader(input_file)
page = inp.getPage(0)

wrt = PdfFileWriter()
wrt.addPage(page)

r = io.BytesIO()
wrt.write(r)

images = convert_from_bytes(r.getvalue())
images[0].save(input_file[:-4]+".png")
r.close()
