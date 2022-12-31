from django.contrib.auth.models import User
from django.db import models


# form related block
class Question(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="Question to the client")

    def __str__(self):
        return self.name


class Form(models.Model):
    form_type = models.IntegerField(verbose_name="Form type")
    age_from = models.PositiveIntegerField(default=0, verbose_name="Age from")
    age_to = models.PositiveIntegerField(default=200, verbose_name="Age to")
    questions = models.ManyToManyField(Question, related_name="form_question", verbose_name="Question")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.form_type}"


# user related block
class Client(models.Model):
    full_name = models.CharField(max_length=100, help_text="Full Name")
    age = models.PositiveIntegerField(help_text="Age")
    temp_count = models.PositiveIntegerField(default=0)
    press_count = models.PositiveIntegerField(default=0)
    temp_sum = models.PositiveIntegerField(default=0)
    press_sum = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.id}. {self.full_name}"

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"


# user records related block
class Answer(models.Model):
    questions = models.ForeignKey(
        Question,
        on_delete=models.DO_NOTHING,
        related_name="answer_question",
        verbose_name="Question to the client"
    )
    answer = models.TextField(verbose_name="Answer of the client")

    def __str__(self):
        return f"{self.id}. {self.questions} - {self.answer}"


class Record(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    form = models.ForeignKey(Form, on_delete=models.CASCADE, verbose_name="Form")
    answers = models.ManyToManyField(Answer, related_name="record_answer", verbose_name="Answer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}. [ {self.form.id} ] {self.client.full_name} [ {self.created_at} ]"
