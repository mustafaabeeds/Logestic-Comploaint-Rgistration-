
from flask import Flask,render_template,request
import sqlite3

app = Flask(__name__)


# home page
@app.route("/")
def index():
    return render_template("home.html");


@app.route("/add")
def add():
    return render_template("complain.html")


# ADDCOMPLAIN FUNCTION TO RETRIEVE DETAILS FROM USER AND INSERT INTO DATABASE
@app.route("/addcomplain", methods=["POST"])
def addcomplain():
    msg = "msg"
    if request.method == "POST":
        try:

            #assigning the variables to value adding from user via home.html page
            NAME = request.form["name"]
            INVOICE_REFERENCE = request.form["invref"]
            INVOICE_DATE = request.form["invdate"]
            PRODUCT_NAME = request.form["pname"]
            NATURE_OF_COMPLAINT = request.form["nature"]
            # CONNECTING TO THE DATABASE
            with sqlite3.connect("complain.db") as con:
                cur = con.cursor()
                # INSERTING VALUES TO THE DATABASE
                cur.execute(
                    "INSERT into Complain (NAME, INVOICE_REFERENCE, INVOICE_DATE, PRODUCT_NAME, NATURE_OF_COMPLAINT) values (?,?,?,?,?)",
                    (NAME, INVOICE_REFERENCE, INVOICE_DATE, PRODUCT_NAME, NATURE_OF_COMPLAINT))
                con.commit()
                msg = "Complaint successfully Added"
                # METHOD TO RETRIEVE UNIQUE REGISTERATION NUMBER AND DISPLAY TO THE USER
                k = (cur.lastrowid)
                cur.execute('SELECT * from Complain WHERE UNIQUE_REF_NO=?', (k,))
                row1 = cur.fetchone()
                cur.close()
                return render_template("success_html.html", row1=row1)

        except:
            con.rollback()
            msg = "Complaint not Registered"
        finally:
            print("         SUCESSFULLY REGISTERED        ")

        # INPUT_ID FUNCTION TO RENDER VIEW.HTML FILE WHICH WILL TAKE REFERENCE NUMBER


@app.route("/input_id")
def input_id():
    return render_template("input.html")


# OUTPUT_ID FUNCTION WILL USE THAT REFERENCE NUMBER TO RETRIEVE DETAILS OF THE USER
@app.route("/output_id", methods=["POST"])
def output_id():
    if request.method == "POST":
        unir = request.form["uniref"]
        con = sqlite3.connect("Complain.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        # METHOD TO DISPLAY ONLY THAT ROW WHICH MATCHES UNIQUE REFERENCE NUMBER
        cur.execute('SELECT * from Complain WHERE UNIQUE_REF_NO=?', (unir,))
        rows = cur.fetchone()
        cur.close()
        # METHOD TO DISPLAY NO MATCH FOUND IF USER INPUTS INVALID REFERENCE NUMBER
        #display match fond
        if not rows:
            return render_template("no_match.html", rows=rows)
        else:
            return render_template("unique_id.html", rows=rows)


if __name__ == "__main__":
    app.run(debug = True)