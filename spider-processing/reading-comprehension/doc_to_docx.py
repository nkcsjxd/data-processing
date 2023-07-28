import os
import sys
import comtypes.client

# Set the directory you want to start from
rootDir = r'D:\\Workspace\\PycharmProjects\\Code-pre\\crawler\\bmm_crawler\\read\\docx'

def convert_to_docx(doc_path):
    # Create a new Word.Application object
    word = comtypes.client.CreateObject('Word.Application')
    # Hide the Word application
    word.Visible = 0
    # Open the doc file (in the background)
    doc = word.Documents.Open(doc_path)
    # Save the doc file as a docx file and close it
    doc.SaveAs(doc_path + 'x', FileFormat=16)  # 16 means Word 2007 and up (docx)
    doc.Close()
    # Quit Word
    word.Quit()

for dirName, subdirList, fileList in os.walk(rootDir):
    for fname in fileList:
        if fname.endswith('.doc'):
            convert_to_docx(os.path.join(dirName, fname))
