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