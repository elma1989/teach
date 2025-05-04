Paket: route
############

Modul: site
===========

.. http:get:: /
    
    Rendert die Hauptseite.

    :resheader Content-Type: text/html; charset=utf8

    :statuscode 200: Hauptseite wurde erfolgreich geladen
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

    :statuscode 201: Fach wurde erfolgreich erstellt
    :statuscode 400: Format der übertragenen Daten ist nicht Korrekt
    :statuscode 409: Fach ist bereits vorhanden

.. http:get:: /subjects/(abr)
    
    Gibt das gewählte Fach zurück.

    :param abr: Abkürzung (3 Buchstaben) des Faches
    :type abr: string
    :resheader Content-Type: application/json
    
    :statuscode 200: Fach wurde erfolgreich geladen
    :statuscode 404: Fach wurde nicht gefunden

Modul: teacher
==============

.. http:get:: /teachers/

    Listet alle verfügbaren Lehrer auf.

    :resheader Content-Type: application/json
    :statuscode 200: Lehrer wurden erfolgreich geladen
    :statuscode 404: Noch kein Lehrer vorhanden

.. http:post:: /teachers/

    Erstellt einen neuen Lehrer.

    :reqheader Content-Type: application/json
    :resheader Content-Type: application/json
    :resheader Location: /teachers/<id>

    :json string fname: Vorname des Lehrers
    :json string lname: Nachname des Lehrers
    :json string birthDate: Geburtdatum (JJJJ-MM-TT) des Lehrers

    :statuscode 201: Lehrer erfolgreich erstellt
    :statuscode 400: Fehlende Daten oder Gebursdatum nicht im korrekten Format
    :statuscode 409: Lehrer bereits vorhanden

.. http:get:: /teachers/(int:id)

    Gibt die Daten eines einzelnen Lehrers aus.

    :param id: Id des Lehrers
    :type id: int
    :resheader Content-Type: application/json
    :statuscode 200: Daten wurden erfolgreich geladen
    :statuscode 404: Der Lehrer wurde nicht gefunden

.. http:get:: /teachers/(int:id)/subjects

    Listet alle Fächer eines Lehrers auf.

    :param id: Id des Lehrers
    :type id: int
    :resheader Content-Type: application/json
    :statuscode 200: Die Fächerliste wurde erfolgreich geladen
    :statuscode 204: Der Lehrer hat noch keine Fächer
    :statuscode 404: Der Lehrer wurde nicht gefunden

.. http:post:: /teachers/(int:id)/subjects

    Fügt dem Lehrer ein neues Fach hinzu.

    :param id: Id des Lehrers
    :type id: int
    :reqheader Content-Type: application/json
    :resheader Content-Type: application/json
    :resheader Location: /teachers/<id>/subjects/<abr>
    :json string abr: Abkürzung des Faches in der Datenbank

    :statuscode 201: Fach wurde erfolgreich zum Lehrer hinzugefügt
    :statuscode 400: JSON-Feld 'abr' nicht vorhanden
    :statuscode 404: Der Lehrer oder das Fach wurde nicht gefunden
    :statuscode 409: Der Lehrer unterrichtet das Fach bereits

.. note:: Für das Erstellen einer Klasse oder eines Klassenleiters werden die URL

        :http:get: /teachers/(int:id)/grades
        :http:post: /teachers/(int:id)/grades
        :http:put: /teachers/(int:id)/graddes/(name)
        
        verwendet, da das ER-Diagramm genau einen Lehrer als Klassenleiter verlangt. 
        Bei weiteren Optionen einer Klasse wird direkt die Klassen-URL verwendet, da die Information über den Klassenleiter dann nicht notwendig ist.

.. http:get:: /teachers/(int:id)/grades

    Listed alle Klassen eines Lehrers auf.

    :param id: Id des Lehrers
    :type id: int
    :reqheader Content-Type: application/json
    
    :statuscode 200: Die Klassen wurden erfolgreich geladen
    :statuscode 204: Der Lehrer leitet noch keine Klassen
    :statuscode 404: Der Lehrer wurde nicht gefunden

.. http:post:: /teachers/(int:id)/grades

    Fügt dem Lehrer eine neue Klasse hinzu.

    :param id: Id des Lehrers
    :type id: int
    :reqheader Content-Type: application/json
    :resheader Content-Type: application/json
    :resheader Location: /grades/<name>
    :json string name: Name der Klasse

    :statuscode 201: Klasse wurde erfolgreich erstellt
    :statuscode 400: JSON-Feld 'name' ist nicht vorhanden
    :statuscode 404: Der Lehrer wurde nicht gefunden
    :statuscode 409: Klasse existiert bereits
