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
    :form abr: Abkürzung (3 Buchstaben) des Faches in der Datenbank
    :type abr: string
    :form name: Langbezeichnung des Faches
    :type name: string
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
    :form fname: Vorname des Lehrers
    :form lname: Nachname des Lehrers
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
    :resheader Location: /subjects/<subAbr>
    :json sting subAbr: Abkürzung (3 Buchstaben) in der Datenbank
    :statuscode 201: Fach wurde erfolgreich anglegt
    :statuscode 400: JSON-Feld 'subAbr' fehlt
    :statuscode 404: Lehrer oder Fach nicht gefunden
    :statuscode 409: Der Lehrer unterrichtet das Fach bereits

Kurse
-----

.. http:get:: /teachers/(int:teach_id)/courses

    Liefert die Kurse eines Lehrers.

    :param int teach_id: Id des Lehrers
    :resheader Content-Type: application/json
    :statuscode 200: Kursliste erfolgreich geladen
    :statuscode 204: Lehrer hat noch keine Kurse
    :statuscode 404: Lehrer wurde nicht gefunden

.. http:post:: /teachers/(int:teach_id)/courses

    Legt einen neuen Kurse für einen Lehrer an.

    :param int teach_id: Id des Lehrers
    :reqheader Content-Type: application/json
    :resheader Content-Type: application/json
    :resheader Location: /teachers/<teach_id>/courses/<courseName>
    :json string courseName: Name des Kurses
    :json string subAbr: Abkürzung (3 Buchstaben) des Faches in der Datenbank
    :statuscode 201: Kurs wurde erfolgreich erstellt
    :statuscode 404: Lehrer oder Fach wurde nicht gefunden
    :statuscode 409: Kurs ist bereits vorhanden

.. http:get:: /teachers/(int:teach_id)/courses/(course_name)

    Liefert Details zu einem Kurs.

    :param int teach_id: Id des Lehrers
    :param string course_name: Name des Kurses
    :resheader Content-Type: application/json
    :statuscode 200: Kursdaten wurden erfolgreich geladen
    :statuscode 404: Kursleiter oder Kurs nicht gefunden

.. http:patch:: /teachers/(int:teach_id)/courses/(course_name)

    Wechselt den Kursleiter.

    :param int teach_id: Id des Lehrers (bisheriger Kursleiter)
    :param string course_name: Name des Kurses
    :reqheader Content-Type: application/json
    :resheader Content-Type: application/json
    :json int newLeaderId: Id des neuen Kursleiters
    :statuscode 204: Vorgang abgeschlossen
    :statuscode 404: bisheriger/neuer Kursleiter oder Kurs nicht gefunden

.. http:get:: /teachers/(int:teach_id)/courses/(course_name)/members

    Listet alle Kursteilnehmer auf.

    :param int teach_id: Id des Lehrers
    :param string course_name: Name des Kurses
    :resheader Content-Type: application/json
    :statuscode 200: Kursliste wurde erfolgreich geladen
    :statuscode 204: Noch keine Teilnehmer im Kurs
    :statuscode 404: Kurs oder Kursleiter nicht gefunden

.. http:post:: /teachers/(int:teach_id)/courses/(course_name)/members

    Erstellt eine Mitgleidschaft für einen Schüler in einem Kurs.

    :param int teach_id: Id des Lehrers
    :param string course_name: Name des Kurses
    :reqheader Content-Type: application/json
    :resheader Content-Type: application/json
    :resheader Location: /grades/<grade_name>/students/<student_id>
    :json int newMemberId: Id des Schülers, der Mitglied werden soll
    :statuscode 201: Kursmitgliedschaft wurde erfolgreich erstellt
    :statuscode 400: 'newMemberId' fehlt
    :statuscode 404: Kurs, Kursleiter oder Schüler nicht gefunden
    :statuscode 409: Der Schüler ist bereits Mitglied in dem Kurs

Stunden
-------

.. http:get:: /teachers/(int:teach_id)/courses/(course_name)/lessons

    Listet alle Unterrichtsstunden eines Kurses auf.

    :param int teach_id: Id des Lehrers
    :param string course_name: Name des Kurses
    :resheader Content-Type: application/json
    :statuscode 200: Stundenliste wurde erfolgreich geladen
    :statuscode 204: Zu dem Kurse sind noch keine Stunden geplant wurden
    :statuscode 404: Kurs oder Kursleiter nicht gefunden

.. http:post:: /teachers/(int:teach_id)/courses/(course_name)/lessons

    Legt eine neue Unterrichtsstunde an.

    :param int teach_id: Id des Lehrers
    :param string course_name: Name des Kurses
    :reqheader Content-Type: application/json
    :resheader Content-Type: application/json
    :resheader Location: /teachrs/<int:teach_id>/courses/<course_name>/lessons/<time>
    :json string time: Geplanter Unterrichtsbiginn (JJJJ-MM-TT'T'HH:MM)
    :statuscode 201: Unterrichtsstunde wurde erfolgreich erstellt
    :statuscode 400: Zeit fehlt oder ist im falschem Format
    :statuscode 404: Kurs oder Kursleiter nicht gefunden
    :statuscode 409: Unterrichtsstunde bereits vorhanden

