"""Assemble the 30s page: shared <head> CSS from ad.template.html + the 30s scenes/script in ad30.body.html,
then inject the vector logo via build.py.  usage: python3 build30.py"""
import subprocess, sys
t = open('ad.template.html').read()
head = t[:t.index('</style>') + len('</style>')].replace('Swish Team Orders · 15s ad', 'Swish Team Orders · 30s ad')
open('ad30.template.html', 'w').write(head + '\n' + open('ad30.body.html').read())
subprocess.run([sys.executable, 'build.py', 'ad30.template.html', 'ad30.html'], check=True)
