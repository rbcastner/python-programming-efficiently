
import flask, jinja2, base64
import marsmap

app = flask.Flask(__name__)

@app.route('/')
def hello_world():
    return flask.Response("<html><body><p>Load /XXXX to see Curiosity on Sol XXXX!</p></body></html>")

template = jinja2.Template("""
<html>
<body>
<img src="data:image/png;base64,{{imgdata}}" />
</body>
</html>""")

@app.route('/<sol>')
def getday(sol):
    try:
        lon, lat = marsmap.findcuriosity(sol)
        buffer = marsmap.plotcuriosity(lon,lat)
        img = base64.b64encode(buffer.getvalue()).decode('ascii')
        
        html = template.render(imgdata=img)

        return flask.Response(html)
    except:
        raise
        return flask.Response("<html><body><p>Sorry, I don't have that sol or something else went wrong!</p></body></html>")
    
app.run(host='0.0.0.0')