.. http:get:: /teachers/(int:teach_id)/courses/(course_name)/lessons/(les_time)

    Listet alle Unterrichtsstunden eines Kurses auf.

    :param int teach_id: Id des Lehrers
    :param string course_name: Name des Kurses
    :param string les_time: geplanter Unterrichtsbeginn
    :resheader Content-Type: application/json
    :statuscode 200: Daten der Unterrichtsstunde wurden erfolgreich geladen
    :statuscode 404: Kurs, Kursleiter oder Unterrichtsstunde wurde nicht gefunden

.. http:patch:: /teachers/(int:teach_id)/courses/(course_name)/lessons/(les_time)

    Nimmt Änderungen für eine Unterrichtsstude vor.

    :param int teach_id: Id des Lehrers
    :param string course_name: Name des Kurses
    :param string les_time: geplanter Unterrichtsbeginn
    :reqheader Content-Type: application/json
    :resheader Content-Type: application/json
    :json string topic: Thema der Stunde
    :json string newTime: Neue geplante Zeit der Stunde
    :statuscode 204: Vorgang abgeschlossen
    :statuscode 400: Zeit im falschem Foramt
    :statuscode 404: Kurs, Kursleiter oder Unterrichtsstunde wurde nicht gefunden

Modul: grade
============

.. http:get:: /grades/

    Listet alle Klassen auf.

    :resheader Content-Type: application/json
    :statuscode 200: Klassen erfolgreich geladen
    :statuscode 204: Noch keine Klassen vorhanden

.. http:post:: /grades/

    Erstellt eine neue Klasse.

    :reqheader Content-Type: x-www-form-urlencoded
    :resheader Content-Type: application/json
    :resheader Location: /grades/<name>
    :form name: Name der Klasse
    :form teach-id: Id des Klassenleiters
    :statuscode 201: Klasse wurde erfolgreich erstellt
    :statuscode 400: Ein Forumarfeld felt
    :statuscode 404: Der Klassenleiter wurde nicht gefunden
    :statuscode 409: Die Klasse ist bereits vorhanden

.. http:get:: /grades/(grade_name)

    Prüft, eine Klasse verfügbar ist.

    :param string grade_name: Name der Klasse
    :resheader Content-Type: application/json
    :statuscode 200: Klasse ist vorhanden
    :statuscode 404: Klasse wurde nicht gefunden

.. http:patch:: /grades/(grade_name)

    Nimmt Änderungen an einer Klasse vor.

    :param string grade_name: Name der Klasse
    :reqheader Content-Type: application/json
    :resheader Content-Type: application/json
    :json string name: Neuer Name der Klasse
    :json int leaderId: Id des neuen Klassenleiters
    :statuscode 204: Vorgang abgeschlossen
    :statuscode 404: Klasse oder Klassenleiter nicht gefunden
    :statuscode 409: Neuer Klassenname ist nicht verfügbar

.. http:get:: /grades/(grade_name)/students

    Liefert eine Liste mit allen Mitgliedern einer Klasse.

    :param string grade_name: Name der Klasse
    :resheader Content-Type: application/json
    :statuscode 200: Schülerliste erfolgreich geladen
    :statuscode 204: Noch keine Schüler in der Klasse
    :statuscode 404: Klasse wurde nicht gefunden

    .. note:: Wird für 'grade_name' der String 'none' angegeben, so wird nach Schülern gesucht, die keiner Klasse zugewiesen sind.

        Dieser Zustand kann entstehen, wenn eine Klasse mit noch vorhandenen Schülern gelöscher wird, da eine gemeinschaftliche Löschung nicht vorgesehen ist.

        Für neue Schüler ist jedoch eine Klassenzuweisung notwendig, da möglichst wenig Schüler ohne Klassenzuweisung vorhanden seien sollen.

.. http:post:: /grades/(grade_name)/students

    Erstellt einen neuen Schüler.

    :param string grade_name: Name der Klasse
    :reqheader Content-Type: application/json
    :resheader Content-Type: application/json
    :resheader Location: /grades/<grade_name>/students/<student_id>
    :json string fname: Vorname des Schülers
    :json string lname: Nachname des Schülers
    :json string birthDate: Geburtsdatum (JJJJ-MM-TT) des Schülers
    :statuscode 201: Schüler erfolgreich erstellt
    :statuscode 400: Fehlende JSON-Felder oder ungültiges Geburtsdatum
    :statuscode 404: Klasse nicht gefunden
    :statuscode 409: Schüler bereits vorhanden

.. http:get:: /grades/(grade_name)/students/(int:student_id)

    Liefert Details zu einen Schüler.

    :param string grade_name: Name der Klasse
    :param int student_id: Id des Schülers
    :resheader Content-Type: application/json
    :statuscode 200: Schüulerdaten erfolgreich geladen
    :statuscode 404: Schüler oder Klasse nicht gefunden

.. http:patch:: /grades/(grade_name)/students/(int:student_id)

    Nimmt Änderungen an einem Schüler vor.

    :param string grade_name: Name der aktuellen Klasse
    :param int student_id: Id des Schülers
    :reqheader Content-Type: application/json
    :resheader Content-Type: application/json
    :json string gradeName: Name der neuen Klasse
    :statuscode 204: Vorgang abgeschlossen
    :statuscode 404: Alte/neue Klasse oder Schüler nicht gefunden