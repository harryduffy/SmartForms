from dateutil.parser import parse
from weasyprint import HTML

def makepdf(html):
    
    htmldoc = HTML(string=html, base_url="")

    return htmldoc.write_pdf()

def is_date(string, fuzzy=False):

    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def holder_replacer(form_dict, content, type):

    inline_list = []
    break_list = []
    for i in form_dict:
        j = form_dict[i]
        try:
            if i.split("-")[1] == type:
                if i.split("-")[0] == "inline":
                    inline_list.append(j[0])
                else:
                    break_list.append(j[0])\
                        
        except IndexError as e:
            print("Error: " + str(e))

    count = 0
    while count <= len(break_list) - 1:
        
        element = '<div style="display: block">' + break_list[count] + '</div>'
        content = content.replace(f" <div class='{type}-question-answer' style='color: #808080; display: block;'><i>->{type} answer<-</i></div> ", element, 1)
        count += 1

    count = 0
    while count <= len(inline_list) - 1:
        
        content = content.replace(f" <div class='{type}-question-answer' style='color: #808080; display: inline;'><i>->{type} answer<-</i></div> ", inline_list[count], 1)
        count += 1

    return content

def create_table(rows, cols, form_dict={}):
    
    tableHTML = "<div class='final-table'><table cellspacing='0'>"

    values = list(form_dict.values())
    
    string_values = []
    for value in values:
        string_values.append(value[0])
    
    i = 1
    cell_counter = 0
    while i <= rows: 
        tr = '<tr>'
        td = ''

        j = 1
        while j <= cols:
            
            if form_dict == {}:
                td = f'<td><input type="text" placeholder="Answer..." name="td-{cell_counter}"/></td>'
            else:
                td = f'<td>{string_values[cell_counter]}</td>';
    
            tr += td

            j += 1
            cell_counter += 1
    
        tr += '</tr>'
        tableHTML += tr

        i += 1
            

    tableHTML += '</table></div>'

    return tableHTML

def replace_table(table, content, form_dict):

    new_content = content

    values = list(form_dict.values())
    
    string_values = []
    for value in values:
        string_values.append(value[0])

    cell_counter = len(string_values)
    iterator = 0
    while iterator <= cell_counter - 1:
        
        replacement_string = f'<input type="text" placeholder="Answer..." name="td-{iterator}"/>'
        replacement_value = string_values[iterator]

        new_content = new_content.replace(replacement_string, replacement_value)

        iterator += 1    

    return new_content