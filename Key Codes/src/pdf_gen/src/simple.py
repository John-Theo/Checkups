from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.units import inch, cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from src.pdf_gen.src.backend_data_hub import Db2Pdf, BackendApiDev
from math import log

"""
Color Scheme
"""
standard_colors = {
    'DO': (255, 111, 2),
    'MO': (254, 195, 120),
    'LO': (255, 223, 202),
    'DB': (30, 169, 254),
    'LB': (199, 234, 254)
}
sc = {key: tuple((x + 1) / 256 for x in value) for key, value in standard_colors.items()}

"""
Global rulers
"""
# # Local pdf for download
# PADDING_TOP = 35
# PADDING_BOTTOM = 30
# ILLU_X = 58
# TABLE_LEFT = ILLU_X + 267
# PAGE_SIZE = (297 * mm, 180 * mm)

# Web pdf for display
PADDING_TOP = 5
PADDING_BOTTOM = 5
ILLU_X = 5
TABLE_LEFT = ILLU_X + 242
PAGE_SIZE = (252 * mm, 160.6 * mm)

TABLE_PADDING = 2.7
COL_WIDTH = 24
TABLE_SCALAR = 1.07
ROW_HEIGHT = [1.8] + [1] * 10 + [6, 0.2]
ILLU_WIDTH = 187
ROW_HEIGHT = [x * TABLE_SCALAR for x in ROW_HEIGHT]
PAGE_HEIGHT = PAGE_SIZE[1]
FIRST_SUBTITLE = PAGE_HEIGHT - (PADDING_BOTTOM + 5 * 60) + 15


def up_2_down_axis(padding_top, height):
    return PAGE_HEIGHT - padding_top - height


def get_color(start_c, end_c=None, step=None):
    def inner_color():
        def gradient(s, e):
            return [s + x * (e - s) / step for x in range(step)]

        s_r, s_g, s_b = start_c
        e_r, e_g, e_b = end_c
        r = gradient(s_r, e_r)
        g = gradient(s_g, e_g)
        b = gradient(s_b, e_b)
        return [(r[x], g[x], b[x]) for x in range(step)]

    if end_c is None:
        if start_c == colors.white:
            return [0, 0, 0]
        elif start_c == colors.black:
            return [1, 1, 1]
        elif isinstance(start_c, str):
            return sc[start_c]
    else:
        return inner_color()


def front_color(back_color):
    if back_color == sc['DO']:
        return tuple([1, 1, 1])
    elif back_color == sc['LB']:
        return sc['DB']
    elif back_color == sc['LO']:
        return sc['DO']
    pass


def valid_numbers(a_number, mode='value'):
    if a_number <= 0.:
        return '0.00'
    float_num = int(log(a_number, 10))
    if float_num < 0:
        a_number = round(a_number, 2)
    elif float_num > 1:
        a_number = int(a_number)
    else:
        a_number = round(a_number, 2 - float_num)
    if mode == 'str':
        len_str = len(str(a_number))
        if '.' not in str(a_number):
            return str(a_number)
        return str(a_number)+''.join(['0']*(4-len_str))
    return a_number


