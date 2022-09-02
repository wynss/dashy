import dashy.dashy as dy
import dashy.components as dc


layout = [
    dc.navbar("Hello Tabs!", dark=True),
    dc.button(
        "Hover over me!",
        id="my-btn",
        popover_trigger="hover",
        popover_header="Pop pop",
        popover_body="pop message",
        popover_placement="bottom",
    ),
]

app = dy.create_app("MyApp", layout=layout)


app.run(debug=True)
