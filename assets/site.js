
(function(){
  var top=document.getElementById('top');
  function s(){top.classList.toggle('scrolled',scrollY>10)}
  addEventListener('scroll',s,{passive:true});s();
  var bk=document.getElementById('booking'),mn=document.getElementById('mnav');
  document.querySelectorAll('[data-book]').forEach(function(b){b.addEventListener('click',function(){mn.classList.remove('show');bk.classList.add('open')})});
  bk.querySelectorAll('[data-close]').forEach(function(b){b.addEventListener('click',function(){bk.classList.remove('open')})});
  document.getElementById('menuBtn').addEventListener('click',function(){mn.classList.add('show')});
  document.getElementById('menuX').addEventListener('click',function(){mn.classList.remove('show')});
  mn.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){mn.classList.remove('show')})});
  addEventListener('keydown',function(e){if(e.key==='Escape'){bk.classList.remove('open');mn.classList.remove('show');if(document.activeElement)document.activeElement.blur()}});
  document.querySelectorAll('.mega a,.mega button').forEach(function(a){a.addEventListener('click',function(){a.blur()})});
  if(matchMedia('(prefers-reduced-motion: reduce)').matches){document.querySelectorAll('video').forEach(function(v){v.removeAttribute('autoplay');v.pause()})}
  if('IntersectionObserver' in window&&!matchMedia('(prefers-reduced-motion: reduce)').matches){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.remove('wait');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
    document.querySelectorAll('.rv').forEach(function(el){if(el.getBoundingClientRect().top>innerHeight){el.classList.add('wait');io.observe(el)}});
  }
})();

/* Forms: posts to data-endpoint when one is set (e.g. a Google Apps Script web app).
   Until then it tells the visitor which address to email instead. */
(function(){
  document.querySelectorAll('form.form').forEach(function(f){
    var msg=f.querySelector('.form-msg');
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var bad=null;
      f.querySelectorAll('[required]').forEach(function(el){
        var ok=el.value.trim()!=='' && (el.type!=='email' || /.+@.+\..+/.test(el.value));
        el.setAttribute('aria-invalid',ok?'false':'true');
        if(!ok&&!bad)bad=el;
      });
      if(bad){msg.className='form-msg err';msg.textContent='Please fill in the highlighted fields.';bad.focus();return}
      var ep=f.getAttribute('data-endpoint');
      if(!ep){msg.className='form-msg err';msg.textContent='This form is not connected yet. Please email '+f.getAttribute('data-fallback')+'.';return}
      var btn=f.querySelector('button[type=submit]');btn.disabled=true;
      fetch(ep,{method:'POST',body:new FormData(f)}).then(function(r){
        if(!r.ok)throw 0;msg.className='form-msg';msg.textContent='Thank you. We will be in touch soon.';f.reset();
      }).catch(function(){msg.className='form-msg err';msg.textContent='Sorry, that did not send. Please email '+f.getAttribute('data-fallback')+'.'})
      .finally(function(){btn.disabled=false});
    });
  });
  /* Menu tabs: highlight the section in view */
  var tabs=document.querySelectorAll('.mtabs a');
  if(tabs.length&&'IntersectionObserver' in window){
    var map={};tabs.forEach(function(a){map[a.getAttribute('href').slice(1)]=a});
    var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){tabs.forEach(function(a){a.classList.remove('on')});var a=map[e.target.id];if(a){a.classList.add('on');a.scrollIntoView({block:'nearest',inline:'center'})}}})},{rootMargin:'-40% 0px -55% 0px'});
    document.querySelectorAll('.msec,.sets').forEach(function(s){o.observe(s)});
  }
})();

/* Menu page: switch between the restaurant menu and the everyday menu */
(function(){
  var btns=document.querySelectorAll('.mswitch button');
  if(!btns.length)return;
  function show(which,scroll){
    btns.forEach(function(b){var on=b.getAttribute('data-menu')===which;b.setAttribute('aria-selected',on?'true':'false');document.getElementById('menu-'+b.getAttribute('data-menu')).hidden=!on});
    if(scroll){document.querySelector('.mswitch').scrollIntoView({behavior:'smooth',block:'start'})}
  }
  btns.forEach(function(b){b.addEventListener('click',function(){show(b.getAttribute('data-menu'))})});
  var h=location.hash.slice(1);
  if(h==='menu-every'||h.indexOf('e-')===0||h==='sets-every'){show('every',h==='menu-every')}
  else if(h==='menu-full'){show('full',true)}
})();
