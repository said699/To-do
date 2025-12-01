from flask import Flask, render_template
import psycopg2, os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'efjkt49u34923c23ruc3i34^£$B^£$%2c4£"4c!"445£$45vb4n543$52£c"£$23%!'
app.config['MAX_CONTENT_LENGTH'] = 5*1024*1024

@app.route('/')
def main():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)