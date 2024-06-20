import logging
from typing import Dict, Any
from channels.db import database_sync_to_async
from django.utils import timezone
from reactpy import component, event, html
from reactpy.core.events import EventHandler
from reactpy_django.hooks import use_query
from reactpy_router import use_params, link

from reactpy_forms import create_form, FormModel, use_form_state

from ..models import Question

EventArgs = Dict[str, Any]

log = logging.getLogger(__name__)

class ChoiceData(FormModel):
    choice: int = 0


async def get_questions():

    def query():
        return Question.objects.filter(pub_date__lte=timezone.now())

    return await database_sync_to_async(query)()

@component
def detail():

    model, set_model = use_form_state(ChoiceData())
    Form, Field = create_form(model, set_model)

    params = use_params()
    qs = use_query(get_questions)

    if qs.error:
        return html.h2(f"Error when loading - {qs.error}")
    elif qs.data is None:
        return html.h2("Loading...")

    @component
    def SubmitButton(model: FormModel):

        @event(prevent_default=True)
        def onclick(event: EventArgs):
            log.info(model)

        return html.input({
            'type': 'submit',
            'value': 'Vote',
            'class_name': 'btn btn-success btn-lg btn-block mt-4',
            'on_click': onclick
            })


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

    question = qs.data[int(params['pk']) - 1]
    error_message = None

    return html.div(
        link("Back To Polls", to='/polls/', class_name='btn btn-secondary btn-sm mb-3'),
        html.h1({'class_name': 'text-center mb-3'}, f"{question.question_text}"),
        # html.p({'class_name': 'alert alert-danger'},
        #     html.strong(f"{error_message}")
        # ),

        Form(
            [choice_field(choice, i+1) for i, choice in enumerate(question.choice_set.all())],
            SubmitButton(model)

        )

    )
