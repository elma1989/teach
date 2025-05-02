Paket: route
############

Modul: site
===========

.. http:get:: /
    
    Rendert die Hauptseite.

    :resheader Content-Type: text/html

    :statuscode 200: Hauptseite wurde erfogreich geladen
    :statuscode 404: index.html wurde nicht gefunden

Modul: subject
==============

.. http:get:: /subjects/

    Listet alle verfügbaren Unterrichtsfächer auf.

    :resheader Content-Type: application/json
    
    :statuscode 200: Fächer wurden erfolgreich geladen
    :statuscode 404: Noch kein Fach vorhanden

.. http:post:: /subjects/

    Fügt ein neues Unterrichtsfach hinzu.

    :reqheader Content-Type: application/json
    :resheader Content-Type: application/json
    :resheader Location: /subjects/<abr>

    :json string abr: Abkürzung (3 Buchstaben) des Faches
    :json string name: Langbezeichnung des Faches

    :statuscode 201: Fach wurde erfogreich erstellt
    :statuscode 400: Format der übertragenen Daten ist nicht Korrekt
    :statuscode 409: Fach ist bereits vorhanden

.. http:get:: /subjects/(string:abr)
    
    Gibt das gewählte Fach zurück.

    :param abr: Abkürzung (3 Buchstaben) des Faches
    :type abr: string
    :resheader Content-Type: application/json
    
    :statuscode 200: Fach wurde erfolgreich geladen
    :statuscode 404: Fach wurde nicht gefunden