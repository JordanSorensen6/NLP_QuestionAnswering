import sys
import re
import question_classifier as qc
from question_classifier import identify_parse_tag_story


class Story:
    def __init__(self, headline, date, id_, text=''):
        self.headline = headline
        self.date = date
        self.id = id_
        self.text = text


class Question:
    def __init__(self, id_, question, difficulty):
        self.id = id_
        self.question = question
        self.difficulty = difficulty


class Answer:
    def __init__(self, q_id, answer=''):
        self.q_id = q_id
        self.answer = answer


def parse_story(filename):
    with open(filename) as story_file:
        s_info_re = re.compile(r"HEADLINE: (.*)\nDATE: (.*)\nSTORYID: (.*)", re.MULTILINE)#Process stories with no headline, date, or storyID. This cost us points.
        s_text_re = re.compile(r"TEXT:\n\n(.+)", re.DOTALL)
        story_txt = story_file.read()
        m1 = s_info_re.match(story_txt)
        m2 = s_text_re.search(story_txt)
        if m1:
            story = Story(m1.group(1), m1.group(2), m1.group(3))
            if m2:
                story.text = m2.group(1)
                return story
    return None


def parse_questions(filename):
    questions = []
    with open(filename) as questions_file:
        q_re = re.compile(r"QuestionID: (.+)(?:\n|\n\r)Question: (.+)(?:\n|\n\r)Difficulty: (.+)", re.MULTILINE)
        matches = q_re.findall(questions_file.read())
        if matches:
            for m in matches:
                questions.append(Question(m[0], m[1], m[2]))
    return questions


def answer_questions(story, questions):
    answers = []

    identify_parse_tag_story(story)
    for q in questions:
        q_class = qc.classify(q.question)

        if q_class is not None:
            answers.append(Answer(q.id, q_class.answer(story)))
        else:  #QuestionID: 1999-W32-3-5 -- this throws off alignment.
            answers.append(Answer(q.id, ""))

    return answers


def print_answers(answers):
    for a in answers:
        print('QuestionID: {}'.format(a.q_id))
        print('Answer: {}'.format(a.answer))
        print()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Invalid command line arguments.')
        sys.exit()
    file = open("response.txt", "w")
    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()
        directory = lines[0]
        for id in lines[1:]:
            story = parse_story(directory + id + '.story')
            if story is None:  # error occurred when parsing story file
                continue
            questions = parse_questions(directory + id + '.questions')
            if not questions:  # error occurred when parsing questions files
                continue
            answers = answer_questions(story.text, questions)
            print_answers(answers)
            for a in answers:
                file.write('QuestionID: {}\n'.format(a.q_id))
                file.write('Answer: {}\n\n'.format(a.answer))
    file.close()
