# Floss API Triage

Quickly analyze malware API combinations with 
[FLOSS](https://github.com/fireeye/flare-floss).

Differently from `strings` `FLOSS` also searches for obfuscated string in
binary files (e.g. stack strings), which makes it better suited for quick
malware triage.

The idea behind this project is that many attack patterns use a combination of
API calls to work (e.g. LoadLibraryA and GetProcAddress is a combination often
used in shellcode).  By combining APIs the likelihood for false positives
decreases and the number of true positives increases.

As a small example, the file `floss-suspicious-test.txt` contains a few strings
that form suspicious combinations (and one that is missing a single API to form
a suspicious combination) and the results of running
`floss-suspicious.py floss-suspicious-test.txt` are stored in 
`floss-suspicious-test.txt_floss.txt`.

Custom APIs or API combinations can be added to the file `floss-suspicious.txt`.

Of course you can also add other suspicious string combinations, this is not
restricted to API calls, although that was my original intended purpose.

References:
https://posts.specterops.io/detection-spectrum-198a0bfb9302
https://github.com/xme/fame_modules/tree/master/processing/floss_str
https://ired.team/offensive-security/code-injection-process-injection/shellcode-execution-in-a-local-process-with-queueuserapc-and-nttestalert
https://www.elastic.co/blog/ten-process-injection-techniques-technical-survey-common-and-trending-process
https://ired.team/offensive-security/code-injection-process-injection/reflective-dll-injection
https://www-users.math.umn.edu/~math-sa-sara0050/space16/slides/space2016121708-06.pdf
