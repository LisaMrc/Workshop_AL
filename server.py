# -*- coding: utf-8 -*-
from flask import Flask,request,render_template,jsonify,abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#les absences, c'est pour un dictionnaire qui pour un entier donne le nom et le nombre d'absences
# structure absences : { 1:{'nom':'toto', 'abs':3}, 2:{'nom':'bob', 'abs':3} }
cpt=0
absences={}

@app.route("/")
def index():
    return render_template('userDives.html')

@app.route("/absences", methods=['GET', 'POST'])
def general():
    if request.method == 'POST':
        nom = request.json['nom']
        # On vérifie d'abord si ce n'est pas déjà présent
        for eleve in absences.values():
        	if eleve['nom'] == nom:
        	    return jsonify(absences),409
        # OK on ajoute
        global cpt
        cpt=cpt+1 
        absences[cpt]={'nom':nom, 'abs':1} 
    return jsonify(absences), 201;

@app.route("/absence/<int:id>", methods=[ 'PUT', 'DELETE'])
def abs(id):
    if request.method == 'PUT':
        if id in absences:
            absences[id]['abs']=absences[id]['abs']+1
        else:
            abort(404)
    else:
        if id in absences:
            absences[id]['abs']=absences[id]['abs']-1
            if absences[id]['abs'] == 0:
                del(absences[id])
        else:
            abort(404)
    	# et au final on retourne tout le json    
    return jsonify(absences);

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
