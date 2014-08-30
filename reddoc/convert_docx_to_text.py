__author__ = 'tmwsiy'

from docx import Document

previous_bold_state=False

def check_bodmer_begin(state_to_check):
    global previous_bold_state
    if previous_bold_state == None and state_to_check == True:
        return True
    else:
        return False


document = Document('Stg7 01 01.docx')

for paragraph in document.paragraphs:
    print('')
    for run in paragraph.runs:
        if check_bodmer_begin(run.bold) == True:
            print('Bodmer: '+run.text, end='')
        else:
            print(run.text, end='')
        previous_bold_state=run.bold