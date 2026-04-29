#!/usr/bin/env python3
"""Generator for the Community Breakfast presentation deck."""
import os, sys

BASE = '/Users/kond/bobcats/presentations/20260430_Community_Breakfast'
ASSETS = BASE + '/assets'

f400 = open(f'{ASSETS}/bai-jamjuree-400.b64').read().strip()
f500 = open(f'{ASSETS}/bai-jamjuree-500.b64').read().strip()
f600 = open(f'{ASSETS}/bai-jamjuree-600.b64').read().strip()
qr_js  = open(f'{ASSETS}/qrcode.min.js').read()
gsap_js = open(f'{ASSETS}/gsap.min.js').read()
tp_js   = open(f'{ASSETS}/TextPlugin.min.js').read()

# ── CSS ──────────────────────────────────────────────────────────────────────
CSS = f"""
@font-face{{font-family:'Bai Jamjuree';font-weight:400;font-style:normal;src:url('data:font/woff;base64,{f400}') format('woff');}}
@font-face{{font-family:'Bai Jamjuree';font-weight:500;font-style:normal;src:url('data:font/woff;base64,{f500}') format('woff');}}
@font-face{{font-family:'Bai Jamjuree';font-weight:600;font-style:normal;src:url('data:font/woff;base64,{f600}') format('woff');}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{width:100vw;height:100vh;background:#0d0d0d;overflow:hidden;font-family:'Bai Jamjuree',sans-serif;cursor:none;}}
#deck-wrapper{{position:fixed;inset:0;overflow:hidden;}}
#deck{{position:absolute;top:0;left:0;width:1920px;height:1080px;overflow:hidden;transform-origin:top left;}}
#slides-container{{position:absolute;inset:0;}}
.slide{{position:absolute;top:0;left:0;width:1920px;height:1080px;display:none;flex-direction:column;align-items:center;justify-content:center;background:var(--slide-bg,#334258);color:var(--slide-fg,#FCE3EB);padding:100px 120px;opacity:0;}}
.slide.visible{{display:flex;}}
.h1{{font-size:148px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;line-height:.9;color:var(--slide-fg,#FCE3EB);}}
.h2{{font-size:96px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;line-height:.92;}}
.h3{{font-size:72px;font-weight:600;text-transform:uppercase;letter-spacing:.07em;line-height:.92;}}
.body{{font-size:58px;font-weight:400;line-height:1.35;}}
.body-sm{{font-size:44px;font-weight:400;line-height:1.4;}}
.sub{{font-size:38px;font-weight:400;opacity:.65;line-height:1.35;margin-top:24px;}}
.green{{color:#E1E281;}}
.pink{{color:#F9C7D8;}}
.dim{{opacity:.55;}}
.center{{text-align:center;}}
.gap{{margin-top:48px;}}
.gap-sm{{margin-top:24px;}}
/* progress */
#progress{{position:absolute;bottom:0;left:0;height:4px;background:#E1E281;width:0;z-index:200;transition:width .25s ease;}}
#counter{{position:absolute;bottom:18px;right:32px;font-size:22px;font-weight:500;letter-spacing:.06em;color:rgba(252,227,235,.35);z-index:200;font-family:'Bai Jamjuree',sans-serif;}}
.s-tick{{position:absolute;bottom:0;width:2px;background:rgba(255,255,255,.25);z-index:201;}}
/* overview */
#overview{{position:fixed;inset:0;background:rgba(0,0,0,.96);display:none;overflow-y:auto;z-index:1000;padding:48px 56px;}}
#overview.open{{display:block;}}
#ov-grid{{display:flex;flex-wrap:wrap;gap:12px;}}
.ov-thumb{{width:240px;height:135px;overflow:hidden;position:relative;cursor:pointer;border:2px solid rgba(255,255,255,.1);border-radius:4px;flex-shrink:0;}}
.ov-thumb:hover,.ov-thumb.cur{{border-color:#E1E281;}}
.ov-inner{{position:absolute;top:0;left:0;width:1920px;height:1080px;transform:scale(.125);transform-origin:top left;pointer-events:none;}}
.ov-label{{position:absolute;bottom:0;left:0;right:0;background:rgba(0,0,0,.6);font-size:10px;color:#fff;padding:3px 6px;font-family:'Bai Jamjuree',sans-serif;letter-spacing:.04em;}}
/* blackout */
#blackout{{position:fixed;inset:0;background:#000;display:none;z-index:2000;}}
#blackout.on{{display:block;}}
/* qr */
.qr-wrap{{display:flex;flex-direction:column;align-items:center;gap:14px;}}
.qr-label{{font-size:28px;font-weight:500;letter-spacing:.08em;text-transform:uppercase;opacity:.7;}}
/* carousel */
.carousel{{position:relative;width:100%;height:100%;}}
.c-frame{{position:absolute;inset:0;display:none;align-items:center;justify-content:center;}}
.c-frame.c-active{{display:flex;}}
.c-counter{{position:absolute;bottom:40px;right:60px;font-size:32px;font-weight:500;opacity:.5;letter-spacing:.06em;}}
.screenshot-placeholder{{width:1440px;height:810px;background:#1a2336;border:2px dashed rgba(225,226,129,.4);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;border-radius:6px;}}
.screenshot-placeholder .ph-label{{font-size:40px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;color:#E1E281;opacity:.6;}}
.screenshot-placeholder .ph-hint{{font-size:26px;opacity:.35;}}
.screenshot-img{{max-width:1440px;max-height:810px;object-fit:contain;border-radius:4px;}}
/* dep tree */
#dep-svg{{overflow:visible;}}
.dep-node{{opacity:0;transition:none;}}
.dep-edge{{stroke-dasharray:900;stroke-dashoffset:900;transition:none;}}
/* gastown full bleed */
.full-bleed{{position:absolute;inset:0;overflow:hidden;}}
.full-bleed img{{width:100%;height:100%;object-fit:cover;transform-origin:center center;}}
.full-bleed-overlay{{position:absolute;inset:0;background:linear-gradient(to right,rgba(51,66,88,.85) 40%,rgba(51,66,88,.3));}}
.full-bleed-content{{position:absolute;inset:0;z-index:2;display:flex;flex-direction:column;justify-content:flex-end;padding:100px 120px;}}
/* section 9 pillars */
.pillar-wrap{{display:flex;gap:64px;align-items:flex-start;width:100%;}}
.pillar{{flex:1;padding:52px 44px;border-top:3px solid #E1E281;}}
.pillar .p-num{{font-size:48px;font-weight:600;color:#E1E281;letter-spacing:.12em;margin-bottom:28px;opacity:.6;}}
.pillar .p-claim{{font-size:54px;font-weight:600;text-transform:uppercase;letter-spacing:.07em;line-height:.92;margin-bottom:20px;}}
.pillar .p-sub{{font-size:36px;opacity:.6;}}
/* kinetic */
.kinetic-word{{display:inline-block;}}
/* section bg variants */
.bg-pink{{--slide-bg:#F9C7D8;--slide-fg:#334258;}}
.bg-dark{{--slide-bg:#334258;--slide-fg:#FCE3EB;}}
/* NCR gif bg */
.ncr-bg{{position:absolute;inset:0;object-fit:cover;opacity:1;}}
/* grid SVG animation */
#grid-svg .grid-line{{stroke-dasharray:600;stroke-dashoffset:600;stroke:#E1E281;stroke-width:1;fill:none;opacity:.5;}}
/* logos row */
.logos-row{{display:flex;gap:64px;align-items:center;justify-content:center;flex-wrap:wrap;}}
.logo-wm{{font-size:44px;font-weight:600;text-transform:uppercase;letter-spacing:.1em;opacity:.6;padding:12px 28px;border:1.5px solid rgba(225,226,129,.3);border-radius:3px;}}
.logo-wm.hi{{opacity:1;border-color:#E1E281;color:#E1E281;}}
.logo-box{{display:flex;align-items:center;justify-content:center;height:124px;width:240px;background:#FCE3EB;border-radius:8px;padding:18px 24px;}}
.logo-box img{{max-height:100%;max-width:100%;object-fit:contain;display:block;}}
.logo-claude{{height:160px;object-fit:contain;}}
/* video */
.slide-video{{width:860px;height:483px;border-radius:6px;object-fit:cover;background:#111;}}
/* citation */
.citation-card{{border-left:4px solid #E1E281;padding:32px 48px;max-width:1400px;}}
/* url footnote */
.footnote{{position:absolute;bottom:44px;left:120px;font-size:28px;opacity:.4;letter-spacing:.04em;}}
/* hand */
#hand-svg{{filter:drop-shadow(0 0 80px rgba(249,199,216,.2));}}
"""

