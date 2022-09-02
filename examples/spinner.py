from time import sleep

import dashy.dashy as dy
import dashy.components as dc


layout = [
    dc.navbar("Hello Spinners!", dark=True, color="secondary"),
    dc.button("Spin me!", id="my-btn", spinner_div_id="spinner"),
]

app = dy.create_app("MyApp", layout=layout, theme=dy.dbc.themes.SUPERHERO)


@app.cb(("my-btn", "n_clicks"), ("spinner", "children"))
def switch_tabs(_):
    sleep(200)
    return ""


app.run()
