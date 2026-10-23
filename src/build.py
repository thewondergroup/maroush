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

# ---------------------------------------------------------------- Christmas 2026
XMAS_PRICE = '55'
XMAS = {  # restaurants serving the festive set menu on Christmas Day
 'crockers-folly': dict(where='Crockers Folly', note='The festive menu is served across the restaurant.',
    email='crockersfolly@maroush.com', pdf='assets/christmas-menu-crockers-folly.pdf'),
 'beauchamp-place': dict(where='Beauchamp Place, first floor', note='Festive menu upstairs. Our usual menu on the ground floor.',
    email='maroush2@maroush.com', pdf='assets/christmas-menu-beauchamp-place.pdf'),
}
XMAS_COURSES = [
 ('Cold starters', [('Hommos', 'Chickpeas, tahini and lemon', 'Sesame'),
   ('Mouhamara', 'Roasted red pepper with walnuts, cashews, pistachios, chilli and cumin', 'Nuts, gluten'),
   ('Tabbouleh quinoa salad', 'Parsley, tomato, mint, quinoa and pomegranate', ''),
   ('Wark inab b’zeit', 'Vine leaves rolled with rice, tomato and herbs, slow-cooked with lemon', '')]),
 ('Hot starters', [('Lamb kibbeh', 'Lamb and bulgur croquettes filled with onion, lamb and pine nuts', 'Milk, gluten'),
   ('Spicy soujok', 'Our butchers’ spicy sausages with tomato and lemon', ''),
   ('Halloumi pesto', 'Char-grilled halloumi with cherry tomato and pesto', 'Milk')]),
 ('Main course', [('Maroush mixed grill', 'Lamb kafta, shish taouk and lamb cutlets over charcoal, with grilled tomato and onion', 'Gluten'),
   ('Roasted lamb', 'Braised lamb shank with lamb gravy, and brown rice with minced lamb and pine nuts', 'Milk, celery, gluten')]),
 ('Dessert', [('Mouhallabieh', 'Lebanese milk pudding with rosewater syrup and pistachio', 'Milk, nuts')]),
]

def xmas_menu_card():
    cols = []
    for title, items in XMAS_COURSES:
        li = ''.join(f'<li><b>{n}</b><p>{d}</p>{f"<span class=al>{a}</span>" if a else ""}</li>' for n, d, a in items)
        cols.append(f'<div class="xc"><h3>{title}</h3><ul>{li}</ul></div>')
    return f'''<div class="xcard">
        <div class="xcard-h"><span class="label">Christmas Day set menu</span><b>£{XMAS_PRICE}<small>per person</small></b></div>
        <div class="xcols">{''.join(cols)}</div>
        <p class="xfine">Price includes VAT. A discretionary 12.5% service charge is added to your bill. Allergens are listed under each dish; please tell your server about any allergy.</p>
      </div>'''

def xmas_band(k):
    x = XMAS[k]; v = V[k]
    return f'''<section class="section xmas" id="christmas">
    <div class="wrap">
      <div class="head">
        <div><div class="label">Christmas Day</div><h2>A Lebanese<br><span class="it">Christmas</span></h2></div>
        <p>We are open on Christmas Day with a festive set menu at £{XMAS_PRICE} per person. {x['note']}</p>
      </div>
      {xmas_menu_card()}
      <div class="xbook">
        <div><span class="label">To book</span><b class="sel">{v['phone']}</b><span class="sel">{x['email']}</span></div>
        <div class="btns"><button class="btn btn-cream" type="button" data-book>Book Christmas Day <span class="ar">→</span></button><a class="btn btn-ghost" href="{x['pdf']}" target="_blank" rel="noopener">Menu PDF ↗</a></div>
      </div>
    </div>
  </section>'''

def announce():
    return f'''<a class="announce" href="christmas.html" aria-label="Open on Christmas Day. Festive set menu £{XMAS_PRICE}. See the Christmas menu">
  <div class="wrap">
    <span class="an-date" aria-hidden="true"><b>25</b><small>Dec</small></span>
    <span class="an-text"><b>Open<span class="an-on"> on</span> Christmas Day</b><span class="an-sub">Festive set menu at Crockers Folly &amp; Beauchamp Place</span></span>
    <span class="an-price" aria-hidden="true"><small>Set menu</small>£{XMAS_PRICE}</span>
    <span class="an-cta" aria-hidden="true">See the menu <span class="ar">→</span></span>
  </div>
</a>
'''

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
    return announce() + f'''<header class="top" id="top">
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
            <a class="mfeat" href="christmas.html">
              <div class="ph"><video src="assets/crockers.mp4" poster="assets/crockers.jpg" autoplay muted loop playsinline preload="metadata" aria-label="Maroush at Crockers Folly"></video></div>
              <div class="mfeat-c">
                <span class="label">Christmas Day</span>
                <b>Festive menu<br>£{XMAS_PRICE} a head</b>
                <span class="btn btn-cream">See the menu →</span>
              </div>
            </a>
          </div>
        </div>
      </div>
      {nav_link('menu.html', 'Menu', active)}
      {nav_link('private-dining.html', 'Private dining', active)}
      {nav_link('catering.html', 'Catering', active)}
      {nav_link('about.html', 'Our story', active)}
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
  <a href="christmas.html">Christmas</a>
  <a href="menu.html">Menu</a>
  <a href="about.html">Our story</a>
  <a href="lunch.html">Lunch offer</a>
  <a href="private-dining.html">Private dining</a>
  <a href="catering.html">Catering</a>
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
        <a href="lunch.html">Lunch offer</a>
        <a href="private-dining.html">Private dining</a>
        <a href="christmas.html">Christmas Day</a>
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
    <span class="label">Large group or celebration?</span>
    <a class="di" href="private-dining.html"><div><b>Private dining</b><small>The Lords Room and Beauchamp Place first floor</small></div><span class="ar">→</span></a>
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

def menus_row(k=None, label='Menus'):
    tab = 'menu-full' if k in ('crockers-folly', 'beauchamp-place') else 'menu-every'
    return f'''<div class="menus">
        <span class="label">{label}</span>
        <a href="menu.html#{tab}">Full menu →</a>
        <a href="lunch.html">Lunch offer →</a>
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
    hours += '<dt>Lunch offer</dt><dd><a href="lunch.html">Mon–Thu until 3pm</a></dd>'
    hours += '<dt>Christmas Day</dt><dd>' + ('Open · <a href="#christmas">festive menu</a>' if k in XMAS else 'Open · usual menu') + '</dd>'
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
      {menus_row(k)}
    </div>
  </section>

  {xmas_band(k) if k in XMAS else ''}
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
        <a class="btn btn-red" href="menu.html#menu-every">See the full menu <span class="ar">→</span></a>
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