# ── SVG: raised hand ─────────────────────────────────────────────────────────
HAND_SVG = """<svg id="hand-svg" width="300" height="420" viewBox="0 0 300 420" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Fingers -->
  <rect x="84" y="60" width="30" height="150" rx="15" fill="#FCE3EB"/>
  <rect x="122" y="32" width="30" height="180" rx="15" fill="#FCE3EB"/>
  <rect x="160" y="38" width="30" height="174" rx="15" fill="#FCE3EB"/>
  <rect x="198" y="68" width="30" height="144" rx="15" fill="#FCE3EB"/>
  <!-- Palm -->
  <rect x="84" y="180" width="144" height="140" rx="14" fill="#FCE3EB"/>
  <!-- Thumb (extended outward, "open" pose) -->
  <rect x="50" y="120" width="36" height="110" rx="18" fill="#FCE3EB" transform="rotate(-26 86 230)"/>
  <!-- Wrist -->
  <rect x="100" y="302" width="112" height="70" rx="12" fill="#FCE3EB"/>
</svg>"""

# ── SVG: dependency tree (slide 5.2) ─────────────────────────────────────────
DEP_SVG = """<svg id="dep-svg" width="1200" height="600" viewBox="0 0 1200 600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="rgba(252,227,235,.5)"/>
    </marker>
    <marker id="arr-green" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#E1E281"/>
    </marker>
  </defs>
  <!-- Node: project -->
  <g class="dep-node" id="dn-project">
    <rect x="480" y="40" width="240" height="72" rx="8" fill="#1a2a3d" stroke="rgba(252,227,235,.4)" stroke-width="1.5"/>
    <text x="600" y="84" text-anchor="middle" fill="#FCE3EB" font-family="Bai Jamjuree,sans-serif" font-size="28" font-weight="600">my-project</text>
  </g>
  <!-- Edge project→api -->
  <line class="dep-edge" id="de-pa" x1="540" y1="112" x2="300" y2="260" stroke="rgba(252,227,235,.4)" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Edge project→lodash -->
  <line class="dep-edge" id="de-pl" x1="660" y1="112" x2="900" y2="260" stroke="rgba(252,227,235,.4)" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Node: @api/client -->
  <g class="dep-node" id="dn-api">
    <rect x="160" y="260" width="280" height="72" rx="8" fill="#1a2a3d" stroke="rgba(252,227,235,.4)" stroke-width="1.5"/>
    <text x="300" y="304" text-anchor="middle" fill="#FCE3EB" font-family="Bai Jamjuree,sans-serif" font-size="26" font-weight="500">@api/client</text>
  </g>
  <!-- Node: lodash -->
  <g class="dep-node" id="dn-lodash">
    <rect x="760" y="260" width="280" height="72" rx="8" fill="#1a2a3d" stroke="rgba(252,227,235,.4)" stroke-width="1.5"/>
    <text x="900" y="285" text-anchor="middle" fill="#FCE3EB" font-family="Bai Jamjuree,sans-serif" font-size="26" font-weight="500">lodash</text>
    <text x="900" y="318" text-anchor="middle" fill="rgba(252,227,235,.5)" font-family="Bai Jamjuree,sans-serif" font-size="22">v4.17.19</text>
  </g>
  <!-- Edge api→utils -->
  <line class="dep-edge" id="de-au" x1="300" y1="332" x2="300" y2="432" stroke="rgba(252,227,235,.4)" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Node: utils (ok) -->
  <g class="dep-node" id="dn-utils">
    <rect x="160" y="432" width="280" height="72" rx="8" fill="#1a2a3d" stroke="rgba(252,227,235,.4)" stroke-width="1.5"/>
    <text x="300" y="476" text-anchor="middle" fill="#FCE3EB" font-family="Bai Jamjuree,sans-serif" font-size="26" font-weight="500">utils v2.1.0</text>
  </g>
  <!-- Hook box (hidden initially) -->
  <g id="hook-box" opacity="0">
    <rect x="680" y="380" width="420" height="100" rx="8" fill="#0d1a0d" stroke="#E1E281" stroke-width="2"/>
    <text x="890" y="420" text-anchor="middle" fill="#E1E281" font-family="Bai Jamjuree,sans-serif" font-size="24" font-weight="600">VERSION HOOK</text>
    <text x="890" y="458" text-anchor="middle" fill="rgba(225,226,129,.7)" font-family="Bai Jamjuree,sans-serif" font-size="20">intercepted → pinning to 4.17.21</text>
  </g>
  <!-- Version tag on lodash (changes color) -->
  <rect id="lodash-bg" x="760" y="260" width="280" height="72" rx="8" fill="#1a2a3d" stroke="rgba(252,227,235,.4)" stroke-width="1.5" opacity="0"/>
</svg>"""

# ── SVG: agentic grid (slide 3.1) ────────────────────────────────────────────
GRID_SVG = """<svg id="grid-svg" width="1920" height="1080" viewBox="0 0 1920 1080" style="position:absolute;inset:0;pointer-events:none;" xmlns="http://www.w3.org/2000/svg">
  <!-- Horizontal lines -->
  <line class="grid-line" x1="0" y1="270" x2="1920" y2="270"/>
  <line class="grid-line" x1="0" y1="540" x2="1920" y2="540"/>
  <line class="grid-line" x1="0" y1="810" x2="1920" y2="810"/>
  <!-- Vertical lines -->
  <line class="grid-line" x1="480" y1="0" x2="480" y2="1080"/>
  <line class="grid-line" x1="960" y1="0" x2="960" y2="1080"/>
  <line class="grid-line" x1="1440" y1="0" x2="1440" y2="1080"/>
  <!-- Accent nodes at intersections -->
  <circle class="grid-line" cx="480" cy="270" r="6" stroke="none" fill="#E1E281" opacity="0"/>
  <circle class="grid-line" cx="960" cy="270" r="6" stroke="none" fill="#E1E281" opacity="0"/>
  <circle class="grid-line" cx="1440" cy="270" r="6" stroke="none" fill="#E1E281" opacity="0"/>
  <circle class="grid-line" cx="480" cy="540" r="6" stroke="none" fill="#E1E281" opacity="0"/>
  <circle class="grid-line" cx="960" cy="540" r="6" stroke="none" fill="#E1E281" opacity="0"/>
  <circle class="grid-line" cx="1440" cy="540" r="6" stroke="none" fill="#E1E281" opacity="0"/>
  <circle class="grid-line" cx="480" cy="810" r="6" stroke="none" fill="#E1E281" opacity="0"/>
  <circle class="grid-line" cx="960" cy="810" r="6" stroke="none" fill="#E1E281" opacity="0"/>
  <circle class="grid-line" cx="1440" cy="810" r="6" stroke="none" fill="#E1E281" opacity="0"/>
</svg>"""

