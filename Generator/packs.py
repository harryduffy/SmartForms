from flask import render_template, Blueprint, flash, redirect, url_for, request, Markup, make_response, session
from .Pack import Pack
from .SmartForm import SmartForm
from .PDF import PDF
from Helpers.user_system import db
from Helpers.helper_functions import makepdf
import pickle
from flask_login import login_required, current_user


packs_blueprint = Blueprint("packs", __name__, static_folder="static", template_folder="templates")


@packs_blueprint.route("/my_packs", methods=["POST", "GET"])
@login_required
def my_packs():
    
    if request.method == "POST":

        if request.form["action"] == "+":

            title = request.form["pack-name"]
            session["title"] = title
            
            pack = Pack(title=title, smartforms=pickle.dumps([]), user=current_user.id)
            db.session.add(pack)
            db.session.commit()

            return redirect(url_for("packs.create_pack"))

        else:
            
            if request.form["action"] == "submit":
                pack_title = request.form["nm-pack"]
                session["pack-title"] = pack_title
                return redirect(url_for("packs.pack_document_generation"))
            
            else: 
                pack_title = request.form["nm-pack"]
                session["pack-title"] = pack_title

                return redirect(url_for("generator.sharing_forms", type_of="pack_document_generation"))

    packs = Pack.query.filter_by(user=current_user.id).all()

    return render_template("my_packs.html", packs=packs)

@packs_blueprint.route("/create_pack", methods=["POST", "GET"])
@login_required
def create_pack():

    pack_title = session["title"]
    pack = Pack.query.filter_by(title=pack_title, user=current_user.id).first()
    smartforms_loaded = pickle.loads(pack.smartforms)
    
    if request.method == "POST":
        
        if request.form["action"] == "submit":

            return redirect(url_for("packs.my_packs"))

        sf_name = request.form["nm-smartform"]

        if sf_name not in smartforms_loaded:
            sf = SmartForm.query.filter_by(title=sf_name, user=current_user.id).first()
            smartforms_loaded.append(sf)

            pack.smartforms = pickle.dumps(smartforms_loaded)

            db.session.add(pack)
            db.session.commit()
        else:
            flash("SmartForm already in pack.")

        pack.smartforms = pickle.dumps(smartforms_loaded)
       
    smartforms = SmartForm.query.filter_by(user=current_user.id).all()

    return render_template("create_pack.html", smartforms=smartforms)

@packs_blueprint.route(f"/pack_document_generation", methods=["POST", "GET"])
@login_required
def pack_document_generation():

    pack_title = session['pack-title']
    pack = Pack.query.filter_by(title=pack_title, user=current_user.id).first()
    smartforms = pickle.loads(pack.smartforms)

    if "iterator" not in session:
        session["iterator"] = 0
    
    sf = smartforms[session["iterator"]]
    pdf = PDF.query.filter_by(title=sf.title, user=current_user.id).first()

    if request.method == "POST":

        if request.form["action"] == "Next":
            if session["iterator"] >= len(smartforms) - 1:
                session["iterator"] = 0
            else:
                session["iterator"] = session["iterator"] + 1
            sf = smartforms[session["iterator"]]
            pdf = PDF.query.filter_by(title=sf.title, user=current_user.id).first()
            return render_template("smartform_requested.html", title=Markup(sf.title), content=Markup(sf.content), pack_form=True)
        else:
            rendered = render_template(f"pdf_formed.html", title=Markup(pdf.title), content=Markup(pdf.content))
            pdf = makepdf(rendered)
            response = make_response(pdf)
            response.headers["Content-Type"] = "flask_application/pdf"
            response.headers["Content-Disposition"] = f"attachment; filename={sf.title}.pdf"
            response.headers["X-Frame-Options"] = "SAMEORIGIN"
            return response

    return render_template("smartform_requested.html", title=Markup(sf.title), content=Markup(sf.content), pack_form=True)    