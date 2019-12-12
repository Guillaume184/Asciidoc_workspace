## AsciiDoctor Generation script
# coding: utf-8
import os
import re
import sys

## Capture arguments
if len(sys.argv) < 2:
    print("Please specify the *.adoc file to process")
    sys.exit(1)

adocFileName = str(sys.argv[1])

## Build the Table of Figures as an external *.adoc file called ToF.adoc
doc = open(adocFileName, "r")
strDoc = str(doc.read())

image = r"\.(.*)\nimage::[\w|.|&|_|-]*\[((\S)+( )+)*id=(.*)\]"
imageList = re.findall(image, strDoc)

file = open("ToF.adoc", "w+", re.MULTILINE)
i=1
for ref in imageList:
    line = 'figure-' + str(i) + ': ' + '<<' + ref[4] + ', ' + ref[0] + '>>' '\n'
    file.write(line)
    i=i+1
file.close()

## Acrobat Reader DC close (to enable PDF generation if the file already exists)
myCmd = 'taskkill /IM AcroRd32.exe'
try:
    os.system(myCmd)
except OSError as err:
    print("OS error: {0}".format(err))

## Generate PDF document name
fileNameRegEx = r"(^.*).adoc"
fileName = re.findall(fileNameRegEx, adocFileName)
pdfFileName = str(fileName[0]) + '.pdf'

## Document generation (using AsciiDoctor-pdf cli)
myCmd = 'asciidoctor-pdf .\\' + adocFileName
os.system(myCmd)
print('==> SUCCES: ' + pdfFileName + ' document generated')

## Acrobat Reader DC open (ot open generated PDF file)
myCmd = 'start .\\' + pdfFileName
os.system(myCmd)
