import base64
import io
import json

import streamlit as st
import streamlit.components.v1 as components
from rdkit import Chem
from rdkit.Chem import Draw, rdDepictor

from acid_data import WATER_ACIDS, DMSO_ACIDS, CORE_25_IDS, EXTENDED_50_IDS

st.set_page_config(
    page_title="Acid Battle",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
header[data-testid="stHeader"]{background:transparent;height:0}
[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none!important}
.block-container{padding:0!important;max-width:none!important}
iframe{border:0!important}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def molecule_png_data_uri(smiles: str | None) -> str | None:
    if not smiles:
        return None
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        rdDepictor.Compute2DCoords(mol)
        img = Draw.MolToImage(mol, size=(430, 260), kekulize=True)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
    except Exception:
        return None


def prepared_acids(rows):
    out = []
    for index, row in enumerate(rows):
        item = dict(row)
        item["image"] = molecule_png_data_uri(row.get("smiles"))
        item["instance_order"] = index
        item["pka_sort"] = -100.0 if row.get("pka") is None else float(row["pka"])
        out.append(item)
    return out


WATER = prepared_acids(WATER_ACIDS)
DMSO = prepared_acids(DMSO_ACIDS)


HTML = r'''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no">
<style>
:root{
  --ink:#e4eef4;--muted:#8da5b5;--blue:#78c7ff;--deep:#07111a;--panel:#142635;
  --line:#405c70;--cream:#fffaf0;--cream2:#f0e5c9;--good:#72e49a;--bad:#ff7c7c;
  --gold:#ffd36a;--felt:#19453f;--felt2:#0f312e;--cpu:#90aabb;--player:#68b5e7;
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;min-height:100%;background:#07111a;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Arial,sans-serif;overflow-x:hidden}
body{background-image:radial-gradient(circle at 50% -10%,#18364c 0,transparent 42%),linear-gradient(180deg,#08131d 0,#07111a 48%,#050c12 100%)}
button{font:inherit}
#app{min-height:100vh;padding:12px max(12px,env(safe-area-inset-right)) calc(18px + env(safe-area-inset-bottom)) max(12px,env(safe-area-inset-left));max-width:1320px;margin:auto}
.topbar{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:11px}.brand{display:flex;align-items:center;gap:11px}.brandmark{width:43px;height:43px;border-radius:12px;background:linear-gradient(145deg,#e7edf0,#8396a4);border:2px solid #536b7b;box-shadow:inset 0 0 0 3px rgba(255,255,255,.14),0 7px 18px rgba(0,0,0,.35);display:grid;place-items:center;font-size:23px}.brand h1{font-size:23px;line-height:1;margin:0;font-weight:950;letter-spacing:.025em}.brand small{display:block;color:var(--muted);font-weight:700;margin-top:4px}.top-actions{display:flex;align-items:center;gap:8px}.ghost{border:1px solid #4c687b;background:#132431;color:#dce9f2;border-radius:11px;padding:10px 13px;font-weight:850;cursor:pointer;min-height:44px}.ghost:hover{filter:brightness(1.1)}.sound-btn{min-width:108px}.sound-btn.muted{color:#8ca0ad;background:#0c1a23}.sound-icon{display:inline-block;min-width:18px;text-align:center}
.machine{position:relative;border:2px solid #3d586b;border-radius:24px;background:linear-gradient(180deg,rgba(25,46,61,.96),rgba(10,24,34,.98));box-shadow:inset 0 0 0 1px rgba(255,255,255,.04),0 20px 46px rgba(0,0,0,.42);overflow:hidden}.machine:before{content:"";position:absolute;inset:0;pointer-events:none;opacity:.20;background-image:linear-gradient(45deg,rgba(255,255,255,.05) 25%,transparent 25%,transparent 75%,rgba(255,255,255,.05) 75%),linear-gradient(45deg,rgba(255,255,255,.05) 25%,transparent 25%,transparent 75%,rgba(255,255,255,.05) 75%);background-size:38px 38px;background-position:0 0,19px 19px}.rivets{position:absolute;inset:8px;pointer-events:none;border:1px solid rgba(147,174,192,.14);border-radius:18px}
.setup{padding:clamp(20px,4vw,48px);position:relative;z-index:2}.setup-grid{display:grid;grid-template-columns:1.05fr .95fr;gap:28px;align-items:center}.hero-kicker{color:var(--gold);font-size:12px;letter-spacing:.18em;font-weight:950;text-transform:uppercase}.hero-title{font-size:clamp(38px,6vw,72px);font-weight:1000;line-height:.93;letter-spacing:-.045em;margin:8px 0 14px;text-shadow:0 5px 22px rgba(0,0,0,.3)}.hero-copy{color:#a9bdca;font-size:clamp(15px,2vw,19px);line-height:1.45;max-width:650px}.rule-chip{display:inline-flex;gap:8px;align-items:center;margin-top:18px;padding:9px 12px;border:1px solid #466477;border-radius:999px;background:#0e202d;color:#bcd2df;font-size:13px;font-weight:800}.rule-chip b{color:white}
.console{padding:17px;border-radius:19px;background:linear-gradient(180deg,#d9e0e4,#8597a3);border:3px solid #4f6878;box-shadow:inset 0 0 0 3px rgba(255,255,255,.13),0 14px 25px rgba(0,0,0,.35);color:#102331}.screen{border-radius:13px;background:#091a24;border:2px solid #486271;box-shadow:inset 0 0 18px rgba(93,198,255,.07);padding:17px;color:#d9edf8}.screen-title{font-size:12px;letter-spacing:.12em;text-transform:uppercase;font-weight:950;color:#7cb9dc;margin:2px 0 10px}.choice-row{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}.choice-row.three{grid-template-columns:repeat(3,1fr)}.select-btn{position:relative;border:1px solid #3e6277;background:#102b3b;color:#cbe5f2;border-radius:12px;padding:13px 9px;min-height:58px;font-size:14px;font-weight:950;cursor:pointer;box-shadow:inset 0 -3px 0 rgba(0,0,0,.17)}.select-btn.active{background:#d7edf9;color:#0a293a;border-color:#99d9ff;box-shadow:0 0 0 3px rgba(120,199,255,.15),inset 0 -3px 0 rgba(0,0,0,.10)}.select-btn.disabled{opacity:.42;cursor:not-allowed}.select-btn span{display:block;font-size:10px;font-weight:800;opacity:.72;margin-top:4px}.separator{height:1px;background:#345268;margin:15px 0}.start{width:100%;margin-top:16px;border:2px solid #915d12;background:linear-gradient(180deg,#ffe297,#dfa938);color:#352308;border-radius:14px;padding:15px;font-size:16px;font-weight:1000;letter-spacing:.04em;cursor:pointer;box-shadow:inset 0 0 0 3px rgba(255,255,255,.23),0 8px 15px rgba(0,0,0,.25)}.pool-note{margin-top:10px;color:#8fb0c3;font-size:11px;line-height:1.4}
.battle{display:none;position:relative;z-index:2}.hud{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:8px;padding:10px 13px;border-bottom:1px solid #38566b;background:rgba(6,18,27,.82)}.hud-left,.hud-right{display:flex;align-items:center;gap:7px;flex-wrap:wrap}.hud-right{justify-content:flex-end}.pill{padding:6px 9px;border:1px solid #3e5c70;border-radius:999px;background:#0d202c;font-size:10px;font-weight:900;color:#a9c7d8;white-space:nowrap}.pill b{color:white}.battle-title{text-align:center;font-weight:1000;letter-spacing:.12em;font-size:11px;color:#94b4c5}
.table{position:relative;margin:12px;border:2px solid #153b38;border-radius:18px;background:radial-gradient(circle at center,#285c57 0%,#184641 62%,#103631 100%);box-shadow:inset 0 0 32px rgba(0,0,0,.28),0 12px 28px rgba(0,0,0,.28);padding:12px;min-height:500px}.table:before{content:"";position:absolute;inset:7px;border:1px solid rgba(255,255,255,.08);border-radius:13px;pointer-events:none}.table-grid{position:relative;display:grid;grid-template-columns:150px minmax(150px,190px) minmax(220px,1fr) minmax(150px,190px) 62px;align-items:center;justify-content:center;gap:11px;min-height:310px}
.pile-cluster{display:grid;grid-template-columns:1fr 1fr;gap:7px;align-items:end}.pile{text-align:center;color:#e9f6f4;font-size:9px;font-weight:850}.deck-stack{position:relative;width:52px;height:73px;margin:0 auto 4px}.deck-card{position:absolute;inset:0;border:2px solid #d1b778;border-radius:8px;background:repeating-linear-gradient(45deg,#173d61,#173d61 7px,#204e78 7px,#204e78 14px);box-shadow:0 3px 7px rgba(0,0,0,.25)}.deck-card:nth-child(2){transform:translate(3px,-3px)}.deck-card:nth-child(3){transform:translate(6px,-6px)}.won .deck-card{background:repeating-linear-gradient(135deg,#4a5d31,#4a5d31 7px,#61783e 7px,#61783e 14px);border-color:#b8cc80}.pile-count{font-size:13px;color:#fff}.pile-label{opacity:.9}
.card{position:relative;width:100%;aspect-ratio:.72;border:2px solid #c5a85c;border-radius:13px;background:linear-gradient(180deg,#fffefa,#f5ecd7);box-shadow:0 5px 12px rgba(0,0,0,.24);padding:7px;display:flex;flex-direction:column;overflow:hidden;transition:transform .14s ease,box-shadow .14s ease,border-color .14s ease;transform-style:preserve-3d}.card.cpu{border-color:#8ba4b6}.card.player-center{border-color:#4a86b8}.card.selectable{cursor:pointer}.card.selectable:hover{transform:translateY(-5px);border-color:#4aa7e1;box-shadow:0 9px 18px rgba(0,0,0,.30)}.card.locked{cursor:default;opacity:.68}.card.deal{animation:deal .32s cubic-bezier(.2,.8,.2,1)}.card.flip{animation:flip .43s cubic-bezier(.45,.05,.2,1)}.card.win{animation:winPulse .36s alternate 2;border-color:#63d889;box-shadow:0 0 0 4px rgba(105,224,145,.16),0 8px 18px rgba(0,0,0,.26)}.card.loss{animation:wrongShake .22s linear 2;border-color:#ef7272}.card.tie{border-color:#ffd36a;box-shadow:0 0 0 4px rgba(255,211,106,.14),0 8px 18px rgba(0,0,0,.26)}
@keyframes deal{0%{opacity:0;transform:translateY(-28px) scale(.96)}100%{opacity:1;transform:none}}@keyframes flip{0%{transform:rotateY(0)}48%{transform:rotateY(88deg)}52%{transform:rotateY(92deg)}100%{transform:rotateY(0)}}@keyframes winPulse{to{transform:translateY(-5px) scale(1.015);filter:brightness(1.05)}}@keyframes wrongShake{25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}
.card-title{font-weight:950;font-size:clamp(10px,1.05vw,14px);line-height:1.08;text-align:center;min-height:30px;display:flex;align-items:center;justify-content:center;color:#172033}.card img{width:100%;height:calc(100% - 61px);object-fit:contain;background:#fff;border-radius:7px;margin:3px 0}.formula-fallback{height:calc(100% - 61px);display:flex;align-items:center;justify-content:center;background:#fff;border-radius:7px;margin:3px 0;color:#182737;font-weight:950;font-size:clamp(18px,2vw,27px);padding:8px;text-align:center}.pka{height:23px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:950;color:#5d4817}.pka.hidden{color:#8b7c5b}.estimate{font-size:8px;color:#806c42;text-align:center;height:10px;margin-top:-4px}.empty-card{width:100%;aspect-ratio:.72;border:2px dashed rgba(255,255,255,.28);border-radius:12px;display:flex;align-items:center;justify-content:center;color:rgba(255,255,255,.62);font-size:11px;font-weight:850;text-align:center;padding:8px}
.result-box{align-self:center;min-height:166px;border-radius:14px;background:rgba(255,255,255,.96);border:1px solid #d0dde4;box-shadow:0 4px 12px rgba(0,0,0,.17);padding:13px 15px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}.result-head{font-size:17px;font-weight:1000;color:#173d61;margin-bottom:6px}.result-head.win{color:#166534}.result-head.loss{color:#9f1239}.result-head.tie{color:#6b5b20}.capture-note{font-size:11px;font-weight:900;color:#294e68;margin:1px 0 7px}.result-detail{font-size:10px;line-height:1.35;color:#40586d;max-width:410px}.next-note{font-size:9px;color:#72879a;margin-top:7px}.war-pot{display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;font-weight:950;font-size:9px;gap:3px}.pot-count{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#7c5a22;border:2px solid #d8b66a;font-size:14px;box-shadow:0 2px 7px rgba(0,0,0,.25)}
.hand-area{position:relative;display:grid;grid-template-columns:1fr 150px;gap:10px;align-items:end;margin-top:11px}.hand-wrap{min-width:0}.hand-title{font-size:11px;font-weight:950;color:#e1f0f5;margin:0 0 6px 3px}.hand{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:7px;height:clamp(165px,21vw,215px)}.hand-slot{min-width:0;min-height:0}.hand .card{height:100%;aspect-ratio:auto}.hand .card-title{font-size:clamp(9px,.92vw,12px);min-height:25px}.hand .card img,.hand .formula-fallback{height:calc(100% - 54px)}.player-piles .pile{color:#d7eaf5}.footer-note{text-align:center;color:#6f8b9b;font-size:9px;padding:0 12px 11px}.gameover{display:none;position:absolute;z-index:10;inset:0;background:rgba(4,13,20,.91);backdrop-filter:blur(5px);align-items:center;justify-content:center;padding:25px}.gameover.show{display:flex}.gameover-card{max-width:480px;width:100%;text-align:center;border:2px solid #57788d;border-radius:19px;background:linear-gradient(180deg,#173044,#0c1d29);box-shadow:0 24px 50px rgba(0,0,0,.5);padding:28px}.gameover-title{font-size:34px;font-weight:1000;margin-bottom:8px}.gameover-sub{color:#a8c1d0;line-height:1.45}.gameover-actions{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:18px}.primary{border:2px solid #915d12;background:linear-gradient(180deg,#ffe297,#dfa938);color:#352308;border-radius:12px;padding:12px;font-weight:1000;cursor:pointer}
.spark{position:absolute;width:5px;height:5px;border-radius:50%;background:#ffe089;box-shadow:0 0 10px #ffe089;pointer-events:none;animation:spark .62s ease-out forwards}@keyframes spark{to{transform:translate(var(--dx),var(--dy)) scale(.1);opacity:0}}
@media(max-width:900px){.setup-grid{grid-template-columns:1fr}.hero-copy{max-width:none}.table-grid{grid-template-columns:120px minmax(135px,180px) minmax(190px,1fr) minmax(135px,180px) 50px}.hand-area{grid-template-columns:1fr 120px}.deck-stack{width:44px;height:62px}}
@media(max-width:680px){#app{padding:7px}.topbar{margin-bottom:7px}.brandmark{width:37px;height:37px}.brand h1{font-size:18px}.brand small{display:none}.ghost{min-height:40px;padding:8px 10px}.sound-btn{min-width:42px}.sound-label{display:none}.setup{padding:17px 12px}.choice-row.three{grid-template-columns:1fr}.hud{grid-template-columns:1fr auto;padding:8px}.battle-title{display:none}.hud-left,.hud-right{gap:4px}.hud-right{justify-content:flex-end}.pill{font-size:9px;padding:5px 7px}.table{margin:7px;padding:8px;min-height:0}.table-grid{grid-template-columns:72px minmax(112px,1fr) minmax(135px,1.15fr) 38px;grid-template-areas:"cpiles cpu result pot";gap:5px;min-height:230px}.cpu-piles{grid-area:cpiles;grid-template-columns:1fr;gap:3px}.cpu-card-holder{grid-area:cpu}.result-box{grid-area:result;min-height:122px;padding:8px}.player-center-holder{display:none}.war-pot{grid-area:pot}.deck-stack{width:32px;height:45px}.pile-count{font-size:11px}.pile-label{font-size:8px}.card{padding:4px;border-radius:9px}.card-title{font-size:9px;min-height:21px}.card img,.formula-fallback{height:calc(100% - 48px)}.pka{font-size:10px;height:19px}.estimate{font-size:7px}.result-head{font-size:12px}.capture-note,.result-detail{font-size:8.5px}.next-note{display:none}.hand-area{display:block;margin-top:8px}.player-piles{display:none}.hand{display:flex;height:166px;overflow-x:auto;gap:7px;scroll-snap-type:x mandatory;padding:0 2px 5px}.hand-slot{flex:0 0 132px;scroll-snap-align:start}.hand .card-title{font-size:9px}.hand-title{font-size:10px}.footer-note{padding-bottom:8px}.gameover-actions{grid-template-columns:1fr}}
</style>
</head>
<body>
<div id="app">
  <div class="topbar">
    <div class="brand"><div class="brandmark">⚗️</div><div><h1>ACID BATTLE</h1><small>Physical Organic Chemistry</small></div></div>
    <div class="top-actions">
      <button class="ghost sound-btn" id="sound"><span class="sound-icon" id="soundIcon">🔊</span> <span class="sound-label" id="soundLabel">Sound on</span></button>
      <button class="ghost" id="fullscreen">⛶ Full screen</button>
    </div>
  </div>

  <div class="machine">
    <div class="rivets"></div>
    <section class="setup" id="setup">
      <div class="setup-grid">
        <div>
          <div class="hero-kicker">War-style pKa card game</div>
          <div class="hero-title">Choose your hand.<br>Capture the deck.</div>
          <div class="hero-copy">The computer reveals an acid. You choose one acid from your five-card hand to fight it. The lower pKa wins the trick and captures the cards. Each acid type starts with one copy on each side, so both players begin with the same chemistry deck.</div>
          <div class="rule-chip"><b>LOWER pKa WINS</b><span>•</span><span>ties build the war pot</span></div>
        </div>
        <div class="console">
          <div class="screen">
            <div class="screen-title">Solvent / pKa scale</div>
            <div class="choice-row">
              <button type="button" class="select-btn active" data-solvent="water" aria-pressed="true">H₂O<span>water reference scale</span></button>
              <button type="button" class="select-btn" data-solvent="dmso" aria-pressed="false">DMSO<span>DMSO reference scale</span></button>
            </div>
            <div class="separator"></div>
            <div class="screen-title">Acid deck</div>
            <div class="choice-row three">
              <button type="button" class="select-btn active" data-deck="25" aria-pressed="true">25 acids<span>core deck</span></button>
              <button type="button" class="select-btn" data-deck="50" aria-pressed="false">50 acids<span>extended deck</span></button>
              <button type="button" class="select-btn" data-deck="all" aria-pressed="false">WHOLE LIST<span id="allCount">63 acids</span></button>
            </div>
            <div class="pool-note" id="poolNote">Every selected acid appears once in the physical battle deck. An odd-sized deck is split as evenly as possible.</div>
            <button class="start" id="start">DEAL THE CARDS</button>
          </div>
        </div>
      </div>
    </section>

    <section class="battle" id="battle">
      <div class="hud">
        <div class="hud-left">
          <span class="pill"><b id="solventHud">H₂O</b></span>
          <span class="pill"><b id="deckHud">25</b> cards</span>
          <span class="pill">Trick <b id="trickHud">1</b></span>
          <span class="pill">War pot <b id="potHud">0</b></span>
        </div>
        <div class="battle-title">LOWER pKa WINS • CAPTURE THE WHOLE DECK</div>
        <div class="hud-right"><button class="ghost" id="change">Change deck</button></div>
      </div>

      <div class="table" id="table">
        <div class="table-grid">
          <div class="pile-cluster cpu-piles">
            <div class="pile"><div class="deck-stack"><div class="deck-card"></div><div class="deck-card"></div><div class="deck-card"></div></div><div class="pile-count" id="cpuDrawCount">0</div><div class="pile-label">CPU DRAW</div></div>
            <div class="pile won"><div class="deck-stack"><div class="deck-card"></div><div class="deck-card"></div><div class="deck-card"></div></div><div class="pile-count" id="cpuWonCount">0</div><div class="pile-label">CPU WON</div></div>
          </div>
          <div class="cpu-card-holder" id="cpuCard"></div>
          <div class="result-box" id="resultBox"></div>
          <div class="player-center-holder" id="playerCenter"></div>
          <div class="war-pot"><div class="pot-count" id="potCount">0</div><div>WAR POT</div></div>
        </div>

        <div class="hand-area">
          <div class="hand-wrap"><div class="hand-title">YOUR HAND — CHOOSE ONE CARD</div><div class="hand" id="hand"></div></div>
          <div class="pile-cluster player-piles">
            <div class="pile"><div class="deck-stack"><div class="deck-card"></div><div class="deck-card"></div><div class="deck-card"></div></div><div class="pile-count" id="drawCount">0</div><div class="pile-label">YOUR DRAW</div></div>
            <div class="pile won"><div class="deck-stack"><div class="deck-card"></div><div class="deck-card"></div><div class="deck-card"></div></div><div class="pile-count" id="wonCount">0</div><div class="pile-label">YOUR WON</div></div>
          </div>
        </div>

        <div class="gameover" id="gameover"><div class="gameover-card"><div class="gameover-title" id="gameoverTitle"></div><div class="gameover-sub" id="gameoverSub"></div><div class="gameover-actions"><button class="primary" id="again">BATTLE AGAIN</button><button class="ghost" id="newDeck">CHANGE DECK</button></div></div></div>
      </div>
      <div class="footer-note">pKa values are revealed only after you commit a card. Close values within 0.20 pKa units are treated as a tie.</div>
    </section>
  </div>
</div>

<script>
(function(){
const args=__ACID_BATTLE_DATA__; let solvent='water', deckChoice='25', pool=[];
let hand=[], playerDraw=[], playerWon=[], cpuDraw=[], cpuWon=[], cpuCurrent=null, warPot=[];
let turn=0, waiting=false, gameOver=false, timer=null, audioCtx=null, muted=false, lastPlayed=null;
const HAND_SIZE=5, TIE_TOL=0.20, HOLD_MS=3600;
const $=id=>document.getElementById(id);
function send(type,data){window.parent.postMessage(Object.assign({isStreamlitMessage:true,type:type},data||{}),'*')}
function setHeight(){setTimeout(()=>send('streamlit:setFrameHeight',{height:Math.max(document.body.scrollHeight+6,620)}),20)}
function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function loadSoundPref(){try{muted=localStorage.getItem('acidBattleMuted')==='1'}catch(e){muted=false}updateSoundButton()}
function updateSoundButton(){const b=$('sound');b.classList.toggle('muted',muted);b.setAttribute('aria-pressed',muted?'true':'false');b.title=muted?'Turn sound on':'Mute sound';$('soundIcon').textContent=muted?'🔇':'🔊';$('soundLabel').textContent=muted?'Muted':'Sound on'}
function ensureAudio(){if(muted)return null;try{const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return null;if(!audioCtx)audioCtx=new AC();if(audioCtx.state==='suspended')audioCtx.resume();return audioCtx}catch(e){return null}}
function tone(freq,dur,vol=.05,type='sine',delay=0,endFreq=null){const ac=ensureAudio();if(!ac)return;const now=ac.currentTime+delay,o=ac.createOscillator(),g=ac.createGain();o.type=type;o.frequency.setValueAtTime(freq,now);if(endFreq)o.frequency.exponentialRampToValueAtTime(Math.max(25,endFreq),now+dur);g.gain.setValueAtTime(.0001,now);g.gain.exponentialRampToValueAtTime(vol,now+.008);g.gain.exponentialRampToValueAtTime(.0001,now+dur);o.connect(g).connect(ac.destination);o.start(now);o.stop(now+dur+.02)}
function noise(dur=.075,vol=.03,delay=0){const ac=ensureAudio();if(!ac)return;const len=Math.max(1,Math.floor(ac.sampleRate*dur)),buf=ac.createBuffer(1,len,ac.sampleRate),d=buf.getChannelData(0);for(let i=0;i<len;i++)d[i]=(Math.random()*2-1)*(1-i/len);const src=ac.createBufferSource(),f=ac.createBiquadFilter(),g=ac.createGain(),now=ac.currentTime+delay;f.type='bandpass';f.frequency.value=1700;f.Q.value=.7;g.gain.setValueAtTime(vol,now);g.gain.exponentialRampToValueAtTime(.0001,now+dur);src.buffer=buf;src.connect(f).connect(g).connect(ac.destination);src.start(now)}
function sfxFlip(delay=0){if(muted)return;noise(.08,.029,delay);tone(235,.055,.016,'triangle',delay+.012,155)}
function sfxDeal(){sfxFlip(0);sfxFlip(.07)}
function sfxWin(){tone(590,.11,.043,'sine',0,720);tone(880,.16,.035,'sine',.08,1040)}
function sfxLoss(){tone(180,.17,.046,'triangle',0,105);tone(116,.17,.028,'square',.05,78)}
function sfxTie(){tone(430,.10,.032,'sine',0,430);tone(430,.10,.032,'sine',.11,430)}
function sfxCaptureBig(){tone(650,.08,.032,'sine',0,780);tone(900,.09,.032,'sine',.06,1080);tone(1250,.13,.028,'sine',.12,1420)}
function toggleSound(){muted=!muted;try{localStorage.setItem('acidBattleMuted',muted?'1':'0')}catch(e){}if(!muted)ensureAudio();updateSoundButton()}
function currentList(){return solvent==='water'?(args.water||[]):(args.dmso||[])}
function acidById(id,list){return list.find(a=>a.id===id)}
function buildPool(){const list=currentList();if(deckChoice==='all'){pool=list.slice();return}if(solvent==='water'){const ids=deckChoice==='25'?(args.core25||[]):(args.extended50||[]);pool=ids.map(id=>acidById(id,list)).filter(Boolean)}else{pool=list.slice(0,Math.min(Number(deckChoice),list.length))}}
function refreshDeckControls(){const n=currentList().length;document.querySelectorAll('[data-deck]').forEach(b=>{const need=b.dataset.deck==='all'?0:Number(b.dataset.deck),disabled=need>n;b.disabled=disabled;b.classList.toggle('disabled',disabled);b.setAttribute('aria-disabled',disabled?'true':'false')});$('allCount').textContent=n+' acids';if((deckChoice==='25'&&n<25)||(deckChoice==='50'&&n<50))deckChoice='all';document.querySelectorAll('[data-deck]').forEach(b=>{const active=b.dataset.deck===deckChoice;b.classList.toggle('active',active);b.setAttribute('aria-pressed',active?'true':'false')});const selected=(deckChoice==='all')?n:Number(deckChoice);$('poolNote').textContent=(n<25?'This solvent currently has '+n+' reference acids, so the whole-list deck is used. ':'')+selected+' acid types = '+(selected*2)+' physical cards. Each selected acid appears once in your starting deck and once in the computer’s, so both sides begin with identical acid-strength distributions.'}
function setSolvent(v){if(v!=='water'&&v!=='dmso')return;solvent=v;document.querySelectorAll('[data-solvent]').forEach(b=>{const active=b.dataset.solvent===v;b.classList.toggle('active',active);b.setAttribute('aria-pressed',active?'true':'false')});refreshDeckControls();setHeight()}
function setDeck(v){const b=document.querySelector('[data-deck="'+v+'"]');if(!b||b.disabled)return;deckChoice=v;document.querySelectorAll('[data-deck]').forEach(x=>{const active=x.dataset.deck===v;x.classList.toggle('active',active);x.setAttribute('aria-pressed',active?'true':'false')});refreshDeckControls();setHeight()}
function makeInstance(card,side,n){return Object.assign({},card,{instance_id:card.id+'__'+side+'__'+n+'__'+Math.random().toString(36).slice(2,7)})}
function makeDeal(){buildPool();const p=[],c=[];pool.forEach((card,i)=>{p.push(makeInstance(card,'P',i));c.push(makeInstance(card,'C',i))});return[shuffle(p),shuffle(c)]}
function refillHand(){while(hand.length<HAND_SIZE){if(playerDraw.length===0){if(playerWon.length===0)break;playerDraw=shuffle(playerWon.splice(0));sfxDeal()}if(playerDraw.length)hand.push(playerDraw.shift());else break}}
function prepareCpu(){if(cpuCurrent)return;if(cpuDraw.length===0){if(cpuWon.length===0)return;cpuDraw=shuffle(cpuWon.splice(0));sfxDeal()}cpuCurrent=cpuDraw.shift()||null}
function playerTotal(includeCenter=true){let n=hand.length+playerDraw.length+playerWon.length;if(includeCenter&&lastPlayed&&waiting)n++;return n}
function cpuTotal(includeCenter=true){let n=cpuDraw.length+cpuWon.length+(cpuCurrent?1:0);if(includeCenter&&!cpuCurrent&&lastPlayed&&waiting)n++;return n}
function pkaText(c){return c?(c.pka_text||String(c.pka)):''}
function formula(c){return c?(c.ref||c.name||''):''}
function cardNode(card,kind='hand',reveal=false,selectable=false){if(!card){const e=document.createElement('div');e.className='empty-card';e.textContent='card played';return e}const el=document.createElement('div');el.className='card '+(kind||'')+(selectable?' selectable':'');el.dataset.id=card.instance_id||'';const t=document.createElement('div');t.className='card-title';t.textContent=card.name||'';el.appendChild(t);if(card.image){const img=document.createElement('img');img.src=card.image;img.alt=(card.name||'acid')+' structure';el.appendChild(img)}else{const f=document.createElement('div');f.className='formula-fallback';f.textContent=formula(card);el.appendChild(f)}const p=document.createElement('div');p.className='pka'+(reveal?'':' hidden');p.textContent=reveal?('pKa '+pkaText(card)):'pKa ?';el.appendChild(p);const est=document.createElement('div');est.className='estimate';est.textContent=reveal&&card.estimated?'* estimated / extrapolated':'';el.appendChild(est);if(selectable)el.onclick=()=>playCard(card.instance_id,el);return el}
function renderPiles(){$('drawCount').textContent=playerDraw.length;$('wonCount').textContent=playerWon.length;$('cpuDrawCount').textContent=cpuDraw.length;$('cpuWonCount').textContent=cpuWon.length;$('potCount').textContent=warPot.length;$('potHud').textContent=warPot.length;$('trickHud').textContent=turn+1}
function renderIdle(){renderPiles();const cpu=$('cpuCard');cpu.innerHTML='';const node=cardNode(cpuCurrent,'cpu',false,false);node.classList.add('deal');cpu.appendChild(node);setTimeout(()=>node.classList.remove('deal'),350);const pc=$('playerCenter');pc.innerHTML='';pc.appendChild(cardNode(null));const rb=$('resultBox');rb.innerHTML='<div class="result-head">Computer has played</div><div class="result-detail">Choose the acid you want to commit. Won cards recycle into your draw pile when your draw pile runs out.</div>';const h=$('hand');h.innerHTML='';hand.forEach(c=>{const slot=document.createElement('div');slot.className='hand-slot';slot.appendChild(cardNode(c,'hand',false,true));h.appendChild(slot)});while(h.children.length<HAND_SIZE){const slot=document.createElement('div');slot.className='hand-slot';slot.appendChild(cardNode(null));h.appendChild(slot)}sfxDeal();setHeight()}
function renderResult(player,opp,winner,delta,captureCount){renderPiles();const cpu=$('cpuCard');cpu.innerHTML='';const cn=cardNode(opp,'cpu',true,false);cn.classList.add('flip');cpu.appendChild(cn);const pc=$('playerCenter');pc.innerHTML='';const pn=cardNode(player,'player-center',true,false);pn.classList.add('flip');pc.appendChild(pn);const h=$('hand');h.innerHTML='';hand.forEach(c=>{const slot=document.createElement('div');slot.className='hand-slot';const n=cardNode(c,'hand',false,false);n.classList.add('locked');slot.appendChild(n);h.appendChild(slot)});while(h.children.length<HAND_SIZE){const slot=document.createElement('div');slot.className='hand-slot';slot.appendChild(cardNode(null));h.appendChild(slot)};sfxFlip();setTimeout(()=>{cn.classList.remove('flip');pn.classList.remove('flip');if(winner==='player'){pn.classList.add('win');cn.classList.add('loss')}else if(winner==='computer'){cn.classList.add('win');pn.classList.add('loss')}else{cn.classList.add('tie');pn.classList.add('tie')}},450);const rb=$('resultBox');let head='',cls='',capture='',detail='';if(winner==='player'){head='You win the trick';cls='win';capture='You capture '+captureCount+' card'+(captureCount===1?'':'s')+'.';detail=pkaText(player)+' vs '+pkaText(opp)+' — '+(delta==null?'the reference table ranks the winner as the stronger acid.':'lower pKa wins.');if(captureCount>=6)sfxCaptureBig();else sfxWin();sparks(pn)}else if(winner==='computer'){head='Computer wins the trick';cls='loss';capture='CPU captures '+captureCount+' card'+(captureCount===1?'':'s')+'.';detail=pkaText(player)+' vs '+pkaText(opp)+' — '+(delta==null?'the reference table ranks the winner as the stronger acid.':'lower pKa wins.');sfxLoss()}else{head='Tie — cards go to the war pot';cls='tie';capture='The pot now holds '+(warPot.length+2)+' cards. The next winner takes them all.';detail=(delta!=null&&delta<=1e-12)?'Same reference pKa.':('ΔpKa = '+Number(delta).toFixed(2)+'; differences ≤ '+TIE_TOL.toFixed(2)+' are treated as a tie.');sfxTie()}rb.innerHTML='<div class="result-head '+cls+'">'+head+'</div><div class="capture-note">'+capture+'</div><div class="result-detail">'+detail+'</div><div class="next-note">Cards move to the winner’s pile, then the next trick is dealt…</div>';setHeight()}
function sparks(card){const table=$('table'),r=card.getBoundingClientRect(),tr=table.getBoundingClientRect();for(let n=0;n<14;n++){const s=document.createElement('span');s.className='spark';s.style.left=(r.left-tr.left+r.width/2)+'px';s.style.top=(r.top-tr.top+35)+'px';const a=Math.random()*Math.PI*2,d=28+Math.random()*70;s.style.setProperty('--dx',(Math.cos(a)*d)+'px');s.style.setProperty('--dy',(Math.sin(a)*d)+'px');table.appendChild(s);setTimeout(()=>s.remove(),700)}}
function playCard(id,clicked){if(waiting||gameOver||!cpuCurrent)return;ensureAudio();const idx=hand.findIndex(c=>c.instance_id===id);if(idx<0)return;waiting=true;const player=hand.splice(idx,1)[0],opp=cpuCurrent;cpuCurrent=null;lastPlayed={player,opp};const numericBoth=(player.pka!=null&&opp.pka!=null);const delta=numericBoth?Math.abs(Number(player.pka)-Number(opp.pka)):null;let winner='tie';if(!numericBoth){winner=Number(player.pka_sort)<Number(opp.pka_sort)?'player':'computer'}else if(delta>TIE_TOL+1e-12){winner=Number(player.pka)<Number(opp.pka)?'player':'computer'};const captureCount=winner==='tie'?0:warPot.length+2;renderResult(player,opp,winner,delta,captureCount);if(timer)clearTimeout(timer);timer=setTimeout(()=>advance(player,opp,winner),HOLD_MS)}
function advance(player,opp,winner){if(!waiting)return;if(winner==='player'){playerWon.push(...warPot.splice(0),player,opp)}else if(winner==='computer'){cpuWon.push(...warPot.splice(0),player,opp)}else{warPot.push(player,opp)}turn++;waiting=false;lastPlayed=null;refillHand();prepareCpu();const p=playerTotal(false),c=cpuTotal(false);if(p<=0||c<=0){if(p<=0&&c>0)cpuWon.push(...warPot.splice(0));else if(c<=0&&p>0)playerWon.push(...warPot.splice(0));finishGame(p,c);return}renderIdle()}
function finishGame(p,c){gameOver=true;renderPiles();let title,sub;if(p<=0&&c<=0){title='DRAW';sub='Both sides ran out of cards at the same time.'}else if(p<=0){title='CPU WINS';sub='The computer captured the battle deck.'}else{title='YOU WIN';sub='You captured the battle deck.'}$('gameoverTitle').textContent=title;$('gameoverSub').textContent=sub+'  Tricks played: '+turn+'.';$('gameover').classList.add('show');if(p>0)sfxCaptureBig();else sfxLoss();setHeight()}
function startBattle(){ensureAudio();const [p,c]=makeDeal();hand=[];playerDraw=p;playerWon=[];cpuDraw=c;cpuWon=[];cpuCurrent=null;warPot=[];turn=0;waiting=false;gameOver=false;lastPlayed=null;if(timer){clearTimeout(timer);timer=null}$('setup').style.display='none';$('battle').style.display='block';$('gameover').classList.remove('show');$('solventHud').textContent=solvent==='water'?'H₂O':'DMSO';$('deckHud').textContent=pool.length+' acids';refillHand();prepareCpu();renderIdle()}
function backToSetup(){if(timer){clearTimeout(timer);timer=null}$('battle').style.display='none';$('setup').style.display='block';$('gameover').classList.remove('show');refreshDeckControls();setHeight()}
function battleAgain(){startBattle()}
$('setup').addEventListener('click',e=>{const solventButton=e.target.closest('button[data-solvent]');if(solventButton){setSolvent(solventButton.dataset.solvent);return}const deckButton=e.target.closest('button[data-deck]');if(deckButton){setDeck(deckButton.dataset.deck);return}});$('start').addEventListener('click',startBattle);$('sound').addEventListener('click',toggleSound);$('change').addEventListener('click',backToSetup);$('newDeck').addEventListener('click',backToSetup);$('again').addEventListener('click',battleAgain);
$('fullscreen').addEventListener('click',async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen()}catch(e){}setHeight()});document.addEventListener('fullscreenchange',()=>{$('fullscreen').textContent=document.fullscreenElement?'↙ Exit full screen':'⛶ Full screen';setHeight()});window.addEventListener('resize',setHeight);
loadSoundPref();setSolvent('water');setDeck('25');refreshDeckControls();setHeight();
})();
</script>
</body>
</html>'''



def acid_battle_component():
    payload = {
        "water": WATER,
        "dmso": DMSO,
        "core25": CORE_25_IDS,
        "extended50": EXTENDED_50_IDS,
    }
    html = HTML.replace("__ACID_BATTLE_DATA__", json.dumps(payload, ensure_ascii=False))
    components.html(html, height=1080, scrolling=False)


acid_battle_component()
