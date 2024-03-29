from flask import render_template, Blueprint, flash, redirect, url_for, request, Markup, make_response, session
from flask_login import login_required, current_user
from Helpers.helper_functions import makepdf, is_date, replace_table, holder_replacer
from Helpers.user_system import db, csrf, serialiser
from Helpers.Email import Email
from Exceptions.exceptions import ContentNull, CSRFTokenMissingException
import pickle
import secrets
from .SmartForm import SmartForm
from .PDF import PDF
from .Pack import Pack

generator_blueprint = Blueprint("generator", __name__, static_folder="static", template_folder="templates")

@generator_blueprint.route("/initial_form", methods=["POST", "GET"])
@login_required
def initial_form():
    
    if request.method == "POST":

        smartform_name = request.form["name"]
        session["smartform-name"] = smartform_name

        smartform = SmartForm.query.filter_by(title=smartform_name, user=current_user.id).first()

        if smartform:
            flash("Error: SmartForm with that name already exists.")
            return redirect(url_for("generator.initial_form"))

        else: 
            new_smartform = SmartForm(user=current_user.id, title=smartform_name)
            new_pdf = PDF(user=current_user.id, title=smartform_name)

            new_smartform.init_imitator()
            new_pdf.init_imitator()

            db.session.add(new_smartform)
            db.session.add(new_pdf)
            db.session.commit()

        return redirect(url_for("generator.generator"))

    return render_template("initial_form.html")

@generator_blueprint.route("/generator", methods=["POST", "GET"])
@login_required
def generator():
    
    smartform_name = session["smartform-name"]
    
    sf = SmartForm.query.filter_by(title=smartform_name, user=current_user.id).first()
    pdf = PDF.query.filter_by(title=smartform_name, user=current_user.id).first()
        
    if request.method == "POST":

        try:
            action = request.form["action"]
        except KeyError:
            action = 'table-question'
        
        if action == "short-question":

            question = request.form["short-question"]

            if request.form["inline"] == "inline":
                pdf.add_text_answer_holder(True)
                sf.add_short_question_input(question, True)
            else:
                pdf.add_text_answer_holder(False)
                sf.add_short_question_input(question, False)

            db.session.add(sf)
            db.session.add(pdf)
            db.session.commit()

        elif action == "list-question":

            question = request.form["list-question"]
            amount = request.form["list-options-number"]
            options = request.form["list-options"]
            options = options.split(", ")

            if request.form["inline"] == "inline":
                pdf.add_list_answer_holder(True)
                sf.add_list_question_input(question, options, amount, True)
            else:
                pdf.add_list_answer_holder(False)
                sf.add_list_question_input(question, options, amount, False)

            db.session.add(sf)
            db.session.add(pdf)
            db.session.commit()
            
        elif action == "long-question":

            question = request.form["long-question"]
            sf.add_long_question_input(question)
            pdf.add_text_answer_holder()
            db.session.add(sf)
            db.session.add(pdf)
            db.session.commit()

        elif action == "table-question":

            rows = request.form["table-rows"]
            cols = request.form["table-cols"]

            session["rows"] = rows
            session["cols"] = cols

            pdf.add_table_holder(rows, cols)

            db.session.add(sf)
            db.session.add(pdf)
            db.session.commit()

        elif action == "date-question":

            question = request.form["date-question"]

            if request.form["inline"] == "inline":
                pdf.add_date_holder(True)
                sf.add_date_input(question, True)
            else:
                pdf.add_date_holder(False)
                sf.add_date_input(question, False)

            db.session.add(sf)
            db.session.add(pdf)
            db.session.commit()

        elif action == "address-question":

            question = request.form["address-question"]

            if request.form["inline"] == "inline":
                pdf.add_address_holder(True)
                sf.add_address_input(question, True)
            else:
                pdf.add_address_holder(False)
                sf.add_address_input(question, False)

            db.session.add(sf)
            db.session.add(pdf)
            db.session.commit()

        # elif action == "CheckBox Question":

        #     question = request.form["question-text"]
        #     text_on = request.form["text-on"]
        #     text_off = request.form["text-off"]
        #     pdf.add_boolean_text(text_on, text_off)
        #     pdf.add_checkbox_holder()
        #     sql_session.add(pdf)
        #     sf.add_boolean_input(question)
        #     sql_session.add(sf)
        #     sql_session.commit()

        elif action == "pdf-text":

            content = request.form["pdf-text"]
            pdf.add_text(content)
            db.session.add(pdf)
            db.session.commit()

        elif action == "clear-all":
            pdf.clear_content()
            sf.clear_content()
            db.session.add(sf)
            db.session.add(pdf)
            db.session.commit()

        elif action == "generate-smartform":

            db.session.add(sf)
            db.session.add(pdf)
            db.session.commit()

            flash("SmartForm successfully created!")
            return redirect(url_for("generator.my_smartforms"))

        return render_template("generator.html", smartform_title=smartform_name, sf_content=Markup(sf.content), pdf_content=Markup(pdf.content))
    
    if smartform_name == None or sf.content == None or pdf.content == None:
        raise ContentNull(f'''Generator content is null: \nSmartForm Name: {smartform_name}, \nSmartForm Content: {sf.content}, \nPDF Content: {pdf.content}''')

    else:
        return render_template("generator.html", smartform_title=smartform_name, sf_content=Markup(sf.content), pdf_content=Markup(pdf.content))

