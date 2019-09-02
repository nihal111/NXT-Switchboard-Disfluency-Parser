import os
import xml.etree.ElementTree as ET
import sys


#########################################################################
# Adapted from:
# https://github.com/Jonbean/switchboard_parse/blob/master/parsing_all.py
# and modified to simplify nested disfluencies for extraction.
#########################################################################

'''
PART ONE:
Terminals Parsing
'''
# get_IDdict will return built up IDdict and IDlist


def get_IDdict(root, IDdict, IDlist):
    for child in root:
        if child.tag == 'word':
            wordid = child.get(namespaceIdentifier + 'id')
            IDdict[wordid] = []
            IDlist.append(wordid)
            # attach the word
            IDdict[wordid].append(child.get('orth'))
            # attach pos tag
            # IDdict[wordid].append(child.get('pos'))
            # attach start end time
            # IDdict[wordid].append(child.get(namespaceIdentifier+'start'))
            # IDdict[wordid].append(child.get(namespaceIdentifier+'end'))

            # build Phonedict if link exists
            phoneword = child.find(namespaceIdentifier + 'pointer')
            if phoneword is not None:
                phoneword_ID = phoneword.get('href').split('#')[1][3:-1]
                Phoneword_dict[phoneword_ID] = wordid
            else:
                continue

        if child.tag == 'punc':
            wordid = child.get(namespaceIdentifier + 'id')
            IDdict[wordid] = []
            # attach the word
            IDlist.append(wordid)
            IDdict[wordid].append(child.text)
            # attach pos tag
            # IDdict[wordid].append(None)
            # attach start end time
            # IDdict[wordid].append(None)
            # IDdict[wordid].append(None)
        if child.tag == 'sil':
            wordid = child.get(namespaceIdentifier + 'id')
            IDdict[wordid] = []
            IDlist.append(wordid)
            IDdict[wordid].append('SILENCE')
            # attach pos tag
            # IDdict[wordid].append(None)
            # attach start end time
            # IDdict[wordid].append(None)
            # IDdict[wordid].append(None)
        if child.tag == 'trace':
            wordid = child.get(namespaceIdentifier + 'id')
            IDdict[wordid] = []
            IDlist.append(wordid)
            IDdict[wordid].append('TRACE')
            # attach pos tag
            # IDdict[wordid].append(None)
            # attach start end time
            # IDdict[wordid].append(None)
            # IDdict[wordid].append(None)
        else:
            continue
    return IDdict, IDlist


# print out sentence with word-level attributes
# print out with space between sentences
def pretty_print(AIDdict, AIDlist, BIDdict, BIDlist):
    indexA = 0
    indexB = 0
    inwhich = ''
    if AIDlist[0][1:].split('_')[0] == '1':
        inwhich = 'A'
    else:
        inwhich = 'B'

    while indexA < len(AIDlist) - 1 or indexB < len(BIDlist) - 1:
        if inwhich == 'A':
            if indexA >= len(AIDlist) - 1 and indexB < len(BIDlist):
                print 'A', AIDlist[indexA],
                for element in AIDdict[AIDlist[indexA]]:
                    if type(element) is tuple:
                        for subele in element:
                            print subele,
                    elif type(element) is list:
                        for subele in element:
                            print subele,
                    else:
                        print element,
                print ""
                inwhich = 'B'
                print ''
                continue

            print 'A', AIDlist[indexA],
            for element in AIDdict[AIDlist[indexA]]:
                if type(element) is tuple:
                    for subele in element:
                        print subele,
                elif type(element) is list:
                    for subele in element:
                        print subele,
                else:
                    print element,
            print ""
            nextsentnum = int(AIDlist[indexA + 1].split('_')[0][1:])
            sentnum = int(AIDlist[indexA].split('_')[0][1:])
            if nextsentnum - sentnum > 1:
                inwhich = 'B'
                print ''
            if nextsentnum - sentnum == 1:
                print ''
            indexA += 1
            # if indexA >= len(AIDlist) and indexB >= len(BIDlist):
            #     break

        if inwhich == 'B':
            if indexB >= len(BIDlist) - 1 and indexA < len(AIDlist):
                print 'B', BIDlist[indexB],
                for element in BIDdict[BIDlist[indexB]]:
                    if type(element) is tuple:
                        for subele in element:
                            print subele,
                    elif type(element) is list:
                        for subele in element:
                            print subele,
                    else:
                        print element,
                print ""
                inwhich = 'A'
                print ''
                continue

            print 'B', BIDlist[indexB],
            for element in BIDdict[BIDlist[indexB]]:
                if type(element) is tuple:
                    for subele in element:
                        print subele,
                elif type(element) is list:
                    for subele in element:
                        print subele,
                else:
                    print element,
            print ""
            nextsentnum = int(BIDlist[indexB + 1].split('_')[0][1:])
            sentnum = int(BIDlist[indexB].split('_')[0][1:])
            if nextsentnum - sentnum > 1:
                inwhich = 'A'
                print ''
            if nextsentnum - sentnum == 1:
                print ''
            indexB += 1
            # if indexA >= len(AIDlist) and indexB >= len(BIDlist):
            #     break


def attach_to_terminal_func(termi_attribute_dict, IDdict):
    for ID in IDdict:
        IDdict[ID].append(termi_attribute_dict[ID])


def None_dflfile_dict_builder(IDdict, reparandum_dict, repair_dict):
    termi_dfl_dict = {}
    for key in IDdict:
        if key not in reparandum_dict and key not in repair_dict:
            termi_dfl_dict[key] = None

    return termi_dfl_dict