# ---------------------------------------------------------------- menu (September 2026)
# Each item: (name, description, price, marks). price is '9.25' or a list of (label, price).
# marks: 'vg' vegan, 'v' vegetarian, 'hot' spicy — as printed on the Sep 2026 menus.
FULL_BRANCHES = ['crockers-folly', 'beauchamp-place']
EVERY_BRANCHES = ['earls-court', 'edgware-road', 'kings-road', 'high-street-kensington']

MENU_FULL = [
 ('f-cold', 'Cold mezze', 'مازة باردة', 'Served with Lebanese bread', [
  ('Hommos', 'Chickpeas blended with tahini, garlic and lemon, finished with olive oil', '9.25', 'vg'),
  ('Hommos Beiruty', 'Hommos with parsley and fresh green chilli', '9.50', 'vg hot'),
  ('Moutabal baba ghanouj', 'Grilled aubergine with tahini, lemon and sumac', '9.95', 'vg'),
  ('Mouhamara', 'Roasted red pepper with walnuts, cashews, pistachios, chilli and cumin', '12.00', 'vg hot'),
  ('Wark inab b’zeit', 'Vine leaves rolled with rice, tomato and herbs, slow-cooked with lemon', '10.00', 'vg'),
  ('Moussaka', 'Aubergine and chickpeas in a rich tomato sauce', '9.75', 'vg'),
  ('Bammieh b’zeit', 'Okra with tomato, garlic and fresh coriander', '9.75', 'vg'),
  ('Labneh', 'Strained yoghurt with olive oil and dried mint', '8.75', 'v'),
  ('Cucumber salad with yoghurt', 'Yoghurt with chopped cucumber and dried mint', '8.00', 'v'),
  ('Kabis', 'Cucumber, turnip and chilli pickled with garlic', '6.50', 'vg'),
 ]),
 ('f-salads', 'Salads &amp; soup', 'سلطات', '', [
  ('Tabbouleh', 'Parsley, tomato, mint, onion and bulgur with lemon and olive oil', '9.50', 'vg'),
  ('Fattoush', 'Mixed salad with crispy Lebanese bread, sumac and pomegranate molasses', '9.50', 'vg'),
  ('Maroush salad', 'Lettuce, tomato, cucumber, radish and peppers with thyme, mint and sumac', '9.75', 'vg'),
  ('Lentil soup', 'Red lentils with onion, garlic and cumin, with crispy bread and lemon', '7.50', 'vg'),
 ]),
 ('f-hot', 'Hot mezze', 'مازة ساخنة', 'Served with Lebanese bread', [
  ('Falafel', 'Chickpea and fava bean croquettes with tahini', '8.95', 'vg'),
  ('Foul moudamas', 'Broad beans with garlic, cumin, lemon and olive oil', '9.95', 'vg'),
  ('Batata harra', 'Spicy potatoes with garlic, coriander, peppers and chilli', '9.00', 'vg hot'),
  ('Hommos awarma', 'Hommos topped with sautéed diced lamb and pine nuts', '12.00', ''),
  ('Hommos shawarma chicken', 'Hommos topped with sliced chicken shawarma', '13.00', ''),
  ('Hommos shawarma lamb', 'Hommos topped with sliced lamb shawarma', '14.50', ''),
  ('Kibbeh', 'Lamb and bulgur croquettes filled with onion, lamb and pine nuts', '9.95', ''),
  ('Halloum meshwi', 'Char-grilled halloumi with tomato and cucumber', '10.50', 'v'),
  ('Jawaneh', 'Char-grilled chicken wings with lemon, garlic and garlic sauce', '8.50', ''),
  ('Chicken liver', 'Pan-fried with lemon and garlic, with pomegranate molasses', '9.50', ''),
  ('Soujok', 'Our butchers’ spicy sausages with tomato and lemon', '10.50', 'hot'),
 ]),
 ('f-bakery', 'Bakery', 'معجنات', '', [
  ('Maroush kalaj', 'Char-grilled flatbread filled with halloumi and thyme', '9.50', 'v'),
  ('Maroush arayes', 'Char-grilled flatbread filled with spiced minced lamb', '9.95', ''),
  ('Sambousek cheese', 'Crisp pastries filled with feta and thyme', '9.50', 'v'),
  ('Sambousek lamb', 'Crisp pastries filled with lamb, cheese and pine nuts', '9.75', ''),
 ]),
 ('f-grill', 'From the charcoal grill', 'مشاوي', '', [
  ('Lahem meshwi', 'Skewers of lamb cubes with grilled tomato, onion and parsley', '21.50', ''),
  ('Shish taouk', 'Skewers of chicken with garlic sauce', '18.50', ''),
  ('Kafta meshwi', 'Skewers of spiced minced lamb with onion and parsley', '19.50', ''),
  ('Maroush mixed grill', 'Kafta, shish taouk and lamb cubes with garlic sauce', '22.50', ''),
  ('Kafta khosh-khash', 'Lamb kafta on a spicy ratatouille', '20.00', 'hot'),
  ('Kastaleta lamb', 'Lamb cutlets with black pepper and thyme, with thick-cut fries', '23.00', ''),
  ('Farrouj meshwi', 'Boneless baby chicken with lemon, garlic and herbs', '19.95', ''),
  ('Grilled sea bass', 'Whole sea bass from the grill, with tahini', '27.00', ''),
 ]),
 ('f-shawarma', 'Shawarma &amp; mains', 'شاورما', '', [
  ('Shawarma lamb', 'British lamb with black pepper and nutmeg, with bread, grilled tomato and tahini', '21.00', ''),
  ('Shawarma chicken', 'British chicken with lemon, garlic, cinnamon and cardamom, with garlic sauce', '18.50', ''),
  ('Mixed shawarma', 'Lamb and chicken shawarma with bread and tahini', '20.00', ''),
  ('Lamb shank', 'Braised with Mediterranean spices, with gravy and brown rice with minced lamb', '22.00', ''),
  ('Roasted chicken', 'British baby chicken with garlic, lemon and herbs, with brown rice with minced lamb', '19.00', ''),
  ('Aubergine &amp; chickpea casserole', 'With white rice', '18.00', 'vg'),
  ('Okra stew', 'With white rice', '18.00', 'vg'),
 ]),
 ('f-wraps', 'Wraps', 'لفائف', 'In Lebanese bread', [
  ('Falafel', 'With tomato, lettuce and tahini', '7.50', 'vg'),
  ('Batata harra &amp; fried vegetables', 'With pickles and garlic sauce', '7.50', 'vg hot'),
  ('Halloumi', 'With tomato, cucumber and olive oil', '8.50', 'v'),
  ('Shawarma lamb', 'With tahini, tomato, pickles, onion, parsley and sumac', '9.75', ''),
  ('Shawarma chicken', 'With tomato, pickles and garlic sauce', '9.75', ''),
  ('Mixed shawarma', 'Lamb and chicken with tahini and garlic sauce', '8.50', ''),
  ('Shish taouk', 'With tomato, pickles and garlic sauce', '9.50', ''),
  ('Lahem meshwi', 'Lamb cubes with hommos, tomato, pickles and onion', '8.50', ''),
  ('Kafta meshwi', 'Minced lamb with hommos, tomato, pickles and onion', '8.50', ''),
  ('Chicken liver', 'With pomegranate molasses, garlic sauce and pickles', '8.25', ''),
  ('Soujok', 'With garlic sauce and pickles', '8.50', 'hot'),
 ]),
 ('f-sides', 'Sides &amp; sauces', '', '', [
  ('Fries', '', '5.75', 'vg'), ('White basmati rice', '', '5.50', 'vg'),
  ('Lebanese vermicelli rice', '', '7.50', 'v'), ('Brown rice with minced lamb', '', '7.95', ''),
  ('Garlic sauce', '', '2.25', 'vg'), ('Chilli sauce', '', '2.75', 'vg'), ('Tahini sauce', '', '2.75', 'vg'),
 ]),
 ('f-sweets', 'Desserts', 'حلويات', '', [
  ('Mouhallabieh', 'Milk pudding with rosewater syrup and pistachio', '7.50', 'v'),
  ('Rice pudding', 'With rosewater syrup and pistachio', '7.50', 'v'),
  ('Baklawa', 'Miniature Lebanese pastries with nuts and syrup', '8.50', 'v'),
 ]),
 ('f-drinks', 'Soft drinks &amp; coffee', 'مشروبات', 'Cocktails and wine have their own lists', [
  ('Fresh orange', '', '5.50', ''), ('Mango', '', '5.50', ''), ('Fresh lemonade', '', '5.50', ''), ('Fruit cocktail', '', '5.95', ''),
  ('Laban ayran', 'Salted yoghurt drink', '4.50', ''), ('Soft drinks', 'Coca-Cola, Diet Coke, Coke Zero, 7UP, Fanta, tonic, ginger ale', '4.50', ''),
  ('Still water', '', [('Small', '3.50'), ('Large', '4.50')], ''), ('Sparkling water', '', [('Small', '3.75'), ('Large', '4.75')], ''),
  ('Lebanese coffee', '', '3.75', ''), ('Espresso', '', '3.75', ''), ('Double espresso', '', '4.50', ''),
  ('Cappuccino, latte or flat white', '', '4.00', ''), ('Americano', '', '4.00', ''), ('Café mocha', '', '4.50', ''),
  ('Iced coffee', '', '4.00', ''), ('Hot chocolate', '', '4.00', ''), ('Irish coffee', '', '11.00', ''),
  ('Mint tea', '', '3.75', ''), ('English or peppermint tea', '', '3.75', ''),
 ]),
]
SETS_FULL = [
 ('Lunch platter', 'Hommos, moutabal, tabbouleh, falafel and cheese sambousek, then two skewers of shish taouk or kafta', '32'),
 ('Vegan sharing menu for two', 'Hommos, moutabal, Maroush salad, falafel and batata harra, then aubergine casserole with rice and bammieh', '75'),
 ('Sharing menu for two', 'Hommos, moutabal, tabbouleh, falafel, soujok and batata harra, then shish taouk and a Lebanese dessert', '85'),
 ('Sharing menu for four', 'Eight mezze, then lamb shank with rice and the Maroush mixed grill, with dessert and mint tea', '160'),
]

