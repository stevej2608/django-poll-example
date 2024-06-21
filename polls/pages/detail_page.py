import logging
from typing import Dict, Any
from channels.db import database_sync_to_async
from django.utils import timezone
from reactpy import component, event, html, use_state
from reactpy_django.hooks import use_query, use_mutation
from reactpy_router import use_params, link

from reactpy_forms import create_form, FormModel, use_form_state

from ..models import Question, Choice

from .page_404 import Page_404


EventArgs = Dict[str, Any]

log = logging.getLogger(__name__)

class ChoiceData(FormModel):
    choice: int = 0


async def get_questions():

    # https://reactive-python.github.io/reactpy-django/latest/reference/hooks/#use-query

    def query():
        return Question.objects.filter(pub_date__lte=timezone.now())

    return await database_sync_to_async(query)()

@component
def detail():

    model, set_model = use_form_state(ChoiceData())
    Form, Field = create_form(model, set_model)

    error, set_error = use_state('')

    params = use_params()
    qs = use_query(get_questions)

    if qs.error:
        return html.h2(f"Error when loading - {qs.error}")
    elif qs.data is None:
        return html.h2("Loading...")

    @component
    def SubmitButton(question: Question, choice:int):

        async def _inc_vote():
            selected_choice = await database_sync_to_async(question.choice_set.get)(pk=choice)
            selected_choice.votes += 1
            await database_sync_to_async(selected_choice.save)()

        inc_vote = use_mutation(_inc_vote)

        @event(prevent_default=True)
        def onclick(event: EventArgs):
            log.info(model)
            if choice == 0:
                set_error("You didn't select a choice.")
            else:
                set_error("")
                inc_vote()



        return html.input({
            'type': 'submit',
            'value': 'Vote',
            'class_name': 'btn btn-success btn-lg btn-block mt-4',
            'on_click': onclick
            })


    @component
    def error_message(error_message:str):
        if error_message:
            return html.p({'class_name': 'alert alert-danger'},
                html.strong(f"{error_message}")
            )
        return ""


    def choice_field(choice, i):

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
                        'value': f'{choice.id}'
                        }),
                    i
                    ))

    try:
        question: Question = qs.data[int(params['pk']) - 1]


        return html.div(
            link("Back To Polls", to='/polls/', class_name='btn btn-secondary btn-sm mb-3'),
            html.h1({'class_name': 'text-center mb-3'}, f"{question.question_text}"),
            error_message(error),

            Form(
                [choice_field(choice, i+1) for i, choice in enumerate(question.choice_set.all())],
                SubmitButton(question, model.choice)

            )

        )
    except Exception as error:
        return Page_404(str(error))
