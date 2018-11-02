from parse import split_sentences

class QuestionClass:
    def __init__(self, type, question):
        self.type = type
        self.question = question

    def answer(self, story):
        # ans_func = {'who': who_answer, 'what': what_answer, 'when': when_answer,
        #             'where': where_answer, 'why': why_answer, 'how': how_answer}
        # ans_func[self.type](self, story)
        sentence_match = []
        for sentence in split_sentences(story):
            sentence_match.append((sentence, word_matches(self.question, sentence)))
        return max(sentence_match, key=lambda x: x[1])[0]


def classify(question):
    types = ['who', 'what', 'when', 'where', 'why', 'how']
    first = question.split()[0].lower()
    if first in types:
        return QuestionClass(first, question)
    else:
        for type in types:
            if type in [x.lower() for x in question.split()]:
                return QuestionClass(type, question)


def word_matches(sent1, sent2):
    count = 0
    for w in sent1.split():
        if w in sent2:
            count += 1
    return count


def who_answer(question, story): # easy jordan
    return ''


def what_answer(question, story): # hard
    return ''


def when_answer(question, story): # easy mitch
    return ''


def where_answer(question, story): # easy jordan
    return ''


def why_answer(question, story): # easy mitch
    return ''


def how_answer(question, story): # hard
    return ''
