/* ============================================================
   Nottingville — landing page behaviour.

   DELIBERATE DIFFERENCE FROM index.html:
   index.html intercepts every WhatsApp click with e.preventDefault()
   and forces a 7-field modal before opening the chat. That gate is why
   WhatsApp logged only 6 conversions in 90 days against 29 on-page
   entry points, while ungated tel: clicks logged 16.

   Landing pages carry paid traffic and must not add friction, so here
   WhatsApp links open directly. The qualifying context that the modal
   used to collect is instead baked into the prefilled WhatsApp message
   per page, and the enquiry is still logged to the Google Sheet via a
   fire-and-forget pixel.
   ============================================================ */
(function () {
  'use strict';

  var SHEETS_ENDPOINT = 'https://script.google.com/macros/s/AKfycbyu68FWby2Rzmrxl8sIzZS4iGSvVcr3ICUEgJd6yst7PIpZGJHWSn1oKNTiFKpov4opiw/exec';

  /* ── Nav shadow ── */
  var nav = document.getElementById('nav');
  if (nav) {
    window.addEventListener('scroll', function () {
      nav.classList.toggle('scrolled', window.scrollY > 40);
    }, { passive: true });
  }

  /* ── Hero parallax (skipped when the user prefers reduced motion) ── */
  var heroBg = document.getElementById('heroBg');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (heroBg && !reduce) {
    window.addEventListener('scroll', function () {
      heroBg.style.transform = 'scale(1.06) translateY(' + (window.scrollY * 0.24) + 'px)';
    }, { passive: true });
  }

  /* ── Scroll fade-in ── */
  var faders = document.querySelectorAll('.fade-in');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry, i) {
        if (entry.isIntersecting) {
          setTimeout(function () { entry.target.classList.add('visible'); }, i * 70);
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    faders.forEach(function (el) { io.observe(el); });
  } else {
    faders.forEach(function (el) { el.classList.add('visible'); });
  }

  /* ── Log the enquiry without blocking the click ── */
  function logEnquiry(channel, cta) {
    if (!SHEETS_ENDPOINT) return;
    try {
      var qs = new URLSearchParams({
        source: 'lp:' + channel,
        cta: cta || '',
        page_url: location.href,
        page: location.pathname.replace(/^\//, '').replace(/\.html$/, '') || 'home'
      }).toString();
      new Image().src = SHEETS_ENDPOINT + '?' + qs;
    } catch (e) { /* never block the conversion on analytics */ }
  }

  /* ── Conversion tracking. Links are NOT intercepted. ── */
  document.addEventListener('click', function (e) {
    var link = e.target.closest && e.target.closest('a[href]');
    if (!link) return;

    var href = link.getAttribute('href') || '';
    var cta = link.getAttribute('data-cta') || '';

    if (href.indexOf('tel:') === 0) {
      if (typeof gads_phone_conversion === 'function') gads_phone_conversion();
      if (typeof fbq === 'function') {
        fbq('track', 'Contact', { content_name: 'Phone Call', content_category: 'Phone' });
      }
      logEnquiry('phone', cta);
      return; // let the dialler open
    }

    if (href.indexOf('wa.me/') !== -1) {
      if (typeof gads_whatsapp_conversion === 'function') gads_whatsapp_conversion();
      if (typeof fbq === 'function') {
        fbq('track', 'Lead', { content_name: 'WhatsApp Lead', content_category: 'WhatsApp' });
      }
      logEnquiry('whatsapp', cta);
      return; // let WhatsApp open
    }
  }, { passive: true });
})();
