"""film.template.html + dialogue.json + traced Swish logo -> film.html"""
import json
paths = open('logo_paths.txt').read().split('\n')
spark, word = paths[5], [p for i, p in enumerate(paths) if i != 5]
logo = (f'<svg class="logo" viewBox="-10 0 1602 525" xmlns="http://www.w3.org/2000/svg"><path fill="#fff" fill-rule="evenodd" d="{" ".join(word)}"/>'
        f'<g class="spark" style="transform-origin:91px 136px;transform-box:view-box"><path fill="#fff" d="{spark}"/></g></svg>')
h = open('film.template.html').read().replace('%%LOGO%%', logo).replace('%%DIALOGUE%%', open('dialogue.json').read())
open('film.html', 'w').write(h); print('built film.html', len(h))
