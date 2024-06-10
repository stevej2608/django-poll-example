from channels.db import database_sync_to_async
from django.utils import timezone
from reactpy import component, html
from reactpy_django.hooks import use_query
from reactpy_router import use_params, link

from ..models import Question

async def get_questions():

    def query():
        return Question.objects.filter(pub_date__lte=timezone.now())

    return await database_sync_to_async(query)()


@component
def results():

    @component
    def ChoiceVote(choice):

        def pluralize(count):
            return "s" if count != 1 else ""

        return html.li({'class_name': 'list-group-item'},
            f"{choice.choice_text}",
            html.span({'class_name': 'badge badge-success float-right'}, f"{choice.votes} vote{pluralize(choice.votes)}")
        )

    params = use_params()
    qs = use_query(get_questions)

    if qs.error:
        return html.h2(f"Error when loading - {qs.error}")
    elif qs.data is None:
        return html.h2("Loading...")

    pk = int(params['pk']) - 1

    question = qs.data[pk]


    return html.div(
        html.h1({'class_name': 'mb-5 text-center'}, f"{question.question_text}"),
        html.ul({'class_name': 'list-group mb-5'},

            [ChoiceVote(choice) for choice in question.choice_set.all()],

        ),

        html.div({'class_name':'btn-group'},
            link("Back To Polls", to='/polls/', class_name='btn btn-secondary  mx-1'),
            link("Vote again?", to=f'/polls/detail/{pk}/', class_name='btn btn-dark'),
        ),

    )