MENU_EVERY = [
 ('e-cold', 'Cold mezze', 'مازة باردة', '', [
  ('Hommos', 'Chickpeas, tahini, lemon and olive oil', '9.00', 'vg'),
  ('Moutabal', 'Chargrilled aubergine, tahini and lemon', '9.75', 'vg'),
  ('Warak inab', 'Vine leaves filled with rice and herbs', '9.00', 'vg'),
  ('Hommos Beiruty', 'Chickpeas, tahini, parsley and green chilli', '9.25', 'vg'),
  ('Moussaka', 'Aubergine, chickpeas and tomato', '9.75', 'vg'),
  ('Labneh', 'Strained yoghurt, olive oil and dried mint', '8.75', 'v'),
  ('Kabis', 'Pickled cucumber, turnip and chilli', '6.50', 'vg'),
 ]),
 ('e-hot', 'Hot mezze', 'مازة ساخنة', 'Most also come as a wrap', [
  ('Falafel', 'Chickpea and fava bean croquettes with tahini', [('Wrap', '7.50'), ('Plate', '8.95')], 'vg'),
  ('Batata harra', 'Spiced potatoes, garlic, coriander and chilli', [('Wrap', '7.50'), ('Plate', '8.95')], 'vg'),
  ('Halloumi meshwi', 'Chargrilled halloumi with tomato, lettuce and cucumber', [('Wrap', '8.50'), ('Plate', '10.50')], 'v'),
  ('Soujok', 'Spicy sausages, tomato and fresh lemon', [('Wrap', '8.50'), ('Plate', '10.00')], ''),
  ('Chicken liver', 'Pan-fried with lemon, garlic and pomegranate molasses', [('Wrap', '8.25'), ('Plate', '9.50')], ''),
  ('Kibbeh', 'Lamb and bulgur croquettes with pine nuts', '9.95', ''),
  ('Jawaneh', 'Chargrilled chicken wings, lemon and garlic', '8.50', ''),
  ('Sambousek cheese', 'Crisp pastry filled with feta and thyme', '9.50', 'v'),
  ('Sambousek lamb', 'Crisp pastry with lamb, cheese and pine nuts', '9.75', ''),
  ('Lentil soup', 'Red lentils, cumin, crisp bread and lemon', '7.50', 'vg'),
 ]),
 ('e-shawarma', 'Shawarma', 'شاورما', 'Slowly roasted, freshly carved. Loaded hommos is hommos topped with shawarma.', [
  ('Chicken shawarma', 'British chicken with lemon, garlic and Lebanese spices', [('Loaded hommos', '13.00'), ('Wrap', '8.50'), ('Plate', '18.50')], ''),
  ('Lamb shawarma', 'British lamb with warm Lebanese spices', [('Loaded hommos', '14.50'), ('Wrap', '9.75'), ('Plate', '21.00')], ''),
  ('Mixed shawarma', 'Our chicken and lamb shawarma together', [('Loaded hommos', '14.50'), ('Wrap', '9.75'), ('Plate', '20.00')], ''),
 ]),
 ('e-grill', 'Maroush grill', 'مشاوي', '', [
  ('Shish taouk', 'Chicken skewers with garlic sauce', [('Wrap', '8.50'), ('Plate', '18.50')], ''),
  ('Kafta meshwi', 'Seasoned minced lamb, onion and parsley', [('Wrap', '8.50'), ('Plate', '19.50')], ''),
  ('Lahem meshwi', 'Grilled lamb cubes with tomato, onion and parsley', [('Wrap', '9.50'), ('Plate', '21.00')], ''),
  ('Farrouj meshwi', 'Boneless baby chicken with lemon, garlic and herbs, with garlic sauce', '19.00', ''),
  ('Lamb cutlets', 'Kastaleta with black pepper, thyme and fries', '22.00', ''),
  ('Maroush mixed grill', 'Kafta, shish taouk and lamb cubes', '22.00', ''),
 ]),
 ('e-salads', 'Salads', 'سلطات', '', [
  ('Tabbouleh', 'Parsley, tomato, bulgur, mint and lemon', '8.95', 'vg'),
  ('Fattoush', 'Mixed salad with crisp bread, sumac and pomegranate', '9.50', 'vg'),
  ('Maroush salad', 'Lettuce, tomato, cucumber, radish, onion and peppers with sumac and lemon', '8.95', 'vg'),
 ]),
 ('e-mains', 'Mains', 'أطباق رئيسية', '', [
  ('Braised lamb shank', 'Braised lamb, gravy and aromatic lamb brown rice', '22.00', ''),
  ('Aubergine &amp; chickpea casserole', 'Aubergine, chickpeas and tomato with white rice', '17.00', 'vg'),
 ]),
 ('e-sides', 'Sides &amp; sauces', '', '', [
  ('Fries', '', '5.75', 'vg'), ('White basmati rice', '', '5.50', 'vg'), ('Lebanese vermicelli rice', '', '7.50', 'v'),
  ('Garlic sauce', '', '2.25', 'vg'), ('Chilli sauce', '', '2.75', 'vg'), ('Tahini sauce', '', '2.75', 'vg'),
 ]),
 ('e-sweets', 'Desserts', 'حلويات', '', [
  ('Lebanese baklawa', 'Mini Lebanese pastries with nuts and syrup', '8.50', 'v'),
  ('Orange blossom mouhallabieh', 'Milk pudding with orange blossom and pistachio', '7.50', 'v'),
  ('Rice pudding', 'With rosewater and pistachio', '7.50', 'v'),
 ]),
 ('e-drinks', 'Drinks', 'مشروبات', '', [
  ('Fresh juices', 'Lebanese lemonade, fruit cocktail', '5.50', ''), ('Mango juice', '', '5.95', ''), ('Fresh orange juice', '', '4.50', ''),
  ('Ayran', 'Yoghurt drink', '3.50', ''), ('Soft drinks', 'Coca-Cola, Diet Coke, Coke Zero, 7UP, 7UP Zero, Fanta', '4.00', ''),
  ('Still water', '', [('Small', '3.75'), ('Large', '4.75')], ''), ('Sparkling water', '', [('Small', '3.50'), ('Large', '4.50')], ''),
  ('Château Ksara wines', 'White Blanc de l’Observatoire, red Le Prieuré, rosé', [('125ml', '8'), ('175ml', '9.50'), ('Bottle', '29')], ''),
  ('Lebanese beer', '', '7.50', ''), ('Al-Karram arak 53%', 'From the Bekaa Valley', [('125ml', '9'), ('18.7cl', '30')], ''),
  ('Lebanese coffee', '', '3.75', ''), ('Espresso', '', '3.50', ''), ('Cappuccino or latte', '', '4.00', ''),
  ('Americano or iced coffee', '', '3.75', ''), ('Mint or English breakfast tea', '', '3.50', ''),
 ]),
]
SETS_EVERY = [
 ('Chicken shawarma &amp; wings feast', 'Chicken shawarma and chargrilled wings with fries, two cheese sambousek, hommos, bread and sauces', '39'),
 ('Maroush mezze platter', 'Hommos, moutabal, tabbouleh and labneh with four falafel, batata harra, pickles and bread', '30'),
 ('Beirut sharing menu for two', 'Six hot and cold mezze, then chargrilled shish taouk with bread and sauces, finished with baklawa', '79'),
]