@generator_blueprint.route("/sf_form", methods=["POST", "GET"])
@login_required
def sf_form():

    if request.method == "POST":

        if request.form["action"] == "Generate PDF":
            smartform_name = session["sf-title"]
            pdf = PDF.query.filter_by(title=smartform_name, user=current_user.id).first()
            
            form_data = list(request.form.values())
            form_data.remove("Generate PDF")
            
            if form_data[0] == csrf._get_csrf_token():
                form_data.pop(0)
            else:
                raise CSRFTokenMissingException('The CSRF Token is missing.')

            form_dict = request.form.to_dict(flat=False)

            content = pdf.content

            content = holder_replacer(form_dict, content, "text")
            content = holder_replacer(form_dict, content, "address")
            content = holder_replacer(form_dict, content, "list")
            content = holder_replacer(form_dict, content, "date")

            form_dates = []
            for i in form_data:
                if is_date(i):
                    form_dates.append(i)
                    form_data.remove(i)

            count = 0
            while count <= len(form_dates) - 1:

                content = content.replace(f" <div id='date-question-answer' style='color: #808080; display: inline;'><i>->date answer<-</i></div> ", form_dates[count], 1)
                count += 1

            session["updated-content"] = content
                
            return redirect(url_for('generator.preview'))

        else:
            return redirect(url_for("generator.sharing_forms", type_of="sf_form"))

    return render_template(f"smartform_requested.html", title=Markup(session["sf-title"]), content=Markup(session["sf-content"]))

@generator_blueprint.route("/preview", methods=["POST", "GET"])
def preview():

    smartform_name = session["sf-title"]
    try:
        pdf = PDF.query.filter_by(title=smartform_name, user=current_user.id).first()
    except AttributeError:
        user_id = session['user_id']
        pdf = PDF.query.filter_by(title=smartform_name, user=user_id).first()
    
    
    updated_content = session["updated-content"]

    if request.method == "POST":

        form_dict = request.form.to_dict(flat=False)
        
        if list(form_dict.keys())[0] == 'csrf_token':
            if form_dict['csrf_token'][0] == csrf._get_csrf_token():
                form_dict.pop('csrf_token')
            else:
                raise CSRFTokenMissingException('The CSRF Token is missing.')

        updated_content = replace_table(updated_content, form_dict)

        rendered = render_template(f"pdf_formed.html", title=Markup(pdf.title), content=Markup(updated_content))
        
        pdf = makepdf(rendered)
        response = make_response(pdf)
        response.headers["Content-Type"] = "flask_application/pdf"
        response.headers["Content-Disposition"] = f"attachment; filename={smartform_name}.pdf"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"

        return response

    

    return render_template("preview.html", title=Markup(pdf.title), content=Markup(updated_content))