# ── SVG: clutter architecture (slide 7.2) ────────────────────────────────────
ARCH_SVG = """<svg width="760" height="520" viewBox="0 0 760 520" fill="none" xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0;">
  <defs>
    <marker id="a2" markerWidth="7" markerHeight="5" refX="7" refY="2.5" orient="auto">
      <polygon points="0 0, 7 2.5, 0 5" fill="#E1E281" opacity=".7"/>
    </marker>
  </defs>
  <!-- K8s boundary -->
  <rect x="1" y="1" width="758" height="518" rx="10" stroke="rgba(225,226,129,.3)" stroke-width="1.5" stroke-dasharray="8 4"/>
  <text x="16" y="22" fill="rgba(225,226,129,.5)" font-family="Bai Jamjuree,sans-serif" font-size="14" font-weight="600" letter-spacing="2">K8S NAMESPACE</text>
  <!-- Control Plane box -->
  <rect x="20" y="40" width="340" height="200" rx="7" fill="rgba(26,42,61,.8)" stroke="rgba(252,227,235,.25)" stroke-width="1"/>
  <text x="34" y="62" fill="rgba(252,227,235,.5)" font-family="Bai Jamjuree,sans-serif" font-size="13" font-weight="600" letter-spacing="1.5">CONTROL PLANE</text>
  <rect x="36" y="74" width="140" height="42" rx="5" fill="#1a2a3d" stroke="rgba(225,226,129,.4)" stroke-width="1"/>
  <text x="106" y="100" text-anchor="middle" fill="#FCE3EB" font-family="Bai Jamjuree,sans-serif" font-size="14">Swarm Worker</text>
  <rect x="188" y="74" width="152" height="42" rx="5" fill="#1a2a3d" stroke="rgba(225,226,129,.4)" stroke-width="1"/>
  <text x="264" y="100" text-anchor="middle" fill="#FCE3EB" font-family="Bai Jamjuree,sans-serif" font-size="14">Dashboard API</text>
  <rect x="36" y="132" width="304" height="42" rx="5" fill="#1a2a3d" stroke="rgba(225,226,129,.4)" stroke-width="1"/>
  <text x="188" y="158" text-anchor="middle" fill="#FCE3EB" font-family="Bai Jamjuree,sans-serif" font-size="14">NATS Subscriber</text>
  <!-- NATS -->
  <rect x="390" y="40" width="160" height="60" rx="7" fill="#1a2a3d" stroke="rgba(225,226,129,.5)" stroke-width="1.5"/>
  <text x="470" y="75" text-anchor="middle" fill="#E1E281" font-family="Bai Jamjuree,sans-serif" font-size="18" font-weight="600">NATS</text>
  <!-- SurrealDB -->
  <rect x="576" y="40" width="166" height="60" rx="7" fill="#1a2a3d" stroke="rgba(225,226,129,.4)" stroke-width="1"/>
  <text x="659" y="75" text-anchor="middle" fill="#FCE3EB" font-family="Bai Jamjuree,sans-serif" font-size="16">SurrealDB</text>
  <!-- Arrows CP → NATS -->
  <line x1="360" y1="158" x2="388" y2="70" stroke="#E1E281" stroke-width="1" opacity=".5" marker-end="url(#a2)"/>
  <!-- Agent 1 namespace -->
  <rect x="20" y="310" width="340" height="140" rx="7" fill="rgba(26,42,61,.6)" stroke="rgba(225,226,129,.25)" stroke-dasharray="6 3" stroke-width="1"/>
  <text x="34" y="330" fill="rgba(225,226,129,.4)" font-family="Bai Jamjuree,sans-serif" font-size="12" font-weight="600" letter-spacing="1.5">AGENT NS 1</text>
  <rect x="40" y="340" width="300" height="90" rx="5" fill="#1a2a3d" stroke="rgba(225,226,129,.4)" stroke-width="1"/>
  <text x="190" y="375" text-anchor="middle" fill="#FCE3EB" font-family="Bai Jamjuree,sans-serif" font-size="16" font-weight="500">Agent Pod</text>
  <text x="190" y="402" text-anchor="middle" fill="rgba(225,226,129,.6)" font-family="Bai Jamjuree,sans-serif" font-size="12">bash loop · claude CLI</text>
  <!-- Agent 2 namespace -->
  <rect x="390" y="310" width="352" height="140" rx="7" fill="rgba(26,42,61,.6)" stroke="rgba(225,226,129,.25)" stroke-dasharray="6 3" stroke-width="1"/>
  <text x="404" y="330" fill="rgba(225,226,129,.4)" font-family="Bai Jamjuree,sans-serif" font-size="12" font-weight="600" letter-spacing="1.5">AGENT NS 2</text>
  <rect x="410" y="340" width="314" height="90" rx="5" fill="#1a2a3d" stroke="rgba(225,226,129,.4)" stroke-width="1"/>
  <text x="567" y="375" text-anchor="middle" fill="#FCE3EB" font-family="Bai Jamjuree,sans-serif" font-size="16" font-weight="500">Agent Pod</text>
  <text x="567" y="402" text-anchor="middle" fill="rgba(225,226,129,.6)" font-family="Bai Jamjuree,sans-serif" font-size="12">bash loop · claude CLI</text>
  <!-- CP → Agent arrows -->
  <line x1="190" y1="240" x2="190" y2="308" stroke="rgba(225,226,129,.5)" stroke-width="1" marker-end="url(#a2)"/>
  <line x1="190" y1="240" x2="567" y2="308" stroke="rgba(225,226,129,.3)" stroke-width="1" marker-end="url(#a2)"/>
</svg>"""

# ── Slides HTML ───────────────────────────────────────────────────────────────
def qr_cell(qr_id, label="AI Field Notes"):
    return f"""<div class="qr-wrap"><canvas id="{qr_id}" data-qr-url=""></canvas><div class="qr-label">{label}</div></div>"""