# Simplifies nested disfluencies to only retain the outermost repair
def get_dfl_dict(root):
    reparandum_dict = {}
    repair_dict = {}
    for child in root:
        # since disfluency is in tree structrue, the depth are not decided
        # we use iter() to convert every disfluency child into a list.
        all_children = list(child.iter())
        reparandum_depth = 1

        for subchild in all_children:
            if subchild.tag == 'reparandum':
                if subchild.find(namespaceIdentifier + 'child') is None:
                    reparandum_depth += 1
                else:
                    words = []
                    termis = subchild.findall(namespaceIdentifier + 'child')
                    for word in termis:
                        words.append(word.get('href').split('#')[1][3:-1])
                    reparandum_dict[words[0]] = '+'
                    if len(words) > 1:
                        for i in range(1, len(words)):
                            reparandum_dict[words[i]] = '+'

            elif subchild.tag == 'repair':
                if subchild.find(namespaceIdentifier + 'child') is None:
                    continue
                else:
                    repair_words = []
                    termis = subchild.findall(namespaceIdentifier + 'child')
                    for word in termis:
                        repair_words.append(
                            word.get('href').split('#')[1][3:-1])
                    if (reparandum_depth > 1):
                        repair_dict[repair_words[-1]] = '+'
                    else:
                        repair_dict[repair_words[-1]] = '-'
                    if len(repair_words) > 1:
                        for i in range(len(repair_words) - 1):
                            if (reparandum_depth > 1):
                                repair_dict[repair_words[i]] = '+'
                            else:
                                repair_dict[repair_words[i]] = '-'
                    reparandum_depth -= 1
    return reparandum_dict, repair_dict


# create terminals disfluency dict
def terminal_dfl_dict_builder(reparandum_dict, repair_dict, IDdict):
    # termi_dfl_dict structure:
    # {termi_wordID: disfluency_label}
    termi_dfl_dict = {}
    for key in reparandum_dict:
        termi_dfl_dict[key] = reparandum_dict[key]
    for key in repair_dict:
        termi_dfl_dict[key] = repair_dict[key]

    for key in IDdict:
        if key not in reparandum_dict and key not in repair_dict:
            termi_dfl_dict[key] = None

    return termi_dfl_dict


'''======================part_one======================'''
# namespace is retrieved by hand ahead, it's correct
namespaceIdentifier = '{http://nite.sourceforge.net/}'

# for iteration purpose, we split filename according to
# their name pattern, only the first part varies
swnumb = sys.argv[1]

# use ET package retrieve tree structure data for A and B speaker
Afilepath = os.path.join(os.getcwd(), 'terminals', swnumb + '.A.terminals.xml')
Bfilepath = os.path.join(os.getcwd(), 'terminals', swnumb + '.B.terminals.xml')
Atree = ET.parse(Afilepath)
Btree = ET.parse(Bfilepath)

Aroot = Atree.getroot()
Broot = Btree.getroot()

# IDdict is a dictionary for quick checking attribute of each word
# IDdict structure:
# {terminal_wordID: ['word', 'pos', 'starttime', 'endtime', ]}
AIDdict = {}
BIDdict = {}

# IDlist is an array, for sequence record, because IDdict will loss sequence
AIDlist = []
BIDlist = []

# phoneword_dict is a dict to link between terminal and phonewords transcripts
# Don't distinguish A and B as they have different wordID, they won't conflict
Phoneword_dict = {}

AIDdict, AIDlist = get_IDdict(Aroot, AIDdict, AIDlist)
BIDdict, BIDlist = get_IDdict(Broot, BIDdict, BIDlist)

'''======================part_three======================'''
try:
    Afilepath = os.path.join(os.getcwd(), 'disfluency',
                             swnumb + '.A.disfluency.xml')
    Bfilepath = os.path.join(os.getcwd(), 'disfluency',
                             swnumb + '.B.disfluency.xml')
    Atree = ET.parse(Afilepath)
    Aroot = Atree.getroot()
    Btree = ET.parse(Bfilepath)
    Broot = Btree.getroot()

    # create 2 list to record the position of reparandum and repair in
    # terminal

    # get reparandum_dict and repair_dict
    Areparandum_dict, Arepair_dict = get_dfl_dict(Aroot)
    Breparandum_dict, Brepair_dict = get_dfl_dict(Broot)

    # link termi_wordID to reparandum and repair
    Atermi_dfl_dict = terminal_dfl_dict_builder(
        Areparandum_dict, Arepair_dict, AIDdict)
    Btermi_dfl_dict = terminal_dfl_dict_builder(
        Breparandum_dict, Brepair_dict, BIDdict)

    # attach reparandum/repair for pretty print
    # attach_to_terminal_func(Atermi_dfl_dict, AIDdict)
    # attach_to_terminal_func(Btermi_dfl_dict, BIDdict)

    # pretty_print(AIDdict, AIDlist, BIDdict, BIDlist)
except:
    Atermi_dfl_dict = None_dflfile_dict_builder(
        AIDdict, Areparandum_dict, Arepair_dict)
    Btermi_dfl_dict = None_dflfile_dict_builder(
        BIDdict, Breparandum_dict, Brepair_dict)


'''======================combination======================'''


attach_to_terminal_func(Atermi_dfl_dict, AIDdict)
attach_to_terminal_func(Btermi_dfl_dict, BIDdict)

pretty_print(AIDdict, AIDlist, BIDdict, BIDlist)