@generator_blueprint.route("/my_smartforms", methods=["POST", "GET"])
@login_required
def my_smartforms():
    
    if request.method == "POST":

        smartform_name = request.form["smartform-name"]

        sf = SmartForm.query.filter_by(title=smartform_name, user=current_user.id).first()
        pdf = PDF.query.filter_by(title=smartform_name, user=current_user.id).first()
        
        session["pdf-content"] = pdf.content
        session["pdf-title"] = pdf.title
        session["sf-content"] = sf.content
        session["sf-title"] = sf.title
        session["url-access-token"] = serialiser.dumps({'user_id': current_user.id, 'title': sf.title}).decode('utf-8')

        return redirect(url_for("generator.sf_form", token=session["url-access-token"]))

    smartforms = SmartForm.query.filter_by(user=current_user.id).all()

    return render_template("my_smartforms.html", smartforms=smartforms)

@generator_blueprint.route(f"/sharing_forms/<type_of>", methods=["POST", "GET"])
@login_required
def sharing_forms(type_of):

    email = Email("Harry Duffy", "0450322069", "Project Analyst")
    if type_of == 'pack_document_generation':
        token = serialiser.dumps({'user_id': current_user.id, 'title': session["pack-title"], 'type': type_of}).decode('utf-8')
    else:
        token = serialiser.dumps({'user_id': current_user.id, 'title': session["sf-title"], 'type': type_of}).decode('utf-8')
    one_time_link = f"https://smartforms-app.herokuapp.com/generator/shared_resource/" + token
    body = f'''<p>Here is the one time link to access the document forms: <a href="{one_time_link}">link</a></p>'''

    if request.method == "POST":

        receiver = request.form["receiver"]
        email.send_email("Documents", body, receiver)

    return render_template("sharing_forms.html")

@generator_blueprint.route("/shared_resource/<token>", methods=["POST", "GET"])
def shared_resource(token):

    data = serialiser.loads(token)
    title = data['title']
    type_of = data['type']
    user_id = data['user_id']
    session['user_id'] = user_id

    if type_of == "pack_document_generation":
        pack = Pack.query.filter_by(title=title, user=user_id).first()
        smartforms = pickle.loads(pack.smartforms)

        if "iterator" not in session:
            session["iterator"] = 0
        
        sf = smartforms[session["iterator"]]
        pdf = PDF.query.filter_by(title=sf.title, user=user_id).first()

        if request.method == "POST":

            if request.form["action"] == "Next":
                if session["iterator"] >= len(smartforms) - 1:
                    session["iterator"] = 0
                else:
                    session["iterator"] = session["iterator"] + 1
                sf = smartforms[session["iterator"]]
                pdf = PDF.query.filter_by(title=sf.title, user=user_id).first()
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
    
    
    else:

        sf = SmartForm.query.filter_by(title=title, user=user_id).first()
        session['sf-title'] = sf.title

        if request.method == "POST":

            if request.form["action"] == "Generate PDF":

                pdf = PDF.query.filter_by(title=title, user=user_id).first()

                form_data = list(request.form.values())
                form_data.remove("Generate PDF")
                
                if form_data[0] == csrf._get_csrf_token():
                    form_data.pop(0)
                else:
                    raise CSRFTokenMissingException('The CSRF Token is missing.')

                form_dict = request.form.to_dict(flat=False)

                content = pdf.content

                content = holder_replacer(form_dict, content, "text")
                content = holder_replacer(form_dict, content, "address")
                content = holder_replacer(form_dict, content, "list")
                content = holder_replacer(form_dict, content, "date")

                form_dates = []
                for i in form_data:
                    if is_date(i):
                        form_dates.append(i)
                        form_data.remove(i)

                count = 0
                while count <= len(form_dates) - 1:

                    content = content.replace(f" <div id='date-question-answer' style='color: #808080; display: inline;'><i>->date answer<-</i></div> ", form_dates[count], 1)
                    count += 1

                session["updated-content"] = content
                    
                return redirect(url_for('generator.preview'))

        return render_template(f"smartform_requested.html", title=Markup(sf.title), content=Markup(sf.content))