SLIDES_HTML = f"""
<!-- 1.1 Audience Interaction -->
<div class="slide bg-dark" id="s1-1" data-id="1.1" data-section="1" data-section-title="Audience Interaction" data-anim="hand" data-notes="Three questions: Raise your hand if you've used an AI coding tool. Keep it up if you've used it in production. Keep it up if it changed how you plan.">
  {HAND_SVG}
</div>

<!-- 2.1 Vibe Coding: title + video + logos -->
<div class="slide bg-dark" id="s2-1" data-id="2.1" data-section="2" data-section-title="Vibe Coding" data-anim="vibe-title" data-notes="Andrej Karpathy coined the term. These tools are remarkable for MVPs.">
  <div class="h1 green center" id="vibe-title-text" style="margin-bottom:56px;font-size:120px;">VIBE CODING</div>
  <video class="slide-video" src="assets/vibe-coding.mp4" loop muted playsinline id="vibe-video"></video>
  <div class="logos-row" style="margin-top:48px;">
    <div class="logo-box"><img src="assets/logo-lovable.png" alt="Lovable"></div>
    <div class="logo-box"><img src="assets/logo-base44.svg" alt="Base44"></div>
    <div class="logo-box"><img src="assets/logo-bolt.png" alt="Bolt.new"></div>
    <div class="logo-box"><img src="assets/logo-bubble.svg" alt="Bubble.io"></div>
  </div>
</div>

<!-- 2.2 The pitch -->
<div class="slide bg-dark" id="s2-2" data-id="2.2" data-section="2" data-anim="fade-up" data-notes="">
  <div class="body center" style="max-width:1400px;font-style:italic;">Intuitive, prompt-based AI development.<br>Great for MVPs and quick iteration.</div>
</div>

<!-- 2.3 Where it breaks -->
<div class="slide bg-dark" id="s2-3" data-id="2.3" data-section="2" data-anim="vibe-bullets" data-notes="This is where vibe coding hits a wall.">
  <img class="ncr-bg" src="assets/giphy-chaos.gif" alt="">
  <div style="position:relative;z-index:2;background:rgba(51,66,88,.88);padding:60px 80px;border-radius:8px;max-width:900px;align-self:flex-end;margin-right:80px;">
    <div class="h3" style="margin-bottom:36px;color:#E1E281;">Where It Breaks</div>
    <div class="body-sm" id="vibe-b1" style="margin-bottom:20px;padding-left:24px;border-left:3px solid #E1E281;">no architectural memory</div>
    <div class="body-sm" id="vibe-b2" style="margin-bottom:20px;padding-left:24px;border-left:3px solid #E1E281;">fragile at scale</div>
    <div class="body-sm" id="vibe-b3" style="padding-left:24px;border-left:3px solid #E1E281;">hard to harden for production</div>
  </div>
</div>

<!-- 3.1 Agentic Engineering title -->
<div class="slide bg-dark" id="s3-1" data-id="3.1" data-section="3" data-section-title="Agentic Engineering" data-anim="grid-materialize" data-notes="">
  {GRID_SVG}
  <div style="position:relative;z-index:2;text-align:center;">
    <div class="h1" style="font-size:120px;">Agentic</div>
    <div class="h1 green">Engineering</div>
  </div>
</div>

<!-- 3.2 Claude Code -->
<div class="slide bg-dark" id="s3-2" data-id="3.2" data-section="3" data-anim="fade-up" data-notes="Claude Code by Anthropic is the canonical example I'll use today.">
  <img src="assets/logo-claude-code.png" alt="Claude Code" style="max-width:1100px;max-height:640px;object-fit:contain;">
</div>

<!-- 3.3 The pitch -->
<div class="slide bg-dark" id="s3-3" data-id="3.3" data-section="3" data-anim="fade-up" data-notes="">
  <div class="body center" style="max-width:1400px;font-style:italic;">Structured, autonomous workflows.<br>Plan, code, test, with minimal oversight.<br>Built for reliability and maintenance.</div>
</div>

<!-- 3.4 Transition -->
<div class="slide bg-dark" id="s3-4" data-id="3.4" data-section="3" data-anim="fade-up" data-notes="Pause here for a beat.">
  <div class="body center dim" style="font-style:italic;font-size:64px;">Let me show you what this actually looks like.</div>
</div>

<!-- 4.1 48 → 8 countdown -->
<div class="slide bg-dark" id="s4-1" data-id="4.1" data-section="4" data-section-title="Frontend Experiment" data-anim="countdown" data-notes="48-hour estimate. Built in 8. Let that land.">
  <div style="display:flex;align-items:center;gap:48px;margin-bottom:48px;">
    <span id="count-num" style="font-size:280px;font-weight:600;line-height:1;color:#E1E281;letter-spacing:-.02em;">48</span>
    <div style="display:flex;flex-direction:column;gap:0;">
      <span style="font-size:280px;font-weight:600;line-height:1;color:rgba(252,227,235,.2);">→</span>
    </div>
    <span id="count-target" style="font-size:280px;font-weight:600;line-height:1;color:#FCE3EB;opacity:.2;letter-spacing:-.02em;">8</span>
  </div>
  <div class="sub center">Frontend module. Estimated at 48 hours. Built in 8.</div>
</div>

<!-- 4.2 Screenshots carousel -->
<div class="slide bg-dark" id="s4-2" data-id="4.2" data-section="4" data-anim="carousel" data-carousel="true" data-notes="Walk through each screenshot slowly. Point out the Figma designs, then the Claude Code session, Playwright run, final output.">
  <div class="carousel">
    <div class="c-frame c-active" data-ci="0"><img class="screenshot-img" src="assets/section-4/1.png" alt=""></div>
    <div class="c-frame" data-ci="1"><img class="screenshot-img" src="assets/section-4/2.png" alt=""></div>
    <div class="c-frame" data-ci="2"><img class="screenshot-img" src="assets/section-4/3.png" alt=""></div>
    <div class="c-frame" data-ci="3"><img class="screenshot-img" src="assets/section-4/4.png" alt=""></div>
    <div class="c-frame" data-ci="4"><img class="screenshot-img" src="assets/section-4/5.png" alt=""></div>
    <div class="c-frame" data-ci="5"><img class="screenshot-img" src="assets/section-4/6.jpg" alt=""></div>
  </div>
</div>

<!-- 4.3 Stack logos -->
<div class="slide bg-dark" id="s4-3" data-id="4.3" data-section="4" data-anim="stack-logos" data-notes="The five tools that made this possible.">
  <div class="logos-row" id="stack-logos">
    <span class="logo-wm hi">Claude Code</span>
    <span class="logo-wm hi">Figma MCP</span>
    <span class="logo-wm hi">Playwright MCP</span>
    <span class="logo-wm hi">OpenAPI</span>
    <span class="logo-wm hi">BDD</span>
  </div>
</div>

<!-- 4.4 Takeaway + QR -->
<div class="slide bg-dark" id="s4-4" data-id="4.4" data-section="4" data-anim="fade-up" data-notes=""
     data-qr-url="https://www.notion.so/bobcats-coding/Frontend-development-with-Claude-Code-Opus-4-6-Figma-MCP-Playwright-MCP-OpenAPI-spec-32d1c06aab6e80ceb0a3c9872fc704dc">
  <div style="display:flex;align-items:center;gap:120px;width:100%;">
    <div style="flex:1;">
      <div class="body" style="font-style:italic;font-size:62px;">The leverage came from the spec,<br>not the typing.</div>
    </div>
    <div class="qr-wrap"><canvas class="qr-canvas" data-qr-id="qr-4-4"></canvas><div class="qr-label">AI Field Notes</div></div>
  </div>
</div>

<!-- 5.1 Title -->
<div class="slide bg-dark" id="s5-1" data-id="5.1" data-section="5" data-section-title="Version Checker" data-anim="fade-up" data-notes="">
  <div class="h2 center" style="max-width:1400px;">Small Guardrails,<br><span class="green">Compounding Returns</span></div>
</div>

<!-- 5.2 Version checker hook -->
<div class="slide bg-dark" id="s5-2" data-id="5.2" data-section="5" data-anim="fade-up" data-notes="The version checker hook intercepts the bad version. Walk through what they're seeing.">
  <div class="h3 green center" style="margin-bottom:48px;">The Version Checker Hook</div>
  <img src="assets/version-checker.gif" alt="Version checker hook" style="max-width:1500px;max-height:720px;object-fit:contain;border-radius:6px;">
</div>

<!-- 5.3 Takeaway + QR -->
<div class="slide bg-dark" id="s5-3" data-id="5.3" data-section="5" data-anim="fade-up" data-notes=""
     data-qr-url="https://www.notion.so/bobcats-coding/Version-checker-hook-Claude-Code-31b1c06aab6e809496c2de877f9b77ab">
  <div class="body center" style="max-width:1400px;font-style:italic;margin-bottom:80px;">Each small guardrail removes one<br>human-in-the-loop step. They compound.</div>
  <div class="qr-wrap"><canvas class="qr-canvas" data-qr-id="qr-5-3"></canvas><div class="qr-label">AI Field Notes</div></div>
</div>

<!-- 6.1 Story -->
<div class="slide bg-pink" id="s6-1" data-id="6.1" data-section="6" data-section-title="Quick Win" data-anim="fade-up" data-notes="Student worker doing repetitive admin tasks. An afternoon of work.">
  <div class="body center" style="max-width:1400px;font-style:italic;">We automated our student worker's process<br>into Claude slash commands.<br><span style="opacity:.6;">In an afternoon.</span></div>
</div>

<!-- 6.2 The quote -->
<div class="slide bg-pink" id="s6-2" data-id="6.2" data-section="6" data-anim="typewriter" data-notes="This is the most quotable line. Let it breathe."
     data-qr-url="https://www.notion.so/bobcats-coding/Automating-processes-with-Claude-slash-command-3501c06aab6e800b8e5cd22e57d90206">
  <div style="display:flex;align-items:center;gap:100px;width:100%;">
    <div style="flex:1;">
      <div id="tw-quote" class="h3" style="font-size:80px;font-weight:600;max-width:1100px;line-height:1.05;color:#334258;"></div>
      <div id="tw-sub" class="sub" style="color:#334258;opacity:0;margin-top:32px;">The cost of "worth automating" just collapsed.</div>
    </div>
    <div class="qr-wrap"><canvas class="qr-canvas" data-qr-id="qr-6-2"></canvas><div class="qr-label" style="color:#334258;">AI Field Notes</div></div>
  </div>
</div>

<!-- 7.1 Headline -->
<div class="slide bg-dark" id="s7-1" data-id="7.1" data-section="7" data-section-title="Bottleneck" data-anim="fade-up" data-notes="The fundamental shift.">
  <div class="h2 center" style="max-width:1600px;">Typing Is No Longer<br>The Bottleneck.<br><span class="green">Thinking Is.</span></div>
</div>

<!-- 7.2 Story + images -->
<div class="slide bg-dark" id="s7-2" data-id="7.2" data-section="7" data-anim="arch-diagram" data-notes="My colleague: Istvan Markkovari. Built it on a walk.">
  <div style="display:flex;align-items:stretch;gap:48px;width:100%;">
    <img src="assets/notion-hero.png" alt="AI Field Notes article" style="width:440px;max-height:780px;object-fit:contain;border-radius:8px;flex-shrink:0;border:1px solid rgba(225,226,129,.2);">
    <div style="flex:1;display:flex;flex-direction:column;gap:32px;justify-content:center;">
      <div class="body" style="font-style:italic;font-size:48px;line-height:1.2;">My colleague wrote an agent orchestrator while walking his dog.</div>
      <div>{ARCH_SVG.replace('width="760"','width="640"').replace('height="520"','height="438"')}</div>
    </div>
    <img src="assets/colleagues-dog.jpg" alt="The colleague's dog" style="width:380px;max-height:780px;object-fit:cover;border-radius:8px;flex-shrink:0;align-self:center;">
  </div>
</div>

<!-- 7.3 Takeaway + QR -->
<div class="slide bg-dark" id="s7-3" data-id="7.3" data-section="7" data-anim="fade-up" data-notes=""
     data-qr-url="https://www.notion.so/bobcats-coding/Typing-is-no-longer-the-bottleneck-Thinking-is-3481c06aab6e80f78daafc46d8e7155b">
  <div style="display:flex;align-items:center;gap:120px;width:100%;">
    <div style="flex:1;">
      <div class="body" style="font-style:italic;font-size:58px;">The constraint moved from output speed<br>to direction quality.</div>
    </div>
    <div class="qr-wrap"><canvas class="qr-canvas" data-qr-id="qr-7-3"></canvas><div class="qr-label">AI Field Notes</div></div>
  </div>
</div>

<!-- 8.1 Cold open -->
<div class="slide bg-dark" id="s8-1" data-id="8.1" data-section="8" data-section-title="Gastown" data-anim="fade-up" data-notes="Real story. Sets the tone for Gastown.">
  <div style="display:flex;align-items:center;gap:80px;width:100%;max-width:1700px;">
    <div style="flex:1;">
      <div class="body" style="font-style:italic;font-size:54px;">A guy got fired from Meta and<br>taught his dog to ship video games.</div>
    </div>
    <img src="assets/dog-game-arch.webp" alt="Dog game architecture" style="flex:1;max-width:780px;max-height:680px;object-fit:contain;border-radius:6px;">
  </div>
  <div class="footnote">calebleak.com/posts/dog-game</div>
</div>

<!-- 8.2 Gastown full-bleed -->
<div class="slide" id="s8-2" data-id="8.2" data-section="8" data-anim="kenburns" data-notes="Let the image breathe. Big headline."
     data-qr-url="https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04"
     style="--slide-bg:#334258;padding:0;">
  <div class="full-bleed">
    <img id="gastown-img" src="assets/gastown.webp" alt="Gastown">
    <div class="full-bleed-overlay"></div>
  </div>
  <div class="full-bleed-content">
    <div style="display:flex;align-items:flex-end;justify-content:space-between;gap:64px;width:100%;">
      <div class="h1" style="font-size:200px;line-height:.85;">GASTOWN</div>
      <div class="qr-wrap"><canvas class="qr-canvas" data-qr-id="qr-8-2" data-qr-bg="#ffffff"></canvas><div class="qr-label" style="color:#ffffff;">Steve Yegge essay</div></div>
    </div>
  </div>
</div>

<!-- 8.4 Takeaway -->
<div class="slide bg-dark" id="s8-4" data-id="8.4" data-section="8" data-anim="fade-up" data-notes="The real engineering problem of the next five years.">
  <div class="body center" style="max-width:1500px;font-style:italic;">Agents are non-deterministic.<br>The architecture problem of the next five years<br>is <span class="green">orchestration</span>, not generation.</div>
</div>

<!-- 9.1 The equation changed -->
<div class="slide bg-dark" id="s9-1" data-id="9.1" data-section="9" data-section-title="Rethink" data-anim="fade-up" data-notes="Quiet. Confident. Let it land.">
  <div class="h1 center" style="font-size:160px;color:#E1E281;">The Equation<br>Changed.</div>
</div>

<!-- 9.2 Code cheap judgment expensive -->
<div class="slide bg-dark" id="s9-2" data-id="9.2" data-section="9" data-anim="fade-up" data-notes="">
  <div style="display:flex;gap:80px;align-items:center;justify-content:center;">
    <div style="text-align:center;padding:60px 80px;border:2px solid rgba(225,226,129,.3);border-radius:6px;">
      <div class="body-sm dim" style="margin-bottom:16px;text-transform:uppercase;letter-spacing:.12em;">Code</div>
      <div class="h2 green">Cheap</div>
    </div>
    <div class="h2 dim" style="font-size:80px;">·</div>
    <div style="text-align:center;padding:60px 80px;border:2px solid rgba(252,227,235,.2);border-radius:6px;">
      <div class="body-sm dim" style="margin-bottom:16px;text-transform:uppercase;letter-spacing:.12em;">Judgment</div>
      <div class="h2" style="color:#F9C7D8;">Expensive</div>
    </div>
  </div>
</div>

<!-- 9.3 Pillar 1 -->
<div class="slide bg-dark" id="s9-3" data-id="9.3" data-section="9" data-anim="pillar-rise" data-notes="">
  <div class="pillar" id="p9-3" style="max-width:1400px;border-top:3px solid #E1E281;padding:52px 0;">
    <div class="p-num" style="font-size:48px;font-weight:600;color:#E1E281;letter-spacing:.12em;opacity:.6;margin-bottom:28px;">01</div>
    <div class="h2" style="margin-bottom:24px;">Specification<br>Is the New Code.</div>
    <div class="sub">Spec quality determines output quality.</div>
  </div>
</div>

<!-- 9.4 Pillar 2 -->
<div class="slide bg-dark" id="s9-4" data-id="9.4" data-section="9" data-anim="pillar-rise" data-notes="">
  <div class="pillar" id="p9-4" style="max-width:1400px;border-top:3px solid #E1E281;padding:52px 0;">
    <div class="p-num" style="font-size:48px;font-weight:600;color:#E1E281;letter-spacing:.12em;opacity:.6;margin-bottom:28px;">02</div>
    <div class="h2" style="margin-bottom:24px;">Senior Engineers<br>Become Leverage,<br><span class="green">Not Bottlenecks.</span></div>
    <div class="sub">They direct fleets of agents.</div>
  </div>
</div>

<!-- 9.5 Pillar 3 -->
<div class="slide bg-dark" id="s9-5" data-id="9.5" data-section="9" data-anim="pillar-rise" data-notes=""
     data-qr-url="https://www.bobcatscoding.com/ai-native-team-augmentation">
  <div style="display:flex;align-items:center;gap:120px;width:100%;">
    <div class="pillar" id="p9-5" style="flex:1;max-width:1400px;border-top:3px solid #E1E281;padding:52px 0;">
      <div class="p-num" style="font-size:48px;font-weight:600;color:#E1E281;letter-spacing:.12em;opacity:.6;margin-bottom:28px;">03</div>
      <div class="h2" style="margin-bottom:24px;">Hire AI-Native<br>Developers as<br><span class="green">Team Augmentation.</span></div>
      <div class="sub">Faster and cheaper than retraining.</div>
    </div>
    <div class="qr-wrap"><canvas class="qr-canvas" data-qr-id="qr-9-5"></canvas><div class="qr-label">Bobcats Coding</div></div>
  </div>
</div>

<!-- 10.1 -->
<div class="slide bg-dark" id="s10-1" data-id="10.1" data-section="10" data-section-title="Conclusions" data-anim="kinetic" data-notes="">
  <div class="h2 center kinetic-container" style="max-width:1600px;" id="kt-10-1">AI changes how software is built.<br>Not whether developers exist.</div>
</div>

<!-- 10.2 -->
<div class="slide bg-dark" id="s10-2" data-id="10.2" data-section="10" data-anim="kinetic" data-notes="">
  <div class="h2 center kinetic-container" style="max-width:1600px;" id="kt-10-2">Specify <span class="green">→</span> Build <span class="green">→</span> Analyze.<br><br><span style="display:inline-block;margin-top:48px;">Document your experiments.</span></div>
</div>

<!-- 10.4 Q&A hold frame -->
<div class="slide bg-dark" id="s10-4" data-id="10.4" data-section="10" data-anim="qr-fade" data-notes="Hold here for Q&A. Stay on this slide for 20 minutes."
     data-qr-url="https://www.notion.so/bobcats-coding/Welcome-To-AI-Field-Notes-2f11c06aab6e8145a180d3e7d80aee84">
  <div id="hold-frame" style="display:flex;flex-direction:column;align-items:center;gap:56px;">
    <img src="assets/bobcats-logo.png" alt="Bobcats Coding" style="height:160px;object-fit:contain;filter:brightness(1.1);">
    <div class="h3 green center" style="letter-spacing:.15em;">AI Field Notes</div>
    <div class="qr-wrap"><canvas class="qr-canvas" data-qr-id="qr-10-4" style="width:280px;height:280px;"></canvas><div class="qr-label">Scan to subscribe</div></div>
    <div class="body-sm dim center" style="font-size:34px;">Questions? Let's talk.</div>
  </div>
</div>

<!-- 10.5 Link to this presentation -->
<div class="slide bg-dark" id="s10-5" data-id="10.5" data-section="10" data-anim="qr-fade" data-notes="Final slide — share the deck."
     data-qr-url="https://kondfox.github.io/presentations/20260430_Community_Breakfast/">
  <div class="hold-frame-link" style="display:flex;flex-direction:column;align-items:center;gap:56px;">
    <img src="assets/bobcats-logo.png" alt="Bobcats Coding" style="height:160px;object-fit:contain;filter:brightness(1.1);">
    <div class="h3 green center" style="letter-spacing:.15em;">Link to this presentation</div>
    <div class="qr-wrap"><canvas class="qr-canvas" data-qr-id="qr-10-5" style="width:280px;height:280px;"></canvas><div class="qr-label">Scan to open</div></div>
  </div>
</div>
"""

