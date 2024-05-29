from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses = []

@app.route('/')
def show_start():
    """shows title of survey, the instructions, and button to start the survey"""
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("start_survey.html", title=title, instructions=instructions)

@app.route('/new-survey')
def empty_responses():
    """creates a new survey by emptying responses"""
    responses.clear()
    return redirect('/questions/0')

@app.route('/questions/<int:id>')
def show_question(id):
    """shows the current question and answer options"""
    if id != len(responses):
        flash("Invalid question id.")
        return redirect(f"/questions/{len(responses)}")
    if id == len(satisfaction_survey.questions) == len(responses):
        flash("Survey has been completed")
        return redirect('/complete')
    
    question = satisfaction_survey.questions[id]
    return render_template('questions.html', question=question)

@app.route('/answer', methods = ["POST"])
def add_response():
    """appends the answer to the responses list"""
    response = request.form["option"]
    responses.append(response)
    
    if len(responses) < len(satisfaction_survey.questions):
        return redirect(f"/questions/{len(responses)}")
    else:
        return redirect("/complete")

@app.route('/complete')
def thank_user():
    """thanks the user once survey is complete"""
    return render_template('complete.html')


