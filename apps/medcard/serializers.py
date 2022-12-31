from rest_framework import serializers
from .models import Client, Form, Question, Answer, Record


class QuestionSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField()

    class Meta:
        model = Question
        fields = ['id', 'name']


class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Form
        fields = ['form_type', 'age_from', 'age_to', 'questions']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['full_name', 'age']


class AnswerSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(partial=True)

    class Meta:
        model = Answer
        fields = ['questions', 'answer']


class RecordSerializer(serializers.ModelSerializer):
    client = serializers.IntegerField()
    form = serializers.IntegerField()
    answers = serializers.ListField()

    class Meta:
        model = Record
        fields = ['client', 'form', 'answers']
