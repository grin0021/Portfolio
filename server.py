from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

# @app.route('/')
# def my_home():
#     return render_template('index.html')

# @app.route('/works.html')
# def my_work():
#     return render_template('works.html')

# @app.route('/about.html')
# def about_me():
#     return render_template('about.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

def write_to_file(data):
    with open('database.txt', 'a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f'\n{email}, {subject}, {message}')

def write_to_csv(data):
    with open('./Portfolio/database.csv', mode = 'a', newline = '') as database2:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(database2, delimiter=',', quotechar = ' ', quoting = csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])

@app.route('/submit_form', methods = ['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/thankyou.html')
        except:
            return 'message send unsuccessful'
    else:
        return 'something went wrong, try again'