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

.. note:: Für das Erstellen einer Klasse oder das Wechseln eines Klassenleiters werden die URLs

        :http:get: /teachers/(int:id)/grades
        :http:post: /teachers/(int:id)/grades
        :http:put: /teachers/(int:id)/graddes/(name)
        
        verwendet, da das ER-Diagramm genau einen Lehrer als Klassenleiter verlangt. 
        Bei weiteren Optionen einer Klasse wird direkt die Klassen-URL verwendet, da die Information über den Klassenleiter dann nicht notwendig ist.

.. http:get:: /teachers/(int:id)/grades

    Listet alle Klassen eines Lehrers auf.

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

    .. note:: Bei jährlich wechselnden Klassennamen ist bei Klassenstufen unter 10 ein Klassename mit führender "0" zu empehlen,
        um eine korrekte alphabetische Sortierung der Klassen zu ermöglichen

.. http:put:: /teachers/(int:id)/grades/(name)

    Führt einen Wechsel des Klassenleiters für eine Klasse durch.

    :param id: Id des neuen Lehrers
    :type id: int
    :param name: Name der Klasse
    :type name: string
    :resheader Content-Type: application/json

    :statuscode 200: Wechsel des Klassenleiters wurde erfolgreich durchgeführt
    :statuscode 404: Neuer Klasssenleiter oder Klasse wurde nicht gefunden

Modul: grade
============

.. http:get:: /grades/

    Zeigt alle Klassen in alphabetischer Reihenfolge.

    :resheader Content-Type: application/json
    :statuscode 200: Klassenliste wurde erfolgreich geladen
    :statuscode 404: Noch keine Klasse vorhanden

    .. note:: Bei :http:statuscode:`404` muss mindestens eine Klasse über :http:post:`/teachers/(int:id)/grades` erstellt werden!

.. http:patch:: /grades/(gradename)

    Ändert den Klasennamen (z. B. bei jählich wechselden Klassenstufen).

    :param gradename: Bisherigier Klassenname
    :type gradename: string
    :reqheader Content-Type: application/json
    :resheader Content-Type: application/json
    :json string name: Neuer Klassenname

    :statuscode 200: Klassenname wurde erfolgreich geändert
    :statuscode 400: JSON-Feld 'name' ist nicht vorhanden
    :statuscode 404: Bisherige Klasse wurde nicht gefunden
    :statuscode 409: Neuer Klassenname ist nicht verfügbar

.. http:get:: /grades/(gradename)/students

    Zeigt alle Schüler in einer Klasse.

    :param gradename: Name der Klasse
    :type gradename: string
    :resheader Content-Type: application/json
    :statuscode 200: Klassenliste wurde erfolgreich geleden
    :statuscode 204: Klassenliste enthält noch keine Schüler
    :statuscode 404: Klasse wurde nicht gefunden

    .. note:: Wird für den Parameter 'gradename' der String 'none' übergeben, so wird nach Schülern ohne Klassenzuweisung gesucht. Dieser Fall kann eintreten, wenn eine Klasse gelöscht wurde und die Schüler noch nicht gelöscht worden sind.

.. http:post:: /grades/(gradename)/students

    Erstellt einen neuen Schüler in einer Klasse.

    :param gradename: Name der Klasse
    :type gradename: string
    :reqheader Content-Type: application/json
    :resheader Content-Type: application/json
    :resheader Location: /grades/<gradename>/students/<id>

    :json string fname: Vorname des Schülers
    :json string lname: Nachname des Schülers
    :json string birthDate: Geburtsdatum (JJJJ-MM-TT)

    :statuscode 201: Schüler wurde erfolgreich erstellt
    :statuscode 400: Fehlendes JSON-Feld oder ungültiges Geburtsdatum
    :statuscode 404: Klasse wurde nicht gefunden
    :statuscode 409: Der Schüler existiert bereits