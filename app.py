from flask import Flask, render_template, request, session, redirect
import random
from database import logg_inn, opprett_bruker, sebokbestillinger, delete_bestillinger, admin_info, highscore

app = Flask(__name__)

app.secret_key = "idkmaaaan"

bruker = None

@app.context_processor
def current_user():
    
    return dict(username=session.get('username'), role=session.get('role'), logg_inn=session.get('logginn'))
@app.route('/')
def home():
    return render_template("index.html")

@app.errorhandler(404)
def error(error_code):
    return render_template("404.html"), 404

@app.route('/admin')
def admin():
    if session.get('role') == 'admin':
        bruker_info = admin_info()
        brukere = len(bruker_info)

        return render_template("admin.html", bruker_info=bruker_info, brukere=brukere)
    else:
        return render_template("index.html"), 401
    
@app.route('/logginn')
def logginn():
    return render_template("logginn.html")
    



@app.route('/loggut')
def loggut():
    global bruker 
    session.clear()
    bruker = None
    
    return redirect('/logginn')

@app.route('/sebestillinger')
def sebestillinger():
    if session.get('email'):
        try:
            bokbestillingliste = sebokbestillinger()
            bok_id = len(bokbestillingliste[0])
            print(bok_id) 
        
            return render_template("sebestillinger.html", bestilling_liste=bokbestillingliste, bok_id=bok_id)
        except TypeError:
            return "Logg inn for å se bestillinger"
    else:
        tilbakemelding = "Logg inn for å se bestillinger" 
        return render_template("logginn.html", tilbakemelding_registrering=tilbakemelding)
    

@app.route('/sebestillinger', methods=['GET', 'POST'])
def slett_bestillinger():
    if request.method == "POST":
        bok_id = request.form.get("bok")
        delete_bestillinger(bok_id)


@app.route('/registrer')
def registrer():
    liste = []
    for i in range(100):
        tall = random.randint(0, 100)
        liste.append(tall)
    return render_template("registrer.html", tall_liste=liste)

@app.route('/registrer', methods=['GET', 'POST'])
def hent_registrering():
    global navn,etternavn,email
    if request.method == 'POST':
        navn = request.form['navn']
        etternavn = request.form['etternavn']
        email = request.form['email']
        passord = request.form['passord'] 
        role = request.form.get('role')
        admin_passord = request.form.get('admin_passord')
        if admin_passord == "admin123":
            tilbakemelding_registrering = opprett_bruker(navn, etternavn, email, passord, role)
        else:
            tilbakemelding_registrering = opprett_bruker(navn, etternavn, email, passord)

        return render_template("registrer.html", tilbakemelding_registrering=tilbakemelding_registrering)
       

@app.route('/logginn', methods=['GET', 'POST'])
def hent_logginn():
    global bruker
    if request.method == 'POST':
        email = request.form['email']
        passord = request.form['passord']
        tilbakemelding_registrering = logg_inn(email, passord)
        bruker = tilbakemelding_registrering
        if bruker == "Feil email eller passord.":
            return render_template("logginn.html", tilbakemelding_registrering=tilbakemelding_registrering)
        else:
           
            session["email"] = email
            session["role"] = bruker[2]
            session["username"] = bruker[3]
            session["logginn"] = True
            tilbakemelding_registrering = "Innlogging vellyket"
            return render_template("logginn.html", tilbakemelding_registrering=tilbakemelding_registrering)
        
@app.route('/global')
def global_score():
    global_highscore = highscore()

    highscore_liste = len(global_highscore)

    return render_template("global.html", global_highscore=global_highscore, highscore_liste=highscore_liste)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)
