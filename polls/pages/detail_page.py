import logging
from typing import Dict, Any
from channels.db import database_sync_to_async
from django.urls import reverse
from reactpy import component, event, html, use_state
from reactpy_django.hooks import use_mutation
from reactpy_router import use_params, link, Navigate

from reactpy_forms import create_form, FormModel, use_form_state

from ..models import Question, Choice
from .common import use_params, use_query, LoadingException

from .page_404 import Page_404


EventArgs = Dict[str, Any]

log = logging.getLogger(__name__)

class ChoiceData(FormModel):
    choice: int = 0


@component
def detail():

    model, set_model = use_form_state(ChoiceData())
    Form, Field = create_form(model, set_model)

    error, set_error = use_state('')
    voted, set_voted = use_state(False)

    if voted:
        return Navigate(reverse("polls:index"))


    @component
    def SubmitButton(question: Question, choice:int):

        inc_vote = use_mutation(question.inc_vote)

        @event(prevent_default=True)
        def onclick(event: EventArgs):
            log.info(model)
            if choice == 0:
                set_error("You didn't select a choice.")
            else:
                inc_vote(choice=choice)
                set_error("")
                set_voted(True)


        return html.input({
            'type': 'submit',
            'value': 'Vote',
            'class_name': 'btn btn-primary btn-lg btn-block mt-4',
            'on_click': onclick
            })


    @component
    def error_message(error_message:str):
        if error_message:
            return html.p({'class_name': 'alert alert-danger'},
                html.strong(f"{error_message}")
            )
        return ""


    def choice_field(choice: Choice):

        @component
        def ChoiceElement(props, counter):
            return html.div({'class_name': 'form-check'},
                html.input(props),
                html.label({'html_for': f'choice{counter}'}, f"{choice.choice_text}")
        )

        return Field('choice', lambda props, field: ChoiceElement(
                    props(
                        {'type': 'radio',
                        'class_name': 'form-check-input',
                        'value': f'{choice.pk}'
                        }),
                    choice.pk
                    ))

    try:

        params = use_params()
        question: Question = use_query(Question.get_question, pk=params.pk )

        return html.div(
            link("Back To Polls", to=reverse('polls:index'), class_name='btn btn-secondary btn-sm mb-3'),
            html.h1({'class_name': 'text-center mb-3'}, f"{question.question_text}"),
            error_message(error),

            Form(
                [choice_field(choice) for choice in question.choice_set.all()],
                SubmitButton(question, model.choice)

            )

        )
    except LoadingException as ex:
        return html.h2(str(ex))
    except Exception as error:
        return Page_404(str(error))
