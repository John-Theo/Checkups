from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus.doctemplate import BaseDocTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageTemplate
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
import os


def myMainPageFrame(canvas, doc):  # 全局应用
    # "The page frame used for all PDF documents."
    canvas.saveState()
    canvas.setFont('Times-Roman', 12)
    pageNumber = canvas.getPageNumber()
    if pageNumber > 0:
        pic_yemei = os.path.join(os.path.dirname(__file__), 'yemei01.jpg')  # 页眉图片
        pic_line_file = os.path.join(os.path.dirname(__file__), 'line.jpg')  # 页眉线
        canvas.drawImage(pic_yemei, 60, 60, width=100, height=25)
        canvas.drawImage(pic_line_file, 60, 60, width=450, height=15)
        canvas.drawString(10 * cm, cm, str(pageNumber))
    canvas.restoreState()


class MyDocTemplate(BaseDocTemplate):  # 自定义模版类
    # "The document template used for all PDF documents."
    _invalidInitArgs = ('pageTemplates',)

    def __init__(self, filename, **kw):
        frame1 = Frame(2.5 * cm, 2.5 * cm, 16 * cm, 16 * cm, id='A4-landscape')
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)
        template = PageTemplate('normal', [frame1], myMainPageFrame)
        self.addPageTemplates(template)  # 绑定全局应用


def table_model(data):
    width = 7.2  # 总宽度
    colWidths = (width / len(data[0])) * inch  # 每列的宽度

    dis_list = []
    for x in data:
        # dis_list.append(map(lambda i: Paragraph('%s' % i, cn), x))
        dis_list.append(x)

    style = [
        # ('FONTNAME', (0, 0), (-1, -1), 'song'),  # 字体
        ('FONTSIZE', (0, 0), (-1, 0), 15),  # 字体大小
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#d5dae6')),  # 设置第一行背景颜色
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#d5dae6')),  # 设置第二行背景颜色

        # 合并 （'SPAN',(第一个方格的左上角坐标)，(第二个方格的左上角坐标))，合并后的值为靠上一行的值，按照长方形合并
        ('SPAN', (0, 0), (0, 1)),
        ('SPAN', (1, 0), (2, 0)),
        ('SPAN', (3, 0), (4, 0)),
        ('SPAN', (5, 0), (7, 0)),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 对齐
        ('VALIGN', (-1, 0), (-2, 0), 'MIDDLE'),  # 对齐
        ('LINEBEFORE', (0, 0), (0, -1), 0.1, colors.grey),  # 设置表格左边线颜色为灰色，线宽为0.1
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.royalblue),  # 设置表格内文字颜色
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.red),  # 设置表格内文字颜色
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # 设置表格框线为grey色，线宽为0.5
    ]

    component_table = Table(data=dis_list, colWidths=colWidths, style=style)

    return component_table


Style = getSampleStyleSheet()
n = Style['Normal']
data = [[0, 1, 2, 3, 4, 5, 6, 7],
        [00, 11, 22, 33, 44, 55, 66, 77],
        [000, 111, 222, 333, 444, 555, 666, 777],
        [0000, 1111, 2222, 3333, 4444, 5555, 6666, 7777], ]

z = table_model(data)

pdf = MyDocTemplate('ppff.pdf', pagesize=landscape(A4))

pdf.multiBuild([Paragraph('Title', n), z])
