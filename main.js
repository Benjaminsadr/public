/* Dari-Gerichtsübersetzung – minimal JavaScript (Seite funktioniert auch ohne JS) */
(function () {
  "use strict";

  // Mobile Navigation
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("hauptnavigation");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Untermenü "Dokumente"
  document.querySelectorAll(".sub-toggle").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var li = btn.closest(".has-sub");
      var open = li.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
  document.addEventListener("click", function () {
    document.querySelectorAll(".has-sub.open").forEach(function (li) {
      li.classList.remove("open");
      var b = li.querySelector(".sub-toggle");
      if (b) b.setAttribute("aria-expanded", "false");
    });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") document.body.click();
  });

  // Jahreszahl in der Fußzeile
  var y = document.getElementById("jahr");
  if (y) y.textContent = new Date().getFullYear();

  // Honorarrechner nach § 11 JVEG
  var form = document.getElementById("jveg-rechner");
  if (form) {
    var RATES = {            // Euro je angefangene 55 Anschläge
      grund: 1.95,           // § 11 Abs. 1 S. 1 – editierbare Datei
      erhoeht: 2.15,         // § 11 Abs. 1 S. 2 – nicht editierbar (Scan, Papier, Fax)
      grund_erschwert: 2.15, // § 11 Abs. 1 S. 3 – besonders erschwert, editierbar
      erhoeht_erschwert: 2.30// § 11 Abs. 1 S. 3 – besonders erschwert, nicht editierbar
    };
    var MIN = 20;            // § 11 Abs. 3 S. 2 – Mindesthonorar je Auftrag
    var out = document.getElementById("rechner-ergebnis");
    var euro = new Intl.NumberFormat("de-DE", { style: "currency", currency: "EUR" });
    var num = new Intl.NumberFormat("de-DE");

    var calc = function () {
      var chars = parseInt(form.anschlaege.value, 10);
      if (!chars || chars < 1) {
        out.innerHTML = "Bitte die Zahl der Anschläge (mit Leerzeichen) eingeben.";
        return;
      }
      var editierbar = form.textform.value === "editierbar";
      var erschwert = form.erschwert.checked;
      var key = (editierbar ? "grund" : "erhoeht") + (erschwert ? "_erschwert" : "");
      var rate = RATES[key];
      var units = Math.ceil(chars / 55);
      var fee = Math.max(MIN, units * rate);
      out.innerHTML =
        "<strong>" + euro.format(fee) + "</strong>" +
        num.format(units) + " Einheiten zu je 55 Anschlägen × " + euro.format(rate) +
        (units * rate < MIN ? " – Mindesthonorar von " + euro.format(MIN) + " angesetzt" : "") +
        "<br><span class=\"hint\">Netto, zzgl. Umsatzsteuer soweit anfallend (§ 12 Abs. 1 S. 2 Nr. 4 JVEG). Unverbindliche Orientierung; die Festsetzung erfolgt durch die heranziehende Stelle.</span>";
    };
    form.addEventListener("input", calc);
    form.addEventListener("submit", function (e) { e.preventDefault(); calc(); });
    calc();
  }
})();
