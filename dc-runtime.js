// Mini-runtime : affiche le gabarit <template id="dc"> (exporté du canevas Claude Design)
// avec la logique du <script type="text/x-dc">. Gère {{ trous }}, onClick, <sc-if> et <sc-for>.
(function () {
  var tpl = document.getElementById("dc");
  var app = document.getElementById("app");
  var src = document.getElementById("dc-logic").textContent;
  var HOLE = /\{\{\s*([^}]+?)\s*\}\}/g;
  var WHOLE = /^\{\{\s*([^}]+?)\s*\}\}$/;
  var instance, pending = false;

  function DCLogic(props) { this.props = props || {}; this.state = {}; }
  DCLogic.prototype.setState = function (patch) {
    Object.assign(this.state, typeof patch === "function" ? patch(this.state) : patch);
    schedule();
  };
  DCLogic.prototype.forceUpdate = function () { schedule(); };

  function lookup(path, scope) {
    if (path === "true") return true;
    if (path === "false") return false;
    if (/^-?\d+(\.\d+)?$/.test(path)) return Number(path);
    var parts = path.split("."), v = scope;
    for (var i = 0; i < parts.length; i++) {
      if (v == null) return undefined;
      v = v[parts[i]];
    }
    return v;
  }
  function interp(str, scope) {
    return str.replace(HOLE, function (_, p) { var v = lookup(p, scope); return v == null ? "" : String(v); });
  }

  function build(node, scope, out) {
    if (node.nodeType === 3) { out.push(document.createTextNode(interp(node.nodeValue, scope))); return; }
    if (node.nodeType !== 1) return;
    var tag = node.localName;
    if (tag === "sc-if") {
      var m = WHOLE.exec(node.getAttribute("value") || "");
      if (m && lookup(m[1], scope)) children(node, scope, out);
      return;
    }
    if (tag === "sc-for") {
      var lm = WHOLE.exec(node.getAttribute("list") || "");
      var list = lm ? lookup(lm[1], scope) : null;
      var as = node.getAttribute("as") || "item";
      (list || []).forEach(function (item, i) {
        var s = Object.create(scope); s[as] = item; s.$index = i;
        children(node, s, out);
      });
      return;
    }
    var el = document.createElementNS(node.namespaceURI, tag);
    for (var i = 0; i < node.attributes.length; i++) {
      var a = node.attributes[i], name = a.name, val = a.value;
      if (name.indexOf("hint-") === 0) continue;
      var w = WHOLE.exec(val);
      if (name.indexOf("on") === 0 && w) {
        var fn = lookup(w[1], scope);
        if (typeof fn === "function") el.addEventListener(name.slice(2), fn);
        continue;
      }
      if (w) { var v = lookup(w[1], scope); if (v == null) continue; el.setAttribute(name, String(v)); }
      else el.setAttribute(name, interp(val, scope));
    }
    var kids = [];
    children(node, scope, kids);
    kids.forEach(function (k) { el.appendChild(k); });
    out.push(el);
  }
  function children(node, scope, out) {
    var c = node.content || node;
    for (var n = c.firstChild; n; n = n.nextSibling) build(n, scope, out);
  }

  function render() {
    pending = false;
    var out = [];
    children(tpl, instance.renderVals(), out);
    app.replaceChildren.apply(app, out);
  }
  function schedule() { if (!pending) { pending = true; requestAnimationFrame(render); } }

  var Component = new Function("DCLogic", src + "\nreturn Component;")(DCLogic);
  instance = new Component({});
  if (!instance.state) instance.state = {};
  render();
  if (instance.componentDidMount) instance.componentDidMount();
})();
