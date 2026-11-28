"""Builds the classic-style copy of the site into /classic, from the built pages in the repo root.
Same pages and content; adds assets/classic.css on top of site.css."""
import os, glob, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'classic'); os.makedirs(OUT, exist_ok=True)
for f in glob.glob(os.path.join(ROOT, '*.html')):
    s = open(f).read()
    s = re.sub(r'(src|href|poster)="assets/', r'\1="../assets/', s)
    s = s.replace('<link rel="stylesheet" href="../assets/site.css">', '<link rel="stylesheet" href="../assets/site.css">\n<link rel="stylesheet" href="../assets/classic.css">')
    s = s.replace("url('assets/", "url('../assets/").replace('url(assets/', 'url(../assets/')
    open(os.path.join(OUT, os.path.basename(f)), 'w').write(s)
print('classic pages:', len(glob.glob(os.path.join(OUT, '*.html'))))
