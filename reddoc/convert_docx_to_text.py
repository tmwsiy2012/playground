__author__ = 'tmwsiy'

from docx import Document
import io
import sys
import re
import pymongo
import copy

previous_bold_state = False

def check_bodmer_begin(state_to_check):
    global previous_bold_state
    if previous_bold_state == None and state_to_check == True:
        return True
    else:
        return False

def read_chap_verse(chap, verse, dir_prefix='', output_to=sys.stdout):
    global previous_bold_state
    document = Document(dir_prefix+'Stg7 ' + '%02d' % (chap)+ ' ' + '%02d' %  (verse) +'.docx')
    doc_string = io.StringIO()
    if output_to is None:
        output_to = doc_string
    for paragraph in document.paragraphs:
        print('',file=output_to)
        for run in paragraph.runs:
            if check_bodmer_begin(run.bold) == True:
                print('Bodmer: '+run.text, end='', file=output_to)
            else:
                print(run.text, end='', file=output_to)
            previous_bold_state=run.bold
    return doc_string.getvalue()

def get_chap_verse(chap, verse, dir_prefix=''):
    return read_chap_verse(chap, verse, dir_prefix='', output_to=None)

def print_chap_verse(chap, verse, dir_prefix=''):
    read_chap_verse(chap, verse, dir_prefix='', output_to=sys.stdout)

def split_on_number_boundary(string_to_split):
    m = re.search("\d", string_to_split)
    if m:
        index = m.start()
        return [ string_to_split[:index].strip(), string_to_split[index:].strip()]
    else:
        return []

def listify_manuscript_list(input_list):
    text_reading = input_list[0]
    manuscript_list = input_list[1].split()
    for manuscript in range(len(manuscript_list)):
        # need to fix 2 digit manuscripts to add leading zero
        if len(manuscript_list[manuscript]) == 2:
            manuscript_list[manuscript] = '0'+ manuscript_list[manuscript]
        # need to fix 2 digit corrected (ie ends with 'c')
        if len(manuscript_list[manuscript]) == 3 and manuscript_list[manuscript][2] == 'c':
            manuscript_list[manuscript] = '0'+ manuscript_list[manuscript]
    return [ text_reading, manuscript_list]

def listify_apparatus_verse_document(raw_utf8):
    current_bodmer_line = ''
    # ffb is "found first bodmer" passage in verse document
    ffb=False
    listified_document = []
    previous_line=''
    for line in str.splitlines(raw_utf8):
        if line.startswith('Bodmer:'):
            ffb=True
            current_bodmer_line = ['B',line[8:].strip()]
            listified_document.append(current_bodmer_line)
        else: # Not a bodmer line
            split_line = split_on_number_boundary(line)
            if len(split_line) > 0 and len(split_line[0]) == 0 and ffb==True:
                # bodmer manuscript list
                split_line[0] = 'BML'
                # add bodmer number
                split_line[1] = '031 ' + split_line[1]
                listified_document.append(listify_manuscript_list(split_line))
            elif len(split_line) == 0:
                pass
            else:
                # "normal" split line
                # check for mising BML if bodmer was only reading and insert bodmer number
                if previous_line.startswith('Bodmer:'):
                   listified_document.append(['BML',['031']])
                listified_document.append(listify_manuscript_list(split_line))
        previous_line = line
    return listified_document


def write_listified_document(raw_list, collection, chap, verse):
    '''for line in raw_list:
        for c in line[0]:
            print(c,ord(c))'''
    current_bodmer = ''
    lemma_list = []
    lemma_position = 0
    for line in raw_list:
        lemma_dict = {"isBR":False, "isBR_ext":False}
        if len(line[0]) > 0:
            if line[0] == 'B' :
                current_bodmer=line[1]
                lemma_position = lemma_position + 1
            elif line[0] == 'BML' :
                print('BD:', current_bodmer, line[1])
                lemma_dict['isBR']= True
                lemma_dict['base_text_position'] = str(lemma_position)
                lemma_dict['text']= current_bodmer
                lemma_dict['manuscripts']=line[1]
                lemma_list.append(lemma_dict)

            else:
                gc = False
                for c in line[0][:5]:
                    if (ord(c) < 970 and ord(c) > 944):
                        gc = True
                if gc:
                    print(line[0], line[1])
                    lemma_dict['base_text_position'] = str(lemma_position)
                    lemma_dict['text']=line[0]
                    lemma_dict['manuscripts']=line[1]
                    lemma_list.append(lemma_dict)
                else:
                    pass
                    #print('NOT CAUGHT *' + line[0] + '*')
                    #for c in line[0]:
                    #    print(c,ord(c)


    verse_doc = {'chapter': str(chap),'verse': str(verse)}
    verse_doc['lemmas'] = lemma_list
    collection.insert(verse_doc)


conn = None
try:
    conn=pymongo.MongoClient()
    print ("Connected successfully!!!")
except pymongo.errors.ConnectionFailure as e:
   print("Could not connect to MongoDB: " + e)

db = conn.corpus
collection = db.lemmas



#print_chap_verse(1,1)
chap=1
for verse in range(1,14):
    raw_list = get_chap_verse(chap,verse)
    intermediate_list = listify_apparatus_verse_document(raw_list )
    write_listified_document( intermediate_list, collection,chap,verse)
chap=2
for verse in range(1,15):
    raw_list = get_chap_verse(chap,verse)
    intermediate_list = listify_apparatus_verse_document(raw_list )
    write_listified_document( intermediate_list, collection,chap,verse)



'''
output = cStringIO.StringIO()sudop
output.write('First line.\n')
print >>output, 'Second line.'
previous_bold_state=False



            elif line[0] == '[]' :
                print('[]:', line[1])
                lemma_dict['base_text_position'] = str(lemma_position)
                lemma_dict['text']='[]'
                lemma_dict['manuscripts']=line[1]
                lemma_list.append(lemma_dict)
            elif line[0] == '-' :
                print('-:', line[1])
                lemma_dict['base_text_position'] = str(lemma_position)
                lemma_dict['text']='-'
                lemma_dict['manuscripts']=line[1]
                lemma_list.append(lemma_dict)
                #print('bodmer manuscript line ' )
            elif line[0].startswith('+'):
                print('add ' + current_bodmer + ' ' + line[0][2:], line[1])
                lemma_dict['isBR_ext'] = True
                lemma_dict['base_text_position'] = str(lemma_position)
                lemma_dict['text']= '+ ' + line[0][2:]
                lemma_dict['manuscripts']=line[1]
                lemma_list.append(lemma_dict)
'''