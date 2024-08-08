import json
import re
import urllib.request
import io

def grab_card(req, cards):
    """Busca una carta en la lista de cartas basada en el código."""
    try:
        req = re.compile(req, re.IGNORECASE)
    except re.error as e:
        print(f"Error en la expresión regular: {e}")
        return ''
    
    for x in cards:
        if re.search(req, x.get('Code', '').upper()):
            return x
    return ''

def grab_cards(req, cards):
    """Busca cartas en la lista de cartas basada en el nombre."""
    try:
        req = re.compile(req, re.IGNORECASE)
    except re.error as e:
        print(f"Error en la expresión regular: {e}")
        return []
    
    result = []
    for x in cards:
        if re.search(req, x.get('name_en', '').lower()):
            result.append(x)
    return result

def prettyCode(card):
    """Formatea el código de la carta para su presentación."""
    element_mapping = {
        u"\u571F": "Earth",
        u"\u6c34": "Water",
        u"\u706b": "Fire",
        u"\u98a8": "Wind",
        u"\u6c37": "Ice",
        u"\u5149": "Light",
        u"\u95c7": "Dark",
        u"\u96f7": "Lightning"
    }
    element = element_mapping.get(card.get('element', ''), '')
    multicard = '(Generic)' if card.get('multicard', '') == u"\u25cb" else ''
    line1 = f"{card.get('code', '')} - {card.get('name_en', '')} - {element} {card.get('cost', '')} - {card.get('type_en', '')} {multicard}"
    return line1

def prettyCard(card):
    """Formatea los detalles de la carta para su presentación."""
    element_mapping = {
        u"\u571F": "Earth",
        u"\u6c34": "Water",
        u"\u706b": "Fire",
        u"\u98a8": "Wind",
        u"\u6c37": "Ice",
        u"\u5149": "Light",
        u"\u95c7": "Dark",
        u"\u96f7": "Lightning"
    }
    element = element_mapping.get(card.get('element', ''), '')
    multicard = '(Generic)' if card.get('multicard', '') == u"\u25cb" else ''
    line1 = f"{card.get('name_en', '')} - {element} {card.get('cost', '')} - ({card.get('code', '')}) {multicard}"
    line2 = f"{card.get('type_en', '')} {card.get('job_en', '')} {card.get('category_1', '')}"
    line3 = card.get('text_es', '')
    line4 = card.get('power', '')
    finished_string = f"{line1}\n{line2}\n{line3}"
    if line4:
        finished_string += f"\n{line4}"
    finished_string = finished_string.replace('[[ex]]', '').replace('[[/]]', '').replace('EX BURST', '[EX BURST]')
    finished_string = finished_string.replace(u"\u300a"u"\u0053"u"\u300b", '[Special]')
    finished_string = finished_string.replace('[[', '<').replace(']]', '>').replace('<s>', '').replace('</>', '').replace('<i>', '').replace('<br> ', '\n').replace('<br>', '\n')
    finished_string = finished_string.replace(u"\u571F", '(Earth)').replace(u"\u6c34", '(Water)').replace(u"\u706b", '(Fire)').replace(u"\u98a8", '(Wind)').replace(u"\u6c37", '(Ice)').replace(u"\u5149", '(Light)').replace(u"\u95c7", '(Dark)').replace(u"\u96f7", '(Lightning)')
    finished_string = finished_string.replace(u"\uFF11", '1').replace(u"\uFF12", '2').replace(u"\uFF13", '3').replace(u"\uFF14", '4').replace(u"\uFF15", '5').replace(u"\uFF16", '6').replace(u"\uFF17", '7').replace(u"\uFF18", '8').replace(u"\uFF19", '9').replace(u"\uFF10", '0')
    finished_string = finished_string.replace(u"\u300a"u"\u0031"u"\u300b", '(1)').replace(u"\u300a"u"\u0032"u"\u300b", '(2)').replace(u"\u300a"u"\u0033"u"\u300b", '(3)').replace(u"\u300a"u"\u0034"u"\u300b", '(4)').replace(u"\u300a"u"\u0035"u"\u300b", '(5)').replace(u"\u300a"u"\u0036"u"\u300b", '(6)').replace(u"\u300a"u"\u0037"u"\u300b", '(7)').replace(u"\u300a"u"\u0038"u"\u300b", '(8)').replace(u"\u300a"u"\u0039"u"\u300b", '(9)').replace(u"\u300a"u"\u0030"u"\u300b", '(0)')
    finished_string = finished_string.replace(u"\u4E00"u"\u822C", '(Generic)').replace(u"\u30C0"u"\u30EB", '(Dull)')
    finished_string = finished_string.replace(u"\u300a", '').replace(u"\u300b", '').replace('&middot;', u"\u00B7").replace("\"\"", '\"')
    return finished_string

def getImage(code):
    """Obtiene la imagen de la carta y la devuelve como un archivo en memoria."""
    url = f"https://fftcg.cdn.sewest.net/images/cards/full/{code[-6:] if re.search(r'[0-9]+\-[0-9]{3}[a-zA-Z]/[0-9]+\-[0-9]{3}[a-zA-Z]', code) else code}_eg.jpg"
    try:
        with urllib.request.urlopen(url) as response:
            data = io.BytesIO(response.read())
            return data
    except Exception as e:
        print(f"Error al obtener la imagen: {e}")
        return None

def getimageURL(code):
    """Devuelve la URL de la imagen de la carta."""
    return f"https://fftcg.cdn.sewest.net/images/cards/full/{code[-6:] if re.search(r'[0-9]+\-[0-9]{3}[a-zA-Z]/[0-9]+\-[0-9]{3}[a-zA-Z]', code) else code}_eg.jpg"

def loadJson(path):
    """Carga los datos JSON desde una URL dada."""
    try:
        with urllib.request.urlopen(path) as response:
            content = response.read().decode('utf-8')
            data = json.loads(content)
            return data.get('cards', [])
    except urllib.error.URLError as e:
        print(f"Error al cargar la URL: {e}")
    except json.JSONDecodeError as e:
        print(f"Error al analizar el JSON: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    return []

def prettyTrice(string):
    """Formatea el texto para su presentación."""
    string = string.replace(u"\u300a", '(').replace(u"\u300b", ')').replace('&middot;', u"\u00B7")
    string = string.replace(u"\u571F", 'Earth').replace(u"\u6c34", 'Water').replace(u"\u706b", 'Fire').replace(u"\u98a8", 'Wind').replace(u"\u6c37", 'Ice').replace(u"\u5149", 'Light').replace(u"\u95c7", 'Dark').replace(u"\u96f7", 'Lightning')
    string = string.replace('[[ex]]', '').replace('[[/]]', '').replace('EX BURST', '[EX BURST]')
    string = string.replace(u"\u300a"u"\u0053"u"\u300b", '[Special]')
    string = string.replace('[[', '<').replace(']]', '>').replace('<s>', '').replace('</>', '').replace('<i>', '').replace('<br> ', '\n').replace('<br>', '\n')
    string = string.replace(u"\uFF11", '1').replace(u"\uFF12", '2').replace(u"\uFF13", '3').replace(u"\uFF14", '4').replace(u"\uFF15", '5').replace(u"\uFF16", '6').replace(u"\uFF17", '7').replace(u"\uFF18", '8').replace(u"\uFF19", '9').replace(u"\uFF10", '0')
    string = string.replace(u"\u4E00"u"\u822C", 'Generic').replace(u"\u30C0"u"\u30EB", 'Dull')
    string = string.replace(u"\u300a", '').replace(u"\u300b", '').replace('&middot;', u"\u00B7").replace("\"\"", '\"')
    return string
