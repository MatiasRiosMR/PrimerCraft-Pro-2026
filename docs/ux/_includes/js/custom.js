// Visor de diagramas Mermaid: cada diagrama se muestra ajustado al ancho y se puede
// abrir en tamaño real, con zoom y arrastre para recorrerlo.
(function () {
  'use strict';

  function titulo(pre) {
    for (var el = pre.previousElementSibling; el; el = el.previousElementSibling) {
      if (/^H[1-4]$/.test(el.tagName)) return el.textContent.trim();
    }
    var h1 = document.querySelector('.main-content h1');
    return h1 ? h1.textContent.trim() : 'Diagrama';
  }

  function abrir(svg, nombre) {
    var vb = svg.viewBox && svg.viewBox.baseVal;
    var ancho = vb && vb.width ? vb.width : svg.getBoundingClientRect().width;
    var escala = 1;

    var capa = document.createElement('div');
    capa.className = 'pc-viewer';
    capa.setAttribute('role', 'dialog');
    capa.setAttribute('aria-modal', 'true');
    capa.setAttribute('aria-label', nombre);
    capa.innerHTML =
      '<div class="pc-viewer-bar">' +
        '<span class="pc-viewer-title"></span>' +
        '<span class="pc-viewer-zoom" aria-live="polite"></span>' +
        '<button type="button" data-z="-1" aria-label="Alejar">−</button>' +
        '<button type="button" data-z="1" aria-label="Acercar">+</button>' +
        '<button type="button" data-z="fit">Ajustar</button>' +
        '<button type="button" data-z="real">100 %</button>' +
        '<button type="button" class="pc-viewer-close" aria-label="Cerrar">✕</button>' +
      '</div>' +
      '<div class="pc-viewer-body"></div>';
    capa.querySelector('.pc-viewer-title').textContent = nombre;

    var cuerpo = capa.querySelector('.pc-viewer-body');
    var copia = svg.cloneNode(true);
    copia.removeAttribute('style');
    copia.removeAttribute('height');
    cuerpo.appendChild(copia);

    function aplicar() {
      copia.style.width = Math.round(ancho * escala) + 'px';
      copia.style.maxWidth = 'none';
      copia.style.height = 'auto';
      capa.querySelector('.pc-viewer-zoom').textContent = Math.round(escala * 100) + ' %';
    }
    function ajustar() {
      escala = Math.min(2, (cuerpo.clientWidth - 48) / ancho);
      aplicar();
    }

    capa.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) { if (e.target === capa) cerrar(); return; }
      var z = b.getAttribute('data-z');
      if (z === 'fit') ajustar();
      else if (z === 'real') { escala = 1; aplicar(); }
      else if (z) { escala = Math.max(0.3, Math.min(4, escala * (z === '1' ? 1.25 : 0.8))); aplicar(); }
      else cerrar();
    });

    // arrastrar para recorrer
    var arr = null;
    cuerpo.addEventListener('pointerdown', function (e) {
      arr = { x: e.clientX, y: e.clientY, l: cuerpo.scrollLeft, t: cuerpo.scrollTop };
      cuerpo.classList.add('is-dragging');
    });
    window.addEventListener('pointermove', function (e) {
      if (!arr) return;
      cuerpo.scrollLeft = arr.l - (e.clientX - arr.x);
      cuerpo.scrollTop = arr.t - (e.clientY - arr.y);
    });
    window.addEventListener('pointerup', function () { arr = null; cuerpo.classList.remove('is-dragging'); });

    function tecla(e) { if (e.key === 'Escape') cerrar(); }
    var previo = document.activeElement;
    function cerrar() {
      document.removeEventListener('keydown', tecla);
      document.documentElement.classList.remove('pc-viewer-open');
      capa.remove();
      if (previo) previo.focus();
    }
    document.addEventListener('keydown', tecla);
    document.documentElement.classList.add('pc-viewer-open');
    document.body.appendChild(capa);
    ajustar();
    capa.querySelector('.pc-viewer-close').focus();
  }

  // Colores de la marca en los nodos (Mermaid escribe los de classDef como estilo en
  // línea con !important, así que se reemplazan acá; el código de cada .md no cambia).
  var MARCA = {
    '#4f46e5': '#0e6660', '#312e81': '#12324a', '#475569': '#12324a',
    '#ecfeff': '#e6f2f1', '#0e7490': '#0e6660', '#083344': '#12324a'
  };
  function recolorear(svg) {
    svg.querySelectorAll('[style]').forEach(function (el) {
      var st = el.getAttribute('style');
      var nuevo = st.replace(/#[0-9a-f]{6}/gi, function (c) { return MARCA[c.toLowerCase()] || c; });
      if (nuevo !== st) el.setAttribute('style', nuevo);
    });
  }

  function preparar(code) {
    var pre = code.closest('pre') || code;
    if (pre.classList.contains('pc-diagram')) return;
    var svg = code.querySelector('svg');
    if (!svg) return;
    pre.classList.add('pc-diagram');
    recolorear(svg);
    var nombre = titulo(pre);
    var vb = svg.viewBox && svg.viewBox.baseVal;
    if (vb && vb.width > pre.clientWidth * 1.8) {
      var nota = document.createElement('p');
      nota.className = 'pc-diagram-hint';
      nota.textContent = 'Diagrama grande: tocá "Ampliar" o hacé clic sobre él para verlo en tamaño real.';
      pre.appendChild(nota);
    }
    var boton = document.createElement('button');
    boton.type = 'button';
    boton.className = 'pc-diagram-expand';
    boton.innerHTML = '<span aria-hidden="true">⤢</span> Ampliar';
    boton.setAttribute('aria-label', 'Ampliar diagrama: ' + nombre);
    boton.addEventListener('click', function () { abrir(svg, nombre); });
    pre.appendChild(boton);
    svg.addEventListener('click', function () { abrir(svg, nombre); });
  }

  // Mermaid inserta el SVG y lo termina de dibujar después: se espera a que el DOM
  // quede quieto y a que el SVG tenga su tamaño final antes de prepararlo.
  var espera = null;
  function revisar() {
    clearTimeout(espera);
    espera = setTimeout(function () {
      document.querySelectorAll('code.language-mermaid').forEach(function (code) {
        var svg = code.querySelector('svg');
        if (svg && svg.getAttribute('aria-roledescription') !== 'error' && svg.viewBox && svg.viewBox.baseVal && svg.viewBox.baseVal.width > 0) preparar(code);
      });
    }, 300);
  }

  document.addEventListener('DOMContentLoaded', function () {
    if (!document.querySelector('code.language-mermaid')) return;
    new MutationObserver(revisar).observe(document.querySelector('.main-content') || document.body, { childList: true, subtree: true, attributes: true });
    revisar();
  });
})();
