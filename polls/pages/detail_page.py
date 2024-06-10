from channels.db import database_sync_to_async
from django.utils import timezone
from reactpy import component, html
from reactpy_django.hooks import use_query
from reactpy_router import use_params, link

from ..models import Question


def url(path:str, args):
    return ""

async def get_questions():

    def query():
        return Question.objects.filter(pub_date__lte=timezone.now())

    return await database_sync_to_async(query)()

@component
def detail():

    @component
    def ChoiceElement(choice, counter):
        return html.div({'class_name': 'form-check'},
            html.input({'type': 'radio', 'name': 'choice', 'class_name': 'form-check-input', 'id': f'choice{counter}', 'value': f'{choice.id}'}),
            html.label({'html_for': f'choice{counter }'}, f"{choice.choice_text}")
        )

    params = use_params()
    qs = use_query(get_questions)

    if qs.error:
        return html.h2(f"Error when loading - {qs.error}")
    elif qs.data is None:
        return html.h2("Loading...")

    question = qs.data[int(params['pk']) - 1]
    error_message = None

    return html.div(
        link("Back To Polls", to='/polls/', class_name='btn btn-secondary btn-sm mb-3'),
        html.h1({'class_name': 'text-center mb-3'}, f"{question.question_text}"),
        # html.p({'class_name': 'alert alert-danger'},
        #     html.strong(f"{error_message}")
        # ),

        html.form({'action': "{% url 'polls:vote' question.id %}", 'method': 'post'},

            [ChoiceElement(choice, i+1) for i, choice in enumerate(question.choice_set.all())],

            html.input({'type': 'submit', 'value': 'Vote', 'class_name': 'btn btn-success btn-lg btn-block mt-4'})
        )
    )