# Lunch offer, all restaurants. Baklawa removed at the client's request (Oct 2026).
LUNCH = dict(two='14.95', three='19.95', when='Monday to Thursday, 11am to 3pm',
  starters=[('Hommos', 'Chickpeas, tahini, lemon and garlic, with olive oil'), ('Moutabal', 'Smoky aubergine with tahini, lemon and sumac'),
            ('Tabbouleh', 'Parsley, tomato, mint and bulgur with lemon'), ('Fattoush', 'Crisp salad with Lebanese bread, sumac and pomegranate'),
            ('Labneh', 'Strained yoghurt with olive oil and dried mint'), ('Lentil soup', 'Red lentils with cumin, crispy bread and lemon'),
            ('Falafel', 'Chickpea and broad bean croquettes with tahini'), ('Batata harra', 'Potatoes with garlic, coriander, chilli and lemon')],
  mains=[('Chicken shawarma', 'British chicken, slowly roasted, with garlic sauce'), ('Shish taouk', 'Chargrilled chicken skewers with garlic sauce'),
         ('Kafta meshwi', 'Chargrilled minced lamb with parsley and onion'), ('Farrouj meshwi', 'Boneless baby chicken with lemon, garlic and herbs'),
         ('Aubergine &amp; chickpea casserole', 'With white basmati rice')],
  premium=[('Lamb shawarma', 'British lamb with tahini sauce'), ('Mixed shawarma', 'Chicken and lamb shawarma'), ('Lahem meshwi', 'Chargrilled lamb cubes with sumac')],
  desserts=[('Mouhallabieh', 'Orange blossom milk pudding with pistachio'), ('Rice pudding', 'With rosewater and pistachio')],
)

