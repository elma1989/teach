Paket: route
############

.. note:: Werden variable Endpunkte direkt über Python verarbeitet, so werden die Variablen in **snake_case** geschrieben, da dieser Stil in Python an gängigsten ist.

    Können die benötigten Daten direkt über ein Webforular an den Server geschickt werden, so werden die Name-Tags in **kebab-case** geschrieben, da dieser Stil in HTML am gängigsten ist.

    Wird ein JSON-String erwartet, da URL dynamisch abhängig von einer zuvor getätigten Auswahl ist, so werden die JSON-Felder in **camelCase** geschrieben, da dieser Stil in JavaScript am gängigsten ist.

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

.. http:get:: /subjects/(sub_abr)

    Zeigt Details eines Faches.

    :param string sub_abr: Abkürzung (3 Buchstaben) in der Datenbank
    :resheader Content-Type: application/json
    :statuscode 200: Fachdaten wurden erfolgreich geladen
    :statuscode 404: Fach wurde nicht gefunden

Modul: teacher
==============

.. http:get:: /teachers/

    Listet alle Lehrer auf.

    :resheader Content-Type: application/json
    :statuscode 200: Lehrerliste wurde erfolgreich geladen
    :statuscode 204: Noch keine Lehrer vorhanden

.. http:post:: /teachers/

    Legt einen neuen Lehrer an.

    :reqheader Content-Type: application/x-www-form-urlencoded
    :resheader Content-Type: application/json
    :resheader Location: /teachers/<teach_id>
    :form string fname: Vorname des Lehrers
    :form string lname: Nachname des Lehrers
    :form birth-date: Geburtsdatum (JJJJ-MM-TT) des Lehrers
    :statuscode 201: Lehrer wurde erfolgreich erstellt
    :statuscode 400: Ein Formularfeld fehlt oder Geburtsdatum im falchem Format
    :statuscode 409: Lehrer ist bereits vorhanden

.. http:get:: /teachers/(int:teach_id)

    Zeigt Details zu einem Lehrer

    :param int teach_id: Id des Lehrers
    :resheader Content-Type: application/json
    :statuscode 200: Daten wurden erfolgreich geladen
    :statuscode 404: Lehrer nicht gefunden

.. http:get:: /techers/(int:teach_id)/subjects

    Zeigt alle Fächer eines Lehrer.

    :param int teach_id: Id des Lehrers
    :resheader Content-Type: application/json
    :statuscode 200: Fächer wurden erfolgreich geladen
    :statuscode 204: Lehrer hat noch keine Fächer
    :statuscode 404: Lehrer wurde nicht gefunden

.. http:post:: /techers/(int:teach_id)/subjects

    Legt für den Lehrer ein neues Fach an.

    :param int teach_id: Id des Lehrers
    :reqheader Content-Type: application/json
    :resheader Content-Type: application/json
    :json sting subAbr: Abkürzung (3 Buchstaben) in der Datenbank
    :statuscode 201: Fach wurde erfolgreich anglegt
    :statuscode 400: JSON-Feld 'subAbr' fehlt
    :statuscode 404: Lehrer oder Fach nicht gefunden
    :statuscode 409: Der Lehrer unterrichtet das Fach bereits