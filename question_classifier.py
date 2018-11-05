from parse import split_sentences, tag_sentence
from nltk.corpus import wordnet

class QuestionClass:
    def __init__(self, type_, question):
        self.type = type_
        self.question = question

    def answer(self, story):
        ans_func = {'who': who_answer, 'what': what_answer, 'when': when_answer,
                    'where': where_answer, 'why': why_answer, 'how': how_answer}
        return ans_func[self.type](self.question, story)


def classify(question):
    types = ['who', 'what', 'when', 'where', 'why', 'how']
    q_split = [x.lower() for x in question.split()]
    if q_split[0] in types:  # the first word in the question typically gives us the type of question
        return QuestionClass(q_split[0], question)
    else:
        for t in types:
            if t in q_split:
                return QuestionClass(type, question)


def word_matches(sent1, sent2):
    count = 0
    for w in sent1.split():
        if w in sent2:
            count += 1
    return count


def who_answer(question, story): # easy jordan
    sentences = split_sentences(story)
    scores = []
    for sentence in sentences:
        scores.append((sentence, word_matches(question, sentence)))
    scores.sort(key=lambda x: x[1], reverse=True)
    for s in scores:  # search highest scored sentences for a person
        tagged = tag_sentence(s[0])
        for pair in tagged:
            if pair[1] == 'PERSON' and pair[0] not in question:
                return pair[0]
    return scores[0]


def what_answer(question, story): # hard
    return ''


def when_answer(question, story): # easy mitch
    return ''


def where_answer(question, story): # easy jordan
    location_preps = ['above', 'across', 'after', 'along', 'around', 'at', 'behind', 'below',
                      'beside', 'between', 'by', 'close to', 'from', 'in front of', 'inside', 'in', 'into',
                      'near', 'next to', 'onto', 'opposite', 'out of', 'outside', 'over', 'past',
                      'to', 'towards', 'under', 'up']
    sentences = split_sentences(story)
    scores = []
    for sentence in sentences:
        bonus = 0
        for word in sentence:  # add bonus points if the sentence contains a location preposition
            if word.lower() in location_preps:
                bonus = 3
                break
        scores.append((sentence, word_matches(question, sentence) + bonus))
    scores.sort(key=lambda x: x[1], reverse=True)
    for s in scores:  # search highest scored sentences for a location
        tagged = tag_sentence(s[0].split())
        for pair in tagged:
            if pair[1] == 'LOCATION':
                return pair[0]
    return scores[0]


def why_answer(question, story): # easy mitch
    return ''


def how_answer(question, story): # hard
    return ''
