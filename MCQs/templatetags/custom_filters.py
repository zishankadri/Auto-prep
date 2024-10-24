from django import template
import random
from core.models import Student
from MCQs.models import CorrectAnswerList
from courses.models import Chapter

register = template.Library()

@register.filter(name='shuffle')
def shuffle(value):
    shuffled_list = list(value)
    random.shuffle(shuffled_list)
    return shuffled_list


@register.filter(name='get_shuffled_answers')
def get_shuffled_answers(question, student):
    test = question.test

    shuffled_answers = shuffle([question.ans_a, question.ans_b, question.ans_c, question.ans_d])

    correct_answer_list = CorrectAnswerList.objects.get(test=test, student=student)
    if shuffled_answers[0] == question.get_correct_ans():
        correct_answer_list.answer_list += "A"
        print("A")
    if shuffled_answers[1] == question.get_correct_ans():
        correct_answer_list.answer_list += "B"
        print("B")
    if shuffled_answers[2] == question.get_correct_ans():
        correct_answer_list.answer_list += "C"
        print("C")
    if shuffled_answers[3] == question.get_correct_ans():
        correct_answer_list.answer_list += "D"
        print("D")

    correct_answer_list.save()

    alphabet = ["A", "B", "C", "D"]
    for i, ans in enumerate(shuffled_answers):
        shuffled_answers[i] = f"{alphabet[i]}) {ans}"

    return shuffled_answers


@register.filter(name='get_average_grade')
def get_average_grade(student_list) -> float:
    if not student_list:
        return 0
    
    total_tests = len(student_list[0].grades)
    total_students = len(student_list)
    
    denominator = 0
    numerator =  (total_students*total_tests)
    
    try:
        for student in student_list:
            for grade in student.grades:
                denominator += grade

        return denominator / numerator
    except:
        return 0
    