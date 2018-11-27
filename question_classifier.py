from parse import split_sentences, tag_sentence_3, tag_sentence_7, get_root_sub_obj, pos_tags
import re
from nltk.stem import WordNetLemmatizer

sentences = []
tagged_sentences7 = []
tagged_sentences3 = []
pos_sentences = []


class QuestionClass:
    def __init__(self, type_, question):
        self.type = type_
        self.question = question

    def answer(self, story):
        ans_func = {'who': who_answer, 'what': what_answer, 'when': when_answer,
                    'where': where_answer, 'why': why_answer, 'how': how_answer}
        return ans_func[self.type](self.question)


def identify_parse_tag_story(story):
    # sentence_parses.clear()
    sentences.clear()
    tagged_sentences7.clear()
    tagged_sentences3.clear()
    pos_sentences.clear()
    for sentence in split_sentences(story):
        sentences.append(sentence)
        # sentence_parses.append(sentence_parse(sentence))
        tagged_sentences7.append(tag_sentence_7(sentence))
        tagged_sentences3.append(tag_sentence_3(sentence))
        pos_sentences.append(pos_tags(sentence))


def classify(question):
    types = ['who', 'what', 'when', 'where', 'why', 'how']
    q_split = [x.lower() for x in question.split()]
    if q_split[0] in types:  # the first word in the question typically gives us the type of question
        return QuestionClass(q_split[0], question)
    else:
        for t in types:
            if t in q_split:
                return QuestionClass(t, question)


def word_matches(question, i):  # Check sentence similarity.
    sentence = sentences[i]
    pos_sent = pos_sentences[i]
    count = 0
    bonus = 0
    question = normalize(question)
    wnl = WordNetLemmatizer()

    # verb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBZ']
    # verb_ignore = ['do', 'be', 'have']
    # verbs = []
    # pos_q = pos_tags(question)
    # for pair in pos_q:
    #     if pair[1] in verb_tags:
    #         lemmatized = wnl.lemmatize(pair[0], 'v')
    #         if lemmatized not in verb_ignore:
    #             verbs.append(lemmatized)
    # for pair in pos_sent:
    #     if pair[1] in verb_tags:
    #         if wnl.lemmatize(pair[0], 'v') in verbs:
    #             bonus = 3

    sentence = normalize(sentence)
    for w in question.split():
        if w in sentence:
            count += 1
    return count + bonus
  

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


def who_answer(question):
    scores = []
    main_words = get_root_sub_obj(question)
    for x in range(len(sentences)):
        scores.append((x, word_matches(question, x) + sentence_score(main_words, sentences[x])))
        # scores.append((sentences[x], tagged_sentences3[x], pos_sentences[x],
        #                word_matches(question, sentences[x]) + sentence_score(main_words, sentences[x])))
    scores.sort(key=lambda x: x[1], reverse=True)
    for s in scores[:3]:  # search highest scored sentences for a person
        tagged = tagged_sentences3[s[0]]
        answer = ''
        for pair in tagged:
            if (pair[1] == 'PERSON' or pair[1] == 'ORGANIZATION') and pair[0] not in question:
                answer += pair[0] + ' '
        if answer != '':
            return answer

    # if a person wasn't found, return all nouns in the highest scored sentence
    n_tags = ['NN', 'NNS', 'NNP', 'NNPS']
    answer = ''
    for pair in pos_sentences[scores[0][0]]:
        if pair[1] in n_tags:
            answer += pair[0] + ' '
    if answer != '':
        return answer

    return sentences[scores[0][0]]


def normalize(sent):  # Convert to lowercase and remove non letter and number chars.
    return re.sub('[^a-zA-Z0-9\s]+', '', sent).lower()


def what_answer(question):
    return find_close_sentence(question)


def find_close_sentence(question):
    main_words = get_root_sub_obj(question)
    sentence_scores = []
    for i, sent in enumerate(sentences):
        wm = word_matches(question, i)
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
        return sentences[max_index]
    else:
        return ''


def where_answer(question):
    location_preps = ['above', 'across', 'after', 'along', 'around', 'at', 'behind', 'below',
                      'beside', 'between', 'by', 'close to', 'from', 'in front of', 'inside', 'in', 'into',
                      'near', 'next to', 'onto', 'opposite', 'out of', 'outside', 'over', 'past',
                      'to', 'towards', 'under', 'up']
    main_words = get_root_sub_obj(question)
    scores = []
    for x in range(len(sentences)):
        bonus = 0
        for word in sentences[x]:  # add bonus points if the sentence contains a location preposition
            if word.lower() in location_preps:
                bonus = 3
                break
        scores.append((x, word_matches(question, x) + bonus + sentence_score(main_words, sentences[x])))
    scores.sort(key=lambda x: x[1], reverse=True)
    for s in scores[:3]:  # search highest scored sentences for a location
        tagged = tagged_sentences3[s[0]]
        answer = ''
        for pair in tagged:
            if pair[1] == 'LOCATION':
                answer += pair[0] + ' '
        if answer != '':
            return answer

    # if a location wasn't found, return all nouns in the highest scored sentence
    n_tags = ['NN', 'NNS', 'NNP', 'NNPS']
    answer = ''
    for pair in pos_sentences[scores[0][0]]:
        if pair[1] in n_tags:
            answer += pair[0] + ' '
    if answer != '':
        return answer

    return sentences[scores[0][0]]


def check_number(word):
    word = normalize(word)
    return re.match("[1-9]+", word)


def how_much_how_many(question, type):
    main_words = get_root_sub_obj(question)
    sentence_scores = []
    possible_sentence_answer = []
    possible_answers = []
    answer = ""

    for i, sentence in enumerate(sentences):
        wm = word_matches(question, i)
        sc = sentence_score(main_words, sentence)
        sentence_scores.append(wm + sc)

    i = 0
    for sentence in tagged_sentences7:
        for pair in sentence:
            if type == 'much':
                if pair[1] == 'MONEY':
                    possible_sentence_answer.append(i)
                    answer += pair[0] + " "
            elif type == 'many':
                if check_number(pair[0]):
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


def when_answer(question):
    main_words = get_root_sub_obj(question)
    # identify_parse_tag_story(story)
    sentence_scores = []
    possible_sentence_answer = []
    possible_answers = []
    answer = ""

    for i, sentence in enumerate(sentences):
        wm = word_matches(question, i)
        sc = sentence_score(main_words, sentence)
        sentence_scores.append(wm + sc)

    i = 0
    for sentence in tagged_sentences7:
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


def why_answer(question):
    common_answer_words = [("why", "because"), ("why", "so")]
    main_words = get_root_sub_obj(question)
    main_words = main_words + common_answer_words
    sentence_scores = []
    # sents = split_sentences(story)
    for i, sent in enumerate(sentences):
        wm = word_matches(question, i)
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
        return sentences[max_index]
    else:
        return ''


def how_answer(question):
    if 'how much' in normalize(question):
        return how_much_how_many(question, 'much')
    elif 'how many' in normalize(question):
        return how_much_how_many(question, 'many')
    return find_close_sentence(question)