def price_html(p):
    if isinstance(p, list):
        return '<span class="pr multi">' + ''.join(f'<span><small>{l}</small>£{v}</span>' for l, v in p) + '</span>'
    return f'<span class="pr">£{p}</span>'

def marks_html(m):
    out = ''
    if 'vg' in m.split(): out += '<span class="mk vg" title="Vegan">VG</span>'
    if 'v' in m.split(): out += '<span class="mk v" title="Vegetarian">V</span>'
    if 'hot' in m.split(): out += '<span class="mk hot" title="Spicy">Spicy</span>'
    return out

def menu_sections(menu):
    secs = []
    for sid, title, ar, note, items in menu:
        rows = []
        for n, d, p, m in items:
            multi = isinstance(p, list)
            top = f'<div class="mi-top"><b>{n}</b>{marks_html(m)}' + ('' if multi else '<span class="dots"></span>' + price_html(p)) + '</div>'
            rows.append(f'<li>{top}{f"<p>{d}</p>" if d else ""}{price_html(p) if multi else ""}</li>')
        secs.append(f'''<section class="msec" id="{sid}">
        <div class="msec-h"><h2>{title}</h2>{f'<i>{ar}</i>' if ar else ''}{f'<span>{note}</span>' if note else ''}</div>
        <ul class="mlist">{''.join(rows)}</ul>
      </section>''')
    return ''.join(secs)

def sets_html(sets, sid):
    cards = ''.join(f'<div class="setc"><b>{n}</b><p>{d}</p><span class="pr">£{p}</span></div>' for n, d, p in sets)
    return f'''<section class="sets" id="{sid}">
        <div class="msec-h"><h2>To share</h2><i>للمشاركة</i><span>The easiest way to try a bit of everything</span></div>
        <div class="setgrid">{cards}</div>
      </section>'''

def lunch_html():
    L = LUNCH
    def col(title, items, extra=''):
        li = ''.join(f'<li><b>{n}</b><p>{d}</p></li>' for n, d in items)
        return f'<div class="lcol"><h3>{title}</h3><ul>{li}</ul>{extra}</div>'
    prem = ''.join(f'<li><b>{n} <em>+£3</em></b><p>{d}</p></li>' for n, d in L['premium'])
    return f'''<section class="lunch" id="lunch">
      <div class="lunch-h">
        <div><span class="label">Lunch offer · every Maroush</span><h2>Lunch, <span class="it">the Lebanese way</span></h2><p>{L['when']}. Choose a starter and main, or a main and dessert, or have all three.</p></div>
        <div class="lprices"><div><b>£{L['two']}</b><span>Two courses</span></div><div><b>£{L['three']}</b><span>Three courses</span></div></div>
      </div>
      <div class="lcols">
        {col('Starters', L['starters'])}
        {col('Mains', L['mains'], f'<h4>Premium mains</h4><ul class="prem">{prem}</ul>')}
        {col('Desserts', L['desserts'])}
      </div>
      <p class="lfine">Per person. Drinks are not included. A discretionary 12.5% service charge applies to dine-in. Please tell our team about any allergies before ordering.</p>
    </section>'''

def menu_page():
    def tabs(menu, extra):
        return ''.join(f'<a href="#{sid}">{re.sub("&amp;.*", "", t).strip()}</a>' for sid, t, _, _, _ in menu) + extra
    full_names = ' &amp; '.join(V[k]['short'] for k in FULL_BRANCHES)
    every_names = ', '.join(V[k]['short'] for k in EVERY_BRANCHES[:-1]) + ' and ' + V[EVERY_BRANCHES[-1]]['short']
    return crumbs(('', 'Menu')) + f'''<main>
  <section class="hero solo">
    <img class="hero-mark" src="assets/mark-cream.png" alt="" aria-hidden="true">
    <div class="wrap">
      <div class="hero-copy">
        <div class="label">Food · drinks · lunch · Christmas</div>
        <h1><span class="ln"><span class="it">The</span></span><span class="ln"><span>Menu</span></span></h1>
        <p class="hero-sub">Order lots and share everything. That’s the Lebanese way. Start with cold mezze, add a few hot dishes, then something from the charcoal grill.</p>
        <div class="jump"><a href="#lunch">Lunch offer</a><a href="christmas.html">Christmas Day</a><a href="{MENU_PDF['drinks']}" target="_blank" rel="noopener">Cocktails ↗</a><a href="{MENU_PDF['wine']}" target="_blank" rel="noopener">Wine list ↗</a></div>
      </div>
    </div>
  </section>

  <div class="mswitch" role="tablist" aria-label="Choose a restaurant menu"><div class="wrap">
    <button type="button" role="tab" id="tab-full" aria-controls="menu-full" aria-selected="true" data-menu="full"><b>Restaurant menu</b><small>{full_names}</small></button>
    <button type="button" role="tab" id="tab-every" aria-controls="menu-every" aria-selected="false" data-menu="every"><b>Everyday menu</b><small>{every_names}</small></button>
  </div></div>

  <div id="menu-full" class="mpanel" role="tabpanel" aria-labelledby="tab-full">
    <nav class="mtabs" aria-label="Menu sections"><div class="wrap">{tabs(MENU_FULL, '<a href="#sets-full">To share</a>')}</div></nav>
    <div class="section menu-body"><div class="wrap">
      {sets_html(SETS_FULL, 'sets-full')}
      {menu_sections(MENU_FULL)}
    </div></div>
  </div>

  <div id="menu-every" class="mpanel" role="tabpanel" aria-labelledby="tab-every" hidden>
    <nav class="mtabs" aria-label="Menu sections"><div class="wrap">{tabs(MENU_EVERY, '<a href="#sets-every">To share</a>')}</div></nav>
    <div class="section menu-body"><div class="wrap">
      {sets_html(SETS_EVERY, 'sets-every')}
      {menu_sections(MENU_EVERY)}
    </div></div>
  </div>

  <div class="section menu-body" style="padding-top:0"><div class="wrap">
    {lunch_html()}
    <div class="xpromo">
      <div><span class="label">Christmas Day</span><b>Festive set menu, £{XMAS_PRICE} a head</b><p>At Crockers Folly and upstairs at Beauchamp Place. Every other Maroush is open with its usual menu.</p></div>
      <a class="btn btn-cream" href="christmas.html">See the Christmas menu <span class="ar">→</span></a>
    </div>
    <div class="mnote">
      <p><b>VG</b> vegan · <b>V</b> vegetarian · <b>Spicy</b>. Our kitchens handle all 14 regulated allergens, so we can’t guarantee any dish is free of them. Please ask our team for allergen and calorie information and tell us about any allergy before ordering. Some meat dishes may contain small bones.</p>
      <p>Prices in pounds, including VAT. A discretionary 12.5% service charge is added to your bill.</p>
    </div>
  </div></div>
</main>'''
PAGES['menu'] = ('Maroush Menu', "The Maroush menu: Lebanese cold and hot mezze, shawarma, charcoal grills, wraps, desserts and sharing menus, plus the weekday lunch offer from £14.95 and the Christmas Day menu.", menu_page())


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
        <p class="small">Planning dinner in one of our restaurants? See <a href="private-dining.html">private dining</a>.</p>
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

