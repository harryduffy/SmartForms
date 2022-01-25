from Generator.SmartForm import SmartForm
from dateutil.parser import parse
from Generator.PDF import PDF
from weasyprint import HTML

def get_pdf_and_sf(smartform_name, sql_session, sf, pdf):
    sfs = sql_session.query(SmartForm).all()

    for i in sfs:
        if i.title == smartform_name:
            sf = i

    pdfs = sql_session.query(PDF).all()

    for i in pdfs:
        if i.title == smartform_name:
            pdf = i

    return sf, pdf

def makepdf(html):
    
    htmldoc = HTML(string=html, base_url="")

    return htmldoc.write_pdf()

def is_date(string, fuzzy=False):

    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

