import os
from nltk.parse import stanford
import nltk.data
from nltk.tag.stanford import StanfordNERTagger

java_path = "C:\\Program Files\\Java\\jdk1.8.0_131\\bin\\java.exe"
os.environ['JAVAHOME'] = java_path
os.environ['STANFORD_PARSER'] = 'jars\\stanford-parser.jar'
os.environ['STANFORD_MODELS'] = 'jars\\stanford-parser-3.9.2-models.jar'

parser = stanford.StanfordParser(model_path="englishPCFG.ser.gz")
tokenizer = nltk.data.load('tokenizers\\punkt\\english.pickle')
ner = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz','jars\\stanford-ner.jar')

def get_sentence_parse(sentence):
    return parser.raw_parse(sentence)

def split_sentences(text):
    return tokenizer.tokenize(text)

def tag_sentence(sentence):
    return ner.tag(sentence)