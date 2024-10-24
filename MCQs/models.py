from django.db import models
from core.models import Student
from django.utils import timezone

class Test(models.Model):
    ANSWER_SHEET_TYPE_CHOICES = (
        ("SAME_TEST", "All students have the same test"),
        ("UNIQUE_TEST", "Each student has a unique test"),
    )

    RUNNING = "RUNNING"
    ANALIZING = "ANALIZING"
    COMPLETED = "COMPLETED"
    STATUS_CHOICES = (
        (RUNNING, "Running"),
        (ANALIZING, "Analizing"),
        (COMPLETED, "Completed"),
    )

    name = models.CharField(max_length=50)
    klass = models.ForeignKey("core.Klass", on_delete=models.CASCADE)
    answer_sheet_type = models.CharField(choices=ANSWER_SHEET_TYPE_CHOICES, max_length=50, default="SAME_TEST")
    no_of_questions = models.IntegerField()
    simple_answer_list = models.CharField(max_length=40, default="")  # Max number of questions a user can create is 40
    rendered_html = models.TextField(null=True, default=None)

    status = models.CharField(choices=STATUS_CHOICES, default=RUNNING, max_length=10)

    date_completed = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    average_grades = models.FloatField(null=True, blank=True)
    completion_rate = models.IntegerField(default=0, null=True, blank=True)
    

    def __str__(self) -> str:
        return self.name

    def distribute_scores(self, data):
        self.klass.add_grade_column()
        average_denominator = 0
        average_numerator = len(data)
        full_completed_students = 0

        for student_id, answer_list in data.items():
            full_completion = True
            student = Student.objects.get(id=student_id)
            if self.answer_sheet_type == "SAME_TEST":
                correct_answer_list = self.simple_answer_list
            if self.answer_sheet_type == "UNIQUE_TEST":
                correct_answer_list = CorrectAnswerList.objects.get(test=self, student=student).answer_list

            if student.klass != self.klass:
                continue  # Mistake in QR code recognition

            points = 0
            for i, answer in enumerate(answer_list):
                if answer == correct_answer_list[i]:
                    points += 1

                if answer == "": full_completion = False

            print(f"{student.first_name} points: ", points)

            score = points / self.no_of_questions * 20  # Out of 20
            student.grades[-1] = score
            student.save()

            average_denominator += score
            if full_completion:
                full_completed_students += 1

        self.date_completed = timezone.now().date()
        self.average_grades = average_denominator / average_numerator
        self.completion_rate = (full_completed_students / len(data)) * 100
        self.save()


class Question(models.Model):
    CORRECT_ANS_CHOICES = (
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
    )

    test = models.ForeignKey("MCQs.Test", on_delete=models.CASCADE, null=True, blank=True)
    chapter = models.ForeignKey("courses.Chapter", on_delete=models.CASCADE, null=True)

    question = models.TextField()
    
    # Answers a), b), c), d)
    ans_a = models.CharField(max_length=100)
    ans_b = models.CharField(max_length=100)
    ans_c = models.CharField(max_length=100)
    ans_d = models.CharField(max_length=100)

    correct_ans = models.CharField(choices=CORRECT_ANS_CHOICES ,max_length=1)
    likes = models.ManyToManyField("accounts.UserAccount", related_name="liked_questions", blank=True)
    dislikes = models.ManyToManyField("accounts.UserAccount", related_name="disliked_questions", blank=True)
    is_public = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.question

    def save(self, *args, **kwargs):
        # Check if the question is duplicate and set is_public accordingly.
        # existing_question = Question.objects.filter(question=self.question).first()

        # if existing_question:
            # self.is_public = False

        super().save(*args, **kwargs)

    def get_correct_ans(self):
        if self.correct_ans == "A":
            return self.ans_a
        if self.correct_ans == "B":
            return self.ans_b
        if self.correct_ans == "C":
            return self.ans_c
        if self.correct_ans == "D":
            return self.ans_d
        
class CorrectAnswerList(models.Model):
    test = models.ForeignKey("MCQs.Test", on_delete=models.CASCADE)
    student = models.ForeignKey("core.Student", on_delete=models.CASCADE)

    answer_list = models.CharField(max_length=40, default="")  # Max number of questions a user can create is 40