def xmas_page():
    usual = [k for k in V if k not in XMAS]
    where = ''
    for k, x in XMAS.items():
        v = V[k]
        where += f'''<article class="xwhere rv">
          {ph(v['img'], v['name'], 'ph peak')}
          <div class="label">{v['area']}</div>
          <h3><a href="{k}.html">{x['where']}</a></h3>
          <p>{x['note']}</p>
          <dl><dt>Call</dt><dd class="sel">{v['phone']}</dd><dt>Email</dt><dd class="sel">{x['email']}</dd><dt>Address</dt><dd>{', '.join(v['addr'])}</dd></dl>
          <div class="rcard-btns"><button class="btn btn-red" type="button" data-book>Book</button><a class="btn btn-line" href="{x['pdf']}" target="_blank" rel="noopener">Menu PDF ↗</a></div>
        </article>'''
    usual_cards = ''.join(f'<a class="other" href="{k}.html"><b>{V[k]["short"]}</b><small>{V[k]["area"]} · {V[k]["phone"]}</small><span class="tag">Usual menu</span></a>' for k in usual)
    return crumbs(('', 'Christmas')) + f'''<main>
  <section class="hero rest">
    <img class="hero-mark" src="assets/mark-cream.png" alt="" aria-hidden="true">
    <div class="wrap">
      <div class="hero-copy">
        <div class="label">Christmas Day 2026</div>
        <h1 class="long"><span class="ln"><span class="it">A Lebanese</span></span><span class="ln"><span>Christmas</span></span></h1>
        <p class="hero-sub">Every Maroush is open on Christmas Day. Book our festive set menu at Crockers Folly or upstairs at Beauchamp Place, or come in for our usual menu anywhere else.</p>
        <div class="hero-btns"><button class="btn btn-cream" type="button" data-book>Book Christmas Day <span class="ar">→</span></button><a class="btn btn-ghost" href="#festive-menu">See the menu</a></div>
      </div>
      <div class="hero-art">
        {ph('room-crockers', 'The chandeliered Lords Dining Room at Crockers Folly', 'ph peak', eager=True)}
        <div class="stamp"><div><span>Set menu</span><b>£{XMAS_PRICE}</b><span>per person</span></div></div>
      </div>
    </div>
  </section>

  <section class="section" id="festive-menu">
    <div class="wrap">
      <div class="head"><div><div class="label">The festive menu</div><h2>Four courses,<br><span class="it">one price</span></h2></div><p>Cold and hot mezze, the mixed grill or slow-braised lamb, and a rosewater milk pudding to finish.</p></div>
      {xmas_menu_card()}
    </div>
  </section>

  <section class="section lords" id="book">
    <div class="wrap" style="display:block">
      <div class="lords-copy" style="margin-bottom:40px"><div class="label">Where to book</div><h2>Two rooms,<br><span class="it">one feast</span></h2></div>
      <div class="xwheres">{where}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="head"><div><div class="label">Also open</div><h2>Our usual menu,<br><span class="it">all day</span></h2></div><p>No festive menu, just Maroush as you know it. Walk in for mezze, shawarma and grills on Christmas Day.</p></div>
      <div class="others">{usual_cards}</div>
    </div>
  </section>
</main>'''
PAGES['christmas'] = ('Maroush Christmas Day', f"Christmas Day at Maroush: a £{XMAS_PRICE} festive Lebanese set menu at Crockers Folly and Beauchamp Place, and every other Maroush open with its usual menu.", xmas_page())

def home_lunch():
    L = LUNCH
    picks = lambda items, n: ', '.join(x[0] for x in items[:n])
    return f"""<section class="section hlunch" id="lunch">
    <div class="wrap hl-grid">
      <div class="hl-copy">
        <div class="label">Lunch offer · every Maroush</div>
        <h2>Lunch,<br><span class="it">the Lebanese way</span></h2>
        <p>Monday to Thursday, 11am to 3pm. Pick a starter and a main, or a main and a dessert, or treat yourself to all three.</p>
        <div class="lprices big"><div><b>£{L['two']}</b><span>Two courses</span></div><div><b>£{L['three']}</b><span>Three courses</span></div></div>
        <dl class="hl-list">
          <dt>Starters</dt><dd>{picks(L['starters'], 8)}</dd>
          <dt>Mains</dt><dd>{picks(L['mains'], 5)}, or lamb or mixed shawarma for £3 more</dd>
          <dt>Desserts</dt><dd>{picks(L['desserts'], 2)}</dd>
        </dl>
        <div class="hero-btns"><a class="btn btn-red" href="lunch.html">See the lunch menu <span class="ar">→</span></a><button class="btn btn-line" type="button" data-book>Book a table</button></div>
      </div>
      <div class="hl-art rv">
        {ph('mezze', 'Hommos and cold mezze', 'ph peak a1')}
        {ph('shawarma-spit', 'Chicken shawarma carved from the spit', 'ph peak a2')}
        <div class="hl-stamp"><span>From</span><b>£{L['two']}</b><span>Mon–Thu</span></div>
      </div>
    </div>
  </section>
  <section class="xstrip">
    <div class="wrap"><div class="xpromo">
      <div><span class="label">Christmas Day</span><b>Every Maroush is open. Festive menu £{XMAS_PRICE}.</b><p>At Crockers Folly and upstairs at Beauchamp Place.</p></div>
      <a class="btn btn-cream" href="christmas.html">See the Christmas menu <span class="ar">→</span></a>
    </div></div>
  </section>"""

