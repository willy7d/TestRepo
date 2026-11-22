import sys,re
s=open('template.html').read(); r=open('rig.json').read()
for kv in sys.argv[2:]:
    k,v=kv.split('='); s=re.sub(r'/\*%s\*/-?[\d.]+'%k,'/*%s*/%s'%(k,v),s)
open(sys.argv[1] if len(sys.argv)>1 else 'Lexia-camminata.html','w').write(s.replace('/*RIG*/null',r))
