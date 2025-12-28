// Animations using GSAP and small interactions
document.addEventListener('DOMContentLoaded', function(){
  // GSAP intro for hero title and CTAs
  try{
    gsap.from('.title', {y: 40, opacity: 0, duration: 0.9, ease: 'power3.out'});
    gsap.from('.lead', {y: 20, opacity: 0, duration: 0.9, delay:0.15, ease: 'power3.out'});
    gsap.from('.btn-book', {scale: 0.95, opacity:0, duration:0.6, delay:0.3});
    gsap.from('.card-card', {scale:0.95, opacity:0, duration:0.7, delay:0.2});
  }catch(e){console.warn('GSAP init error', e)}

  // small hover micro-interactions
  document.querySelectorAll('.feature').forEach(function(el){
    el.addEventListener('mouseenter', function(){ gsap.to(el, {y:-6, boxShadow:'0 18px 40px rgba(0,0,0,0.45)', duration:0.35}) });
    el.addEventListener('mouseleave', function(){ gsap.to(el, {y:0, boxShadow:'none', duration:0.35}) });
  });

  // AOS will initialize in template script
});
