Paket: route
############

Modul: subject
==============

.. http:get:: /subjects/

    Listet alle verfügbaren Fächer auf.

    :resheader Content-Type: application/json
    :statuscode 200: Fächer wurden erfolgreich geladen
    :statuscode 204: Noch keine Fächer vorhanden

.. http:post:: /subjects/

    Legt ein neues Fach an.

    :reqheader Content-Type: application/x-www-form-urlencoded
    :resheader Content-Type: application/json
    :resheader Location: /subjects/<abr>
    :form string abr: Abkürzung (3 Buchstaben) des Faches in der Datenbank
    :form string name: Langbezeichnung des Faches
    :statuscode 201: Fach wurde erfolgreich erstellt
    :statuscode 400: Forulardaten wurde nicht korrekt validiert
    :statuscode 409: Fach ist bereits vorhanden

Modul: teacher
==============

.. http:get:: /teachers/

    Listet alle Lehrer auf.

    :resheader Content-Type: application/json
    :statuscode 200: Lehrerliste wurde erfolgreich geladen
    :statuscode 204: Noch keine Lehrer vorhanden

.. http:post:: /teachers/

    Legt einen neuen Leher an.

    :reqheader Content-Type: application/x-www-form-urlencoded
    :resheader Content-Type: application/json
    :resheader Location: /teachers/<teach_id>
    :form string fname: Vorname des Lehrers
    :form string lname: Nachname des Lehrers
    :form birth_date: Geburtsdatum (JJJJ-MM-TT) des Lehrers
    :statuscode 201: Lehrer wurde erfolgreich erstellt
    :statuscode 400: Ein Formularfeld fehlt oder Geburtsdatum im falchem Format
    :statuscode 409: Lehrer ist bereits vorhanden