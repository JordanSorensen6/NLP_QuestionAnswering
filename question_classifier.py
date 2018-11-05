from parse import split_sentences, tag_sentence_3, tag_sentence_7, sentence_parse, get_root_sub_obj
import re
sentence_parses = []
sentences = []
tagged_sentences = []
from nltk.corpus import wordnet

class QuestionClass:
    def __init__(self, type_, question):
        self.type = type_
        self.question = question

    def answer(self, story):
        ans_func = {'who': who_answer, 'what': what_answer, 'when': when_answer,
                    'where': where_answer, 'why': why_answer, 'how': how_answer}
        return ans_func[self.type](self.question, story)


def identify_parse_tag_story(story):
    sentence_parses.clear()
    sentences.clear()
    tagged_sentences.clear()
    for sentence in split_sentences(story):
        sentences.append(sentence)
        sentence_parses.append(sentence_parse(sentence))
        tagged_sentences.append(tag_sentence_7(sentence))


def classify(question):
    types = ['who', 'what', 'when', 'where', 'why', 'how']
    q_split = [x.lower() for x in question.split()]
    if q_split[0] in types:  # the first word in the question typically gives us the type of question
        return QuestionClass(q_split[0], question)
    else:
        for t in types:
            if t in q_split:
                return QuestionClass(t, question)


def word_matches(sent1, sent2):  # Check sentence similarity.
    count = 0
    sent1 = normalize(sent1)
    sent2 = normalize(sent2)
    for w in sent1.split():
        if w in sent2:
            count += 1
    return count
  

def sentence_score(main_words, sent):  # Check for key words in the sentence for additional points.
    sent = normalize(sent)
    score = 0
    for tup in main_words:
        if normalize(tup[1]) in sent:
            if tup[0] == "root":
                score += 3
            else:
                score += 2
    return score


def who_answer(question, story):
    sentences = split_sentences(story)
    scores = []
    for sentence in sentences:
        scores.append((sentence, word_matches(question, sentence)))
    scores.sort(key=lambda x: x[1], reverse=True)
    for s in scores:  # search highest scored sentences for a person
        tagged = tag_sentence_3(s[0])
        for pair in tagged:
            if pair[1] == 'PERSON' and pair[0] not in question:
                return s[0]
    return scores[0][0]


def normalize(sent):  # Convert to lowercase and remove non letter and number chars.
    return re.sub('[^a-zA-Z0-9\s]+', '', sent).lower()


def what_answer(question, story):  # hard
    return ''

def where_answer(question, story):
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
        tagged = tag_sentence_3(s[0])
        for pair in tagged:
            if pair[1] == 'LOCATION':
                return s[0]
    return scores[0][0]


def when_answer(question, story):
    main_words = get_root_sub_obj(question.question)
    identify_parse_tag_story(story)
    sentence_scores = []
    possible_sentence_answer = []
    possible_answers = []
    answer = ""

    for sentence in sentences:
        wm = word_matches(question.question, sentence)
        sc = sentence_score(main_words, sentence)
        sentence_scores.append(wm + sc)

    i = 0
    for sentence in tagged_sentences:
        for pair in sentence:
            if pair[1] == 'TIME' or pair[1] == 'DATE':
                possible_sentence_answer.append(i)
                answer += pair[0] + " "
        possible_answers.append(answer)
        answer = ""
        i += 1

    maximum = -1
    answer_index = -1
    i = 0
    for answer in possible_answers:
        if answer != "":
            if maximum < sentence_scores[i]:
                maximum = sentence_scores[i]
                answer_index = i
        i += 1

    if answer_index != -1:
        return possible_answers[answer_index]
    else:
        return ''


def why_answer(question, story):  # easy mitch
    common_answer_words = [("why", "because"), ("why", "so")]
    main_words = get_root_sub_obj(question.question)
    main_words = main_words + common_answer_words
    sentence_scores = []
    sents = split_sentences(story)
    for sent in sents:
        wm = word_matches(question.question, sent)
        sc = sentence_score(main_words, sent)
        sentence_scores.append(wm + sc)

    maximum = -1
    max_index = 0
    index = 0
    for score in sentence_scores:
        if score > maximum:
            maximum = score
            max_index = index
        index += 1

    if maximum > 5:
        return sents[max_index]
    else:
        return ''


def how_answer(question, story):  # hard
    return ''
