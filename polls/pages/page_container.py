from reactpy import component, html
from reactpy.core.types import VdomDictConstructor
from reactpy_router import link

from utils.types import Props


@component
def _navbar():
    return html.nav({'class_name': 'navbar navbar-dark bg-primary mb-4'},
        html.div({'class_name': 'container'},
            link(html.div({'class_name': 'btn navbar-brand'}, "Pollster"), to="/polls/"),
        ),

        html.ul({'class_name': 'navbar-nav ml-auto'},
            html.li({'class_name': 'nav-item'},
                html.a({'class_name': 'btn navbar-brand', 'href': '/admin/'}, "Admin")
            )
        )


    )

@component
def page_container(page: VdomDictConstructor, **props: Props):
    return html._(
        _navbar(),
        html.div({'class_name': 'container'},
            html.div({'class_name': 'row'},
                html.div({'class_name': '.col-md-6 m-auto'},
                    page(**props)
                )
            )
        )
    )
