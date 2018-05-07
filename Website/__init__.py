from flask import Flask, redirect, url_for, request, render_template
import json
from flask_wtf import Form
from wtforms import TextField
from  NamesCode.Web_Fulfilling_Name_Request import main as get_names
app = Flask(__name__)
from NamesCode.Web_Name_Feedback import main as train_names

# # inputs name, pul, value modifier
# class Train_PULs(Form):
#    training = RadioField('training', choices = [('Good','good'),('Ok','ok'),('Bad','bad'),('Wrong','wrong')])
#    submit = SubmitField("Send")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/display/', methods = ['POST','GET'])
def display(PULs=None):
    PULs = request.args['PULs']  # counterpart for url_for()
    message = json.loads(PULs)
    if request.method == 'POST':
        #RadioField('training', choices=[('good','bad','ok','wrong')])
        train = request.form.get('training')
        modifier = 0
        if train == 'good':
            modifier = 2
        if train == 'ok':
            modifier = 1
        if train == 'bad':
            modifier = -2
        if train == 'wrong':
            modifier = -3
        print(train,modifier)
        return render_template('display.html', PULs=message)
    return render_template('display.html', PULs=message)

@app.route('/bot', methods = ['POST','GET'])
def bot():
    if request.method == 'POST':
        # do stuff when the form is submitted
        keyword = request.form['keyword']
        # name = request.form['nameword']
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        # os.system("Web_Fulfilling_Name_Request.py " + str(keyword))
        PULs = get_names(str(keyword))
        print(PULs)
        if PULs == "No Lines.":
            PULs = get_names("random")
            # Replace this with the categories later
        messages = json.dumps(PULs)
        return redirect(url_for('display',PULs=messages))

    # show the form, it wasn't submitted
    return render_template('bot.html')

# with app.test_request_context():
#     print(url_for('index'))
#     print( url_for('about'))


if __name__ == '__main__':
   app.run(debug = True)
