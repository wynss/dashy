import dashy.dashy as dy
import dashy.components as cp


layout = [
    cp.navbar('Hello Tabs!', dark=True),
    cp.button('Hover over me!', id='my-btn', pop_type='hover',
              pop_header='Pop pop', pop_body='pop message', pop_place='bottom')
]

app = dy.create_app('MyApp', layout=layout)


app.run(debug=True)
