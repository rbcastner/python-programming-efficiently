
import flask, jinja2, io, base64
import stereo

app = flask.Flask(__name__)

template = jinja2.Template("""
<html>
  <body>
    <img src="data:image/png;base64,{{imgdata}}"/>
  </body>
</html>
""")

def makeimgdata(img):
    buffer = io.BytesIO()
    img.save(buffer,format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('ascii')

@app.route('/<sol>')
def getsol(sol):
    left, right = stereo.getday(sol).__next__()
    img = stereo.blend(stereo.getimage(left),stereo.getimage(right))
    
    html = template.render(imgdata=makeimgdata(img))
    
    return flask.Response(html)

@app.route('/')
def hello_world():
    return flask.Response('<html><body><p>Hello, world!</p></body></html>')

app.run(host='0.0.0.0')