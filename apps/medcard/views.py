import logging
from datetime import datetime

from rest_framework.response import Response
from rest_framework.decorators import api_view

from medhub.settings import PROJECT_NAME
from .serializers import (
    QuestionSerializer,
    FormSerializer,
    ClientSerializer,
    AnswerSerializer,
    RecordSerializer
)
from .models import (
    Question,
    Form,
    Client,
    Answer,
    Record
)


logger = logging.getLogger(PROJECT_NAME)


@api_view(['GET'])
def average_temp_pressure(request, pk=None):
    if pk:
        client = Client.objects.get(pk=pk)
        if client.temp_count == 0 or client.press_count == 0:
            return Response(data={"Error": "User has no temperature nor blood pressure records"}, status=204)
        avg_temp = round(client.temp_sum/client.temp_count, 2)
        avg_press = round(client.press_sum/client.press_count, 2)
        data = {"full_name": client.full_name, "avg_temperature": avg_temp, "avg_blood_pressure": avg_press}
        return Response(data=data, status=200)
    return Response(data={"Error": "Enter client id"}, status=404)


# QUESTION BLOCK
def question_response_data(question_obj: Question):
    return {
        'id': question_obj.id,
        'name': question_obj.name,
    }


@api_view(['GET'])
def question_list(request, pk=None):
    if pk:
        model = Question.objects.get(pk=pk)
        data = question_response_data(model)

    else:
        model = Question.objects.all()
        data = [question_response_data(question_obj) for question_obj in model]
    return Response(data=data)


@api_view(['POST'])
def question_create(request):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        name = serializer.data['name']
        question = Question.objects.create(name=name)
        return Response(question_response_data(question))
    return Response(status=400)


