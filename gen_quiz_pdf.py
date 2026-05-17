#!/usr/bin/env python3
"""Generate P2 Math Quiz Paper PDF using ReportLab"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.colors import HexColor

# Colors
DARK = HexColor('#222222')
LIGHT_GRAY = HexColor('#f0f0f0')
YELLOW_BG = HexColor('#fff8e6')
BORDER = HexColor('#d4a843')
GREEN_BG = HexColor('#e8f5e9')

# Page setup
WIDTH, HEIGHT = A4
MARGIN = 18 * mm

# Styles
styles = getSampleStyleSheet()

title_style = ParagraphStyle('Title',
    fontSize=18, alignment=TA_CENTER, spaceAfter=4,
    fontName='Helvetica-Bold', textColor=DARK)

subtitle_style = ParagraphStyle('Subtitle',
    fontSize=10, alignment=TA_CENTER, spaceAfter=6,
    textColor=HexColor('#666666'))

section_style = ParagraphStyle('Section',
    fontSize=13, fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=6,
    backColor=LIGHT_GRAY, leftIndent=8, borderPadding=(4, 4, 4, 4))

question_style = ParagraphStyle('Question',
    fontSize=12, fontName='Helvetica-Bold', spaceAfter=4)

text_style = ParagraphStyle('Text',
    fontSize=11, leading=16, spaceAfter=2)

option_style = ParagraphStyle('Option',
    fontSize=11, leading=14, leftIndent=20, spaceAfter=1)

small_style = ParagraphStyle('Small',
    fontSize=9, textColor=HexColor('#666666'))

def build_question(text, options=None, is_tf=False, answer_box=None):
    items = []
    items.append(Paragraph(text, question_style))
    if options:
        for opt in options:
            items.append(Paragraph(opt, option_style))
    if answer_box:
        items.append(Paragraph(answer_box, small_style))
    items.append(Spacer(1, 8))
    return items

def header_table(name, class_num, student_id):
    data = [
        ['姓名：' + '_' * 25, '班別：' + '_' * 15, '學號：' + '_' * 15]
    ]
    t = Table(data, colWidths=[110*mm, 75*mm, 75*mm])
    t.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    return t

def exam_info_row():
    data = [['日期：____________', '時間：________分鐘', '滿分：100分']]
    t = Table(data, colWidths=[80*mm, 80*mm, 80*mm])
    t.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('TEXTCOLOR', (0,0), (-1,-1), HexColor('#666666')),
    ]))
    return t

def notice_box():
    text = '<b>📌 注意事項：</b> 請用鉛筆作答。選擇題請在正確答案的方格內填寫，填空題請直接在橫線上寫答案。'
    p = Paragraph(text, ParagraphStyle('Notice', fontSize=9, backColor=YELLOW_BG,
        borderPadding=6, leading=14))
    return p

def answer_table():
    """Answer marking table"""
    data = [
        ['題號', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        ['作答', '', '', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '', '', ''],
    ]
    col_w = [20*mm] + [14.5*mm]*10
    t = Table(data, colWidths=col_w, rowHeights=[10*mm, 10*mm, 12*mm])
    t.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,0), LIGHT_GRAY),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, HexColor('#f9f9f9')]),
    ]))
    return t

def make_pdf(filename):
    doc = SimpleDocTemplate(filename, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=15*mm, bottomMargin=15*mm)

    story = []

    # ========== PAGE 1 ==========
    story.append(Paragraph('📝 小二數學測驗卷', title_style))
    story.append(Paragraph('單元五：基本除法　・　單元六：方向', subtitle_style))
    story.append(Spacer(1, 4))
    story.append(header_table('', '', ''))
    story.append(Spacer(1, 4))
    story.append(exam_info_row())
    story.append(Spacer(1, 6))
    story.append(notice_box())
    story.append(Spacer(1, 8))

    story.append(Paragraph('第一部份：選擇題（第1-8題，每題4分）',
        ParagraphStyle('Section', fontSize=12, fontName='Helvetica-Bold',
            backColor=LIGHT_GRAY, leftIndent=6, spaceBefore=8, spaceAfter=6,
            borderPadding=(4, 4, 4, 4))))
    story.append(Paragraph('👆 請在正確答案的字母上打「✓」',
        ParagraphStyle('Instruct', fontSize=9, textColor=HexColor('#555'),
            spaceAfter=6)))

    # Q1-4
    story.append(build_question('1. 把 12 個蘋果平均分給 3 個小朋友，每人可分到多少個？',
        ['A. 2個　　B. 3個　　C. 4個　　D. 6個'], answer_box='作答：□ A　□ B　□ C　□ D')[0])
    for item in build_question('1. 把 12 個蘋果平均分給 3 個小朋友，每人可分到多少個？',
        ['A. 2個　　B. 3個　　C. 4個　　D. 6個'], answer_box='作答：□ A　□ B　□ C　□ D')[1:]:
        story.append(item)

    story.append(build_question('2. 有 15 粒糖，每 5 粒裝一包，可以裝多少包？',
        ['A. 2包　　B. 3包　　C. 4包　　D. 5包'], answer_box='作答：□ A　□ B　□ C　□ D')[0])
    for item in build_question('2. 有 15 粒糖，每 5 粒裝一包，可以裝多少包？',
        ['A. 2包　　B. 3包　　C. 4包　　D. 5包'], answer_box='作答：□ A　□ B　□ C　□ D')[1:]:
        story.append(item)

    story.append(build_question('3. 在除法算式 18 ÷ 3 = 6 中，哪個是除數？',
        ['A. 18　　B. 3　　C. 6　　D. 以上都不是'], answer_box='作答：□ A　□ B　□ C　□ D')[0])
    for item in build_question('3. 在除法算式 18 ÷ 3 = 6 中，哪個是除數？',
        ['A. 18　　B. 3　　C. 6　　D. 以上都不是'], answer_box='作答：□ A　□ B　□ C　□ D')[1:]:
        story.append(item)

    story.append(build_question('4. 根據 4 × 6 = 24，以下哪個除法算式是正確的？',
        ['A. 24 ÷ 4 = 5　　B. 24 ÷ 4 = 6　　C. 24 ÷ 4 = 7　　D. 24 ÷ 6 = 3'], answer_box='作答：□ A　□ B　□ C　□ D')[0])
    for item in build_question('4. 根據 4 × 6 = 24，以下哪個除法算式是正確的？',
        ['A. 24 ÷ 4 = 5　　B. 24 ÷ 4 = 6　　C. 24 ÷ 4 = 7　　D. 24 ÷ 6 = 3'], answer_box='作答：□ A　□ B　□ C　□ D')[1:]:
        story.append(item)

    story.append(build_question('5. 17 ÷ 3 = 5 … 2，以下哪個說法是正確的？',
        ['A. 商是 2，餘數是 5　　B. 商是 5，餘數是 2', 'C. 商是 17，餘數是 3　　D. 沒有餘數'], answer_box='作答：□ A　□ B　□ C　□ D')[0])
    for item in build_question('5. 17 ÷ 3 = 5 … 2，以下哪個說法是正確的？',
        ['A. 商是 2，餘數是 5　　B. 商是 5，餘數是 2', 'C. 商是 17，餘數是 3　　D. 沒有餘數'], answer_box='作答：□ A　□ B　□ C　□ D')[1:]:
        story.append(item)

    story.append(PageBreak())

    # ========== PAGE 2 ==========
    story.append(Paragraph('📝 小二數學測驗卷（續）', title_style))
    story.append(Paragraph('姓名：________________　班別：_______　學號：_______', subtitle_style))
    story.append(Spacer(1, 6))

    story.append(build_question('6. 每盒有 6 個橙，買 4 盒，共有多少個橙？',
        ['A. 10個　　B. 12個　　C. 24個　　D. 20個'], answer_box='作答：□ A　□ B　□ C　□ D')[0])
    for item in build_question('6. 每盒有 6 個橙，買 4 盒，共有多少個橙？',
        ['A. 10個　　B. 12個　　C. 24個　　D. 20個'], answer_box='作答：□ A　□ B　□ C　□ D')[1:]:
        story.append(item)

    story.append(build_question('7. 24 個橙平均放在 4 盒，每盒有多少個橙？',
        ['A. 4個　　B. 6個　　C. 8個　　D. 12個'], answer_box='作答：□ A　□ B　□ C　□ D')[0])
    for item in build_question('7. 24 個橙平均放在 4 盒，每盒有多少個橙？',
        ['A. 4個　　B. 6個　　C. 8個　　D. 12個'], answer_box='作答：□ A　□ B　□ C　□ D')[1:]:
        story.append(item)

    story.append(build_question('8. 學校有 48 個乒乓球，平均分給 8 個班，每班可得多少個？',
        ['A. 5個　　B. 6個　　C. 7個　　D. 8個'], answer_box='作答：□ A　□ B　□ C　□ D')[0])
    for item in build_question('8. 學校有 48 個乒乓球，平均分給 8 個班，每班可得多少個？',
        ['A. 5個　　B. 6個　　C. 7個　　D. 8個'], answer_box='作答：□ A　□ B　□ C　□ D')[1:]:
        story.append(item)

    story.append(Paragraph('第二部分：是非題（第9-13題，每題4分）',
        ParagraphStyle('Section', fontSize=12, fontName='Helvetica-Bold',
            backColor=LIGHT_GRAY, leftIndent=6, spaceBefore=8, spaceAfter=6,
            borderPadding=(4, 4, 4, 4))))
    story.append(Paragraph('👆 請在正確答案上打「✓」',
        ParagraphStyle('Instruct', fontSize=9, textColor=HexColor('#555'), spaceAfter=4)))

    story.append(build_question('9. 除法和乘法是相反的運算。', answer_box='□ 正確　　□ 錯誤')[0])
    for item in build_question('9. 除法和乘法是相反的運算。', answer_box='□ 正確　　□ 錯誤')[1:]:
        story.append(item)

    story.append(build_question('10. 在除法算式中，被除數一定比除數大。', answer_box='□ 正確　　□ 錯誤')[0])
    for item in build_question('10. 在除法算式中，被除數一定比除數大。', answer_box='□ 正確　　□ 錯誤')[1:]:
        story.append(item)

    story.append(build_question('11. 把 16 個蘋果平均分給 4 個小朋友，每人可得 4 個。', answer_box='□ 正確　　□ 錯誤')[0])
    for item in build_question('11. 把 16 個蘋果平均分給 4 個小朋友，每人可得 4 個。', answer_box='□ 正確　　□ 錯誤')[1:]:
        story.append(item)

    story.append(build_question('12. 可以利用乘法表來幫助計算除法答案。', answer_box='□ 正確　　□ 錯誤')[0])
    for item in build_question('12. 可以利用乘法表來幫助計算除法答案。', answer_box='□ 正確　　□ 錯誤')[1:]:
        story.append(item)

    story.append(build_question('13. 四個主要方向是：東、南、西、北。', answer_box='□ 正確　　□ 錯誤')[0])
    for item in build_question('13. 四個主要方向是：東、南、西、北。', answer_box='□ 正確　　□ 錯誤')[1:]:
        story.append(item)

    story.append(PageBreak())

    # ========== PAGE 3 ==========
    story.append(Paragraph('📝 小二數學測驗卷（續）', title_style))
    story.append(Paragraph('姓名：________________　班別：_______　學號：_______', subtitle_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph('第三部分：選擇題（第14-16題，每題4分）',
        ParagraphStyle('Section', fontSize=12, fontName='Helvetica-Bold',
            backColor=LIGHT_GRAY, leftIndent=6, spaceBefore=8, spaceAfter=6,
            borderPadding=(4, 4, 4, 4))))

    story.append(build_question('14. 如果面向北方，哪個方向是你的右手邊？',
        ['A. 東　　B. 南　　C. 西　　D. 北'], answer_box='作答：□ A　□ B　□ C　□ D')[0])
    for item in build_question('14. 如果面向北方，哪個方向是你的右手邊？',
        ['A. 東　　B. 南　　C. 西　　D. 北'], answer_box='作答：□ A　□ B　□ C　□ D')[1:]:
        story.append(item)

    story.append(build_question('15. 如果學校在圖書館的北方，那麼圖書館在學校的哪個方向？',
        ['A. 北方　　B. 南方　　C. 西方　　D. 東方'], answer_box='作答：□ A　□ B　□ C　□ D')[0])
    for item in build_question('15. 如果學校在圖書館的北方，那麼圖書館在學校的哪個方向？',
        ['A. 北方　　B. 南方　　C. 西方　　D. 東方'], answer_box='作答：□ A　□ B　□ C　□ D')[1:]:
        story.append(item)

    story.append(build_question('16. 指南針的針頭指向哪個方向？',
        ['A. 東　　B. 南　　C. 西　　D. 北'], answer_box='作答：□ A　□ B　□ C　□ D')[0])
    for item in build_question('16. 指南針的針頭指向哪個方向？',
        ['A. 東　　B. 南　　C. 西　　D. 北'], answer_box='作答：□ A　□ B　□ C　□ D')[1:]:
        story.append(item)

    story.append(Paragraph('是非題（第17-19題，每題4分）',
        ParagraphStyle('Section', fontSize=12, fontName='Helvetica-Bold',
            backColor=LIGHT_GRAY, leftIndent=6, spaceBefore=8, spaceAfter=6,
            borderPadding=(4, 4, 4, 4))))

    story.append(build_question('17. 如果 A 在 B 的東方，那麼 B 一定在 A 的西方。', answer_box='□ 正確　　□ 錯誤')[0])
    for item in build_question('17. 如果 A 在 B 的東方，那麼 B 一定在 A 的西方。', answer_box='□ 正確　　□ 錯誤')[1:]:
        story.append(item)

    story.append(build_question('18. 「西」的英文簡稱是 W。', answer_box='□ 正確　　□ 錯誤')[0])
    for item in build_question('18. 「西」的英文簡稱是 W。', answer_box='□ 正確　　□ 錯誤')[1:]:
        story.append(item)

    story.append(build_question('19. 如果面向南方，左手邊是西方。', answer_box='□ 正確　　□ 錯誤')[0])
    for item in build_question('19. 如果面向南方，左手邊是西方。', answer_box='□ 正確　　□ 錯誤')[1:]:
        story.append(item)

    story.append(PageBreak())

    # ========== PAGE 4: Fill in the blanks ==========
    story.append(Paragraph('📝 小二數學測驗卷（續）', title_style))
    story.append(Paragraph('姓名：________________　班別：_______　學號：_______', subtitle_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph('第四部分：填空題（第20-28題，每題4分）',
        ParagraphStyle('Section', fontSize=12, fontName='Helvetica-Bold',
            backColor=LIGHT_GRAY, leftIndent=6, spaceBefore=8, spaceAfter=6,
            borderPadding=(4, 4, 4, 4))))
    story.append(Paragraph('👆 請在橫線上寫出答案',
        ParagraphStyle('Instruct', fontSize=9, textColor=HexColor('#555'), spaceAfter=4)))

    blanks = [
        ('20.', '24 ÷ 6 = ________'),
        ('21.', '在算式 28 ÷ 4 = 7 中，被除數是 ________，除數是 ________，商是 ________。'),
        ('22.', '每盤有 3 個蘋果，5 盤共有 ________ 個蘋果。'),
        ('23.', '35 ÷ 5 = ________（因為 5 × ________ = 35）'),
        ('24.', '把 20 個蘋果平均分給 5 個小朋友，每人可得 ________ 個。'),
        ('25.', '四個主要方向是：________、________、________、________。'),
        ('26.', '記憶口訣：面向北方，右手邊是 ________，左手邊是 ________，背後是 ________。'),
        ('27.', '如果小明站在公園的北方，那麼公園在小明的 ________ 方。'),
        ('28.', '指南針的針頭指向 ________ 方。'),
    ]

    for num, text in blanks:
        story.append(Paragraph(f'<b>{num}</b> {text}',
            ParagraphStyle('BlankQ', fontSize=11, leading=18, spaceAfter=12)))

    story.append(PageBreak())

    # ========== PAGE 5: Application ==========
    story.append(Paragraph('📝 小二數學測驗卷（續）', title_style))
    story.append(Paragraph('姓名：________________　班別：_______　學號：_______', subtitle_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph('第五部分：應用題（第29-32題，每題6分）',
        ParagraphStyle('Section', fontSize=12, fontName='Helvetica-Bold',
            backColor=LIGHT_GRAY, leftIndent=6, spaceBefore=8, spaceAfter=6,
            borderPadding=(4, 4, 4, 4))))
    story.append(Paragraph('👆 請寫出算式並作答',
        ParagraphStyle('Instruct', fontSize=9, textColor=HexColor('#555'), spaceAfter=4)))

    apps = [
        ('29.', '每盒有 6 個蛋糕，買了 4 盒，請回答以下問題：\n\n'
                '　(a) 一共有多少個蛋糕？\n'
                '　　　　算式：____________________　答案：________\n\n'
                '　(b) 如果每人分 4 個，可以分給多少人？\n'
                '　　　　算式：____________________　答案：________'),

        ('30.', '小明有 30 顆糖果，每 6 顆裝一袋，可以裝多少袋？\n\n'
                '　　算式：____________________\n　　答：____________________'),

        ('31.', '小花面向北方站立，請寫出她左手邊、右手邊和背後的方向。\n\n'
                '　　左手邊：____________________\n　　右手邊：____________________\n　　背後：____________________'),

        ('32.', '公園在圖書館的北方，醫院在圖書館的西方。\n'
                '　　請回答：\n'
                '　　(a) 圖書館在公園的哪個方向？\n'
                '　　　　　答：____________________\n\n'
                '　　(b) 圖書館在醫院的哪個方向？\n'
                '　　　　　答：____________________'),
    ]

    for num, text in apps:
        story.append(Paragraph(f'<b>{num}</b>', question_style))
        story.append(Paragraph(text.replace('\n', '<br/>'),
            ParagraphStyle('AppQ', fontSize=11, leading=18, spaceAfter=14)))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # ========== PAGE 6: Answer Sheet ==========
    story.append(Paragraph('📝 小二數學測驗卷（答案紙）', title_style))
    story.append(Paragraph('姓名：________________　班別：_______　學號：_______', subtitle_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph('作答區：', ParagraphStyle('Label', fontSize=10, fontName='Helvetica-Bold', spaceAfter=4)))

    # Create answer table with 4 columns x 8 rows = 32 cells
    ans_data = []
    row = ['題號', '作答', '題號', '作答', '題號', '作答', '題號', '作答']
    ans_data.append(row)

    for i in range(1, 17):
        row = [str(i), '']
        if i + 16 <= 32:
            row += [str(i + 16), '']
        if i + 32 <= 32:
            row += [str(i + 32), '']
        if i + 48 <= 32:
            row += [str(i + 48), '']
        ans_data.append(row)

    col_widths = [22*mm, 43*mm, 22*mm, 43*mm, 22*mm, 43*mm, 22*mm, 43*mm]
    t = Table(ans_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,0), LIGHT_GRAY),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, HexColor('#f9f9f9')]),
        ('ROWHEIGHTS', (0,0), (-1,-1), 12*mm),
    ]))
    story.append(t)

    story.append(Spacer(1, 20))
    story.append(Paragraph('老師用欄：',
        ParagraphStyle('Label', fontSize=10, fontName='Helvetica-Bold', spaceAfter=4)))
    story.append(Paragraph('總分：________　核卷老師：________________',
        ParagraphStyle('Teacher', fontSize=10, leading=16)))

    doc.build(story)
    print(f'PDF created: {filename}')

if __name__ == '__main__':
    import os
    path = os.path.dirname(os.path.abspath(__file__))
    make_pdf(os.path.join(path, 'quiz_p2_unit5_6_print.pdf'))