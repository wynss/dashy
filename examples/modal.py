import dashy
import dashy.components as dc
from dash.exceptions import PreventUpdate


layout = [
    dc.button("Open modal", id="button"),
    dc.modal("A modal", id="modal", body_layout="Body", footer_layout="Footer"),
]
app = dashy.create_app(__name__, layout=layout)


@app.cb(("button", "n_clicks"), ("modal", "is_open"), ("modal", "is_open"))
def toggle_modal(clicks, is_open):
    if clicks == 0:
        raise PreventUpdate
    return not is_open


if __name__ == "__main__":
    app.launch()