# ── JavaScript ────────────────────────────────────────────────────────────────
JS = r"""
(function() {
'use strict';
gsap.registerPlugin(TextPlugin);

// ── Slide data ──────────────────────────────────────────────────────────────
const SLIDE_ELS = Array.from(document.querySelectorAll('.slide'));
const TOTAL = SLIDE_ELS.length;

// Sections: [ {section, title, start, end} ]
const SECTIONS = [];
let curSec = null;
SLIDE_ELS.forEach((el, i) => {
  const s = parseInt(el.dataset.section);
  const t = el.dataset.sectionTitle;
  if (!curSec || curSec.section !== s) {
    if (curSec) curSec.end = i - 1;
    curSec = { section: s, title: t || curSec?.title || '', start: i };
    SECTIONS.push(curSec);
  }
});
if (curSec) curSec.end = TOTAL - 1;

// Carousel state
let carouselIndex = 0;
function getCarouselFrames(el) { return Array.from(el.querySelectorAll('.c-frame')); }

// ── State ───────────────────────────────────────────────────────────────────
let current = 0;
let overviewOpen = false;
let blackoutOn = false;
let mouseMoveTimer = null;

// ── Letterbox ───────────────────────────────────────────────────────────────
const deck = document.getElementById('deck');
function letterbox() {
  const vw = window.innerWidth, vh = window.innerHeight;
  const scale = Math.min(vw / 1920, vh / 1080);
  const ox = (vw - 1920 * scale) / 2;
  const oy = (vh - 1080 * scale) / 2;
  deck.style.transform = `translate(${ox}px,${oy}px) scale(${scale})`;
}
window.addEventListener('resize', letterbox);
letterbox();

// ── Navigation ──────────────────────────────────────────────────────────────
function goTo(idx, skipAnim) {
  if (idx < 0 || idx >= TOTAL) return;
  const from = SLIDE_ELS[current];
  const to   = SLIDE_ELS[idx];
  const crossSection = from.dataset.section !== to.dataset.section;
  const dur = crossSection ? 0.4 : 0.22;

  // Stop vibe video if leaving slide 2.1
  const vibeVid = document.getElementById('vibe-video');
  if (from.dataset.id === '2.1' && vibeVid) vibeVid.pause();

  gsap.to(from, { opacity: 0, duration: dur, ease: 'power2.inOut', onComplete: () => from.classList.remove('visible') });
  // Stage the new slide invisible, run its child animations while still hidden, then fade in.
  // This avoids a flash where children would briefly appear at full opacity before gsap.from() snaps them to 0.
  gsap.set(to, { opacity: 0 });
  to.classList.add('visible');
  if (!skipAnim) runAnim(to, idx);
  gsap.to(to, { opacity: 1, duration: dur, ease: 'power2.inOut', onComplete: () => {
    if (to.dataset.id === '2.1' && vibeVid) { vibeVid.currentTime = 0; vibeVid.play().catch(()=>{}); }
    if (to.dataset.id !== '2.1' && vibeVid) vibeVid.pause();
  }});

  current = idx;
  carouselIndex = 0;
  if (to.dataset.carousel) updateCarouselDisplay(to);
  updateUI();
  broadcastState();
}

function next() {
  const el = SLIDE_ELS[current];
  if (el.dataset.carousel) {
    const frames = getCarouselFrames(el);
    if (carouselIndex < frames.length - 1) { carouselIndex++; updateCarouselDisplay(el); return; }
  }
  goTo(current + 1);
}
function prev() {
  const el = SLIDE_ELS[current];
  if (el.dataset.carousel && carouselIndex > 0) { carouselIndex--; updateCarouselDisplay(el); return; }
  goTo(current - 1);
}

function updateCarouselDisplay(el) {
  const frames = getCarouselFrames(el);
  frames.forEach((f, i) => {
    if (i === carouselIndex) {
      f.classList.add('c-active');
      gsap.fromTo(f, { opacity: 0 }, { opacity: 1, duration: 0.22 });
    } else {
      if (f.classList.contains('c-active')) {
        gsap.to(f, { opacity: 0, duration: 0.22, onComplete: () => f.classList.remove('c-active') });
      }
    }
  });
  const counter = el.querySelector('.c-counter');
  if (counter) counter.textContent = `${String(carouselIndex+1).padStart(2,'0')} / ${String(frames.length).padStart(2,'0')}`;
}

// ── UI ───────────────────────────────────────────────────────────────────────
const progressBar = document.getElementById('progress');
const counterEl   = document.getElementById('counter');
const ticksEl     = document.getElementById('ticks');

function updateUI() {
  const pct = TOTAL > 1 ? (current / (TOTAL - 1)) * 100 : 0;
  progressBar.style.width = pct + '%';

  // Section info
  const secObj = SECTIONS.find(s => current >= s.start && current <= s.end);
  const slideInSec = current - (secObj ? secObj.start : 0) + 1;
  const secLen = secObj ? (secObj.end - secObj.start + 1) : 1;
  const secTotal = secObj ? (secObj.end - secObj.start + 1) : 1;
  counterEl.textContent = `Section ${secObj?.section || 1}  ·  ${String(slideInSec).padStart(2,'0')} / ${String(secTotal).padStart(2,'0')}`;


  // Overview highlight
  document.querySelectorAll('.ov-thumb').forEach((t, i) => t.classList.toggle('cur', i === current));
}

// Draw section ticks
function buildTicks() {
  SECTIONS.forEach(sec => {
    if (sec.start === 0) return;
    const pct = (sec.start / (TOTAL - 1)) * 100;
    const tick = document.createElement('div');
    tick.className = 's-tick';
    tick.style.left = pct + '%';
    tick.style.height = '10px';
    ticksEl.appendChild(tick);
  });
}

// ── Overview grid ────────────────────────────────────────────────────────────
const overview = document.getElementById('overview');
const ovGrid   = document.getElementById('ov-grid');

function buildOverview() {
  SLIDE_ELS.forEach((el, i) => {
    const wrap = document.createElement('div');
    wrap.className = 'ov-thumb';
    wrap.title = el.dataset.id;
    const inner = document.createElement('div');
    inner.className = 'ov-inner';
    // Clone slide for thumbnail
    const clone = el.cloneNode(true);
    clone.style.display = 'flex';
    clone.style.opacity = '1';
    clone.style.position = 'absolute';
    clone.style.top = '0'; clone.style.left = '0';
    // make all dep-nodes visible in thumb
    clone.querySelectorAll('.dep-node').forEach(n => n.style.opacity='1');
    clone.querySelectorAll('.dep-edge').forEach(e => e.style.strokeDashoffset='0');
    inner.appendChild(clone);
    const label = document.createElement('div');
    label.className = 'ov-label';
    label.textContent = el.dataset.id + (el.dataset.sectionTitle ? '  ' + el.dataset.sectionTitle : '');
    wrap.appendChild(inner);
    wrap.appendChild(label);
    wrap.addEventListener('click', () => { toggleOverview(false); goTo(i); });
    ovGrid.appendChild(wrap);
  });
}

function toggleOverview(force) {
  overviewOpen = (force !== undefined) ? force : !overviewOpen;
  overview.classList.toggle('open', overviewOpen);
  updateUI();
}

// ── Blackout ─────────────────────────────────────────────────────────────────
const blackoutEl = document.getElementById('blackout');
function toggleBlackout() {
  blackoutOn = !blackoutOn;
  blackoutEl.classList.toggle('on', blackoutOn);
}

// ── Presenter mode ───────────────────────────────────────────────────────────
let presWin = null;
const bc = (typeof BroadcastChannel !== 'undefined') ? new BroadcastChannel('slides') : null;
function broadcastState() {
  if (bc) bc.postMessage({ type: 'nav', index: current, total: TOTAL, slideId: SLIDE_ELS[current]?.dataset.id, notes: SLIDE_ELS[current]?.dataset.notes || '' });
}
function openPresenter() {
  if (presWin && !presWin.closed) { presWin.focus(); return; }
  presWin = window.open(location.href + (location.href.includes('?') ? '&' : '?') + 'mode=presenter', 'presenter', 'width=1280,height=800');
}

// ── Presenter window logic ───────────────────────────────────────────────────
if (new URLSearchParams(location.search).get('mode') === 'presenter') {
  document.body.innerHTML = `<div style="background:#0d0d0d;color:#FCE3EB;font-family:Bai Jamjuree,sans-serif;height:100vh;display:flex;flex-direction:column;padding:32px;gap:24px;">
    <div style="font-size:18px;letter-spacing:.1em;text-transform:uppercase;color:rgba(255,255,255,.3);margin-bottom:8px;">Presenter View</div>
    <div style="display:flex;gap:24px;flex:1;min-height:0;">
      <div style="flex:2;display:flex;flex-direction:column;gap:16px;">
        <div style="background:#1a2336;border-radius:6px;padding:20px;flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;">
          <div style="font-size:13px;color:#E1E281;letter-spacing:.1em;margin-bottom:12px;">CURRENT</div>
          <div id="p-current" style="font-size:28px;font-weight:600;text-align:center;"></div>
          <div id="p-id" style="font-size:18px;color:#E1E281;margin-top:8px;"></div>
        </div>
        <div style="background:#111;border-radius:6px;padding:20px;">
          <div style="font-size:13px;color:rgba(255,255,255,.3);letter-spacing:.1em;margin-bottom:10px;">NOTES</div>
          <div id="p-notes" style="font-size:18px;line-height:1.5;"></div>
        </div>
      </div>
      <div style="flex:1;display:flex;flex-direction:column;gap:16px;">
        <div style="background:#0a1420;border-radius:6px;padding:20px;flex:1;">
          <div style="font-size:13px;color:rgba(255,255,255,.3);letter-spacing:.1em;margin-bottom:12px;">NEXT</div>
          <div id="p-next" style="font-size:22px;"></div>
        </div>
        <div style="background:#0a1420;border-radius:6px;padding:16px;text-align:center;">
          <div style="font-size:13px;color:rgba(255,255,255,.3);letter-spacing:.1em;margin-bottom:8px;">TIMER</div>
          <div id="p-timer" style="font-size:40px;font-weight:600;color:#E1E281;font-family:monospace;">00:00</div>
        </div>
        <div style="background:#0a1420;border-radius:6px;padding:16px;text-align:center;">
          <div id="p-progress" style="font-size:22px;color:#E1E281;"></div>
        </div>
      </div>
    </div>
  </div>`;
  // Timer
  const startTime = Date.now();
  const SLIDES_DATA = [];
  setInterval(() => {
    const s = Math.floor((Date.now() - startTime) / 1000);
    const m = Math.floor(s / 60).toString().padStart(2,'0');
    const sec = (s % 60).toString().padStart(2,'0');
    document.getElementById('p-timer').textContent = m + ':' + sec;
  }, 1000);
  if (bc) bc.onmessage = (e) => {
    if (e.data.type !== 'nav') return;
    document.getElementById('p-current').textContent = 'Slide ' + e.data.slideId;
    document.getElementById('p-id').textContent = e.data.index + 1 + ' / ' + e.data.total;
    document.getElementById('p-notes').textContent = e.data.notes || '—';
    document.getElementById('p-progress').textContent = e.data.index + 1 + ' / ' + e.data.total;
  };
  return; // stop rest of init for presenter window
}

// ── Fullscreen ───────────────────────────────────────────────────────────────
function toggleFullscreen() {
  if (!document.fullscreenElement) {
    (document.documentElement.requestFullscreen?.() || Promise.reject()).catch(()=>{});
  } else {
    document.exitFullscreen?.();
  }
}

// ── Keyboard ─────────────────────────────────────────────────────────────────
document.addEventListener('keydown', (e) => {
  if (blackoutOn && e.key !== 'b' && e.key !== 'B') return;
  switch (e.key) {
    case 'ArrowRight': case ' ': case 'PageDown': e.preventDefault(); overviewOpen ? null : next(); break;
    case 'ArrowLeft':  case 'PageUp':             e.preventDefault(); overviewOpen ? null : prev(); break;
    case 'Escape': toggleOverview(); break;
    case 'b': case 'B': toggleBlackout(); break;
    case 'p': case 'P': openPresenter(); break;
    case 'f': case 'F': toggleFullscreen(); break;
  }
});

// ── Mouse cursor ─────────────────────────────────────────────────────────────
document.addEventListener('mousemove', () => {
  document.body.style.cursor = 'default';
  clearTimeout(mouseMoveTimer);
  mouseMoveTimer = setTimeout(() => { document.body.style.cursor = 'none'; }, 2000);
});

// ── Touch navigation (mobile) ────────────────────────────────────────────────
// Swipe horizontally to change slide; tap left/right half also navigates.
let touchStartX = 0, touchStartY = 0, touchStartT = 0;
document.addEventListener('touchstart', (e) => {
  if (e.touches.length !== 1) return;
  touchStartX = e.touches[0].clientX;
  touchStartY = e.touches[0].clientY;
  touchStartT = Date.now();
}, { passive: true });
document.addEventListener('touchend', (e) => {
  if (blackoutOn || overviewOpen) return;
  const t = e.changedTouches[0];
  if (!t) return;
  const dx = t.clientX - touchStartX;
  const dy = t.clientY - touchStartY;
  const adx = Math.abs(dx), ady = Math.abs(dy);
  const dt = Date.now() - touchStartT;
  // Horizontal swipe
  if (adx > 50 && adx > ady * 1.5 && dt < 800) {
    if (dx < 0) next(); else prev();
    return;
  }
  // Quick tap: left half = prev, right half = next
  if (adx < 10 && ady < 10 && dt < 400) {
    if (t.clientX > window.innerWidth / 2) next(); else prev();
  }
}, { passive: true });

// ── QR codes ─────────────────────────────────────────────────────────────────
function makeQR(canvas, url) {
  try {
    const qr = qrcode(0, 'H');
    qr.addData(url);
    qr.make();
    const size = canvas.dataset.qrId === 'qr-10-4' ? 280 : 200;
    canvas.width = size; canvas.height = size;
    const ctx = canvas.getContext('2d');
    const cells = qr.getModuleCount();
    const cellSize = size / cells;
    const bg = canvas.dataset.qrBg || '#FCE3EB';
    const fg = canvas.dataset.qrFg || '#334258';
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, size, size);
    ctx.fillStyle = fg;
    for (let r = 0; r < cells; r++) {
      for (let c = 0; c < cells; c++) {
        if (qr.isDark(r, c)) ctx.fillRect(c * cellSize, r * cellSize, cellSize, cellSize);
      }
    }
  } catch(e) { console.warn('QR failed', e); }
}

function initQRCodes() {
  // Each slide with data-qr-url gets a canvas
  document.querySelectorAll('[data-qr-url]').forEach(slide => {
    const url = slide.dataset.qrUrl;
    if (!url) return;
    const canvas = slide.querySelector('.qr-canvas');
    if (canvas) makeQR(canvas, url);
  });
}

// ── Animations ───────────────────────────────────────────────────────────────
const ANIMS = {
  'hand': (el) => {
    const svg = el.querySelector('svg');
    if (!svg) return;
    gsap.killTweensOf(svg);
    gsap.set(svg, { transformOrigin: '50% 95%' });
    gsap.from(svg, { scale: 0.75, opacity: 0, duration: 0.6, ease: 'back.out(1.4)' });
    // Looping gentle wave
    gsap.to(svg, { rotation: 8, duration: 1.1, repeat: -1, yoyo: true, ease: 'sine.inOut', delay: 0.6 });
  },
  'vibe-title': (el) => {
    const title = el.querySelector('#vibe-title-text');
    if (title) glitchText(title, 'VIBE CODING');
    gsap.from(el.querySelector('.slide-video') || el.querySelector('video'), { opacity: 0, y: 30, duration: 0.5, delay: 0.3 });
    gsap.from(el.querySelectorAll('.logo-wm, .logo-box'), { opacity: 0, y: 20, stagger: 0.08, duration: 0.4, delay: 0.6 });
  },
  'vibe-bullets': (el) => {
    ['#vibe-b1','#vibe-b2','#vibe-b3'].forEach((id, i) => {
      const node = el.querySelector(id);
      if (node) gsap.from(node, { opacity: 0, x: -20, duration: 0.35, delay: i * 0.12 });
    });
  },
  'grid-materialize': (el) => {
    const lines = el.querySelectorAll('.grid-line');
    gsap.fromTo(lines, { strokeDashoffset: 600, opacity: 0 }, { strokeDashoffset: 0, opacity: 0.5, stagger: 0.08, duration: 0.8, ease: 'power2.out' });
    const circles = el.querySelectorAll('circle.grid-line');
    gsap.to(circles, { opacity: 1, stagger: 0.06, duration: 0.4, delay: 0.7 });
    gsap.from(el.querySelectorAll('.h1'), { opacity: 0, y: 20, stagger: 0.1, duration: 0.5, delay: 0.9 });
  },
  'countdown': (el) => {
    const numEl = el.querySelector('#count-num');
    const targetEl = el.querySelector('#count-target');
    if (!numEl) return;
    // First: show 48, arrow, dim 8
    gsap.from(numEl, { opacity: 0, scale: 1.2, duration: 0.4 });
    // After 0.8s start counting down
    const counter = { val: 48 };
    gsap.to(counter, { val: 8, duration: 1.6, delay: 0.8, ease: 'power2.inOut', snap: { val: 1 },
      onUpdate: () => { numEl.textContent = Math.round(counter.val); },
      onComplete: () => {
        numEl.style.color = '#E1E281';
        if (targetEl) gsap.to(targetEl, { opacity: 1, color: '#E1E281', duration: 0.3 });
      }
    });
    gsap.from(el.querySelector('.sub'), { opacity: 0, y: 20, duration: 0.4, delay: 2.6 });
  },
  'carousel': (el) => {
    carouselIndex = 0;
    updateCarouselDisplay(el);
  },
  'stack-logos': (el) => {
    const logos = el.querySelectorAll('.logo-wm');
    gsap.from(logos, { opacity: 0, x: -30, stagger: 0.1, duration: 0.4, ease: 'power2.out' });
  },
  'dep-tree': (el) => {
    // kill any existing tween on dep elements
    gsap.killTweensOf(['#dn-project','#dn-api','#dn-lodash','#dn-utils','#de-pa','#de-pl','#de-au','#hook-box','#lodash-bg']);
    // reset
    gsap.set(['#dn-project','#dn-api','#dn-lodash','#dn-utils','#hook-box'], { opacity: 0 });
    gsap.set(['#de-pa','#de-pl','#de-au'], { strokeDashoffset: 900 });
    gsap.set('#lodash-bg', { opacity: 0, attr: { stroke: 'rgba(252,227,235,.4)', fill: '#1a2a3d' } });
    const tl = gsap.timeline({ delay: 0.3 });
    tl.to('#dn-project', { opacity: 1, duration: 0.3 })
      .to('#de-pa', { strokeDashoffset: 0, duration: 0.55, ease: 'power2.inOut' })
      .to('#dn-api', { opacity: 1, duration: 0.3 }, '-=0.1')
      .to('#de-pl', { strokeDashoffset: 0, duration: 0.55, ease: 'power2.inOut' }, '-=0.5')
      .to('#dn-lodash', { opacity: 1, duration: 0.3 }, '-=0.1')
      .to('#de-au', { strokeDashoffset: 0, duration: 0.4, ease: 'power2.inOut' })
      .to('#dn-utils', { opacity: 1, duration: 0.3 }, '-=0.1')
      .to('#lodash-bg', { opacity: 1, attr: { stroke: '#cc3333', fill: '#1a0d0d' }, duration: 0.4 }, '+=0.5')
      .to('#hook-box', { opacity: 1, duration: 0.4 }, '+=0.4')
      .to('#lodash-bg', { attr: { stroke: '#E1E281', fill: '#0d1a0d' }, duration: 0.55 }, '+=0.6');
  },
  'typewriter': (el) => {
    const q = el.querySelector('#tw-quote');
    const sub = el.querySelector('#tw-sub');
    if (!q) return;
    const text = "Yesterday's 'not worth it'\nis today's quick win.";
    q.textContent = '';
    let i = 0;
    const iv = setInterval(() => {
      if (i < text.length) { q.textContent += text[i++]; }
      else { clearInterval(iv); if (sub) gsap.to(sub, { opacity: 0.65, duration: 0.6, delay: 0.5 }); }
    }, 38);
  },
  'arch-diagram': (el) => {
    gsap.from(Array.from(el.children), { opacity: 0, y: 20, stagger: 0.12, duration: 0.5 });
    const svg = el.querySelector('svg');
    if (svg) gsap.from(svg.querySelectorAll('rect,line,text'), { opacity: 0, stagger: 0.03, duration: 0.25, delay: 0.5 });
  },
  'kenburns': (el) => {
    const img = el.querySelector('#gastown-img');
    if (!img) return;
    gsap.from(el.querySelector('.h1'), { opacity: 0, y: 30, duration: 0.7, delay: 0.4 });
    gsap.set(img, { transformOrigin: '50% 50%' });
    gsap.fromTo(img, { scale: 1, x: 0, y: 0 }, { scale: 1.08, x: -18, y: -12, duration: 30, ease: 'none' });
  },
  'pillar-rise': (el) => {
    const p = el.querySelector('[id^="p9-"]') || el.querySelector('.pillar');
    if (p) gsap.from(p, { y: 60, opacity: 0, duration: 0.55, ease: 'power2.out' });
  },
  'kinetic': (el) => {
    const container = el.querySelector('.kinetic-container, .h2');
    if (!container) return;
    gsap.from(container, { opacity: 0, y: 24, duration: 0.5, ease: 'power2.out' });
  },
  'qr-fade': (el) => {
    const hf = el.querySelector('#hold-frame, .hold-frame-link');
    if (hf) gsap.from(hf.children, { opacity: 0, y: 20, stagger: 0.1, duration: 0.6, ease: 'power2.out' });
  },
  'fade-up': (el) => {
    const children = el.children;
    gsap.from(children, { opacity: 0, y: 22, duration: 0.45, ease: 'power2.out', stagger: 0.06 });
  },
};

function runAnim(el, idx) {
  const key = el.dataset.anim || 'fade-up';
  const fn = ANIMS[key];
  if (fn) fn(el);
}

// ── Glitch text helper ───────────────────────────────────────────────────────
function glitchText(el, original) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#@!$%';
  let frame = 0;
  const nonSpace = original.replace(/ /g, '').length;
  const totalFrames = nonSpace * 3;
  const iv = setInterval(() => {
    let charsSeen = 0;
    el.textContent = original.split('').map(c => {
      if (c === ' ') return ' ';
      const done = frame > charsSeen * 3;
      charsSeen++;
      return done ? c : chars[Math.floor(Math.random() * chars.length)];
    }).join('');
    frame++;
    if (frame >= totalFrames) { el.textContent = original; clearInterval(iv); }
  }, 40);
}

// ── Init ─────────────────────────────────────────────────────────────────────
buildTicks();
buildOverview();
initQRCodes();

// Show first slide — stage children invisibly, then fade in together.
SLIDE_ELS[0].classList.add('visible');
runAnim(SLIDE_ELS[0], 0);
gsap.to(SLIDE_ELS[0], { opacity: 1, duration: 0.5 });
updateUI();
broadcastState();

})();
"""

# ── Assemble ──────────────────────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Cheaper code, guided by more expensive engineers — Bobcats Coding</title>
<style>{CSS}</style>
</head>
<body>
<div id="deck-wrapper">
  <div id="deck">
    <div id="slides-container">
{SLIDES_HTML}
    </div>
    <div id="progress"></div>
    <div id="ticks"></div>
    <div id="counter"></div>
  </div>
</div>
<div id="overview"><div id="ov-grid"></div></div>
<div id="blackout"></div>
<script>{gsap_js}</script>
<script>{tp_js}</script>
<script>{qr_js}</script>
<script>{JS}</script>
</body>
</html>"""

out = BASE + '/index.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(HTML)
print(f'Generated {out} ({len(HTML)//1024}KB)')
