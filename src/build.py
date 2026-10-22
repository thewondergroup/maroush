"""Builds the Maroush static site into dist/ (full HTML documents for GitHub Pages)
and artifact/ (same pages; index.html without its own skeleton for the preview)."""
import os, re, shutil, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, 'dist')
UBER = 'https://www.ubereats.com/gb/brand-city/london-eng/maroush'
MENU_PDF = {
    'food': 'https://www.maroush.com/wp-content/uploads/2024/07/Maroush-House-Menu-Sept-2022-with-sandwishes8pp-1.pdf',
    'drinks': 'https://www.maroush.com/wp-content/uploads/2024/07/Cocktail-menu-October-23-1.pdf',
    'wine': 'https://www.maroush.com/wp-content/uploads/2026/02/V2-Wine-List-Feb-2026.pdf',
}
FONTS = 'https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;800;900&family=Instrument+Sans:wght@400;500;600&family=Instrument+Serif:ital@0;1&family=Reem+Kufi:wght@500&display=swap'

def maps(q):
    return 'https://www.google.com/maps/search/?api=1&amp;query=' + q.replace(' ', '+')

# ---------------------------------------------------------------- venues
V = {
 'crockers-folly': dict(name='Crockers Folly', short='Crockers Folly', area="St John's Wood", kind='sit',
    addr=['24 Aberdeen Place', 'London NW8 8JR'], phone='020 7289 9898',
    hours=[('Monday – Sunday', '12pm – 12am')], summary='Daily 12pm–12am',
    blurb="Four rooms in a grand Victorian pub, from the 1898 Bar to the chandeliered Lords Dining Room.",
    img='room-crockers'),
 'beauchamp-place': dict(name='Beauchamp Place', short='Beauchamp Place', area='Knightsbridge', kind='sit',
    addr=['38 Beauchamp Place', 'London SW3 1NU'], phone='020 7581 5434',
    hours=[('Sunday – Wednesday', '12pm – 3am'), ('Thursday – Saturday', '12pm – 4.30am')],
    summary='Until 3am, 4.30am Thu–Sat',
    blurb="Mezze downstairs, a dining room upstairs and one of the latest kitchens in Knightsbridge.",
    img='kebab-platter'),
 'earls-court': dict(name='Earls Court', short='Earls Court', area='Earls Court', kind='sit',
    addr=['131 Earls Court Road', 'London SW5 9RQ'], phone='020 4553 6694',
    hours=[('Sunday – Wednesday', '8am – 12am'), ('Thursday – Saturday', '8am – 1am')],
    summary='From 8am, until 1am Thu–Sat',
    blurb="Breakfast through to late, with our signature chicken shawarma carved fresh all day.",
    img='shawarma-spit'),
 'edgware-road': dict(name='Edgware Road', short='Edgware Road', area='Marble Arch', kind='go',
    addr=['43 Edgware Road', 'London W2 2JE'], phone='020 4553 6690',
    hours=[('Monday – Sunday', '9am – 3am')], summary='Daily 9am–3am',
    blurb="On the street where Maroush began. Breakfast, wraps, shawarma and fresh juice until 3am.",
    img='shawarma-carving'),
 'kings-road': dict(name='Kings Road', short='Kings Road', area='Chelsea', kind='go',
    addr=['338 Kings Road', 'London SW3 5UR'], phone='020 4553 6691',
    hours=[('Monday – Sunday', '12pm – 1am')], summary='Daily 12pm–1am',
    blurb="Sharing platters and takeaway from an open kitchen, a short walk from Sloane Square.",
    img='mixed-grill'),
 'high-street-kensington': dict(name='High Street Kensington', short='High Street Ken', area='Kensington', kind='go',
    addr=['86 High Street Kensington', 'London W8 4SG'], phone='020 7938 2234',
    hours=[('Monday – Sunday', '12pm – 2am')], summary='Daily 12pm–2am',
    blurb="Shawarma to take away, juice pressed to order, Arabic coffee and booths for a slower meal.",
    img='moutabal'),
}
SIT = [k for k in V if V[k]['kind'] == 'sit']
GO = [k for k in V if V[k]['kind'] == 'go']

# ---------------------------------------------------------------- shared chrome
def head(title, desc):
    return f'''<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{html.escape(desc)}">
<link rel="icon" href="assets/logo-red.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/site.css">
'''

def nav_link(href, label, active):
    cur = ' aria-current="page"' if active == href else ''
    return f'<a href="{href}"{cur}>{label}</a>'

def mv(k):
    v = V[k]; verb = 'Book' if v['kind'] == 'sit' else 'Visit'
    return f'<a class="mv" href="{k}.html"><b>{v["short"]}</b><small>{v["area"]} · {v["summary"]}</small><em>{verb} →</em></a>'

def header(active=''):
    rest_cur = ' aria-current="page"' if active in V or active == 'restaurants.html' else ''
    return f'''<header class="top" id="top">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="Maroush home"><img src="assets/logo-red.png" alt="Maroush, Lebanese cuisine since 1981"></a>
    <nav class="nav" aria-label="Main">
      <div class="has-mega">
        <a href="restaurants.html" aria-haspopup="true"{rest_cur}>Restaurants <span class="chev" aria-hidden="true"></span></a>
        <div class="mega">
          <div class="mega-in">
            <div class="mcol">
              <h4>Sit down <span>Mezze, grills, wine · bookable</span></h4>
              {''.join(mv(k) for k in SIT)}
            </div>
            <div class="mcol">
              <h4>Grab &amp; go <span>Shawarma &amp; juice · walk in</span></h4>
              {''.join(mv(k) for k in GO)}
              <a class="mall" href="restaurants.html">All restaurants →</a>
            </div>
            <div class="mfeat">
              <div class="ph"><video src="assets/crockers.mp4" poster="assets/crockers.jpg" autoplay muted loop playsinline preload="metadata" aria-label="Maroush at Crockers Folly"></video></div>
              <div class="mfeat-c">
                <b>The original,<br>since 1981</b>
                <button class="btn btn-cream" type="button" data-book>Book a table →</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      {nav_link('menu.html', 'Menu', active)}
      {nav_link('about.html', 'Our story', active)}
      {nav_link('catering.html', 'Events &amp; catering', active)}
    </nav>
    <div class="top-r">
      <a class="btn btn-ghost" href="{UBER}" target="_blank" rel="noopener">Delivery</a>
      <button class="btn btn-red" type="button" data-book>Book a table</button>
      <button class="menu-btn" type="button" id="menuBtn">Menu</button>
    </div>
  </div>
</header>

<div class="mnav" id="mnav" role="dialog" aria-label="Menu">
  <button class="x" type="button" id="menuX" aria-label="Close menu">×</button>
  <small>Sit down</small>
  {''.join(f'<a class="sub" href="{k}.html">{V[k]["short"]}</a>' for k in SIT)}
  <small>Grab &amp; go</small>
  {''.join(f'<a class="sub" href="{k}.html">{V[k]["short"]}</a>' for k in GO)}
  <small>More</small>
  <a href="menu.html">Menu</a>
  <a href="about.html">Our story</a>
  <a href="catering.html">Events</a>
  <a href="contact.html">Contact</a>
  <a href="{UBER}" target="_blank" rel="noopener">Delivery</a>
</div>
'''

