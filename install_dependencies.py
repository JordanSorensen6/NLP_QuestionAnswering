from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
import os
import nltk

nltk.download('averaged_perceptron_tagger')

# create directories
if not os.path.isdir('jars'):
    os.mkdir('jars')

# download stanford ner dependencies
zip_folder_name = 'stanford-ner-2018-10-16/'
resp = urlopen('https://nlp.stanford.edu/software/stanford-ner-2018-10-16.zip')
zipfile = ZipFile(BytesIO(resp.read()))
if zip_folder_name + 'stanford-ner.jar' in zipfile.namelist():
    with open('jars/stanford-ner.jar', 'wb') as ner_jar:
        ner_jar.write(zipfile.read(zip_folder_name + 'stanford-ner.jar'))

classifier_name = 'english.all.3class.distsim.crf.ser.gz'
if zip_folder_name + 'classifiers/' + classifier_name in zipfile.namelist():
    with open(classifier_name, 'wb') as class_model:
        class_model.write(zipfile.read(zip_folder_name + 'classifiers/' + classifier_name))

classifier_name = 'english.muc.7class.distsim.crf.ser.gz'
if zip_folder_name + 'classifiers/' + classifier_name in zipfile.namelist():
    with open(classifier_name, 'wb') as class_model:
        class_model.write(zipfile.read(zip_folder_name + 'classifiers/' + classifier_name))


# download stanford parser jars
zip_folder_name = 'stanford-parser-full-2018-10-17/'
resp = urlopen('https://nlp.stanford.edu/software/stanford-parser-full-2018-10-17.zip')
zipfile = ZipFile(BytesIO(resp.read()))
file_name = 'stanford-parser.jar'
if zip_folder_name + file_name in zipfile.namelist():
    with open('jars/' + file_name, 'wb') as parser:
        parser.write(zipfile.read(zip_folder_name + file_name))
file_name = 'stanford-parser-3.9.2-models.jar'
if zip_folder_name + file_name in zipfile.namelist():
    with open('jars/' + file_name, 'wb') as parser_models:
        parser_models.write(zipfile.read(zip_folder_name + file_name))
