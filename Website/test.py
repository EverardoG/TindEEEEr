from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/about')
def about():
    return 'The about page'

@app.route('/feedback')
def feedback():
    return hello.html

@app.route('/bot')
def bot():
    return render_template('bot.html', name=name)

@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

if __name__ == '__main__':
   app.run(debug = True)

if __name__ == '__main__':
    app.run(debug=True)
