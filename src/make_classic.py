"""Builds the classic-style copy of the site into /classic, from the built pages in the repo root.
Same pages and content; adds assets/classic.css on top of site.css."""
import os, glob, re
# Homepage only: a full-width wall of four films behind the headline.
# The footage is portrait (540x960), so four panels side by side stay sharp where one stretched film would not.
WALL = [('crockers', 'Lamb over the charcoal grill'), ('hero-feast', 'A Maroush host serving mezze at the table'),
        ('party', 'A celebration at Maroush'), ('beauchamp', 'Behind the bar at Beauchamp Place')]
def home_hero(s):
    panels = ''.join(f'<div class="hw"><video src="../assets/{n}.mp4" poster="../assets/{n}.jpg" autoplay muted loop playsinline preload="auto" aria-label="{a}"></video></div>' for n, a in WALL)
    a = s.index('<div class="hero-art">'); b = s.index('</section>', a)
    art_end = s.rindex('</div>', a, b)            # closes .wrap
    s = s[:a] + s[art_end:]                         # drop the framed portrait film
    s = s.replace('<section class="hero">', '<section class="hero">\n    <div class="hero-wall">' + panels + '</div>', 1)
    s = s.replace('<div class="hero-btns">', '<div class="hero-btns">', 1)
    return s.replace('<body>', '<body class="home fh">', 1)

# Inner pages: a soft, darkened copy of the page's own film or photo fills the header,
# with the sharp original framed beside the headline. Works with the portrait footage we have.
SOLO_BG = {'menu.html': 'grill-flames.webp', 'restaurants.html': 'frontage.webp', 'contact.html': 'lunch-outdoor.webp'}
def inner_hero(s, name):
    m = re.search(r'<section class="hero (rest|solo)">', s)
    if not m: return s
    b = s.index('</section>', m.end())
    art = re.search(r'<div class="hero-art">.*?<(img|video)[^>]*?src="([^"]+)"([^>]*)>', s[m.end():b], re.S)
    if art and art.group(1) == 'video':
        poster = re.search(r'poster="([^"]+)"', art.group(0))
        bg = f'<video src="{art.group(2)}"{" poster=" + chr(34) + poster.group(1) + chr(34) if poster else ""} autoplay muted loop playsinline preload="auto" aria-hidden="true"></video>'
    elif art:
        bg = f'<img src="{art.group(2)}" alt="" aria-hidden="true">'
    else:
        bg = f'<img src="../assets/{SOLO_BG.get(name, "mezze-table.webp")}" alt="" aria-hidden="true">'
    kind = 'soft' if not art else 'blur'
    return s[:m.end()] + f'\n    <div class="hero-bg {kind}">{bg}</div>' + s[m.end():]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'classic'); os.makedirs(OUT, exist_ok=True)
for f in glob.glob(os.path.join(ROOT, '*.html')):
    s = open(f).read()
    s = re.sub(r'(src|href|poster)="assets/', r'\1="../assets/', s)
    s = s.replace('<link rel="stylesheet" href="../assets/site.css">', '<link rel="stylesheet" href="../assets/site.css">\n<link rel="stylesheet" href="../assets/classic.css">')
    s = s.replace("url('assets/", "url('../assets/").replace('url(assets/', 'url(../assets/')
    # drop-down feature: the chandeliered room suits the Christmas card better than the bar film
    s = re.sub(r'(<a class="mfeat"[^>]*>\s*<div class="ph">)<video[^>]*></video>', r'\1<img src="../assets/room-crockers.webp" alt="The Lords Dining Room at Crockers Folly">', s)
    if os.path.basename(f) == 'index.html':
        s = home_hero(s)
    else:
        s = inner_hero(s, os.path.basename(f)).replace('<body>', '<body class="fh">', 1)
    open(os.path.join(OUT, os.path.basename(f)), 'w').write(s)
print('classic pages:', len(glob.glob(os.path.join(OUT, '*.html'))))
