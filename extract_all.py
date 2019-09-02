import sys
import os

swnumb = sys.argv[1]

# Retrieve result file
read_filepath = os.path.join(os.getcwd(), 'result', swnumb)


with open(read_filepath, 'r') as f:
    content = f.readlines()

# List of dicts
sentences = []


sentDict = {}
sentDict['text'] = []
sentDict['labels'] = []
running = "None"
for line in content:
    line = line.strip()
    if len(line) == 0:
        if running != "None":
            if running == '+':
                sentDict['text'].append('<ip>')
                sentDict['text'].append('<r>')
            if running == '-':
                sentDict['text'].append('<r>')
        sentences.append(sentDict)
        sentDict = {}
        sentDict['text'] = []
        sentDict['labels'] = []
        running = "None"
        pass
    else:
        splitted = line.split()
        assert(len(splitted) == 4)
        if splitted[3] != "None" or running != "None":
            if splitted[3] == '+' and running == "None":
                running = '+'
                sentDict['text'].append('<e>')
            elif splitted[3] == '-' and running == '+':
                running = '-'
                sentDict['text'].append('<ip>')
            elif splitted[3] == "None" and running == '-':
                running = "None"
                sentDict['text'].append('<r>')
            elif splitted[3] == "None" and running == '+':
                running = "None"
                sentDict['text'].append('<ip>')
                sentDict['text'].append('<r>')
        sentDict['labels'].append(splitted[1])
        sentDict['text'].append(splitted[2])

for sentDict in sentences:
    idx = "{} - {}".format(sentDict['labels'][0], sentDict['labels'][-1])
    line = "{}".format(" ".join(sentDict['text']))
    print(idx)
    print(line)
