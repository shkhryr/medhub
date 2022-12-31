from django.urls import path

from apps.medcard.views import (
    average_temp_pressure,

    question_list,
    question_create,
    question_update,
    question_delete,

    form_list,
    form_create,
    form_update,
    form_delete,

    client_list,
    client_create,
    client_update,
    client_delete,

    answer_list,
    answer_create,
    answer_update,
    answer_delete,

    record_list,
    record_create,
    record_update,
    record_delete,
)

urlpatterns = [
    path('average/<int:pk>/', average_temp_pressure, name='average'),

    # crud записей клиента
    path('record/', record_list, name='record-list'),
    path('record/<int:pk>/', record_list, name='record-detail'),  # история мед.карты клиента
    path('record/create/', record_create, name='record-create'),
    path('record/<int:pk>/update/', record_update, name='record-update'),
    path('record/<int:pk>/delete/', record_delete, name='record-delete'),

    # crud ответов
    path('answer/', answer_list, name='answer-list'),
    path('answer/<int:pk>/', answer_list, name='answer-detail'),
    path('answer/create/<int:pk>', answer_create, name='answer-create'),  # есть валидация ответов клиента
    path('answer/<int:pk>/update/', answer_update, name='answer-update'),
    path('answer/<int:pk>/delete/', answer_delete, name='answer-delete'),

    # crud клиента
    path('client/', client_list, name='client-list'),
    path('client/<int:pk>/', client_list, name='client-detail'),
    path('client/create/', client_create, name='client-create'),  # есть валидация возраста клиента
    path('client/<int:pk>/update/', client_update, name='client-update'),
    path('client/<int:pk>/delete/', client_delete, name='client-delete'),

    # crud формы из вопросов и параметры формы
    path('form/', form_list, name='form-list'),
    path('form/<int:pk>/', form_list, name='form-detail'),
    path('form/create/', form_create, name='form-create'),
    path('form/<int:pk>/update/', form_update, name='form-update'),
    path('form/<int:pk>/delete/', form_delete, name='form-delete'),

    # crud индивидуальных вопросов
    path('question/', question_list, name='question-list'),
    path('question/<int:pk>/', question_list, name='question-detail'),
    path('question/create/', question_create, name='question-create'),
    path('question/<int:pk>/update/', question_update, name='question-update'),
    path('question/<int:pk>/delete/', question_delete, name='question-delete'),
]
