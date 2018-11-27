import os
from nltk.parse import stanford
from nltk import word_tokenize
import nltk.data
from nltk.tag.stanford import StanfordNERTagger

#java_path = "C:\\Program Files\\Java\\jdk1.8.0_131\\bin\\java.exe"
#java_path = "C:\\Program Files\\Java\\jdk1.8.0_151\\bin\\java.exe"
java_path = "java.exe"
os.environ['JAVAHOME'] = java_path
os.environ['STANFORD_PARSER'] = 'jars\\stanford-parser.jar'
os.environ['STANFORD_MODELS'] = 'jars\\stanford-parser-3.9.2-models.jar'

parser = stanford.StanfordParser(model_path="englishPCFG.ser.gz")
dep_parser = stanford.StanfordDependencyParser('jars\\stanford-parser.jar', 'jars\\stanford-parser-3.9.2-models.jar')
tokenizer = nltk.data.load('tokenizers\\punkt\\english.pickle')
ner3 = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz', 'jars\\stanford-ner.jar')
ner7 = StanfordNERTagger('english.muc.7class.distsim.crf.ser.gz', 'jars\\stanford-ner.jar')


def sentence_parse(sentence):
    return parser.raw_parse(sentence)


def get_root_sub_obj(sentence):
    final_dependency = []
    result = dep_parser.raw_parse(sentence)
    parsetree = list(result)[0]
    for k in parsetree.nodes.values():
        if k["rel"] == "root" or k["rel"] == "nsubj" or k["rel"] == "dobj":
            if k["rel"] == "root":
                final_dependency.append(("root", str(k["word"])))
            elif k["rel"] == "nsubj":
                final_dependency.append(("sub", str(k["word"])))
            elif k["rel"] == "dobj":
                final_dependency.append(("obj", str(k["word"])))

    return final_dependency


def split_sentences(text):
    text = text.replace('\n', ' ')
    return tokenizer.tokenize(text)


def tag_sentence_3(sentence):
    return ner3.tag(word_tokenize(sentence))


def tag_sentence_7(sentence):
    return ner7.tag(word_tokenize(sentence))


def pos_tags(sentence):
    return nltk.pos_tag(word_tokenize(sentence))