def home_private():
    return f"""<section class="section hprivate" id="private-dining">
    <div class="wrap hp-grid">
      <div class="hp-art rv">
        {ph('room-crockers', 'The Lords Dining Room at Crockers Folly', 'ph peak big')}
        {ph('party', 'A celebration at Maroush', 'ph vid', video=True)}
      </div>
      <div class="hp-copy">
        <div class="label">Private dining</div>
        <h2>Your table,<br><span class="it">your celebration</span></h2>
        <p>Birthdays, engagements, family gatherings and company dinners, hosted under the chandelier in the Lords Dining Room at Crockers Folly or upstairs at Beauchamp Place.</p>
        <ul class="ticks"><li>A crystal chandelier, an original fireplace and a view of the chefs</li><li>Sharing feasts built around your guests</li><li>Drinks in the 1898 Bar or on the terrace first</li></ul>
        <div class="hero-btns"><a class="btn btn-red" href="private-dining.html">Plan a private dinner <span class="ar">→</span></a><a class="btn btn-ghost" href="catering.html">Or we cater for you</a></div>
      </div>
    </div>
  </section>"""

_home = PAGES['index'][2]
_home = _home.replace('<section class="section food" id="food"', home_lunch() + '\n\n  <section class="section food" id="food"', 1)
_home = re.sub(r'<section class="section events" id="events">.*?</section>', home_private(), _home, count=1, flags=re.S)
_home = _home.replace('<a href="menu.html">Full menu →</a>', '<a href="menu.html">Full menu →</a><a href="lunch.html">Lunch offer →</a>')
PAGES['index'] = (PAGES['index'][0], PAGES['index'][1], _home)

# ---------------------------------------------------------------- private dining page
def private_page():
    occ = ''.join(f'<span>{o}</span>' for o in ['Birthdays', 'Anniversaries', 'Engagements', 'Family gatherings', 'Company dinners', 'Christmas parties', 'Eid and Ramadan gatherings', 'Wakes and memorials'])
    sets = ''.join(f'<div class="setc"><b>{n}</b><p>{d}</p><span class="pr">£{p}</span></div>' for n, d, p in SETS_FULL[1:])
    return crumbs(('', 'Private dining')) + f"""<main>
  <section class="hero rest">
    <img class="hero-mark" src="assets/mark-cream.png" alt="" aria-hidden="true">
    <div class="wrap">
      <div class="hero-copy">
        <div class="label">Private dining &amp; group bookings</div>
        <h1><span class="ln"><span class="it">Gather at</span></span><span class="ln"><span>Maroush</span></span></h1>
        <p class="hero-sub">Lebanese hospitality is made for a crowd. Bring your people together over a table full of mezze, a feast from the charcoal grill and a room that feels like your own.</p>
        <div class="hero-btns"><a class="btn btn-cream" href="#enquire">Enquire now <span class="ar">→</span></a><a class="btn btn-ghost" href="#rooms">See the rooms</a></div>
      </div>
      <div class="hero-art">
        {ph('room-crockers', 'The Lords Dining Room at Crockers Folly', 'ph peak', eager=True)}
        <div class="stamp"><div><span>The</span><b>Lords</b><span>Room</span></div></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="head"><div><div class="label">Any occasion</div><h2>Something<br><span class="it">to celebrate?</span></h2></div><p>From an intimate family dinner to a full company night out, we plan the menu, the drinks and the timings with you.</p></div>
      <div class="occ">{occ}</div>
    </div>
  </section>

  <section class="section lords" id="rooms">
    <div class="wrap">
      <div class="lords-art rv">
        {ph('room-crockers', 'The Lords Dining Room set for dinner', 'ph big peak')}
        {ph('chef', 'A Maroush chef', 'ph chef')}
      </div>
      <div class="lords-copy">
        <div class="label">Crockers Folly · St John’s Wood</div>
        <h2>The Lords<br><span class="it">Dining Room</span></h2>
        <p>Our grandest room, inside a magnificent Victorian pub. High ceilings, an original fireplace and a crystal chandelier, with a view of the chefs at work.</p>
        <ul class="ticks"><li>Birthdays, celebrations and company dinners</li><li>Drinks in the 1898 Bar or on the terrace before you sit down</li><li>24 Aberdeen Place, NW8 8JR</li></ul>
        <div class="hero-btns"><a class="btn btn-red" href="#enquire">Enquire about the Lords Room <span class="ar">→</span></a><a class="btn btn-line" href="crockers-folly.html">Visit Crockers Folly</a></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap split">
      <div class="split-art rv">
        {ph('kebab-platter', 'A Maroush mixed grill', 'ph big peak')}
        {ph('bar-glass', 'A glass of fizz with mezze', 'ph small')}
      </div>
      <div class="split-copy">
        <div class="label">Beauchamp Place · Knightsbridge</div>
        <h2>The first-floor<br><span class="it">dining room</span></h2>
        <p>Above the buzz of Knightsbridge, our first-floor dining room is made for big tables and long, late dinners. The kitchen stays open until 3am, and 4.30am Thursday to Saturday.</p>
        <ul class="ticks"><li>Groups and late celebrations</li><li>Our full restaurant menu and sharing feasts</li><li>38 Beauchamp Place, SW3 1NU</li></ul>
        <div class="hero-btns"><a class="btn btn-red" href="#enquire">Enquire about a group <span class="ar">→</span></a><a class="btn btn-line" href="beauchamp-place.html">Visit Beauchamp Place</a></div>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0">
    <div class="wrap">
      <div class="head"><div><div class="label">Feasts for the table</div><h2>Everything<br><span class="it">in the middle</span></h2></div><p>Start from one of our sharing menus, or let our chefs build a menu around your guests, including vegan, vegetarian and children’s dishes.</p></div>
      <div class="setgrid three">{sets}</div>
      <div class="menus"><span class="label">Menus</span><a href="menu.html#menu-full">Restaurant menu →</a><a href="{MENU_PDF['wine']}" target="_blank" rel="noopener">Wine list ↗</a><a href="{MENU_PDF['drinks']}" target="_blank" rel="noopener">Cocktails ↗</a></div>
    </div>
  </section>

  <section class="section hiw">
    <div class="wrap">
      <div class="head"><div><div class="label">How it works</div><h2>Three steps<br><span class="it">to the table</span></h2></div></div>
      <ol class="steps">
        <li><b>Tell us the plan</b><p>Send the date, the number of guests and the occasion using the form below, or call the restaurant.</p></li>
        <li><b>Shape the menu</b><p>We come back with a menu and quote, and adjust it until it is exactly right for your guests.</p></li>
        <li><b>Arrive and enjoy</b><p>Your room is set, the mezze is ready and our team looks after everything on the night.</p></li>
      </ol>
    </div>
  </section>

  <section class="section gallery-s" style="padding-top:0">
    <div class="wrap gallery">
      {ph('stained-glass', 'The stained-glass windows at Crockers Folly', 'ph g1')}
      {ph('party', 'A party night at Maroush', 'ph g2', video=True)}
      {ph('terrace', 'The terrace at Crockers Folly', 'ph g3')}
      {ph('bar-1898', 'Fizz at the 1898 Bar', 'ph g4')}
      {ph('mezze-table', 'A table of mezze', 'ph g5')}
    </div>
  </section>

  <section class="section lords" id="enquire">
    <div class="wrap enquire">
      <div class="enq-copy">
        <div class="label">Enquire</div>
        <h2>Tell us about<br><span class="it">your event</span></h2>
        <p>We will come back to you with availability, menus and a quote. For a quick answer, call the restaurant directly.</p>
        <dl class="contact-dl"><dt>Crockers Folly</dt><dd class="sel">020 7289 9898</dd><dt>Beauchamp Place</dt><dd class="sel">020 7581 5434</dd><dt>Email</dt><dd class="sel">hello@maroush.com</dd></dl>
        <p class="small">Hosting at your own venue? See <a href="catering.html">events &amp; catering</a>.</p>
      </div>
      {form('privateForm', [
        field('p-name', 'Your name', req=True), field('p-email', 'Email', 'email', req=True),
        field('p-phone', 'Phone', 'tel', req=True), field('p-date', 'Date', 'date'),
        field('p-guests', 'Number of guests', 'number'),
        field('p-where', 'Where', 'select', opts=['Crockers Folly, Lords Dining Room', 'Beauchamp Place, first floor', 'Not sure yet']),
        field('p-occasion', 'Occasion', 'select', opts=['Birthday', 'Anniversary', 'Engagement', 'Family gathering', 'Company dinner', 'Christmas party', 'Other'], full=True),
        field('p-msg', 'Anything else?', 'textarea', full=True, ph_='Timings, dietary needs, budget, special touches'),
      ], 'Send enquiry', 'hello@maroush.com')}
    </div>
  </section>
</main>"""
PAGES['private-dining'] = ('Maroush Private Dining', "Private dining and group bookings at Maroush: the chandeliered Lords Dining Room at Crockers Folly, St John's Wood, and the first-floor dining room at Beauchamp Place, Knightsbridge. Lebanese sharing feasts for any occasion.", private_page())

