from flask import render_template, Blueprint, flash, redirect, url_for, request, Markup, session, make_response
from flask_login import login_required, current_user
from Helpers.helper_functions import makepdf, is_date
from Helpers.user_system import db, csrf
from Exceptions.exceptions import ContentNull, CSRFTokenMissingException
from .SmartForm import SmartForm
from .PDF import PDF

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

        print(request.form)

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

            print("here")

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


        return redirect(url_for("generator.sf_form"))

    return render_template("my_smartforms.html")

@generator_blueprint.route("/sf_form", methods=["POST", "GET"])
@login_required
def sf_form():

    if request.method == "POST":

        smartform_name = session["sf-title"]

        pdf = PDF.query.filter_by(title=smartform_name, user=current_user.id).first()

        form_data = list(request.form.values())
        form_data.remove("Generate PDF")
        
        if form_data[0] == csrf._get_csrf_token():
            form_data.pop(0)
        else:
            raise CSRFTokenMissingException('The CSRF Token is missing.')

        # split form data into dates, addresses etc
        form_dict = request.form.to_dict(flat=False)

        form_dates = []
        for i in form_data:
            if is_date(i):
                form_dates.append(i)
                form_data.remove(i)

        form_short_inline = []
        form_short_break = []
        for i in form_dict:
            j = form_dict[i]
            try:
                if i.split("-")[1] == "short":
                    if i.split("-")[0] == "inline":
                        form_short_inline.append(j[0])
                    else:
                        form_short_break.append(j[0])
            except IndexError as e:
                print("Error: " + str(e))

        form_addresses_inline = []
        form_addresses_break = []
        for i in form_dict:
            j = form_dict[i]
            try:
                if i.split("-")[1] == "address":
                    if i.split("-")[0] == "inline":
                        form_addresses_inline.append(j[0])
                    else:
                        form_addresses_break.append(j[0])
            except IndexError as e:
                print("Error: " + str(e))

        form_lists_inline = []
        form_lists_break = []
        for i in form_dict:
            j = form_dict[i]
            try:
                print(i.split("-"))
                if i.split("-")[1] == "lists":
                    if i.split("-")[0] == "inline":
                        form_lists_inline.append(j[0])
                    else:
                        form_lists_break.append(j[0])
            except IndexError as e:
                print("Error: " + str(e))

        print(form_lists_inline)
        print(form_lists_break)

        content = pdf.content

        # replacing all the short question answers
        count = 0
        while count <= len(form_short_break) - 1:
            
            element = '<div style="display: block">' + form_short_break[count] + '</div>'
            content = content.replace(" <div id='text-question-answer' style='color: #808080; display: block;'><i>->text question answer<-</i></div> ", element, 1)
            count += 1

        count = 0
        while count <= len(form_short_inline) - 1:
            
            content = content.replace(" <div id='text-question-answer' style='color: #808080; display: inline;'><i>->text question answer<-</i></div> ", form_short_inline[count], 1)
            count += 1

        # # replacing all the date questions
        count = 0
        while count <= len(form_dates) - 1:

            content = content.replace(f" <div id='date-question-answer' style='color: #808080; display: inline;'><i>->date answer<-</i></div> ", form_dates[count], 1)
            count += 1

        # # replacing all the address questions
        count = 0
        while count <= len(form_addresses_inline) - 1:

            content = content.replace(" <div id='address-question-answer' style='color: #808080; display: inline;'><i>->address answer<-</i></div> ", form_addresses_inline[count], 1)
            count += 1

        count = 0
        while count <= len(form_addresses_break) - 1:

            element = '<div style="display: block">' + form_addresses_break[count] + '</div>'
            content = content.replace(" <div id='address-question-answer' style='color: #808080; display: block;'><i>->address answer<-</i></div> ", element, 1)
            count += 1

        count = 0
        while count <= len(form_addresses_inline) - 1:

            content = content.replace(" <div id='list-question-answer' style='color: #808080; display: block;'><i>->list answer<-</i></div> ", form_lists_inline[count], 1)
            count += 1

        count = 0
        while count <= len(form_lists_break) - 1:
            
            element = '<div style="display: block">' + form_lists_break[count] + '</div>'
            content = content.replace(" <div id='lists-question-answer' style='color: #808080; display: block;'><i>->list answer<-</i></div> ", element, 1)
            count += 1

        count = 0
        while count <= len(form_lists_inline) - 1:

            content = content.replace(" <div id='lists-question-answer' style='color: #808080; display: inline;'><i>->list answer<-</i></div> ", form_lists_inline[count], 1)
            count += 1
            
        rendered = render_template(f"pdf_formed.html", title=Markup(session["pdf-title"]), content=Markup(content))
        
        pdf = makepdf(rendered)
        response = make_response(pdf)
        response.headers["Content-Type"] = "flask_application/pdf"
        response.headers["Content-Disposition"] = f"attachment; filename={smartform_name}.pdf"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"

        return response

    return render_template(f"smartform_requested.html", title=Markup(session["sf-title"]), content=Markup(session["sf-content"]))