class DrawElement:

    def __init__(self, file_name, title, summary, result_text, levels,
                 img_dir='../assets/img/', font_dir='../assets/font/'):
        self.canvas = Canvas(file_name, pagesize=PAGE_SIZE)
        self.levels = levels
        self.title = title
        self.summary = summary
        self.result_text = result_text
        self.col_num = len(levels['values'])
        self.terms = ['\n'.join(list(x)) for x in levels['terms']]
        self.img_dir = img_dir
        self.font_dir = font_dir
        self.table_colors = {
            'background': [],
            'text': []
        }
        self.fill_color()
        self.register_font()

        # Draw a small illustration of virus
        self.canvas.drawImage(self.img_dir + 'disease.png',
                              ILLU_X, up_2_down_axis(PADDING_TOP + 60, 46.5), width=46.5, height=46.5)
        pass

    def register_font(self):
        # pdfmetrics.registerFont(TTFont(self.font_dir + 'YaHei-Light', 'wryh.ttf'))
        pdfmetrics.registerFont(TTFont('PingFang-Bold', self.font_dir + 'PingFang Bold.ttf'))
        pdfmetrics.registerFont(TTFont('PingFang-ExtraLight', self.font_dir + 'PingFang ExtraLight.ttf'))
        pdfmetrics.registerFont(TTFont('PingFang-Heavy', self.font_dir + 'PingFang Heavy.ttf'))
        pdfmetrics.registerFont(TTFont('PingFang-Light', self.font_dir + 'PingFang Light.ttf'))
        pdfmetrics.registerFont(TTFont('PingFang-Medium', self.font_dir + 'PingFang Medium.ttf'))
        pdfmetrics.registerFont(TTFont('PingFang-Regular', self.font_dir + 'PingFang Regular.ttf'))
        # pdfmetrics.registerFont(TTFont('DINPro-Bold', self.font_dir + 'DINPro-Bold.ttf'))
        # pdfmetrics.registerFont(TTFont('DINPro-Light', self.font_dir + 'DINPro-Light.ttf'))
        # pdfmetrics.registerFont(TTFont('DINPro-Medium', self.font_dir + 'DINPro-Medium.ttf'))
        pdfmetrics.registerFont(TTFont('AvenirNext-Condensed', self.font_dir + 'avenir-next-condensed.ttf'))
        pdfmetrics.registerFont(TTFont('AvenirNext-DemiBold', self.font_dir + 'AvenirNextCondensed-DemiBold.ttf'))

    def icon(self):
        page_num = self.canvas.getPageNumber()
        if page_num == 0:
            self.canvas.drawImage(self.img_dir + 'Infi-Health-grey.jpg', 30, 400, width=120, height=0.26 * 120)

    def paragraph(self, txt, padding_top, li, ri, color, font_size=5.7, font_name='PingFang-Regular', alignment=0):
        rr, gg, bb = color
        style = ParagraphStyle(
            name='Normal',
            fontName=font_name,
            textColor=colors.Color(rr, gg, bb),
            leading=9,
            fontSize=font_size,
            alignment=alignment
        )
        p = Paragraph(txt, style)
        p.wrapOn(self.canvas, ILLU_WIDTH - li - ri, 120)
        w, h = p.wrap(ILLU_WIDTH - li - ri, 120)
        p.drawOn(self.canvas, ILLU_X + li, up_2_down_axis(padding_top, h))

    def text_on_pdf(self):
        self.paragraph(self.title, PADDING_TOP + 30, 0, 0,
                       sc['DO'], font_size=10.5, alignment=1, font_name='PingFang-Bold')  # Title
        self.paragraph(self.summary, PADDING_TOP + 60, 62, 0,
                       get_color(sc['LO'], sc['DO'], 5)[3], font_name='PingFang-Light')  # Summary
        for i_con, (term, how) in enumerate(self.result_text.items()):
            color = ((1, 1, 1) if how['value'] == -2 else sc['DO'])
            self.paragraph(term, FIRST_SUBTITLE + i_con * 60, 10, 10,
                           color, font_size=7, font_name='PingFang-Bold')  # Subtitles
            self.paragraph(how['disc'], FIRST_SUBTITLE + i_con * 60 + 15, 10, 10,
                           color, font_size=5.5, font_name='PingFang-Light')  # Descriptions

    def table_text(self, data):
        row_height = ROW_HEIGHT.copy()
        row_height.reverse()
        row_height = [.9] + [row_height[0]] + [row_height[1] * 0.95] + [row_height[2] * 10.3] + [row_height[-1]]
        row_height = [x * (COL_WIDTH - TABLE_PADDING * 0.5) for x in row_height]

        t = Table(data, colWidths=COL_WIDTH * TABLE_SCALAR * 1.012, rowHeights=row_height)
        r, g, b = sc['DB']
        style_list = [
            ('FONT', (0, 0), (-1, 0), 'AvenirNext-DemiBold', 10.8),  # Top values
            ('FONT', (0, 2), (-1, 2), 'PingFang-Medium', 7),  # Text line
            ('TEXTCOLOR', (0, 2), (-1, 2), colors.Color(r, g, b)),
            ('FONT', (0, -1), (-1, -1), 'AvenirNext-DemiBold', 7.4),  # Bottom values
            # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, 2), 'CENTER'),
            ('ALIGN', (0, -1), (-1, -1), 'RIGHT')
        ]
        for i_col, column in enumerate(self.table_colors['text']):
            for i_line in range(3):
                r, g, b = column[i_line]
                style_list.append(('TEXTCOLOR', (i_col, i_line * 2), (i_col, i_line * 2), colors.Color(r, g, b)))
        t.setStyle(TableStyle(style_list))
        t.alignment = TA_CENTER
        t.wrapOn(self.canvas, 3 * inch, 3 * inch)
        t.drawOn(self.canvas, TABLE_LEFT - TABLE_PADDING * TABLE_SCALAR / 2, PADDING_BOTTOM - 1.5)

    def table(self):
        empty = ['' for _ in range(self.col_num)]
        ranges = [valid_numbers(x[0], 'str') + ' \n- \n' + valid_numbers(x[1], 'str')
                  + ' ' for x in self.levels['ranges']]
        values = list(map(valid_numbers, self.levels['values']))
        data = [values, empty, self.terms, empty, ranges]

        self.table_bg()
        self.table_text(data)

    def fill_color(self):
        def top_bar():
            if res < 0:
                c = sc['DO']
            else:
                c = sc['LB']
            return c

        def term_bar():
            if res == -1:
                c = sc['LO']
            elif res == -2:
                c = sc['DO']
            else:
                c = sc['LB']
            return c, front_color(c)

        def range_bar():
            if res == -1:
                c = sc['DO']
            elif res == -2:
                c = sc['LO']
            else:
                c = sc['LB']
            return c, front_color(c)

        def gradient():
            if res == -1:
                c = get_color(sc['LO'], sc['MO'], 5) + get_color(sc['MO'], sc['DO'], 6)[1:]
            elif res == -2:
                c = get_color(sc['DO'], sc['MO'], 6)[:-1] + get_color(sc['MO'], sc['LO'], 5)
            else:
                c = [sc['LB'] for _ in range(10)]
                c[res] = sc['DB']
                if res > 0:
                    c[res - 1] = get_color(sc['LB'], sc['DB'], 3)[1]
                if res < 9:
                    c[res + 1] = get_color(sc['LB'], sc['DB'], 3)[1]
            return c

        def top_value():
            if res < 0:
                c = sc['DO']
            else:
                c = sc['DB']
            return c

        block_colors = []
        text_color = []
        for res in self.levels['scales']:
            term_bg, term_text = term_bar()
            range_bg, range_text = range_bar()
            block_colors.append([top_bar(), term_bg] + gradient() + [range_bg])
            text_color.append([top_value(), term_text, range_text])
        self.table_colors['background'] = block_colors
        self.table_colors['text'] = text_color
        # print(json.dumps(self.table_colors, indent=4))
        # exit(0)

    def table_bg(self):
        # c.radialGradient(105 * mm, 200 * mm, 60 * mm, (red, yellow), extend=False)
        block_width = COL_WIDTH
        padding = TABLE_PADDING
        scalar = TABLE_SCALAR
        y_height = ROW_HEIGHT
        y_pos = []
        h_total = 0
        for i_h, h in enumerate(y_height):
            y_pos.append((h_total, int(h * (block_width - padding))))
            if i_h == 0 or i_h == 10 or i_h == 11:
                h_total += padding * 0.3
            h_total += int(h * (block_width - padding)) + padding

        range_end = int(block_width * scalar * 18)
        step = int(block_width * scalar) + 1
        res_colors = self.table_colors['background']

        for ix, x in enumerate(range(0, range_end, step)):
            for iy, (y, height) in enumerate(y_pos):
                r, g, b = res_colors[ix][12 - iy]
                self.canvas.setFillColor(colors.Color(r, g, b))
                self.canvas.roundRect(TABLE_LEFT + x, PADDING_BOTTOM + y, (block_width - padding) * scalar,
                                      height, 2, stroke=0, fill=1)

    def illus_bg(self):
        alert_secs = [1, -1, 1, -1, 1]
        for i_sec, sec in enumerate(alert_secs):
            if sec < 0:
                r, g, b = sc['LO']
            else:
                r, g, b = sc['DO']
            self.canvas.setFillColor(colors.Color(r, g, b))
            self.canvas.roundRect(ILLU_X, PADDING_BOTTOM + i_sec * 60, ILLU_WIDTH, 57, 4, stroke=0, fill=1)
        r, g, b = sc['LO']
        self.canvas.setFillColor(colors.Color(r, g, b))
        self.canvas.roundRect(ILLU_X, up_2_down_axis(PADDING_TOP, 12), ILLU_WIDTH, 12, 2, stroke=0, fill=1)

    def finish(self):
        self.canvas.save()


if __name__ == '__main__':
    test_data = BackendApiDev()
    # d2p = Db2Pdf()
    # test_data.levels = d2p.levels.dict

    drawer = DrawElement(
        file_name='../output_pdf/report_blood.pdf',
        title=test_data.title,
        summary=test_data.summary,
        result_text=test_data.result_text,
        levels=test_data.levels
    )

    # TODO, why icon won't appear ???
    # drawer.icon()
    drawer.illus_bg()
    drawer.table()
    drawer.text_on_pdf()

    drawer.finish()
