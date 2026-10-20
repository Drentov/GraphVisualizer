from flask import Flask, render_template
import mimetypes
mimetypes.add_type('text/javascript', '.js') #needed so flask loads JS code correctly

app = Flask(__name__, template_folder="frontend", static_folder="frontend/static")

@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
