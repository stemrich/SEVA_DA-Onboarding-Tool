def profile_helfen(pandas_profile, create_file: bool=False):

    import json
    from IPython.core.display import HTML

    #Falls create_file true ist, erstellen wir ein JSON File vom Pandas Profilereport. 
    # Es muss existieren, damit der Rest der funktion läuft, 
    # aber wir werden es meistens haben also ist unser Default erstmals false
    if(create_file == True): 
        pandas_profile.to_file("your_report.json")
    
    # JSON File importieren
    with open('your_report.json') as f:
        import_json_data = json.load(f)

    # Kategorische und numerische Werte abfangen:
    categorical_found = False
    numerical_found = False

    if 'Categorical' in import_json_data['table']['types'].keys():
        categorical_found = True
    if 'Numeric' in import_json_data['table']['types'].keys():
        numerical_found = True
    
    # Warnings abfangen:
    # Habe jetzt redudant 3 Varianten gemacht, das ist derzeit noch uneffizient aber übersichtlicher
    # variante 1: einfach eine menge von warnings machen
    warnings_set = set()
    for message in import_json_data['messages']:
        warnings_set.add(message.split(' ')[0])

    # variante 2: dictionary mit warning als key, liste von spalten/variablen als value
    warnings_dict1 = {}
    for message in import_json_data['messages']:
        w = message.split(' ')[0]
        if w in warnings_dict1.keys():
            warnings_dict1[w].append(message.split('column ')[1])
        else:
            warnings_dict1[w] = [message.split('column ')[1]]


    # variante 3: dictionary mit spalten/variablen als key, warnings als value
    warnings_dict2 = {}
    for message in import_json_data['messages']:
        w =  message.split('column ')[1]
        if w in warnings_dict2.keys():
            warnings_dict2[w].append(message.split(' ')[0])
        else:
            warnings_dict2[w] = [message.split(' ')[0]]

    # prints um die abgefangen daten anzuschauen:
    #print(warnings_set)
    #print(warnings_dict1)
    #print(warnings_dict2)

    # Alle abgefangenen Infos verarbeiten, damit Text und Links displayen:

    # Einleitung zu numerischen und kategorischen Werten:
    if(categorical_found or numerical_found):
        numcatstring = "<p style='font-size:15px'>Der Datensatz enthält "
        if(categorical_found and numerical_found):
            numcatstring += "sowohl kategorische als auch numerische Daten. "
        elif(categorical_found):
            numcatstring += "kategorische Daten."
        elif(numerical_found):
            numcatstring += "numerische Daten."
        numcatstring += "Wenn du dir nicht sicher bist, was das bedeutet, <a href='https://wissenschafts-thurm.de/grundlagen-der-statistik-wie-unterscheidet-man-zwischen-nominal-ordinal-und-kardinalskala/' target='_blank'>findest du hier mehr Info dazu.</a></p>"
        display(HTML(numcatstring))
    if(categorical_found):
        catstring = "<p style='font-size:15px'>Einen ersten Überblick über die Möglichkeiten/Methoden um kategorische Daten zu analysieren findest du <a href='https://en.wikipedia.org/wiki/List_of_analyses_of_categorical_data' target='_blank'>hier.</a></p>"
        display(HTML(catstring))
    if(numerical_found):
        numstring = "<p style='font-size:15px'>Weil du numerische Daten hast, könnten <a href='http://analytics.datengeschichten.at/doku.php?id=statistische_grundlagen' target='_blank'>diese statistischen Grundlagen</a> dir weiterhelfen.</p>"
        display(HTML(numstring))
    
    # High correlation Warnings: Link habe ich (Alexander) selber gesucht, brauchen eventuell eine bessere
    if '[HIGH_CORRELATION]' in warnings_dict1:
        highcor_string = "<p style='font-size:15px'>Die Werte " + str(warnings_dict1['[HIGH_CORRELATION]']) + " haben hohe Korellationen untereinander. Der Grund, wieso dein Profilereport Warnungen dafür erstellt ist, dass das manchmal bedeutet, dass diese Werte was ähnliches darstellen/repräsentieren. Man muss sich überlegen, ob man die Spalten mit hoher Korellation vielleicht zusammenfügen möchte, oder ob sie getrennt interessantere Beobachtungen zeigen.</p>"
        display(HTML(highcor_string))

    # Uniform Warning:
    
    #Weitere Warnungen: CONSTANT, HIGH CORRELATION, UNSUPPORTED, ZEROS, DUPLICATE, UNIQUE 
    #Weitere Überprüfungen: Kodierung (0 weiblich, 1 männlich, 2 divers, etc).. wie überprüft man das? Datentyp (Int)?


    # High cardinality Warning:
    if '[HIGH_CARDINALITY]' in warnings_dict1:
        highcard_string = ""
        if len(warnings_dict1['[HIGH_CARDINALITY]']) == 1:
            highcard_string += "<p style='font-size:15px'>Die Spalte " + str(warnings_dict1['[HIGH_CARDINALITY]']) + " hat eine hohe Kardinalität. "
        else:
            highcard_string += "<p style='font-size:15px'>Die Spalten " + str(warnings_dict1['[HIGH_CARDINALITY]']) + " haben eine hohe Kardinalität. "
        highcard_string += "Falls du dir unsicher bist, was das bedeutet und ob das ein Problem sein könnte, <a href='https://www.betriebswirtschaft-lernen.net/erklaerung/kardinalitaet-datenbank/' target='_blank'>kannst du dich hier informieren.</a></p>"
        display(HTML(highcard_string))

    # Uniform + high cardinality als Kombination einfangen: benötigt glaub ich leider eine Schleife um generische Spalten die das haben abzufangen ... man kann aber dann gleich in der Schleife mehrere solcher Kombinationen abfangen
    for column in warnings_dict2:
        if '[HIGH_CARDINALITY]' in warnings_dict2[column] and '[UNIFORM]' in warnings_dict2[column]:       # ich denke, es reicht die Kombination nur einmal zu erklären, außer man will erwähnen, dass das mehreren Spalten passiert ist
            hcu_string = ""     # high cardinality + uniform string
            hcu_string += "<p style='font-size:15px'>" + column + " hat sowohl die Warnung, dass eine hohe Kardinalität vorhanden ist, als auch dass die Spalte uniform verteilt ist. Ein klassisches Beispiel für solche Warnungen sind Spalten wie zum Beispiel 'Name'. Man sollte jedoch beachten, ob man nicht unabsichtlich einen numerischen Wert als Text oder kategorischen Wert kodiert hat. Ein Unterschied zwischen diesen zwei Warnungen und der Warnung 'Unique' ist, dass beim letzteren alle Werte nur einmal vorkommen, während bei hoher Kardinalität und einer uniformen Verteilung, Werte doppelt vorkommen können. </p>"
            display(HTML(hcu_string))
            break

    # Fehlende (missing) Werte:
    if '[MISSING]' in warnings_dict1:
        missing_string = ""
        if len(warnings_dict1['[MISSING]']) == 1:
            missing_string += "<p style='font-size:15px'>Die Spalte " + str(warnings_dict1['[MISSING]']) + " hat fehlende Werte. "
        else:
            missing_string += "<p style='font-size:15px'>Die Spalten " + str(warnings_dict1['[MISSING]']) + " haben fehlende Werte. "
        missing_string += "Fehlende Werte müssen nicht immer ein Problem darstellen. Es macht z.B. Sinn bei Spalten, wo man nur zusätzliche/optionale Infos dazugibt, wie 'zweite Adresse' und manchmal stellt keine Klassifizierung bei kategorischen Daten eigentlich eine zusätzliche Klassifizierung dar. "
        missing_string += "Falls du mehr über fehlende Werte wissen willst, kannst du <a href='https://www.inwt-statistics.de/blog-artikel-lesen/fehlende-werte-verstehen-und-handhaben.html' target='_blank'>hier</a> darüber nachlesen oder <a href='https://www.youtube.com/watch?v=Ft2DZp8gTuA' target='_blank'>ein Video schauen.</a></p>"
        display(HTML(missing_string))


    # Als erstes Beispiel für die Hilfsfunktion: SKEWED Warnung und auf skewness zugreifen:
    if '[SKEWED]' in warnings_dict1:
        skewed_string = ""      # Sammle Text welches dann am Ende mit display(HTML(text)) zu HTML Text wird. Somit ist alles in einer Zeile dann.
        if  len(warnings_dict1['[SKEWED]']) == 1:        # Überprüfe ob nur eine Variable die SKEWED Warnung hat
            skewed_string += "<p style='font-size:15px'>Die Spalte " + str(warnings_dict1['[SKEWED]']) + " hat einen hohen Wert bei Skewness/Schiefe, nämlich " + str(import_json_data['variables'][warnings_dict1['[SKEWED]']]['skewness']) + "."
        else:       # Falls mehrere die SKEWED Warnung haben, will ich alle gleichzeitig erwähnen: 
            skewed_string += "<p style='font-size:15px'>Die Spalten " + str(warnings_dict1['[SKEWED]']) + " haben hohe Werte bei Skewness/Schiefe, nämlich "
            for val in warnings_dict1['[SKEWED]']:      # Schleife für die verschiedenen Werte von den Spalten/Variablen
                if val is warnings_dict1['[SKEWED]'][0]:        # Text etwas anders für den ersten Wert
                    skewed_string += str(import_json_data['variables'][val]['skewness'])
                elif val is warnings_dict1['[SKEWED]'][-1]:     # Text etwas anders für den letzten Wert
                    skewed_string += " und " + str(import_json_data['variables'][val]['skewness']) + "."
                else:       # Beistriche für alle Werte zwischen first und last
                    skewed_string += ", " + str(import_json_data['variables'][val]['skewness'])

        skewed_string += " <a href='https://matheguru.com/stochastik/schiefe-linksschief-rechtsschief-symmetrisch.html' target='_blank'>Hier kannst du mehr darüber erfahren. </a> </p>"    # Hyperlink für Webseite
        display(HTML(skewed_string))        # String via HTML anzeigen.
        
    #display(HTML("<p style='font-size:15px'> Test Text </p>"))