# ---------------------------------------------------------------- lunch page
def lunch_page():
    cards = ''.join(f'<a class="other" href="{k}.html"><b>{V[k]["short"]}</b><small>{V[k]["area"]} · {V[k]["phone"]}</small><span class="tag {"book" if V[k]["kind"]=="sit" else ""}">{"Bookable" if V[k]["kind"]=="sit" else "Walk-in"}</span></a>' for k in V)
    return crumbs(('menu.html', 'Menu'), ('', 'Lunch offer')) + f"""<main>
  <section class="hero rest">
    <img class="hero-mark" src="assets/mark-cream.png" alt="" aria-hidden="true">
    <div class="wrap">
      <div class="hero-copy">
        <div class="label">Lunch offer · Monday to Thursday</div>
        <h1><span class="ln"><span class="it">Lunch at</span></span><span class="ln"><span>Maroush</span></span></h1>
        <p class="hero-sub">Two courses for £{LUNCH['two']} or three for £{LUNCH['three']}, Monday to Thursday from 11am to 3pm, at every Maroush in London.</p>
        <div class="hero-btns"><a class="btn btn-cream" href="#lunch">See what’s on <span class="ar">→</span></a><button class="btn btn-ghost" type="button" data-book>Book a table</button></div>
      </div>
      <div class="hero-art">
        {ph('mezze', 'Hommos and cold mezze', 'ph peak', eager=True)}
        <div class="stamp"><div><span>From</span><b>£{LUNCH['two']}</b><span>Mon–Thu</span></div></div>
      </div>
    </div>
  </section>
  <div class="section menu-body" style="padding-top:0"><div class="wrap">
    {lunch_html()}
  </div></div>
  <section class="section" style="padding-top:0">
    <div class="wrap">
      <div class="head"><div><div class="label">Where</div><h2>At every<br><span class="it">Maroush</span></h2></div><p>Book at our restaurants, or walk in to our shawarma and juice bars.</p></div>
      <div class="others six">{cards}</div>
    </div>
  </section>
</main>"""
PAGES['lunch'] = ('Maroush Lunch Offer', f"Maroush lunch offer: two courses for £{LUNCH['two']} or three courses for £{LUNCH['three']}, Monday to Thursday, 11am to 3pm, at every Maroush restaurant in London.", lunch_page())

_cf = PAGES['crockers-folly'][2]
_cf = _cf.replace('<section class="section visit" id="visit">', xmas_band('crockers-folly') + '\n\n  <section class="section visit" id="visit">', 1)
_cf = _cf.replace('<dl class="hours"><dt>Monday – Sunday</dt><dd>12pm – 12am</dd></dl>', '<dl class="hours"><dt>Monday – Sunday</dt><dd>12pm – 12am</dd><dt>Lunch offer</dt><dd><a href="lunch.html">Mon–Thu until 3pm</a></dd><dt>Christmas Day</dt><dd>Open · <a href="#christmas">festive menu</a></dd></dl>')
_cf = _cf.replace('<a href="menu.html">Full menu →</a>', '<a href="menu.html#menu-full">Full menu →</a><a href="lunch.html">Lunch offer →</a>')
PAGES['crockers-folly'] = (PAGES['crockers-folly'][0], PAGES['crockers-folly'][1], _cf)

_cf2 = PAGES['crockers-folly'][2].replace('href="catering.html">Enquire about private dining','href="private-dining.html">Enquire about private dining')
PAGES['crockers-folly'] = (PAGES['crockers-folly'][0], PAGES['crockers-folly'][1], _cf2)

ACTIVE = {'private-dining': 'private-dining.html', 'lunch': 'menu.html', 'christmas': 'christmas.html', 'menu': 'menu.html', 'about': 'about.html', 'catering': 'catering.html', 'restaurants': 'restaurants.html', 'contact': 'contact.html'}

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
