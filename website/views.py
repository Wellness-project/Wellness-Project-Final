from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
from links import words
import json
import requests
import mysql.connector
from configs import HOST, USER, PASSWORD
import matplotlib.pyplot as plt

# --- if using a Mac add these:
# import matplotlib
# matplotlib.use('Agg')
# ---

views = Blueprint('views', __name__)


@views.route("/mood", methods=['GET', 'POST'])  # creates a mood page by using the html document to create an interface
def mood():
    if request.method == "POST":
        selected_date = request.form.get('calendar')
        if selected_date == "":
            flash('Please select a date!', category='error')
        else:
            # mood levels in variables
            happiness = request.form.get("happiness")
            fitness = request.form.get("fitness")
            sleep = request.form.get("sleep")
            nutrition = request.form.get("nutrition")
            confidence = request.form.get("confidence")
            print('recorded user choices: {}, {}, {}'.format(happiness, fitness,sleep))
            if happiness == None or fitness == None or sleep == None or nutrition == None or confidence == None:
                flash('Please provide all answers!', category='error')
            else:
                class DBConnectionError(Exception):
                    pass
                # Method that connects with the database
                def connect_to_db(db_name):
                    cnx = mysql.connector.connect(
                        host=HOST,
                        user=USER,
                        password=PASSWORD,
                        auth_plugin='mysql_native_password',
                        database=db_name)
                    return cnx
                def update_mood():
                    try:
                        db_name = "journal"
                        db_connection = connect_to_db(db_name)
                        cur = db_connection.cursor()
                        print("connected to DB: %s" % db_name)
                        print(selected_date)
                        insert_entry = ("INSERT INTO mood_tracker (tracker_date, happiness, fitness, sleep, nutrition, confidence) VALUES (%s, %s, %s, %s,%s,%s)")
                        print('code ran past insert_entry')
                        print('insert_entry got these mood values: {}, {}, {},{}'.format(selected_date,happiness, fitness, sleep))
                        cur.execute(insert_entry, (selected_date, happiness, fitness, sleep, nutrition, confidence))
                        db_connection.commit()
                        print('code ran past commit insert_entry')

                    except Exception:
                        raise DBConnectionError("Failed to read data from DB")

                    finally:
                        if db_connection:
                            db_connection.close()
                            print("DB connection is closed")
                update_mood()

                # Method that plots a graph using the data in the SQL table
                def plot_graph():
                    try:
                        db_name = "journal"
                        db_connection = connect_to_db(db_name)
                        cur = db_connection.cursor()
                        print("connected to DB: %s" % db_name)

                        query = """SELECT tracker_date, ((happiness+fitness+sleep+nutrition+confidence)/5) AS average_mood FROM mood_tracker"""
                        cur.execute(query)
                        result = cur.fetchall()
                        mood_date = []
                        mood_average_for_date = []
                        # printing to test the query before plotting the graph
                        print("query to get average mood score has been passed into the database and executed")

                        for i in result:
                            mood_date.append(i[0])
                            mood_average_for_date.append(i[1])
                            # printing for testing the passed values
                            print("Date of mood tracking:", mood_date)
                            print("Average mood on dates tracked:", mood_average_for_date)
                        # to make a scatter plot
                        plt.scatter(mood_date,mood_average_for_date)
                        # OR instead to make a bar graph
                        # plt.bar(mood_date, mood_average_for_date)

                        plt.ylim(0, 5)
                        plt.xlabel("Date of mood tracking")
                        plt.ylabel("Average mood")
                        plt.title("Mood Tracker")
                        plt.show()
                        # check if the graph has been shown in a pop-up
                        print('the graph has been executed')

                        cur.close()
                    except Exception:
                        raise DBConnectionError("Failed to read data from DB")

                    finally:
                        if connect_to_db(db_name):
                            db_connection.close()
                            print("DB connection is closed")

                plot_graph()
                mood_levels = [happiness, fitness, sleep, nutrition, confidence]
                mood_levels = list(map(int, mood_levels))
                average_mood = sum(mood_levels) / len(mood_levels)
                # adding pictures to results.html
                if 0 <= average_mood <= 2.9:
                    f_mood_link = "https://i.guim.co.uk/img/static/sys-images/Guardian/Pix/pictures/2015/7/22/1437565470697/79a7f0ca-44be-408d-987e-e1a64bdd2bcc-894x1020.jpeg?width=445&quality=45&auto=format&fit=max&dpr=2&s=2128cd488153bbf781c8b93199e1838f"
                elif 2.9 < average_mood <= 3.9:
                    f_mood_link = "https://i.pinimg.com/originals/33/57/f3/3357f32aea8abce1b16fa1cb0842b9d3.png"
                elif 3.9 < average_mood <= 5:
                    f_mood_link = "https://i.pinimg.com/originals/ef/c6/d0/efc6d0936036326e4d3b46f79c3fc26a.jpg"

                def pic(mood_link):  # to pass into render_template
                    mood_pic = mood_link
                    return mood_pic

                def overall_mood(average_mood):
                    if 0 <= average_mood <= 2.9:
                        return "low"
                    elif 2.9 < average_mood <= 3.9:
                        return "average"
                    elif 3.9 < average_mood <= 5:
                        return "great!"

                return render_template("results.html", mood=overall_mood(average_mood), date=selected_date, user=current_user, mood_pic=pic(mood_link=f_mood_link))

    return render_template("mood.html", user=current_user)


# provides links to external resources in /external_resources endpoint
@views.route("/external_resources")
def external_resources():
    return render_template("external_resources.html", user=current_user)


# notes will be posted here
@views.route('/', methods=['GET', 'POST'])  # creates the home page by using the html document to create an interface
@login_required
def home():
    if request.method == 'POST':  # posts a note onto the server if it is more than 9 characters or flash error message
        selected_date = request.form.get('calendar')
        if selected_date == "":  # must select date first
            flash('Please select a date!', category='error')
        else:
            note = request.form.get('note')
            if len(note) < 9:  # 9 because date is already 8 characters
                flash('Note is too short!', category='error')
            else:
                new_note = Note(data=note, user_id=current_user.id, date=selected_date)
                db.session.add(new_note)
                db.session.commit()
                flash("Note added on: {}".format(selected_date), category='success')

            # checks to see if word in the notes is related to the links.py file, if so flash a warning.
            for word in words.keys():
                if word in note.lower():  # text in notes converted into lower case to be correctly picked
                    x = words[word]
                    flash(
                        "Please be advised to read the following webpage for more understanding about *{}* on this link {}".format(
                            word, x), category='error')


    return render_template("home.html", user=current_user)


# on /inspiration/ endpoint adds a quote and a cat picture from 2 APIs
@views.route('/inspiration/', methods=['GET'])
def inspire():
    response = requests.get("https://inspiration.goprogram.ai/")
    data = json.loads(response.content)
    quote = "{} - {}".format(data['quote'], data['author'])
    response2 = requests.get("https://api.thecatapi.com/v1/images/search")
    data2 = response2.json()
    cat = data2[0]['url']

    return render_template('inspire.html', data=quote, user=current_user, picture=cat)


@views.route('/delete-note', methods=['POST'])  # deletes note from the website
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
