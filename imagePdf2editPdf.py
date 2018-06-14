# _*_ coding:utf-8 _*_ 

"""
@Author: liupu
@Filename: imagePDF2editPDF.py
@Date: 2018-06-14
"""

"""
目的: 使用Python将图片版PDF转化成可以进行复制粘贴的PDF
操作环境：Windows7 + Python 3.6
所需第三方Python库：pypdf2,ghostscript,PythonMagick,pdfkit
额外需要服务：百度文字识别服务

# --------------第三方库的安装(必须确保你已经在Python中正确安装了这些第三方库）------------------- #
  pip install PyPDF2
  pip install ghostscript
  pip install baidu-aip
  pip install pdfkit
因为使用传统方式无法正确安装PythonMagick，因此请到https://www.lfd.uci.edu/~gohlke/pythonlibs/下载PythonMagick的whl文件，注意下载适合自己机器的版本。
  pip install PythonMagick-0.9.13-cp36-cp36m-win32.whl   # 如果你的机器是32位机
  pip install PythonMagick-0.9.13-cp36-cp36m-win_amd64.whl # 64位机

# -------------百度文字识别服务的开通--------------- #
  No.1： 进入这个网站https://console.bce.baidu.com/#/index/overview,确保你有一个百度账号，如果没有就注册一个
  No.2： 依次点击菜单栏产品服务->人工智能->文字识别->创建应用
  No.3:  随便起一个应用名，然后其它项选择默认即可
  No.4:  注意几下AppID、API Key和Secret Key者三项的值，后面有用
"""

# ================导入相关的第三方库================ #
import os
import ghostscript
from PyPDF2 import PdfFileReader, PdfFileWriter
from PythonMagick import Image
from aip import AipOcr
import pdfkit


work_path = 'C://Users/Administrator/Desktop/'
pdfname = input('请输入你需要进行处理的PDF文件名：')
pdfname = pdfname + '.pdf'
DPI = '85'
APP_ID = '11397854'
API_KEY = '1Kp1yY0bm60EEtaMnXOB4oq5'
SECRET_KEY = 'oIK8uOgyxyzhPFGt4TU8Fbkx8lGzLfIP'
path_wk = r'D://ProgramData/wkhtmltopdf/bin/wkhtmltopdf.exe'
pdfkit_config = pdfkit.configuration(wkhtmltopdf = path_wk)
pdfkit_options = {'encoding': 'UTF-8',}

os.chdir(work_path)
pdf_input = PdfFileReader(open(pdfname, 'rb'))
#获取PDF页数
page_count = pdf_input.getNumPages()
page_range=range(page_count)
for page_num in page_range:
    im = Image()
    im.density(DPI)
    im.read(pdfname + '[' + str(page_num) +']')
    im.write(str(page_num)+ '.jpg')


#新建一个AipOcr
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
#读取本地图片的函数
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
#可选参数
options = {}
options["language_type"] = "CHN_ENG"
options["detect_direction"] = "false"
options["detect_language"] = "false"
options["probability"] = "false"
allteststr=[]
for page_num in page_range:
    #读取本地图片
    image = get_file_content(r'%s\%s.jpg' % (path,page_num))
    #通用文字识别,得到的是一个dict
    testjson=client.basicGeneral(image, options)
    teststr=''
    for x in testjson['words_result']:
        teststr=teststr+x['words']+'</br>'
    allteststr.append(teststr)

#字符串写入PDF
for page_num in page_range:
    pdfkit.from_string((allteststr[page_num]),'%s.pdf' % (str(page_num)),configuration=pdfkit_config,options=pdfkit_options)
#合并单页PDF
pdf_output = PdfFileWriter()
for page_num in page_range:
    os.chdir(path)
    pdf_input = PdfFileReader(open('%s.pdf' % (str(page_num)), 'rb'))
    page = pdf_input.getPage(0)
    pdf_output.addPage(page)
pdf_output.write(open('newpdf.pdf','wb'))