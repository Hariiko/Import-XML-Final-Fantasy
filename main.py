import json
import re

def addcard(theset, name, code, pt, text, card_type, colors, cost, file):
    code_for_image = code

    if re.search('pr', code.lower()):
        code = code
    else:
        code = code

    file.write('    <card>\n')
    file.write('      <name>{} ({})</name>\n'.format(name, code))
    file.write('      <text>{}</text>\n'.format(prettyTrice(text)))
    file.write('      <prop>\n')
    file.write(card_type)
    file.write('        <manacost>{}</manacost>\n'.format(prettyTrice(cost)))
    # Asegúrate de que colors sea una lista
    if colors is None:
        colors = []
    file.write('        <colors>{}</colors>\n'.format(', '.join(prettyTrice(color) for color in colors)))
    file.write('        <pt>{}</pt>\n'.format(pt))
    file.write('      </prop>\n')
    file.write('      <set picurl="{}">{}</set>\n'.format(getimageURL(code_for_image), theset))
    file.write('      <tablerow>{}</tablerow>\n'.format(
        '0' if 'Backup' in card_type 
        else '2' if 'Forward' in card_type 
        else '3' if re.search(r'\bSummon\b', card_type) 
        else '1'
    ))
    file.write('    </card>\n')

def addset(theset, file):
    file.write('    <set>\n')
    file.write('      <name>{}</name>\n'.format(theset))
    file.write('      <longname>{}</longname>\n'.format(theset))
    file.write('      <settype>Custom</settype>\n')
    file.write('      <releasedate></releasedate>\n')
    file.write('    </set>\n')

def loadJson(filepath):
    """Carga los datos JSON desde un archivo dado y devuelve la lista de tarjetas."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError as e:
        print(f"Error: El archivo no se encontró: {e}")
    except json.JSONDecodeError as e:
        print(f"Error al analizar los datos JSON: {e}")
    return []

def prettyTrice(string):
    """Formatea el texto para su presentación."""
    if not isinstance(string, str):
        return string
    string = string.replace(u"\u300a", '(').replace(u"\u300b", ')').replace('&middot;', u"\u00B7")
    string = string.replace(u"\u571F", 'Earth').replace(u"\u6c34", 'Water').replace(u"\u706b", 'Fire').replace(u"\u98a8", 'Wind').replace(u"\u6c37", 'Ice').replace(u"\u5149", 'Light').replace(u"\u95c7", 'Dark').replace(u"\u96f7", 'Lightning')
    string = string.replace('[[ex]]', '').replace('[[/]]', '').replace('EX BURST', '[EX BURST]')
    string = string.replace(u"\u300a"u"\u0053"u"\u300b", '[Special]')
    string = string.replace('[[', '<').replace(']]', '>').replace('<s>', '').replace('</>', '').replace('<i>', '').replace('<br> ', '\n').replace('<br>', '\n')
    string = string.replace(u"\uFF11", '1').replace(u"\uFF12", '2').replace(u"\uFF13", '3').replace(u"\uFF14", '4').replace(u"\uFF15", '5').replace(u"\uFF16", '6').replace(u"\uFF17", '7').replace(u"\uFF18", '8').replace(u"\uFF19", '9').replace(u"\uFF10", '0')
    string = string.replace(u"\u4E00"u"\u822C", 'Generic').replace(u"\u30C0"u"\u30EB", 'Dull')
    string = string.replace(u"\u300a", '').replace(u"\u300b", '').replace('&middot;', u"\u00B7").replace("\"\"", '\"')
    return string

def getimageURL(code):
    """Devuelve la URL de la imagen de la carta."""
    return f"https://fftcg.cdn.sewest.net/images/cards/full/{code[-6:] if re.search(r'[0-9]+\-[0-9]{3}[a-zA-Z]/[0-9]+\-[0-9]{3}[a-zA-Z]', code) else code}_eg.jpg"

# Carga de los datos JSON
a = loadJson('cards.json')

if not a:
    print("Error: No se pudo cargar o analizar los datos JSON.")
else:
    print(f"Datos JSON cargados exitosamente: {len(a)} registros")
    # Extraer los nombres de los sets
    b = [x['set'][0] for x in a if 'set' in x and isinstance(x['set'], list)]

    # Escritura del archivo XML
    with open('cards.xml', 'w', encoding='utf8') as myfile:
        myfile.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        myfile.write('<cockatrice_carddatabase version="4">\n')
        
        myfile.write('  <sets>\n')

        for x in set(b):
            addset(x, myfile)

        myfile.write('  </sets>\n')
        myfile.write('  <cards>\n')

        for x in a:
            card_name = x.get('name_en', '')
            card_name = card_name.replace(u"\u00FA", "u")  # Addresses u Cuchulainn, the Impure 2-133R

            card_type = '        <type>{} - {} - {}</type>\n'.format(
                prettyTrice(x.get('type_en', '')),
                prettyTrice(x.get('category_1', '')),
                prettyTrice(x.get('job_en', ''))
            )
            card_type = card_type.replace(' - ' + u"\u2015" + '</type>', '</type>')
            card_type = card_type.replace(' - </type>', '</type>')

            card_power = x.get('power', '').replace(u"\uFF0D", "").replace(u"\u2015", "")
            card_code = x.get('code', '')
            card_cost = x.get('cost', '')
            card_text = x.get('text_es', '')
            card_element = x.get('element', [])
            card_set = x.get('set', [])

            # Asegúrate de que card_set tenga al menos un valor
            if card_set:
                card_set = card_set[0]  # Ajusta la extracción del primer valor en la lista 'set'

                # Asegúrate de que card_element sea una lista
                if not isinstance(card_element, list):
                    card_element = []

                if re.search(r'\d-\d{3}[a-zA-Z]/', card_code):
                    codes = card_code.replace('(', '').replace(')', '').split('/')
                    for code in codes:
                        addcard(card_set, card_name, code, card_power, card_text, card_type, card_element, card_cost, myfile)
                else:
                    addcard(card_set, card_name, card_code, card_power, card_text, card_type, card_element, card_cost, myfile)

        myfile.write('  </cards>\n')
        myfile.write('</cockatrice_carddatabase>')
