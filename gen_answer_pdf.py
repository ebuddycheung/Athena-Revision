#!/usr/bin/env python3
"""Generate P2 Math Quiz Answer Key PDF using ReportLab"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

DARK = HexColor('#222222')
LIGHT_GRAY = HexColor('#f0f0f0')
GREEN_BG = HexColor('#e8f5e9')
ORANGE_BG = HexColor('#fff3e0')
GREEN_TEXT = HexColor('#2e7d32')

WIDTH, HEIGHT = A4
MARGIN = 18 * mm

title_style = ParagraphStyle('Title', fontSize=18, alignment=TA_CENTER,
    spaceAfter=4, fontName='Helvetica-Bold', textColor=DARK)
subtitle_style = ParagraphStyle('Subtitle', fontSize=10, alignment=TA_CENTER,
    spaceAfter=6, textColor=HexColor('#666666'))
section_style = ParagraphStyle('Section', fontSize=13, fontName='Helvetica-Bold',
    spaceBefore=8, spaceAfter=4, backColor=HexColor('#e8f5e9'),
    leftIndent=6, borderPadding=(4, 4, 4, 4))

def answer_row(num, answer, explanation=''):
    exp_text = f'　→ {explanation}' if explanation else ''
    return Paragraph(
        f'<b>{num}</b>　<font color="#2e7d32"><b>{answer}</b></font><font color="#888888" size="9">{exp_text}</font>',
        ParagraphStyle('AnsRow', fontSize=11, leading=16, spaceAfter=6,
            backColor=HexColor('#f9f9f9'), borderPadding=(6, 6, 6, 6)))

def section_header(text):
    return Paragraph(text, ParagraphStyle('SH', fontSize=13, fontName='Helvetica-Bold',
        spaceBefore=12, spaceAfter=6, backColor=HexColor('#e8f5e9'),
        leftIndent=6, borderPadding=(4, 4, 4, 4)))

def make_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=15*mm, bottomMargin=15*mm)
    story = []

    # Header
    story.append(Paragraph('✅ 小二數學測驗卷答案', title_style))
    story.append(Paragraph('單元五：基本除法　・　單元六：方向', subtitle_style))
    story.append(Spacer(1, 6))

    # Part 1: MCQ
    story.append(section_header('第一部份：選擇題（第1-8, 14-15題）'))
    mcq_answers = [
        ('1.', 'C（4個）', '12÷3=4，均分每人4個'),
        ('2.', 'B（3包）', '15÷5=3，包含每5粒一包'),
        ('3.', 'B（3）', '被除數÷除數=商，18÷3=6，除數是3'),
        ('4.', 'B（24÷4=6）', '4×6=24 → 24÷4=6'),
        ('5.', 'B（商是5，餘數是2）', '17÷3=5…2，商=5，餘數=2'),
        ('6.', 'C（24個）', '6×4=24，乘法應用題'),
        ('7.', 'B（6個）', '24÷4=6，均分每盒6個'),
        ('8.', 'B（6個）', '48÷8=6（8×6=48），每班6個'),
        ('14.', 'A（東）', '面向北方，右手邊是東'),
        ('15.', 'B（南方）', '學校在圖書館北方→圖書館在學校南方'),
    ]
    for num, ans, exp in mcq_answers:
        story.append(answer_row(num, ans, exp))

    story.append(PageBreak())

    # Header page 2
    story.append(Paragraph('✅ 小二數學測驗卷答案（續）', title_style))
    story.append(Paragraph('單元五：基本除法　・　單元六：方向', subtitle_style))
    story.append(Spacer(1, 6))

    # Part 2: True/False
    story.append(section_header('第二部分：是非題（第9-13, 16-19題）'))
    tf_answers = [
        ('9.', '✓ 正確', '乘法和除法互為相反運算'),
        ('10.', '✗ 錯誤', '被除數可小於除數，如5÷10=0…5'),
        ('11.', '✓ 正確', '16÷4=4，每人4個'),
        ('12.', '✓ 正確', '利用乘法表試商'),
        ('13.', '✓ 正確', '四個主要方向：東(E)南(S)西(W)北(N)'),
        ('16.', '✓ 正確', '西=West=W'),
        ('17.', '✓ 正確', '方向相對：東↔西'),
        ('18.', '✓ 正確', '西=West=W'),
        ('19.', '✗ 錯誤', '面向南方時，左手邊是東方'),
    ]
    for num, ans, exp in tf_answers:
        story.append(answer_row(num, ans, exp))

    story.append(Spacer(1, 10))

    # Part 3: Fill in blanks
    story.append(section_header('第三部分：填空題（第20-28題）'))
    fill_answers = [
        ('20.', '4', '6×4=24，所以24÷6=4'),
        ('21.', '28, 4, 7', '被除數=28，除數=4，商=7'),
        ('22.', '15', '3×5=15，5盤共有15個'),
        ('23.', '7；7', '5×7=35，所以35÷5=7'),
        ('24.', '4', '20÷5=4，每人4個'),
        ('25.', '東、南、西、北', '四個主要方向'),
        ('26.', '東、西、南', '面向北方：右手東、左手西、背後南'),
        ('27.', '南', '小明在公園北方→公園在小明南方'),
        ('28.', '北', '指南針針頭指向北方'),
    ]
    for num, ans, exp in fill_answers:
        story.append(answer_row(num, ans, exp))

    story.append(PageBreak())

    # Header page 3
    story.append(Paragraph('✅ 小二數學測驗卷答案（續）', title_style))
    story.append(Paragraph('單元五：基本除法　・　單元六：方向', subtitle_style))
    story.append(Spacer(1, 6))

    # Part 4: Application
    story.append(section_header('第四部分：應用題（第29-32題）'))
    app_answers = [
        ('29.', '(a) 6×4=24（個）　(b) 24÷4=6（人）', '(a)乘法 (b)包含：每人4個可分6人'),
        ('30.', '30÷6=5（袋）', '包含：每6顆裝一袋，30÷6=5袋'),
        ('31.', '左手邊=西方，右手邊=東方，背後=南方', '面向北方口訣：右東左西北是背'),
        ('32.', '(a) 南方　(b) 東方', '方向相對：北↔南，東↔西'),
    ]
    for num, ans, exp in app_answers:
        story.append(answer_row(num, ans, exp))

    story.append(Spacer(1, 20))

    # Score summary
    story.append(Paragraph('📊 分數統計表',
        ParagraphStyle('SumTitle', fontSize=13, fontName='Helvetica-Bold', spaceAfter=8)))

    sum_data = [
        ['部分', '題號', '題數', '每題', '總分'],
        ['選擇題', '1-8, 14-15', '10', '4分', '40分'],
        ['是非題', '9-13, 16-19', '9', '4分', '36分'],
        ['填空題', '20-28', '9', '4分', '36分'],
        ['應用題', '29-32', '4', '6分', '24分'],
        ['總分', '', '', '', '100分'],
    ]
    col_widths = [50*mm, 50*mm, 30*mm, 30*mm, 40*mm]
    t = Table(sum_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,0), HexColor('#e8f5e9')),
        ('BACKGROUND', (0,-1), (-1,-1), HexColor('#c8e6c9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('ROWHEIGHTS', (0,0), (-1,-1), 12*mm),
    ]))
    story.append(t)

    story.append(Spacer(1, 15))

    # Grade guide
    grade_text = '''<b>💡 評分參考：</b><br/>
　• A級（90-100分）：完全掌握除法概念和方向知識<br/>
　• B級（75-89分）：理解基本概念，少許細節需加強<br/>
　• C級（60-74分）：基礎OK，多做練習鞏固<br/>
　• D級（59分以下）：需要重溫課本，多做應用題'''
    story.append(Paragraph(grade_text, ParagraphStyle('Grade', fontSize=10, leading=16,
        backColor=ORANGE_BG, borderPadding=10)))

    doc.build(story)
    print(f'Answer PDF created: {filename}')

if __name__ == '__main__':
    import os
    path = os.path.dirname(os.path.abspath(__file__))
    make_pdf(os.path.join(path, 'quiz_p2_unit5_6_answer.pdf'))