def footer():
    return f'''<footer>
  <div class="wrap">
    <div class="foot">
      <div class="foot-logo"><img src="assets/logo-cream.png" alt="Maroush, Lebanese cuisine since 1981"></div>
      <div class="foot-col"><h4>Restaurants</h4>
        {''.join(f'<a href="{k}.html">{V[k]["name"]}</a>' for k in SIT)}
      </div>
      <div class="foot-col"><h4>Shawarma &amp; juice</h4>
        {''.join(f'<a href="{k}.html">{V[k]["name"]}</a>' for k in GO)}
      </div>
      <div class="foot-col"><h4>Visit</h4>
        <a href="menu.html">Menu</a>
        <a href="about.html">Our story</a>
        <a href="catering.html">Events &amp; catering</a>
        <a href="contact.html">Contact</a>
        <a href="{UBER}" target="_blank" rel="noopener">Delivery</a>
      </div>
      <div class="foot-col"><h4>Say hello</h4>
        <span class="sel">hello@maroush.com</span>
        <span class="sel">020 7723 3666</span>
        <a href="https://www.instagram.com/maroush/" target="_blank" rel="noopener">Instagram</a>
        <a href="https://www.facebook.com/maroushgroup" target="_blank" rel="noopener">Facebook</a>
      </div>
    </div>
    <div class="foot-base"><span>© Maroush 1981–2026</span><span>Halal · Vegetarian and gluten-free options</span></div>
  </div>
</footer>

<div id="booking">
  <div class="scrim" data-close></div>
  <aside class="drawer" role="dialog" aria-modal="true" aria-labelledby="bkT">
    <div class="dh"><h3 id="bkT">Book a table</h3><button class="x" type="button" data-close aria-label="Close">×</button></div>
    <span class="label">Choose a restaurant</span>
    {''.join(f'<a class="di" href="{k}.html#visit"><div><b>{V[k]["short"]}</b><small>{V[k]["area"]} · {V[k]["phone"]}</small></div><span class="ar">→</span></a>' for k in SIT)}
    <span class="label">No booking needed</span>
    <div class="di"><div><b>Edgware Road · Kings Road · High St Ken</b><small>Shawarma &amp; juice bars, walk in any time</small></div></div>
    <span class="label">Large group or private party?</span>
    <a class="di" href="catering.html"><div><b>Events &amp; catering</b><small>catering@maroush.com</small></div><span class="ar">→</span></a>
  </aside>
</div>
<script src="assets/site.js"></script>
'''

