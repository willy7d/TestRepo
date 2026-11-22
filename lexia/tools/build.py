import json
s=open('template.html').read(); r=open('rig.json').read()
open('Lexia-camminata.html','w').write(s.replace('/*RIG*/null',r))
