from flask import Flask, render_template, request, redirect
import smtplib, ssl
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
        name = data['name']
        email = data['email']
        message = data['message']
        csv_writer = csv.writer(database2, delimiter=',', quotechar = ' ', quoting = csv.QUOTE_MINIMAL)
        csv_writer.writerow([name, email, message])

def send_email_message(data):
    try:
        name = data['name']
        email = data['email']
        sender_message = data['message']

        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = "portfo.no.reply@gmail.com"
        receiver_email = "seth.grinstead1@gmail.com"
        password = 'noreplypassword'
        message = f"""
        Name: {name}
        Email: {email}

        {sender_message}"""

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    except SMTPHeloError as e:
        return print(e)

@app.route('/submit_form', methods = ['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            send_email_message(data)
            return redirect('/thankyou.html')
        except:
            return 'message send unsuccessful'
    else:
        return 'something went wrong, try again'