from django.urls import reverse
from reactpy import component, html
from reactpy_router import link

from ..models import Question
from .common import use_query, LoadingException


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

    try:
        qs = use_query(Question.get_ordered_questions)
        if qs.data:
            return html.div(
                html.h1({'class_name':"text-center mb-3"},"Poll Questions"),
                *[QuestionCard(question) for question in qs.data]
                )
        else:
            return html.h2("No polls available.")
    except LoadingException as ex:
        return html.h2(str(ex))
