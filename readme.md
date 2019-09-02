# NXT-Switchboard-Disfluency-Parser

#### A parsing tool to extract converstations from the NXT-Switchboard corpus with disfluency annotations.

Adapted from [Jonbean][https://github.com/Jonbean/switchboard_parse] parsing tool.

## Contents
- `filelist.py`: Prints all conversation names from the "xml/terminals" folder.
- `file_list.txt`: Contains all the 642 conversation IDs obtained using the `filelist.py` script. `python filelist.py > file_list.txt`
- `parsing_all.py`: The script for parsing conversations to extract plain text tokens and disfluency annotations. Runs for one conversation at a time, with the conversation ID specified as argument. Eg- `python parsing_all.py sw2005`. Prints out one word per sentence in the format- "{A/B} {token_ID} {token} {Disfluency Annotation}". This is the main script from [here][https://github.com/Jonbean/switchboard_parse/blob/master/parsing_all.py] adapted to only handle disfluencies and simplify nested disfluencies. Disfluency annotations are either '+' (reparandum) or '-' (repair), with '-' only for the outermost repair.
- `parsing_all.sh`: Shell script to bulk run the `parsing_all.py` script on all conversations from `file_list.txt`.
- `extract_all.py`: The script to convert the resultant parses from `parsing_all.py` into single line sentences with disfluency annotations in the following format- "<e> it was just SILENCE <ip> it was probably <r> one of them", where `<e>` marks start of edit, `<ip>` marks the interruption point and `<r>` marks the end of repair.
- `extract_all.sh`: Shell script to bulk run the `extract_all.py` script on all conversations from `file_list.txt`.

## Usage
- Move the `file_list.txt`, `parsing_all.py`, `parsing_all.sh`, `extract_all.py` and `extract_all.sh` files into the `<root>/xml` directory.
- cd into the `xml` directory and run `./parsing_all.sh file_list.txt`
- run `./extract_all.sh file_list.txt`

The `parsing_all.sh` script creates the `result` folder in which the parsed files are generated. The `extract_all.sh` script creates the `result_extracted` folder in which the extracted sentences with disfluency annotations are placed.