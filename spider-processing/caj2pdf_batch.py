import os
import sys

def caj_list(file_dir):
    flist = []
    for file in os.listdir(file_dir):
            flist.append(file)
    return flist

# if len (sys.argv) < 3:
#     print("请输入正确命令：caj2pdf_batch caj文件位置 pdf保存位置")
#     exit()

fdir = "./caj/" #sys.argv[1]
outdir = "./pdf/" #sys.argv[2]

flist = caj_list(fdir)
i = 0
print(len(flist))
for fname in flist:
    cmd = "caj2pdf convert " + fdir + fname + " -o " + outdir + str(i) + ".pdf"
    i = i + 1
    print(cmd)
    os.system(cmd)