def crumbs(*items):
    parts = ['<a href="index.html">Home</a>']
    for href, label in items[:-1]:
        parts.append(f'<span>/</span><a href="{href}">{label}</a>')
    parts.append(f'<span>/</span><b>{items[-1][1]}</b>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap">{"".join(parts)}</div></nav>\n'

def ph(name, alt, cls='ph peak', video=False, eager=False):
    if video:
        return f'<div class="{cls}"><video src="assets/{name}.mp4" poster="assets/{name}.jpg" autoplay muted loop playsinline preload="{"auto" if eager else "metadata"}" aria-label="{alt}"></video></div>'
    return f'<div class="{cls}"><img src="assets/{name}.webp" alt="{alt}" loading="{"eager" if eager else "lazy"}"></div>'

def dish(img, name, ar):
    return f'<figure class="dish rv">{ph(img, name)}<figcaption><b>{name}</b><i>{ar}</i></figcaption></figure>'

def menus_row(label='Menus'):
    return f'''<div class="menus">
        <span class="label">{label}</span>
        <a href="menu.html">Full menu →</a>
        <a href="{MENU_PDF['drinks']}" target="_blank" rel="noopener">Cocktails ↗</a>
        <a href="{MENU_PDF['wine']}" target="_blank" rel="noopener">Wine ↗</a>
      </div>'''

def others(exclude):
    cards = []
    for k, v in V.items():
        if k == exclude: continue
        tag = '<span class="tag book">Bookable</span>' if v['kind'] == 'sit' else '<span class="tag">Walk-in</span>'
        cards.append(f'<a class="other" href="{k}.html"><b>{v["short"]}</b><small>{v["area"]} · {v["summary"]}</small>{tag}</a>')
    return f'''<section class="section" id="more">
    <div class="wrap">
      <div class="head"><div><div class="label">More Maroush</div><h2>Five more<br><span class="it">across London</span></h2></div></div>
      <div class="others">{''.join(cards)}</div>
    </div>
  </section>'''

def visit_band(k):
    v = V[k]
    hours = ''.join(f'<dt>{d}</dt><dd>{t}</dd>' for d, t in v['hours'])
    q = 'Maroush ' + ' '.join(v['addr'])
    if v['kind'] == 'sit':
        act = '<div class="btns"><button class="btn btn-cream" type="button" data-book>Book a table <span class="ar">→</span></button></div>'
        title = 'See you<br><span class="it">soon</span>'
    else:
        act = f'<p class="walkin">No booking needed. Just walk in.</p><div class="btns"><a class="btn btn-cream" href="{UBER}" target="_blank" rel="noopener">Order delivery <span class="ar">→</span></a></div>'
        title = 'Drop<br><span class="it">by</span>'
    return f'''<section class="section visit" id="visit">
    <div class="wrap visit-grid">
      <div><div class="label" style="opacity:.8">Plan your visit</div><h2 style="margin-top:14px">{title}</h2></div>
      <div class="vcol">
        <h4>Opening hours</h4>
        <dl class="hours">{hours}</dl>
        <h4 style="margin-top:18px">Address</h4>
        <div class="vbig">{'<br>'.join(v['addr'])}</div>
        <div class="btns"><a class="btn btn-ghost" href="{maps(q)}" target="_blank" rel="noopener">Directions ↗</a></div>
      </div>
      <div class="vcol">
        <h4>Get in touch</h4>
        <div class="vbig sel">{v['phone']}</div>
        <div class="sel" style="font-size:17px">hello@maroush.com</div>
        {act}
      </div>
    </div>
  </section>'''

def rest_hero(k, video, sub, stamp):
    v = V[k]
    label = ('Sit down' if v['kind'] == 'sit' else 'Grab &amp; go') + ' · ' + v['area']
    words = v['name'].split(' ')
    if len(words) >= 3:
        lines = [' '.join(words[:2]), ' '.join(words[2:])]
    elif len(words) == 2:
        lines = words
    else:
        lines = [v['name']]
    lns = ''.join(f'<span class="ln"><span>{w}</span></span>' for w in lines)
    if v['kind'] == 'sit':
        b1 = '<button class="btn btn-cream" type="button" data-book>Book a table <span class="ar">→</span></button>'
    else:
        b1 = f'<a class="btn btn-cream" href="{UBER}" target="_blank" rel="noopener">Order delivery <span class="ar">→</span></a>'
    q = 'Maroush ' + ' '.join(v['addr'])
    open_ = v['summary'] if len(v['hours']) > 1 else v['hours'][0][1].replace(' – ', '–')
    open_label = 'Open' if len(v['hours']) > 1 else 'Open daily'
    return f'''<section class="hero rest">
    <img class="hero-mark" src="assets/mark-cream.png" alt="" aria-hidden="true">
    <div class="wrap">
      <div class="hero-copy">
        <div class="label">{label}</div>
        <h1{' class="long"' if len(v['name'])>11 else ''}><span class="ln"><span class="it">Maroush</span></span>{lns}</h1>
        <p class="hero-sub">{sub}</p>
        <dl class="facts">
          <div><dt>{open_label}</dt><dd>{open_}</dd></div>
          <div><dt>Find us</dt><dd>{v['addr'][0]}<br>{v['addr'][1].replace('London ', '')}</dd></div>
          <div><dt>Call</dt><dd class="sel">{v['phone']}</dd></div>
        </dl>
        <div class="hero-btns">
          {b1}
          <a class="btn btn-ghost" href="{maps(q)}" target="_blank" rel="noopener">Directions</a>
        </div>
      </div>
      <div class="hero-art">
        {ph(video, 'Inside Maroush ' + v['name'], video=True, eager=True)}
        <div class="stamp"><div>{stamp}</div></div>
      </div>
    </div>
  </section>'''

# ---------------------------------------------------------------- restaurant pages
def sit_page(k, video, sub, stamp, about_h, about_p, about_points, imgs, dishes_):
    v = V[k]
    pts = ''.join(f'<li>{p}</li>' for p in about_points)
    return crumbs(('restaurants.html', 'Restaurants'), ('', v['name'])) + f'''<main>
  {rest_hero(k, video, sub, stamp)}

  <section class="section">
    <div class="wrap split">
      <div class="split-art rv">
        {ph(imgs[0], imgs[1], 'ph big peak')}
        {ph(imgs[2], imgs[3], 'ph small')}
      </div>
      <div class="split-copy">
        <div class="label">The room</div>
        <h2>{about_h}</h2>
        <p>{about_p}</p>
        <ul class="ticks">{pts}</ul>
      </div>
    </div>
  </section>

  <section class="section" id="food" style="padding-top:0">
    <div class="wrap">
      <div class="head">
        <div><div class="label">What to order</div><h2>Start cold,<br>finish <span class="it">on the grill</span></h2></div>
        <p>Share a spread of mezze for the table, then move on to charcoal-grilled meats and shawarma from the spit.</p>
      </div>
      <div class="dishes">{''.join(dish(*d) for d in dishes_)}</div>
      {menus_row()}
    </div>
  </section>

  {visit_band(k)}
  {others(k)}
</main>'''

COUNTER = [
 ('Chicken shawarma', 'Carved from the spit, with garlic sauce and pickles'),
 ('Lamb shawarma', 'Slow-roasted lamb with tahini'),
 ('Falafel', 'Chickpea and fava, fried to order, with tahini'),
 ('Halloumi', 'Char-grilled cheese with tomato and cucumber'),
 ('Taouk shish', 'Chargrilled chicken with garlic sauce'),
 ('Kafta', 'Minced lamb skewers with parsley and onion'),
 ('Batata harra', 'Spicy potatoes with garlic, coriander and chilli'),
 ('Mezze to go', 'Hommos, moutabal, tabbouleh and more'),
]
JUICES = ['Fresh orange', 'Fresh lemon', 'Mango', 'Fruit cocktail', 'Laban ayran', 'Arabic coffee']

def go_page(k, video, sub, stamp, about_h, about_p, about_points, imgs):
    v = V[k]
    pts = ''.join(f'<li>{p}</li>' for p in about_points)
    items = ''.join(f'<li><b>{n}</b><span>{d}</span></li>' for n, d in COUNTER)
    chips = ''.join(f'<span>{j}</span>' for j in JUICES)
    return crumbs(('restaurants.html', 'Restaurants'), ('', v['name'])) + f'''<main>
  {rest_hero(k, video, sub, stamp)}

  <section class="section">
    <div class="wrap counter">
      <div class="counter-copy">
        <div class="label">On the counter</div>
        <h2>Wrapped <span class="it">to order</span></h2>
        <p>Everything is made in front of you and wrapped in warm Lebanese bread. Eat in or take it with you.</p>
        <ul class="clist">{items}</ul>
        <div class="chips"><span class="label">To drink</span>{chips}</div>
      </div>
      <div class="counter-art rv">
        {ph('wraps', 'Wraps being made at the counter', 'ph peak', video=True)}
      </div>
    </div>
  </section>

  <section class="section lords">
    <div class="wrap">
      <div class="lords-art rv">
        {ph(imgs[0], imgs[1], 'ph big peak')}
        {ph(imgs[2], imgs[3], 'ph chef')}
      </div>
      <div class="lords-copy">
        <div class="label">The place</div>
        <h2>{about_h}</h2>
        <p>{about_p}</p>
        <ul class="ticks">{pts}</ul>
        <a class="btn btn-red" href="menu.html">See the full menu <span class="ar">→</span></a>
      </div>
    </div>
  </section>

  {visit_band(k)}
  {others(k)}
</main>'''

PAGES = {}
PAGES['beauchamp-place'] = ('Maroush Beauchamp Place',
  "Maroush Beauchamp Place, Knightsbridge: Lebanese mezze, grills and wraps until 3am, and 4.30am Thursday to Saturday. 38 Beauchamp Place, SW3 1NU.",
  sit_page('beauchamp-place', 'beauchamp',
    'Knightsbridge’s late-night Lebanese. Hot and cold mezze downstairs, a dining room upstairs, and a kitchen that keeps going long after everywhere else has closed.',
    '<span>Open</span><b>4.30</b><span>Thu–Sat</span>',
    'Lively, late<br><span class="it">and generous</span>',
    'A favourite with a mixed Knightsbridge crowd for decades. Drop in for a quick wrap to take away, share mezze at the counter, or settle into the first-floor dining room for a proper Lebanese feast.',
    ['First-floor dining room for fuller meals', 'Plenty of vegetarian and gluten-free dishes', 'Wraps to go, all evening'],
    ['kebab-platter', 'Mixed grill with kafta and lamb', 'bar-glass', 'A glass of fizz with mezze'],
    [('mezze', 'Cold mezze', 'مازة'), ('fattoush', 'Fattoush', 'فتوش'), ('kebab-platter', 'Mixed grill', 'مشاوي'), ('shawarma-spit', 'Shawarma', 'شاورما')]))
PAGES['earls-court'] = ('Maroush Earls Court',
  "Maroush Earls Court: Lebanese breakfast, mezze, grills and signature chicken shawarma from 8am. 131 Earls Court Road, SW5 9RQ.",
  sit_page('earls-court', 'earls',
    'Breakfast through to late on Earls Court Road. Quick, warm service and our signature chicken shawarma, carved fresh all day.',
    '<span>Open</span><b>8am</b><span>daily</span>',
    'Morning till<br><span class="it">late night</span>',
    'Earls Court is Maroush at its quickest and most relaxed. Start the day with foul moudamas and fresh bread, come back for a shawarma at lunch, or share a table of mezze with friends in the evening.',
    ['Lebanese breakfast from 8am', 'Signature chicken shawarma, carved to order', 'Open until 1am Thursday to Saturday'],
    ['shawarma-spit', 'Chicken shawarma in front of the spit', 'lunch-outdoor', 'A shared lunch of mezze and grills'],
    [('mezze-table', 'Mezze', 'مازة'), ('shawarma-spit', 'Shawarma', 'شاورما'), ('kibbeh', 'Kibbeh', 'كبة'), ('mixed-grill', 'Mixed grill', 'مشاوي')]))
PAGES['edgware-road'] = ('Maroush Edgware Road',
  "Maroush on Edgware Road, where it all began in 1981: shawarma, wraps, Lebanese breakfast and fresh juice, open daily 9am to 3am. 43 Edgware Road, W2 2JE.",
  go_page('edgware-road', 'wraps',
    'On the street where Maroush began in 1981. Breakfast, wraps, shawarma and fresh juice, from 9am until 3am every day.',
    '<span>Est.</span><b>1981</b><span>Edgware Rd</span>',
    'Where it<br><span class="it">all began</span>',
    'Edgware Road is the heart of Lebanese London, and Maroush has been part of it since 1981. This is the fast, friendly side of the family: light breakfasts in the morning, wraps at lunch and shawarma long into the night.',
    ['Walk in any time, no booking', 'Breakfast from 9am', 'Open until 3am, every day'],
    ['shawarma-carving', 'Carving shawarma from the spit', 'moutabal', 'Moutabal with pomegranate']))
PAGES['kings-road'] = ('Maroush Kings Road',
  "Maroush Kings Road, Chelsea: Lebanese sharing platters, wraps and takeaway from an open kitchen, open daily 12pm to 1am. 338 Kings Road, SW3 5UR.",
  go_page('kings-road', 'kings',
    'Lebanese sharing platters and takeaway from an open kitchen on the Kings Road. Open every day from noon until 1am.',
    '<span>Open</span><b>1am</b><span>daily</span>',
    'Chelsea’s<br><span class="it">open kitchen</span>',
    'A modern room with the grill in full view, made for a lunch break between shops or a quick supper before the theatre. Sloane Square, the Royal Court and the Chelsea Antiques Market are all close by.',
    ['Watch everything cooked in the open kitchen', 'Sharing platters to eat in', 'Takeaway and delivery'],
    ['mixed-grill', 'A mixed grill platter', 'charcoal', 'Skewers over charcoal']))
PAGES['high-street-kensington'] = ('Maroush High Street Kensington',
  "Maroush High Street Kensington: shawarma and wraps to take away, fresh juice, Arabic coffee and booths to eat in. Open daily 12pm to 2am. 86 High Street Kensington, W8 4SG.",
  go_page('high-street-kensington', 'hsk',
    'Shawarma to take away, juice pressed to order and Arabic coffee, with cosy booths if you want to stay. Open every day until 2am.',
    '<span>Open</span><b>2am</b><span>daily</span>',
    'Quick bite or<br><span class="it">slow supper</span>',
    'Our Kensington spot works both ways. Grab a wrap and a fresh juice on the way past, or slide into one of the booths for a plate of mezze and a Lebanese coffee.',
    ['Booths for a more relaxed meal', 'Fresh juice and Arabic coffee', 'Open until 2am, every day'],
    ['moutabal', 'Moutabal with pomegranate', 'shawarma-spit', 'Chicken shawarma']))

# ---------------------------------------------------------------- restaurants listing
def rcard(k):
    v = V[k]
    act = ('<button class="btn btn-red" type="button" data-book>Book</button>' if v['kind'] == 'sit'
           else f'<a class="btn btn-red" href="{UBER}" target="_blank" rel="noopener">Delivery</a>')
    return f'''<article class="rcard rv">
        <a href="{k}.html" class="rcard-img">{ph(v['img'], v['name'])}</a>
        <div class="rcard-body">
          <div class="label">{v['area']}</div>
          <h3><a href="{k}.html">{v['name']}</a></h3>
          <p>{v['blurb']}</p>
          <dl><dt>Hours</dt><dd>{'<br>'.join(d + ' ' + t for d, t in v['hours'])}</dd><dt>Address</dt><dd>{', '.join(v['addr'])}</dd><dt>Phone</dt><dd class="sel">{v['phone']}</dd></dl>
          <div class="rcard-btns"><a class="btn btn-line" href="{k}.html">View restaurant</a>{act}</div>
        </div>
      </article>'''

PAGES['restaurants'] = ('Maroush Restaurants',
  "All six Maroush restaurants in London: sit-down Lebanese restaurants in St John's Wood, Knightsbridge and Earls Court, plus shawarma and juice bars on Edgware Road, Kings Road and High Street Kensington.",
  crumbs(('', 'Restaurants')) + f'''<main>
  <section class="hero solo">
    <img class="hero-mark" src="assets/mark-cream.png" alt="" aria-hidden="true">
    <div class="wrap">
      <div class="hero-copy">
        <div class="label">Six in London</div>
        <h1><span class="ln"><span class="it">Find your</span></span><span class="ln"><span>Maroush</span></span></h1>
        <p class="hero-sub">Settle in for mezze and Lebanese wine at one of our restaurants, or walk in to a shawarma and juice bar for something quick.</p>
        <div class="jump"><a href="#sit">Sit down</a><a href="#go">Grab &amp; go</a></div>
      </div>
    </div>
  </section>
  <section class="section" id="sit">
    <div class="wrap">
      <div class="head"><div><div class="label">Sit down · bookable</div><h2>Restaurants</h2></div><p>Hot and cold mezze, charcoal grills and Lebanese wine. Book ahead and stay late.</p></div>
      <div class="rcards">{''.join(rcard(k) for k in SIT)}</div>
    </div>
  </section>
  <section class="section" id="go" style="padding-top:0">
    <div class="wrap">
      <div class="head"><div><div class="label">Grab &amp; go · walk in</div><h2>Shawarma<br><span class="it">&amp; juice</span></h2></div><p>Wraps, shawarma, fresh juice and Arabic coffee. No booking needed, open late.</p></div>
      <div class="rcards">{''.join(rcard(k) for k in GO)}</div>
    </div>
  </section>
</main>''')

# ---------------------------------------------------------------- menu
# (name, description, price, allergens, vegan)
MENU = [
 ('cold', 'Cold mezze', 'مازة باردة', 'Served with Lebanese bread', [
  ('Hommos', 'Chickpeas blended with tahini, lemon and olive oil', '7.25', 'Sesame', 0),
  ('Roasted red pepper hommos', 'Hommos with roasted red pepper and paprika', '7.50', 'Sesame', 0),
  ('Hommos Beiruty', 'Hommos with parsley and green chilli', '7.50', 'Sesame', 0),
  ('Moutabal baba ghanouj', 'Smoked aubergine with tahini and sumac', '7.95', 'Sesame, gluten', 0),
  ('Tabbouleh', 'Parsley, bulgur, tomato and mint', '7.50', 'Gluten', 0),
  ('Mouhamara', 'Roasted red pepper and walnut dip with cumin', '8.50', 'Nuts, gluten', 0),
  ('Wark inab b’zeit', 'Vine leaves stuffed with rice, herbs and lemon', '8.00', '', 1),
  ('Labneh', 'Strained yoghurt with olive oil and mint', '7.00', 'Milk', 0),
  ('Moujaddarah', 'Lentils and rice with cumin and crispy onion', '6.00', '', 0),
  ('Bazenjan al-rahib', 'Grilled aubergine with vegetables and pomegranate', '7.50', '', 0),
  ('Moussaka', 'Fried aubergine and chickpeas in tomato sauce', '7.50', '', 0),
  ('Loubieh b’zeit', 'Green beans stewed in tomato and olive oil', '6.50', '', 1),
  ('Bammieh b’zeit', 'Okra with tomato and coriander', '6.50', '', 1),
  ('Kabis', 'Pickled cucumber, turnip and chilli', '5.50', 'Sulphites', 0),
 ]),
 ('hot', 'Hot mezze', 'مازة ساخنة', 'Served with Lebanese bread', [
  ('Falafel', 'Chickpea and fava croquettes with tahini', '7.50', 'Sesame, sulphites', 0),
  ('Kibbeh', 'Lamb and bulgur croquettes filled with pine nuts', '7.75', 'Milk, gluten', 0),
  ('Halloum meshwi', 'Char-grilled halloumi with tomato and cucumber', '8.50', 'Milk', 0),
  ('Batata harra', 'Spicy potatoes with garlic, coriander and chilli', '7.50', '', 0),
  ('Foul moudamas', 'Broad beans with garlic, cumin and lemon', '7.50', '', 0),
  ('Pumpkin kebbeh', 'Bulgur and pumpkin with spinach and pine nuts', '7.50', 'Gluten', 0),
  ('Awarma hommos', 'Hommos topped with sautéed lamb and pine nuts', '8.50', 'Sesame', 0),
  ('Chicken shawarma hommos', 'Hommos topped with sliced chicken shawarma', '9.00', 'Sesame', 0),
  ('Lamb shawarma hommos', 'Hommos topped with sliced lamb shawarma', '10.50', 'Sesame', 0),
  ('Jawaneh', 'Char-grilled chicken wings with garlic sauce', '6.50', '', 0),
  ('Chicken liver', 'Pan-fried with pomegranate molasses', '7.50', '', 0),
  ('Fattet hommos b’laban', 'Crispy bread, chickpeas and yoghurt', '7.75', 'Milk, gluten', 0),
  ('Maqaneq', 'Flambéed mini sausages with pomegranate molasses', '8.75', '', 0),
  ('Soujok', 'Spicy sausages sautéed with tomato', '8.75', '', 0),
 ]),
 ('salads', 'Salads, soups &amp; bakery', 'سلطات', '', [
  ('Fattoush', 'Mixed salad with crispy bread and pomegranate molasses', '7.50', 'Gluten', 0),
  ('Maroush salad', 'Mixed salad with radish and sumac', '6.50', '', 0),
  ('Spicy Lebanese salad', 'Mixed salad with green chilli and sumac', '6.50', '', 0),
  ('Quinoa tabbouleh', 'Tabbouleh made with quinoa and pomegranate', '7.95', '', 0),
  ('Cucumber with yoghurt', 'Yoghurt, cucumber and mint', '6.00', 'Milk', 0),
  ('Lentil soup', 'Red lentils with cumin', '6.00', 'Gluten', 0),
  ('Creamy chicken soup', 'Chicken broth with cream and black pepper', '6.50', 'Milk, celery, gluten', 0),
  ('Fatayer b’sabanekh', 'Baked spinach pastries', '7.00', 'Gluten', 0),
  ('Mini manakish za’atar', 'Flatbread with thyme and sesame', '4.00', 'Sesame, gluten', 0),
  ('Arayes Maroush', 'Char-grilled bread stuffed with minced lamb', '7.00', 'Gluten', 0),
  ('Sambousek', 'Fried pastries with cheese, or with lamb', '7.00', 'Milk, gluten', 0),
 ]),
 ('grill', 'From the charcoal grill', 'مشاوي', 'Served with Lebanese bread', [
  ('Meshwi lahem', 'Skewers of lamb cubes', '18.50', '', 0),
  ('Taouk shish', 'Skewers of chicken with garlic sauce', '17.00', '', 0),
  ('Meshwi kafta', 'Skewers of minced lamb', '17.00', '', 0),
  ('Maroush mixed grill', 'Lamb kafta, chicken and lamb cubes', '18.50', '', 0),
  ('Kafta khosh-khash', 'Lamb kafta with spicy ratatouille', '17.50', '', 0),
  ('Yoghurtieh kafta', 'Minced lamb with yoghurt and bread', '17.00', 'Milk, gluten', 0),
  ('Lamb kastaleta', 'Lamb cutlets with fries', '20.00', '', 0),
  ('Meshwi farrouj', 'Boneless baby chicken with garlic sauce', '17.50', '', 0),
  ('Grilled sea bass', 'Whole chargrilled sea bass with tahini', '23.00', 'Fish, sesame', 0),
 ]),
 ('shawarma', 'Shawarma &amp; mains', 'شاورما', '', [
  ('Lamb shawarma', 'Roasted lamb from the spit with tahini', '18.00', 'Sesame, gluten', 0),
  ('Chicken shawarma', 'Roasted chicken from the spit with garlic sauce', '17.00', 'Gluten', 0),
  ('Mixed shawarma', 'Lamb and chicken shawarma', '18.00', 'Sesame, gluten', 0),
  ('Lamb shank', 'Mediterranean-spiced lamb shank with brown rice', '19.00', 'Milk, celery, gluten', 0),
  ('Roast chicken', 'Roasted chicken with brown rice', '16.50', 'Milk, celery, gluten', 0),
  ('Aubergine &amp; chickpea casserole', 'With rice', '16.00', '', 1),
  ('Okra stew', 'With rice', '16.00', '', 1),
  ('Green bean stew', 'With rice', '16.00', '', 1),
 ]),
 ('wraps', 'Wraps', 'لفائف', 'In Lebanese bread', [
  ('Falafel', '', '6.00', 'Sesame, sulphites', 0),
  ('Batata harra &amp; fried vegetables', '', '6.00', '', 0),
  ('Halloumi', '', '7.00', 'Milk', 0),
  ('Chicken shawarma', '', '7.50', '', 0),
  ('Lamb shawarma', '', '8.00', 'Sesame', 0),
  ('Mixed shawarma', '', '8.00', 'Sesame', 0),
  ('Taouk shish', '', '7.50', '', 0),
  ('Meshwi lahem', '', '8.50', 'Sesame', 0),
  ('Meshwi kafta', '', '7.50', 'Sesame', 0),
  ('Maqaneq', '', '7.00', 'Sesame', 0),
  ('Soujok', '', '7.00', '', 0),
 ]),
 ('sweets', 'Desserts', 'حلويات', '', [
  ('Knefeh', 'Warm cheese pastry with syrup', '6.00', 'Milk, gluten, nuts, sulphites', 0),
  ('Baklawa', 'Filo pastries with nuts and syrup', '5.50', 'Milk, sesame, nuts, peanuts, gluten', 0),
  ('Ossmallieh', 'Crisp pastry with cream and pistachio', '5.00', 'Milk, nuts, gluten, sulphites', 0),
  ('Mouhallabieh', 'Lebanese milk pudding', '5.00', 'Milk, nuts', 0),
  ('Meghli', 'Spiced rice pudding with nuts', '5.00', 'Nuts, sulphites', 0),
  ('Rice pudding', '', '5.00', 'Milk, nuts', 0),
 ]),
]
SETS = [
 ('Lunch platter', 'Six starters with two skewers of chicken or kafta', '25'),
 ('Vegan sharing menu for two', 'A full spread of vegan mezze and mains', '65'),
 ('Sharing menu for two', 'Mezze, grills and dessert to share', '70'),
 ('Sharing menu for four', 'The full feast, with a bottle of house wine', '130'),
]

def menu_page():
    tabs = ''.join(f'<a href="#{sid}">{t}</a>' for sid, t, _, _, _ in MENU)
    secs = []
    for sid, title, ar, note, items in MENU:
        rows = []
        for n, d, p, al, vg in items:
            vgt = '<span class="vg" title="Vegan">VG</span>' if vg else ''
            alt = f'<span class="al">{al}</span>' if al else ''
            rows.append(f'<li><div class="mi-top"><b>{n}</b>{vgt}<span class="dots"></span><span class="pr">£{p}</span></div>{f"<p>{d}</p>" if d else ""}{alt}</li>')
        secs.append(f'''<section class="msec" id="{sid}">
        <div class="msec-h"><h2>{title}</h2><i>{ar}</i>{f'<span>{note}</span>' if note else ''}</div>
        <ul class="mlist">{''.join(rows)}</ul>
      </section>''')
    sets = ''.join(f'<div class="setc"><b>{n}</b><p>{d}</p><span class="pr">£{p}</span></div>' for n, d, p in SETS)
    return crumbs(('', 'Menu')) + f'''<main>
  <section class="hero solo">
    <img class="hero-mark" src="assets/mark-cream.png" alt="" aria-hidden="true">
    <div class="wrap">
      <div class="hero-copy">
        <div class="label">Food · drinks · wine</div>
        <h1><span class="ln"><span class="it">The</span></span><span class="ln"><span>Menu</span></span></h1>
        <p class="hero-sub">Order lots and share everything. That’s the Lebanese way. Start with cold mezze, add a few hot dishes, then something from the charcoal grill.</p>
        <div class="jump"><a href="{MENU_PDF['food']}" target="_blank" rel="noopener">Food PDF ↗</a><a href="{MENU_PDF['drinks']}" target="_blank" rel="noopener">Cocktails ↗</a><a href="{MENU_PDF['wine']}" target="_blank" rel="noopener">Wine ↗</a></div>
      </div>
    </div>
  </section>
  <nav class="mtabs" aria-label="Menu sections"><div class="wrap">{tabs}<a href="#sets">Set menus</a></div></nav>
  <div class="section menu-body">
    <div class="wrap">
      <section class="sets" id="sets">
        <div class="msec-h"><h2>Set menus</h2><i>للمشاركة</i><span>The easiest way to try a bit of everything</span></div>
        <div class="setgrid">{sets}</div>
      </section>
      {''.join(secs)}
      <div class="mnote">
        <p><b>VG</b> vegan. Allergens are listed under each dish. Our kitchens handle gluten, crustaceans, eggs, fish, peanuts, soya, milk, nuts, celery, mustard, sesame and molluscs, so we can’t guarantee any dish is free of them. Please tell your server about any allergy. Some meat dishes may contain bones.</p>
        <p>Prices in pounds and include VAT. A discretionary 12.5% service charge is added to your bill. Menu shown is for Crockers Folly and Beauchamp Place; dishes and prices vary at other restaurants.</p>
      </div>
    </div>
  </div>
</main>'''
PAGES['menu'] = ('Maroush Menu', "The Maroush menu: Lebanese cold and hot mezze, salads, charcoal grills, shawarma, wraps, desserts and set sharing menus, with prices and allergens.", menu_page())

# ---------------------------------------------------------------- about
PAGES['about'] = ('Maroush Our Story', "The story of Maroush: Marouf and Houda Abouzaki opened London’s original Lebanese restaurant on Edgware Road in 1981. Our food, our hospitality and how we cook.",
  crumbs(('', 'Our story')) + f'''<main>
  <section class="hero rest">
    <img class="hero-mark" src="assets/mark-cream.png" alt="" aria-hidden="true">
    <div class="wrap">
      <div class="hero-copy">
        <div class="label">Our story · since 1981</div>
        <h1><span class="ln"><span class="it">London’s</span></span><span class="ln"><span>original</span></span><span class="ln"><span>Lebanese</span></span></h1>
        <p class="hero-sub">Marouf and Houda Abouzaki opened the first Maroush on Edgware Road in 1981. Forty-five years later, we still cook the way they did: generously, traditionally and to share.</p>
      </div>
      <div class="hero-art">
        {ph('frontage', 'The Maroush frontage with its blue awnings', 'ph peak', eager=True)}
        <div class="stamp"><div><span>Est.</span><b>1981</b><span>Edgware Rd</span></div></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap split">
      <div class="split-art rv">
        {ph('shawarma-carving', 'Carving shawarma from the spit', 'ph big peak')}
        {ph('chef', 'A Maroush chef', 'ph small')}
      </div>
      <div class="split-copy">
        <div class="label">How it started</div>
        <h2>From Beirut<br><span class="it">to Edgware Road</span></h2>
        <p>Marouf and Houda came to London from Lebanon while war was tearing their country apart. Leaving family and friends behind was hard, but London made them welcome, and Londoners were just beginning to discover food from around the world.</p>
        <p>In 1981 they opened Maroush on Edgware Road, serving Lebanese food exactly as it is made at home. It helped turn the street into London’s home of Lebanese cooking, and it is busier today than it was then.</p>
      </div>
    </div>
  </section>

  <section class="section lords">
    <div class="wrap">
      <div class="lords-copy" style="grid-column:1/-1;max-width:none">
        <div class="label">The Lebanese table</div>
        <h2>Many small dishes,<br><span class="it">shared slowly</span></h2>
      </div>
      <div class="pillars" style="grid-column:1/-1">
        <div><b>Generosity</b><p>A Lebanese meal is never three courses. It is a table covered in small dishes, made to nourish and to entertain.</p></div>
        <div><b>Sharing</b><p>Food is how we gather: family dinners, catching up with friends, closing a deal. Everything goes in the middle.</p></div>
        <div><b>Hospitality</b><p>Conversation, family and a cup of kahwah. We want every guest to feel they have stepped into a home in Beirut.</p></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="head"><div><div class="label">Our kitchen</div><h2>Cooked fresh,<br><span class="it">wasted never</span></h2></div><p>Our own production kitchen supplies every restaurant. Our team is trained and vetted, and we meet or beat every health, hygiene and environmental standard.</p></div>
      <div class="facts4">
        <div><b>Zero</b><span>Kitchen waste sent to landfill</span></div>
        <div><b>Food waste</b><span>Turned into energy with Veolia</span></div>
        <div><b>Recyclable</b><span>Food-safe takeaway packaging</span></div>
        <div><b>Cleaner</b><span>LPG-ready delivery vans</span></div>
      </div>
    </div>
  </section>

  <section class="section heritage">
    <div class="wrap">
      <div class="press" style="margin-top:0;border-top:0;padding-top:0">
        <blockquote class="rv"><q>Dazzlingly fresh, beguilingly fragrant, exotic yet earthy.</q><cite>AA Gill</cite></blockquote>
        <blockquote class="rv"><q>Among the best meat-based meals I have ever eaten.</q><cite>Time Out</cite></blockquote>
        <blockquote class="rv"><q>Unbelievably good.</q><cite>The Times</cite></blockquote>
        <blockquote class="rv"><q>Absolutely worth the journey.</q><cite>The Guardian</cite></blockquote>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap welcome">
      <span class="sahtein" aria-hidden="true">أهلاً وسهلاً</span>
      <blockquote>“Thank you for choosing Maroush. Serving the best Lebanese food in London is how we say thank you for the welcome this city gave us.”</blockquote>
      <div class="sig"><b>Marouf Abouzaki</b>Founder</div>
      <div class="hero-btns" style="justify-content:center"><a class="btn btn-red" href="restaurants.html">Find a restaurant <span class="ar">→</span></a><a class="btn btn-line" href="menu.html">See the menu</a></div>
    </div>
  </section>
</main>''')

# ---------------------------------------------------------------- forms
def field(id_, label, kind='text', req=False, opts=None, full=False, ph_=''):
    r = ' required' if req else ''
    star = ' <em>*</em>' if req else ''
    cls = ' class="full"' if full else ''
    if kind == 'select':
        o = ''.join(f'<option>{x}</option>' for x in opts)
        inp = f'<select id="{id_}" name="{id_}"{r}><option value="">Choose one</option>{o}</select>'
    elif kind == 'textarea':
        inp = f'<textarea id="{id_}" name="{id_}" rows="5"{r} placeholder="{ph_}"></textarea>'
    else:
        inp = f'<input id="{id_}" name="{id_}" type="{kind}"{r} placeholder="{ph_}">'
    return f'<div{cls}><label for="{id_}">{label}{star}</label>{inp}</div>'

def form(id_, fields, button, fallback):
    return f'''<form class="form" id="{id_}" data-endpoint="" data-fallback="{fallback}" novalidate>
        {''.join(fields)}
        <div class="full form-foot"><button class="btn btn-red" type="submit">{button} <span class="ar">→</span></button><p class="form-msg" role="status" aria-live="polite"></p></div>
      </form>'''

# ---------------------------------------------------------------- catering
PAGES['catering'] = ('Maroush Events and Catering', "Lebanese catering and private events from Maroush: weddings, corporate events, private parties and intimate dinners across London, with chefs and waiting staff. Free quotes.",
  crumbs(('', 'Events &amp; catering')) + f'''<main>
  <section class="hero rest">
    <img class="hero-mark" src="assets/mark-cream.png" alt="" aria-hidden="true">
    <div class="wrap">
      <div class="hero-copy">
        <div class="label">Events &amp; catering</div>
        <h1><span class="ln"><span class="it">Feed the</span></span><span class="ln"><span>whole</span></span><span class="ln"><span>party</span></span></h1>
        <p class="hero-sub">Weddings, company dinners, private parties and intimate suppers, catered anywhere in London or hosted in the Lords Dining Room at Crockers Folly.</p>
        <div class="hero-btns"><a class="btn btn-cream" href="#enquire">Get a free quote <span class="ar">→</span></a><span class="sel hero-mail">catering@maroush.com</span></div>
      </div>
      <div class="hero-art">
        {ph('party', 'A party night at Maroush', 'ph peak', video=True, eager=True)}
        <div class="stamp"><div><span>Free</span><b>Quote</b><span>Any size</span></div></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="head"><div><div class="label">What we do</div><h2>Any size,<br><span class="it">any occasion</span></h2></div><p>Every event is different, so every menu is built around your guests, your venue and your style. Children and vegetarians are always looked after.</p></div>
      <div class="services">
        <div class="svc rv">{ph('mezze-table', 'A table of mezze', 'ph')}<h3>Weddings</h3><p>Lavish Lebanese feasts for the biggest day, from canapés to the sharing table.</p></div>
        <div class="svc rv">{ph('kebab-platter', 'Grilled meats with salad', 'ph')}<h3>Corporate</h3><p>Lunches, launches and dinners. We have cooked for embassies, chambers of commerce and large companies across London.</p></div>
        <div class="svc rv">{ph('mezze', 'Cold mezze spread', 'ph')}<h3>Private parties</h3><p>Birthdays and celebrations at home, at your venue or in one of our restaurants.</p></div>
        <div class="svc rv">{ph('pastries', 'Lebanese pastries', 'ph')}<h3>Intimate dinners</h3><p>A smaller table, cooked and served by our own chefs and waiting staff.</p></div>
      </div>
    </div>
  </section>

  <section class="section lords">
    <div class="wrap">
      <div class="lords-art rv">
        {ph('lamb-shank', 'Slow-cooked lamb with rice', 'ph big peak')}
        {ph('grill-flames', 'The charcoal grill', 'ph chef')}
      </div>
      <div class="lords-copy">
        <div class="label">Only for events</div>
        <h2>The Lebanese<br><span class="it">Sharing Roast</span></h2>
        <p>A whole shoulder of lamb, slow-cooked until it falls apart, served with oriental rice, seasonal vegetables and gravy. Each shoulder feeds up to six guests.</p>
        <ul class="ticks"><li>Experienced chefs and waiting staff</li><li>Free delivery within our catering area</li><li>Free, no-obligation quotes</li></ul>
        <a class="btn btn-red" href="#enquire">Add it to your event <span class="ar">→</span></a>
      </div>
    </div>
  </section>

  <section class="section" id="enquire">
    <div class="wrap enquire">
      <div class="enq-copy">
        <div class="label">Get a quote</div>
        <h2>Tell us about<br><span class="it">your event</span></h2>
        <p>Pricing depends on your location, guest numbers and menu. Send us the details and we’ll come back with a free quote.</p>
        <dl class="contact-dl"><dt>Email</dt><dd class="sel">catering@maroush.com</dd><dt>Phone</dt><dd class="sel">020 7723 3666</dd></dl>
        <p class="small">Planning dinner at Crockers Folly? See the <a href="crockers-folly.html#private-dining">Lords Dining Room</a>.</p>
      </div>
      {form('cateringForm', [
        field('c-name', 'Your name', req=True), field('c-email', 'Email', 'email', req=True),
        field('c-phone', 'Phone', 'tel'), field('c-date', 'Event date', 'date'),
        field('c-guests', 'Number of guests', 'number'),
        field('c-type', 'Type of event', 'select', opts=['Wedding', 'Corporate', 'Private party', 'Intimate dinner', 'Other']),
        field('c-msg', 'Tell us more', 'textarea', full=True, ph_='Venue, timings, dietary needs, anything else'),
      ], 'Send enquiry', 'catering@maroush.com')}
    </div>
  </section>
</main>''')

# ---------------------------------------------------------------- contact
def contact_rows():
    rows = ''
    for k, v in V.items():
        rows += f'<tr><td><a href="{k}.html">{v["name"]}</a><small>{v["area"]}</small></td><td>{", ".join(v["addr"])}</td><td class="sel">{v["phone"]}</td><td>{"<br>".join(d + " " + t for d, t in v["hours"])}</td></tr>'
    return rows

PAGES['contact'] = ('Maroush Contact', "Contact Maroush: general enquiries, bookings, catering and careers, plus the address, phone number and opening hours of every Maroush restaurant in London.",
  crumbs(('', 'Contact')) + f'''<main>
  <section class="hero solo">
    <img class="hero-mark" src="assets/mark-cream.png" alt="" aria-hidden="true">
    <div class="wrap">
      <div class="hero-copy">
        <div class="label">Contact</div>
        <h1><span class="ln"><span class="it">Say</span></span><span class="ln"><span>hello</span></span></h1>
        <p class="hero-sub">For a table, call the restaurant directly. For anything else, email the right team below or send us a message.</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="cgrid">
        <div class="cbox"><span class="label">General enquiries</span><b class="sel">hello@maroush.com</b><span class="sel">020 7723 3666</span></div>
        <div class="cbox"><span class="label">Bookings</span><b class="sel">bookings@maroush.com</b><span>Or call the restaurant</span></div>
        <div class="cbox"><span class="label">Events &amp; catering</span><b class="sel">catering@maroush.com</b><a href="catering.html">Get a quote →</a></div>
        <div class="cbox"><span class="label">Careers</span><b class="sel">HR@maroush.com</b><span>Join the family</span></div>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0">
    <div class="wrap">
      <div class="head"><div><div class="label">Our restaurants</div><h2>Call us<br><span class="it">directly</span></h2></div></div>
      <div class="tablewrap"><table class="vtable"><thead><tr><th>Restaurant</th><th>Address</th><th>Phone</th><th>Hours</th></tr></thead><tbody>{contact_rows()}</tbody></table></div>
    </div>
  </section>

  <section class="section lords" id="message">
    <div class="wrap enquire">
      <div class="enq-copy">
        <div class="label">Send a message</div>
        <h2>We read<br><span class="it">everything</span></h2>
        <p>Feedback, questions or a problem with your visit: tell us and the right person will get back to you.</p>
      </div>
      {form('contactForm', [
        field('m-name', 'Your name', req=True), field('m-email', 'Email', 'email', req=True),
        field('m-phone', 'Phone', 'tel'),
        field('m-topic', 'What is it about?', 'select', opts=['General feedback', 'A recent visit', 'Catering', 'Something else']),
        field('m-msg', 'Your message', 'textarea', req=True, full=True),
      ], 'Send message', 'hello@maroush.com')}
    </div>
  </section>
</main>''')

# ---------------------------------------------------------------- home + crockers (existing bodies)
def fix_links(s):
    s = s.replace('https://www.maroush.com/restaurants/maroush-at-crockers-folly/', 'crockers-folly.html')
    for k in ['beauchamp-place', 'earls-court', 'edgware-road', 'kings-road', 'high-street-kensington']:
        s = s.replace(f'https://www.maroush.com/restaurants/{k}/', f'{k}.html')
    s = s.replace('https://www.maroush.com/about/', 'about.html').replace('https://www.maroush.com/catering/', 'catering.html')
    return s

home = fix_links(open(os.path.join(ROOT, 'main-home.html')).read())
home = home.replace(f'<a href="{MENU_PDF["food"]}" target="_blank" rel="noopener">Food ↗</a>', '<a href="menu.html">Full menu →</a>')
PAGES['index'] = ('Maroush Homepage',
  "The original Lebanese restaurant in London, since 1981. Sit-down restaurants in St John's Wood, Knightsbridge and Earls Court, plus shawarma and juice bars on Edgware Road, Kings Road and High Street Kensington.",
  home)
cf = fix_links(open(os.path.join(ROOT, 'main-crockers.html')).read())
cf = cf.replace('href="index.html#restaurants">Restaurants', 'href="restaurants.html">Restaurants')
cf = cf.replace(f'<a href="{MENU_PDF["food"]}" target="_blank" rel="noopener">Food ↗</a>', '<a href="menu.html">Full menu →</a>')
PAGES['crockers-folly'] = ('Maroush Crockers Folly',
  "Maroush at Crockers Folly, St John's Wood: Lebanese mezze, charcoal grills and cocktails in a grand Victorian pub. Open daily 12pm to 12am at 24 Aberdeen Place, NW8 8JR.",
  cf)

ACTIVE = {'menu': 'menu.html', 'about': 'about.html', 'catering': 'catering.html', 'restaurants': 'restaurants.html', 'contact': 'contact.html'}

# ---------------------------------------------------------------- write
def build():
    if os.path.exists(DIST): shutil.rmtree(DIST)
    os.makedirs(os.path.join(DIST, 'assets'))
    for f in os.listdir(os.path.join(ROOT, 'assets')):
        shutil.copy(os.path.join(ROOT, 'assets', f), os.path.join(DIST, 'assets', f))
    shutil.copy(os.path.join(ROOT, 'site.css'), os.path.join(DIST, 'assets', 'site.css'))
    shutil.copy(os.path.join(ROOT, 'site.js'), os.path.join(DIST, 'assets', 'site.js'))
    for slug, (title, desc, body) in PAGES.items():
        active = ACTIVE.get(slug, slug if slug in V else '')
        inner = head(title, desc) + '\n' + header(active) + '\n' + body + '\n\n' + footer()
        doc = ('<!doctype html>\n<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n'
               '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
               + inner.replace('\n<header class="top"', '\n</head>\n<body>\n<header class="top"', 1)
               + '\n</body>\n</html>\n')
        open(os.path.join(DIST, slug + '.html'), 'w').write(doc)
        if slug == 'index':
            open(os.path.join(ROOT, 'artifact-index.html'), 'w').write(inner)
    print('built', len(PAGES), 'pages')

if __name__ == '__main__':
    build()