@api_view(['POST'])
def question_update(request, pk):
    model = Question.objects.get(pk=pk)
    serializer = QuestionSerializer(instance=model, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(["DELETE"])
def question_delete(request, pk):
    model = Question.objects.get(pk=pk)
    model.delete()
    return Response(status=204)


# FORM BLOCK
@api_view(['GET'])
def form_list(request, pk=None):
    try:
        if pk:
            model = Form.objects.get(pk=pk)
            data = FormSerializer(model).data

        else:
            model = Form.objects.all()
            data = [FormSerializer(form_obj).data for form_obj in model]
    except Form.DoesNotExist:
        return Response(status=404)
    return Response(data=data)


@api_view(['POST'])
def form_create(request):
    serializer = FormSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    form = serializer.save()

    for question_id in request.data.get('questions'):
        try:
            question = Question.objects.get(id=question_id['id'])
            form.questions.add(question)

        except Question.DoesNotExist:
            pass

    return Response(data=serializer.data, status=201)


@api_view(['POST'])
def form_update(request, pk):
    model = Form.objects.get(pk=pk)
    serializer = FormSerializer(instance=model, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    questions = []

    for question_id in request.data.get('questions'):
        try:
            question = Question.objects.get(id=question_id['id'])
            questions.append(question)
        except Question.DoesNotExist:
            pass

    model.questions.set(questions)
    return Response(serializer.data)


@api_view(["DELETE"])
def form_delete(request, pk):
    try:
        model = Form.objects.get(pk=pk)
        model.delete()
    except Form.DoesNotExist:
        return Response(status=404)
    return Response(status=204)


# CLIENT BLOCK
def client_response_data(client_obj: Client):
    return {
        'id': client_obj.id,
        'full_name': client_obj.full_name,
        'age': client_obj.age
    }


@api_view(['GET'])
def client_list(request, pk=None):
    try:
        if pk:
            model = Client.objects.get(pk=pk)
            data = ClientSerializer(model).data

        else:
            model = Client.objects.all()
            data = [ClientSerializer(client_obj).data for client_obj in model]
    except Client.DoesNotExist:
        return Response(status=404)
    return Response(data=data)


@api_view(['POST'])
def client_create(request):
    serializer = ClientSerializer(data=request.data, partial=True)
    if serializer.is_valid():
        full_name = serializer.data['full_name']
        age = serializer.data['age']
        if age > 18:
            client = Client.objects.create(full_name=full_name, age=age)
            return Response(client_response_data(client))
    return Response(status=400, data={"Error": "Client should be older than 18"})


@api_view(['POST'])
def client_update(request, pk):
    model = Client.objects.filter(pk=pk)
    serializer = ClientSerializer(instance=model, data=request.data)

    if serializer.is_valid():
        age = serializer.data['age']
        if age > 18:
            full_name = serializer.data['full_name']
            client = model.update(age=age, full_name=full_name)
            return Response(serializer.data)
    return Response(status=400, data={"Error": "Client should be older than 18"})


@api_view(["DELETE"])
def client_delete(request, pk):
    model = Client.objects.get(pk=pk)
    model.delete()
    return Response(status=204)


# ANSWER BLOCK
@api_view(['GET'])
def answer_list(request, pk=None):
    try:
        if pk:
            model = Answer.objects.get(pk=pk)
            data = AnswerSerializer(model).data

        else:
            model = Answer.objects.all()
            data = [AnswerSerializer(answer_obj).data for answer_obj in model]
    except Client.DoesNotExist:
        return Response(status=404)
    return Response(data=data)


@api_view(['POST'])
def answer_create(request, pk):
    serializer = AnswerSerializer(partial=True, data=request.data)
    if serializer.is_valid():
        answer = serializer.data['answer']
        questions_name = serializer.data.get('questions').get('name')
        if questions_name == 'Температура':
            if float(answer) not in range(34, 43):
                return Response(status=400, data={"Error": "Temperature can only be between 34 and 43"})
            client = Client.objects.get(pk=pk)
            client.temp_sum += float(answer)
            client.temp_count += 1
            client.save()

        elif questions_name == 'Давление':
            if float(answer) not in range(100, 200):
                return Response(status=400, data={"Error": "Blood pressure can only be between 100 and 200"})
            client = Client.objects.get(pk=pk)
            client.temp_sum += float(answer)
            client.temp_count += 1
            client.save()

        elif questions_name == 'Дата последнего физ. труда':
            last_time = datetime.strptime(answer, "%d/%m/%Y")
            if last_time >= datetime.now():
                return Response(status=400, data={"Error": "Date cannot be in the future or now"})

        questions = Question.objects.filter(name=questions_name)[0]
        Answer.objects.create(questions=questions, answer=answer)
        return Response(data=serializer.data)
    return Response(status=400)


@api_view(['POST'])
def answer_update(request, pk):
    model = Answer.objects.filter(pk=pk)
    serializer = AnswerSerializer(data=request.data, partial=True)

    if serializer.is_valid():
        answer = serializer.data['answer']
        model.update(answer=answer)
    return Response(data=serializer.data)


@api_view(["DELETE"])
def answer_delete(request, pk):
    model = Answer.objects.get(pk=pk)
    model.delete()
    return Response(status=204)


# RECORD BLOCK
def record_response_data(client, form, answers):
    return {
        'client': client,
        'form': form,
        'answers': answers
    }


@api_view(['GET'])
def record_list(request, pk=None):
    try:
        if pk:
            model = Record.objects.get(pk=pk)
            client = model.client.full_name
            form = model.form.form_type
            answers = {}
            for answer in model.answers.all():
                answers[answer.questions.name] = answer.answer
            data = record_response_data(client=client, form=form, answers=answers)
        else:
            model = Record.objects.all()
            data = []
            for obj in model:
                client = obj.client.full_name
                form = obj.form.form_type
                answers = {}
                for answer in obj.answers.all():
                    answers[answer.questions.name] = answer.answer
                data.append(record_response_data(client=client, form=form, answers=answers))
        return Response(data=data)
    except Record.DoesNotExist:
        return Response(status=404)


@api_view(['POST'])
def record_create(request):
    serializer = RecordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    client_id = serializer.data['client']
    client = Client.objects.get(id=client_id)
    form_id = serializer.data['form']
    form = Form.objects.get(id=form_id)
    if client.age not in range(form.age_from, form.age_to):
        return Response(data={"Error": f"Client age is {client.age}. "
                                       f"Form: {form_id} has age restriction "
                                       f"from {form.age_from} to {form.age_to}"},
                        status=400)
    record = Record.objects.create(client=client, form=form)
    answers = serializer.data['answers']
    for answer_id in answers:
        print(answer_id)
        try:
            answer = Answer.objects.get(id=answer_id['id'])
            record.answers.add(answer)

        except Answer.DoesNotExist:
            pass

    return Response(data=serializer.data, status=201)


@api_view(['POST'])
def record_update(request, pk):
    serializer = RecordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    client_id = serializer.data['client_id']
    client = Client.objects.get(id=client_id)
    form_id = serializer.data['form_type']
    form = Form.objects.get(id=form_id)
    record = Record.objects.filter(pk=pk)
    record.update(client=client, form=form)
    return Response(data=serializer.data, status=201)


@api_view(["DELETE"])
def record_delete(request, pk):
    model = Record.objects.get(pk=pk)
    model.delete()
    return Response(status=204)
