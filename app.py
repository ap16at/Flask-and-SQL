
# Andrew Perez-Napan
# ap16at
# Due Date: 2-16-21
# The program in this file is the individual work of Andrew Perez-Napan


from flask import Flask, render_template, request
import sqlite3 as sql
import datetime
app = Flask(__name__)


# this displays the hompage but also reads in the form from the assReview page.
# any exception is rollbacked
# two insertion commands are used, one for each table
# for input is divided up into both tables
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            un = request.form['Username']
            res = request.form['Restaurant']
            fd = request.form['Food']
            ser = request.form['Service']
            am = request.form['Ambience']
            pr = request.form['Price']
            ovr = request.form['Overall']
            rev = request.form['Review']

            with sql.connect("reviewData.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO Reviews(Username,Restaurant,ReviewTime,Rating,Review) VALUES (?,?,?,?,?)", (un, res, datetime.datetime.utcnow(), ovr, rev))
                cur.execute("INSERT INTO Ratings(Restaurant,Food,Service,Ambience,Price,Overall) VALUES (?,?,?,?,?,?)", (res, fd, ser, am, pr, ovr))

                con.commit()
        except:
            con.rollback()

        finally:
            return render_template('index.html')
            con.close()
    else:
        return render_template('index.html')


# This page renders the form for adding a review to the table, the html page then sends the for to the index() function
@app.route('/addReview')
def new_review():
    return render_template('addReview.html')


# renders the template for the get review form
@app.route('/getReviews')
def get_reviews():
    return render_template('getReviews.html')


# reads in the input from the getReviews form
# that input is then used to find all the rows where the particular restaurant is stored
# the SELECT command is then used to display all the reviews for that restaurant
# a message is also sent to the html page so that the title will depend on the restaurant selected
@app.route('/showReviews', methods=['POST', 'GET'])
def show_reviews():
    if request.method == 'POST':
        res = request.form['Restaurant']
        resName = str(res)

        con = sql.connect("reviewData.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM Reviews WHERE Restaurant=?", (res,))
        rows = cur.fetchall()
        return render_template("showReviews.html", rows=rows, resName=resName)
    else:
        return render_template("showReviews.html")
            

# displays top ten restaurant
# SELECT command is used to get the restaurant as well as ...
# the averages of every rating
# the selection is ordered by the average of the Overall field
# if the Overall field is equal to another, then the selection ...
# is ordered alphabetically
# fetchmany() is then used to keep the selection to the top 10
@app.route('/top10')
def show_report():
    con = sql.connect("reviewData.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT Restaurant, AVG(Food) AS Food, AVG(Service) AS Service, AVG(Ambience) AS Ambience, AVG(Price) AS Price, AVG(Overall) AS Overall FROM Ratings GROUP BY Restaurant ORDER BY AVG(Overall) DESC, Restaurant")
    rows = cur.fetchmany(10)
    return render_template("showReport.html", rows=rows)


# if this is the main module, we run the application
if __name__ == '__main__':
    app.run(debug=True)
