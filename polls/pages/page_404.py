from reactpy import component, html
from utils.inline_style import inline_style

STYLE = """
 .error-page {
      display: flex;
      text-align: center;
      align-items: center;
      height: 100vh;
      margin: 0;
}
"""

@component
def Page_404(msg: str):
    return html.div({'class_name': 'container error-page'},
        inline_style(STYLE),
        html.article(
            html.header(
                html.h1("404 Not Found"),
            ),
            html.h5("Sorry, the page you're looking for doesn't exist."),
            html.h5(f"{msg}"),
            html.a({'href': '/', 'role': 'button', 'class_name': 'outline'}, html.h5("Go to Home Page"))
        )
    )
    