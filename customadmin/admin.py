from django.contrib import admin


# Custom Admin Registration.
from core.models import Student, Klass, Faq, Level, Subject
from courses.models import Chapter, SubChapter
from MCQs.models import Test, CorrectAnswerList
from accounts.models import UserAccount
from paypal.standard.ipn.models import PayPalIPN
from .models import GeneralData

class Table:
    def __init__(self, name, model, fields=None, order_by=None) -> None:
        self.name = name
        self.model = model
        self.fields = fields
        self.order_by = order_by

models = [
    Table(
        name="Subjects",
        model=Subject,
        fields = ["name"],
    ),
    Table(
        name="Levels",
        model=Level, 
        fields = ["name"]
    ),
    Table(
        name="Chapters",
        model=Chapter,
        fields=["name", "subject", "level"],
        order_by=["level", "subject"]
    ),
    Table(
        name="Sub Chapters", 
        model=SubChapter,
        fields=["name", "chapter", "chapter.subject", "chapter.level"],
    ),
    Table(
        name="FAQs",
        model=Faq,
        fields = ["question", "answer"],
    ),
    # Table(
    #     name="Test", model=Test,
    #     fields=["id", "name", "status"],
    # ),
    # Users 
    Table(
        name="UserAccounts",
        model=UserAccount,
        fields=["id", "email", "is_superuser"],
        order_by=["-date_joined"],
    ),
    # Paypal IPN
    Table(
        name="PayPalIPN",
        model=PayPalIPN,
        fields=["custom", "mc_gross", "flag","flag_info", "payment_date"],
        order_by=["-payment_date"],
    ),
        # Table(name="Student", model=Student, order_by=""),
    # Table(name="Klass", model=Klass, order_by=""),
    # Table(name="CorrectAnswerList", model=CorrectAnswerList, order_by=""),
]

