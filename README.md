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

Please note that the operator precendence might be different from what you’re
used to: OR binds stronger than AND.  This design decision makes writing rules
a bit easier I think, but it could be confusing for new users.

Of course you can also add other suspicious string combinations, this is not
restricted to API calls, although that was my original intended purpose.

Installation is done with [Pipenv](https://pipenv.pypa.io/en/latest/)

References:  
https://posts.specterops.io/detection-spectrum-198a0bfb9302  
https://github.com/xme/fame_modules/tree/master/processing/floss_str  
https://ired.team/offensive-security/code-injection-process-injection/shellcode-execution-in-a-local-process-with-queueuserapc-and-nttestalert  
https://www.elastic.co/blog/ten-process-injection-techniques-technical-survey-common-and-trending-process  
https://ired.team/offensive-security/code-injection-process-injection/reflective-dll-injection  
https://www-users.math.umn.edu/~math-sa-sara0050/space16/slides/space2016121708-06.pdf
https://shellz.club/bypassing-crowdstrike-endpoint-detection-and-response/

TODO:  
⬚ Use FLOSS python mappings instead  
⬚ Create a YARA extension to decode stack strings/deobfuscate strings and use that instead

## Related projects
[capa](https://www.fireeye.com/blog/threat-research/2020/07/capa-automatically-identify-malware-capabilities.html) ([Github](https://github.com/fireeye/capa/))
