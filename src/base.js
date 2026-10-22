
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
