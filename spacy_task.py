import re
import spacy
from spacy.tokenizer import Tokenizer
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description="parsing txt to html")
parser.add_argument('-input', action='store', dest='input_text')
parser.add_argument('-output', action='store', dest='output_html')

args = parser.parse_args()
input_text = args.input_text
output_html = args.output_html


def custom_tokenizer(nlp):
    infix_re = re.compile(r'''[.\,\?\:\;\...\‘\’\`\“\”\"\'~\/]''')
    return Tokenizer(nlp.vocab,
            infix_finditer=infix_re.finditer,
            token_match=None)

nlp = spacy.load('en_core_web_sm')
nlp.tokenizer = custom_tokenizer(nlp)

with open(input_text) as f:
    doc = nlp(f.read())
    result_list = []
    for token in doc:
        print(token.text)
        if token.is_digit or token.pos_ == "PROPN":
            result_list.append(token.text)

d = defaultdict(int)

for element in result_list:
    d[element] +=1
for key in d:
    print(f"{key} was found {d[key]} times")

html_page = "<html><head><meta charset='utf-8'><title>Result table</title></head><body><table border='1', align='right'><tr><th>Entry</th><th>Count</th></tr>"
for key in d:
    html_page += f"<tr><td>{key}</td><td>{d[key]}</td></tr>"
html_page += "</table></body></html>"

with open(output_html, 'w') as f:
    f.write(html_page)
