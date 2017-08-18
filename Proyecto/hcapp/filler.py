import re
import os
from docx import Document
from django.conf import settings

def docx_replace_regex(doc_obj, regex , replace):

    for p in doc_obj.paragraphs:
        if regex.search(p.text):
            inline = p.runs
            # Loop added to work with runs (strings with same style)
            for i in range(len(inline)):
                if regex.search(inline[i].text):
                    text = regex.sub(replace, inline[i].text)
                    inline[i].text = text

    for table in doc_obj.tables:
        for row in table.rows:
            for cell in row.cells:
                docx_replace_regex(cell, regex , replace)


def reemplaza(a_reemplazar,reemplazo,pacient_name,age,doct,date,doc_name ):
    c_campo = re.compile(r"{0}".format(str('##campo##')))
    campo = r"{0}".format(str(reemplazo))
   

    c_nombre_paciente = re.compile(r"{0}".format('##nombre##'))
    nombre_paciente = r"{0}".format(str(pacient_name))

    c_edad = re.compile(r"{0}".format('##edad##'))
    edad = r"{0}".format(str(age))

    c_doctor= re.compile(r"{0}".format('##doctor##'))
    doctor = r"{0}".format(str(doct))

    c_fecha = re.compile(r"{0}".format('##fecha##'))
    fecha = r"{0}".format(str(date))

    c_espacio = re.compile(r"{0}".format(''))
    espacio = r"{0}".format(' ')
    

    filename =str(doc_name)
    #module_dir=os.path.dirname(__file__)
    file_path =os.path.join((settings.MEDIA_ROOT), filename)
    doc = Document(file_path)


    docx_replace_regex(doc, c_campo, campo)
    docx_replace_regex(doc, c_nombre_paciente, nombre_paciente)
    docx_replace_regex(doc, c_edad, edad)
    docx_replace_regex(doc, c_doctor, doctor)
    docx_replace_regex(doc, c_fecha, fecha)
   #docx_replace_regex(doc, c_espacio, espacio)

    return doc





