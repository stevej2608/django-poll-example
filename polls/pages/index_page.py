from channels.db import database_sync_to_async
from django.utils import timezone
from django.urls import reverse
from reactpy import component, html
from reactpy_django.hooks import use_query
from reactpy_router import link

from ..models import Question


def url(path:str, args):
    return ""

async def get_questions():

    def query():
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

    return await database_sync_to_async(query)()


@component
def index():

    @component
    def QuestionCard(question):
        return html.div({'class_name': 'card-mb-3'},
            html.div({'class_name': 'card-body'},
                html.p({'class_name': 'lead'}, question.question_text),
                html.div({'class_name':'btn-group'},
                    link("Vote Now", to=reverse("polls:detail", kwargs={'pk': question.pk}), class_name='btn btn-primary btn-sm  mx-1'),
                    link("Results", to=reverse("polls:results", kwargs={'pk': question.pk}), class_name='btn btn-secondary btn-sm'),
                )
            )
        )

    qs = use_query(get_questions)

    if qs.error:
        return html.h2(f"Error when loading - {qs.error}")
    elif qs.data is None:
        return html.h2("Loading...")

    if qs.data:
        return html.div(
            html.h1({'class_name':"text-center mb-3"},"Poll Questions"),
            *[QuestionCard(question) for question in qs.data]
            )
    else:
        return html.h2("No polls available.")
