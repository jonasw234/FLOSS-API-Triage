# Floss API Triage

Schnellanalyse von verdächtigen APIs/API-Kombinationen für Malwareanalyse mit
[FLOSS](https://github.com/fireeye/flare-floss).

FLOSS sucht im Gegensatz zu strings auch nach obfuskierten Strings in
Binärdateien (z. B. Stackstrings) und ist damit besser für die schnelle
Malwareanalyse geeignet.

Die Idee hinter diesem Projekt ist es, dass viele Angriffstechniken mehrere
APIs in Kombination benötigen, um zu funktionieren (z. B. LoadLibrary und
GetProcAddress, um dynamisch Funktionen nachzuladen). Dadurch kann die Anzahl
der relevanten Treffer erhöht und die Anzahl der irrelevanten Treffer verringert
werden.

Die Datei `floss-suspicious-test.txt` enthält dabei einige beispielhafte
Strings, die in der Kombination verdächtig sind und in
`floss-suspicious-test.txt_floss.txt` liegt das Ergebnis des Aufrufs von
`floss-suspicious.py floss-suspicious-test.txt`.

Eigene APIs/API-Kombinationen können in der Datei `floss-suspicious.txt`
hinterlegt werden. Erweiterungen und eigene Vorschläge sind gerne gesehen!

Referenzen:
https://posts.specterops.io/detection-spectrum-198a0bfb9302
https://github.com/xme/fame_modules/tree/master/processing/floss_str
https://ired.team/offensive-security/code-injection-process-injection/shellcode-execution-in-a-local-process-with-queueuserapc-and-nttestalert
https://www.elastic.co/blog/ten-process-injection-techniques-technical-survey-common-and-trending-process
https://ired.team/offensive-security/code-injection-process-injection/reflective-dll-injection
https://www-users.math.umn.edu/~math-sa-sara0050/space16/slides/space2016121708-06.pdf
