import base64
import io
import json
import os
import tempfile

import streamlit as st
import streamlit.components.v1 as components
from rdkit import Chem
from rdkit.Chem import Draw, rdDepictor

from acid_data import WATER_ACIDS, DMSO_ACIDS, CORE_25_IDS, EXTENDED_50_IDS

st.set_page_config(page_title='Acid Battle', page_icon='⚗️', layout='wide', initial_sidebar_state='collapsed')

st.markdown('''
<style>
header[data-testid="stHeader"]{background:transparent;height:0}
[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"]{display:none!important}
.block-container{padding:0!important;max-width:none!important}
iframe{border:0!important}
</style>
''', unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def molecule_png_data_uri(smiles: str | None) -> str | None:
    if not smiles:
        return None
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        rdDepictor.Compute2DCoords(mol)
        img = Draw.MolToImage(mol, size=(520, 330), kekulize=True)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode('ascii')
    except Exception:
        return None


def prepared_acids(rows):
    result = []
    for index, row in enumerate(rows):
        item = dict(row)
        item['image'] = molecule_png_data_uri(row.get('smiles'))
        # Reference order is a safe ordering fallback for the non-numeric HF–SbF5 entry.
        item['strength_order'] = index
        result.append(item)
    return result

WATER = prepared_acids(WATER_ACIDS)
DMSO = prepared_acids(DMSO_ACIDS)

HTML = r'''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no">
<style>
:root{--ink:#dce9f2;--muted:#8ea5b5;--blue:#78c7ff;--deep:#08131d;--panel:#142635;--line:#405c70;--steel1:#d6dee3;--steel2:#8999a5;--cream:#f8f1df;--good:#71e69a;--bad:#ff7777;--gold:#ffd36a}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;min-height:100%;background:#07111a;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Arial,sans-serif;overflow-x:hidden}
body{background-image:radial-gradient(circle at 50% -10%,#18364c 0,transparent 42%),linear-gradient(180deg,#08131d 0,#07111a 48%,#050c12 100%)}
#app{min-height:100vh;padding:14px max(14px,env(safe-area-inset-right)) calc(18px + env(safe-area-inset-bottom)) max(14px,env(safe-area-inset-left));max-width:1280px;margin:auto}
.topbar{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px}.brand{display:flex;align-items:center;gap:11px}.brandmark{width:43px;height:43px;border-radius:12px;background:linear-gradient(145deg,#e7edf0,#8396a4);border:2px solid #536b7b;box-shadow:inset 0 0 0 3px rgba(255,255,255,.14),0 7px 18px rgba(0,0,0,.35);display:grid;place-items:center;font-size:23px}.brand h1{font-size:23px;line-height:1;margin:0;font-weight:950;letter-spacing:.025em}.brand small{display:block;color:var(--muted);font-weight:700;margin-top:4px}.top-actions{display:flex;align-items:center;gap:8px}.ghost{border:1px solid #4c687b;background:#132431;color:#dce9f2;border-radius:11px;padding:10px 13px;font-weight:850;cursor:pointer;min-height:44px}.ghost:hover{filter:brightness(1.1)}.sound-btn{min-width:108px}.sound-btn.muted{color:#8ca0ad;background:#0c1a23}.sound-icon{display:inline-block;min-width:18px;text-align:center}
.machine{position:relative;border:2px solid #3d586b;border-radius:24px;background:linear-gradient(180deg,rgba(25,46,61,.95),rgba(10,24,34,.97));box-shadow:inset 0 0 0 1px rgba(255,255,255,.04),0 20px 46px rgba(0,0,0,.42);overflow:hidden}.machine:before{content:"";position:absolute;inset:0;pointer-events:none;opacity:.22;background-image:linear-gradient(45deg,rgba(255,255,255,.05) 25%,transparent 25%,transparent 75%,rgba(255,255,255,.05) 75%),linear-gradient(45deg,rgba(255,255,255,.05) 25%,transparent 25%,transparent 75%,rgba(255,255,255,.05) 75%);background-size:38px 38px;background-position:0 0,19px 19px}.rivets{position:absolute;inset:8px;pointer-events:none;border:1px solid rgba(147,174,192,.14);border-radius:18px}
.setup{padding:clamp(20px,4vw,48px);position:relative;z-index:2}.setup-grid{display:grid;grid-template-columns:1.05fr .95fr;gap:28px;align-items:center}.hero-kicker{color:var(--gold);font-size:12px;letter-spacing:.18em;font-weight:950;text-transform:uppercase}.hero-title{font-size:clamp(38px,6vw,72px);font-weight:1000;line-height:.93;letter-spacing:-.045em;margin:8px 0 14px;text-shadow:0 5px 22px rgba(0,0,0,.3)}.hero-copy{color:#a9bdca;font-size:clamp(15px,2vw,19px);line-height:1.45;max-width:650px}.rule-chip{display:inline-flex;gap:8px;align-items:center;margin-top:18px;padding:9px 12px;border:1px solid #466477;border-radius:999px;background:#0e202d;color:#bcd2df;font-size:13px;font-weight:800}.rule-chip b{color:white}
.console{padding:17px;border-radius:19px;background:linear-gradient(180deg,#d9e0e4,#8597a3);border:3px solid #4f6878;box-shadow:inset 0 0 0 3px rgba(255,255,255,.13),0 14px 25px rgba(0,0,0,.35);color:#102331}.screen{border-radius:13px;background:#091a24;border:2px solid #486271;box-shadow:inset 0 0 18px rgba(93,198,255,.07);padding:17px;color:#d9edf8}.screen-title{font-size:12px;letter-spacing:.12em;text-transform:uppercase;font-weight:950;color:#7cb9dc;margin:2px 0 10px}.choice-row{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}.choice-row.three{grid-template-columns:repeat(3,1fr)}.select-btn{position:relative;border:1px solid #3e6277;background:#102b3b;color:#cbe5f2;border-radius:12px;padding:13px 9px;min-height:58px;font-size:14px;font-weight:950;cursor:pointer;box-shadow:inset 0 -3px 0 rgba(0,0,0,.17)}.select-btn.active{background:#d7edf9;color:#0a293a;border-color:#99d9ff;box-shadow:0 0 0 3px rgba(120,199,255,.15),inset 0 -3px 0 rgba(0,0,0,.10)}.select-btn.disabled{opacity:.45;cursor:not-allowed}.select-btn span{display:block;font-size:10px;font-weight:800;opacity:.7;margin-top:4px}.separator{height:1px;background:#345268;margin:15px 0}.start{width:100%;margin-top:16px;border:2px solid #915d12;background:linear-gradient(180deg,#ffe297,#dfa938);color:#352308;border-radius:14px;padding:15px 15px;font-size:16px;font-weight:1000;letter-spacing:.04em;cursor:pointer;box-shadow:inset 0 0 0 3px rgba(255,255,255,.23),0 8px 15px rgba(0,0,0,.25)}.start:disabled{filter:grayscale(1);opacity:.45;cursor:not-allowed}.pending{margin-top:10px;padding:9px 10px;border-radius:9px;background:#2d2210;border:1px solid #715421;color:#f6cf78;font-size:12px;font-weight:750;display:none}
.battle{display:none;position:relative;z-index:2}.hud{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:10px;padding:12px 16px;border-bottom:1px solid #38566b;background:rgba(6,18,27,.77)}.hud-left,.hud-right{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.hud-right{justify-content:flex-end}.pill{padding:7px 10px;border:1px solid #3e5c70;border-radius:999px;background:#0d202c;font-size:11px;font-weight:900;color:#a9c7d8}.pill b{color:white}.battle-title{text-align:center;font-weight:1000;letter-spacing:.12em;font-size:12px;color:#94b4c5}.arena{position:relative;padding:clamp(14px,3vw,28px);min-height:660px;background:radial-gradient(circle at 50% 48%,rgba(85,170,220,.10),transparent 34%)}.arena:before,.arena:after{content:"";position:absolute;top:50%;height:2px;width:16%;background:linear-gradient(90deg,transparent,#5eaad6);opacity:.45}.arena:before{left:2%}.arena:after{right:2%;transform:scaleX(-1)}
.prompt{text-align:center;color:#e5f4fc;font-size:clamp(18px,2.6vw,29px);font-weight:950;margin:3px 0 18px}.prompt small{display:block;color:#819cab;font-size:12px;letter-spacing:.06em;text-transform:uppercase;margin-top:5px}.cards{display:grid;grid-template-columns:1fr 86px 1fr;align-items:stretch;gap:18px;max-width:1040px;margin:0 auto}.vs{align-self:center;justify-self:center;width:74px;height:74px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(145deg,#edf2f4,#8194a1);border:4px solid #496474;color:#102431;font-size:22px;font-weight:1000;box-shadow:0 0 0 7px rgba(77,113,135,.16),0 12px 24px rgba(0,0,0,.35);z-index:4}.acid-card{position:relative;overflow:hidden;min-height:410px;border:3px solid #516a79;border-radius:20px;background:linear-gradient(180deg,#e9eef0,#9eabb4);padding:10px;box-shadow:inset 0 0 0 3px rgba(255,255,255,.12),0 18px 34px rgba(0,0,0,.35);cursor:pointer;transition:transform .14s ease,filter .14s ease,box-shadow .2s ease;transform-style:preserve-3d;will-change:transform}.acid-card.deal-left{animation:dealLeft .34s cubic-bezier(.2,.8,.2,1)}.acid-card.deal-right{animation:dealRight .34s cubic-bezier(.2,.8,.2,1)}.acid-card.flipping{animation:cardFlip .42s cubic-bezier(.45,.05,.2,1)}.acid-card:hover{transform:translateY(-3px);filter:brightness(1.04)}.acid-card.locked{cursor:default}.acid-card.correct{border-color:#68d98e;box-shadow:0 0 0 5px rgba(105,224,145,.17),0 18px 34px rgba(0,0,0,.35);animation:winPulse .38s alternate 2}.acid-card.wrong{border-color:#f06f6f;box-shadow:0 0 0 5px rgba(255,112,112,.15),0 18px 34px rgba(0,0,0,.35);animation:wrongShake .24s linear 2}.acid-card.tie{border-color:#ffd36a;box-shadow:0 0 0 5px rgba(255,211,106,.15),0 18px 34px rgba(0,0,0,.35)}@keyframes dealLeft{0%{opacity:0;transform:translateX(-42px) rotate(-2deg) scale(.96)}100%{opacity:1;transform:none}}@keyframes dealRight{0%{opacity:0;transform:translateX(42px) rotate(2deg) scale(.96)}100%{opacity:1;transform:none}}@keyframes cardFlip{0%{transform:rotateY(0deg) scale(1)}45%{transform:rotateY(88deg) scale(.985);filter:brightness(.92)}55%{transform:rotateY(92deg) scale(.985);filter:brightness(.92)}100%{transform:rotateY(0deg) scale(1)}}@keyframes winPulse{to{transform:translateY(-5px) scale(1.012);filter:brightness(1.08)}}@keyframes wrongShake{25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}
.card-inner{height:100%;min-height:386px;border-radius:13px;background:var(--cream);border:1px solid rgba(33,51,61,.22);color:#10202c;display:flex;flex-direction:column;overflow:hidden}.card-head{display:flex;align-items:center;justify-content:space-between;padding:10px 12px;background:#ede4cd;border-bottom:1px solid #cfc4aa}.card-tag{font-size:10px;letter-spacing:.12em;font-weight:1000;color:#566069}.card-letter{width:28px;height:28px;border-radius:8px;background:#162d3b;color:white;display:grid;place-items:center;font-weight:1000}.structure{height:220px;display:flex;align-items:center;justify-content:center;padding:10px;background:#fffdf7}.structure img{max-width:100%;max-height:200px;object-fit:contain}.formula-fallback{font-family:"Segoe UI",sans-serif;font-size:clamp(30px,5vw,48px);font-weight:850;letter-spacing:.01em;text-align:center}.name{padding:12px 15px 4px;text-align:center;font-size:clamp(18px,2.2vw,25px);font-weight:1000;line-height:1.05}.formula{text-align:center;color:#52616b;font-size:14px;font-weight:850;padding:2px 10px 10px}.reveal{margin:auto 12px 12px;border-radius:11px;background:#132835;color:white;padding:11px;text-align:center;opacity:0;transform:translateY(8px);transition:.22s}.reveal.show{opacity:1;transform:none;animation:revealPop .28s ease-out}@keyframes revealPop{0%{opacity:0;transform:translateY(8px) scale(.96)}100%{opacity:1;transform:none}}.pka-label{font-size:10px;color:#91afbf;font-weight:900;letter-spacing:.10em;text-transform:uppercase}.pka{font-size:30px;font-weight:1000;letter-spacing:-.03em}.estimated{font-size:10px;color:#f6d27b;font-weight:800;margin-top:2px}.answer-strip{max-width:1040px;margin:18px auto 0;min-height:102px;border:1px solid #3b586a;border-radius:15px;background:#0c1e29;padding:13px 15px;display:flex;align-items:center;justify-content:space-between;gap:15px}.feedback{font-weight:950;font-size:16px}.feedback.good{color:var(--good)}.feedback.bad{color:var(--bad)}.feedback.tie{color:var(--gold)}.explain{font-size:12px;color:#9bb3c2;margin-top:4px;line-height:1.35}.next{border:1px solid #8a5c18;background:#f2c95f;color:#30230a;border-radius:11px;padding:12px 17px;min-height:48px;font-weight:1000;cursor:pointer;display:none;white-space:nowrap}.tap-hint{text-align:center;color:#6f8b9c;font-size:11px;font-weight:750;margin-top:10px}.spark{position:absolute;width:4px;height:4px;border-radius:50%;background:#ffe38b;box-shadow:0 0 9px #ffe38b;pointer-events:none;animation:spark .62s ease-out forwards}@keyframes spark{to{transform:translate(var(--dx),var(--dy));opacity:0}}
@media(max-width:760px){#app{padding:8px 8px calc(12px + env(safe-area-inset-bottom))}.topbar{margin:3px 2px 8px}.brandmark{width:38px;height:38px}.brand h1{font-size:19px}.brand small{display:none}.ghost{padding:8px 10px;min-height:40px}.sound-btn{min-width:48px}.sound-label{display:none}.top-actions{gap:5px}.machine{border-radius:18px}.setup{padding:18px 13px}.setup-grid{grid-template-columns:1fr;gap:18px}.hero-title{font-size:43px}.hero-copy{font-size:15px}.console{padding:10px}.screen{padding:13px 10px}.choice-row.three{grid-template-columns:1fr 1fr 1fr;gap:6px}.select-btn{padding:11px 5px;font-size:12px;min-height:56px}.hud{grid-template-columns:1fr auto;padding:9px 9px}.battle-title{display:none}.hud-right{justify-content:flex-end}.arena{padding:12px 8px 16px;min-height:auto}.prompt{font-size:20px;margin:2px 0 12px}.cards{grid-template-columns:1fr;gap:8px}.vs{width:50px;height:50px;font-size:16px;margin:-2px auto;z-index:6}.acid-card{min-height:300px;border-radius:16px;padding:7px}.acid-card:hover{transform:none}.card-inner{min-height:282px}.structure{height:150px}.structure img{max-height:140px}.name{font-size:20px;padding-top:8px}.formula{padding-bottom:6px}.reveal{margin:5px 9px 9px;padding:7px}.pka{font-size:25px}.answer-strip{margin-top:10px;min-height:88px;padding:10px;flex-direction:column;align-items:stretch}.next{width:100%;display:none}.tap-hint{margin-top:7px}.arena:before,.arena:after{display:none}}
@media(max-width:390px){.pill{padding:6px 7px;font-size:10px}.hud-left{gap:5px}.hero-title{font-size:38px}.structure{height:138px}.acid-card{min-height:286px}.card-inner{min-height:270px}}
</style>
</head>
<body>
<div id="app">
  <div class="topbar">
    <div class="brand"><div class="brandmark">⚗️</div><div><h1>ACID BATTLE</h1><small>Physical Organic Chemistry</small></div></div>
    <div class="top-actions"><button class="ghost sound-btn" id="sound" aria-pressed="false" title="Mute sound"><span class="sound-icon" id="soundIcon">🔊</span> <span class="sound-label" id="soundLabel">Sound on</span></button><button class="ghost" id="fullscreen">⛶ Full screen</button></div>
  </div>
  <div class="machine">
    <div class="rivets"></div>
    <section class="setup" id="setup">
      <div class="setup-grid">
        <div>
          <div class="hero-kicker">pKa combat simulator</div>
          <div class="hero-title">LOWER pKa.<br>STRONGER ACID.</div>
          <div class="hero-copy">Choose your solvent and deck, then tap the stronger acid. Values are revealed only after the battle.</div>
          <div class="rule-chip">⚡ <b>Win condition:</b> choose the lower pKa</div>
        </div>
        <div class="console">
          <div class="screen">
            <div class="screen-title">01 · Solvent</div>
            <div class="choice-row">
              <button class="select-btn active" data-solvent="water">H₂O<span>water pKa scale</span></button>
              <button class="select-btn" data-solvent="dmso">DMSO<span>separate reference scale</span></button>
            </div>
            <div class="pending" id="pending">This solvent currently has fewer acids than the selected deck size. Choose an available deck.</div>
            <div class="separator"></div>
            <div class="screen-title">02 · Deck size</div>
            <div class="choice-row three">
              <button class="select-btn active" data-deck="25">25<span>Core</span></button>
              <button class="select-btn" data-deck="50">50<span>Extended</span></button>
              <button class="select-btn" data-deck="all">ALL<span id="allCount">63 acids</span></button>
            </div>
            <button class="start" id="start">START BATTLE</button>
          </div>
        </div>
      </div>
    </section>
    <section class="battle" id="battle">
      <div class="hud">
        <div class="hud-left"><span class="pill"><b id="solventHud">H₂O</b></span><span class="pill"><b id="deckHud">25</b> deck</span><span class="pill">Round <b id="roundHud">1</b></span></div>
        <div class="battle-title">ACID STRENGTH ARENA</div>
        <div class="hud-right"><span class="pill">Score <b id="scoreHud">0</b></span><span class="pill">Streak <b id="streakHud">0</b></span><button class="ghost" id="change">Change deck</button></div>
      </div>
      <div class="arena" id="arena">
        <div class="prompt">Which is the stronger acid?<small>Tap a card to choose</small></div>
        <div class="cards">
          <div class="acid-card" id="card0" data-side="0"><div class="card-inner"><div class="card-head"><span class="card-tag">CONTENDER A</span><span class="card-letter">A</span></div><div class="structure" id="structure0"></div><div class="name" id="name0"></div><div class="formula" id="formula0"></div><div class="reveal" id="reveal0"><div class="pka-label">pKa · <span class="solvLabel">H₂O</span></div><div class="pka" id="pka0"></div><div class="estimated" id="est0"></div></div></div></div>
          <div class="vs">VS</div>
          <div class="acid-card" id="card1" data-side="1"><div class="card-inner"><div class="card-head"><span class="card-tag">CONTENDER B</span><span class="card-letter">B</span></div><div class="structure" id="structure1"></div><div class="name" id="name1"></div><div class="formula" id="formula1"></div><div class="reveal" id="reveal1"><div class="pka-label">pKa · <span class="solvLabel">H₂O</span></div><div class="pka" id="pka1"></div><div class="estimated" id="est1"></div></div></div></div>
        </div>
        <div class="answer-strip"><div><div class="feedback" id="feedback">Choose a contender.</div><div class="explain" id="explain">Lower pKa means the stronger acid.</div></div><button class="next" id="next">NEXT BATTLE →</button></div>
        <div class="tap-hint">Designed for mouse, touch, and portrait phone screens.</div>
      </div>
    </section>
  </div>
</div>
<script>
(function(){
let args={}, solvent='water', deckChoice='25', pool=[], pair=[], score=0, streak=0, round=1, locked=false, recentPairs=[], audioCtx=null, muted=false;
const $=id=>document.getElementById(id);
function send(type,data){window.parent.postMessage(Object.assign({isStreamlitMessage:true,type:type},data||{}),'*')}
function setHeight(){setTimeout(()=>send('streamlit:setFrameHeight',{height:Math.max(document.body.scrollHeight+6,620)}),20)}
function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function loadSoundPref(){try{muted=localStorage.getItem('acidBattleMuted')==='1'}catch(e){muted=false}updateSoundButton()}
function updateSoundButton(){const b=$('sound');if(!b)return;b.classList.toggle('muted',muted);b.setAttribute('aria-pressed',muted?'true':'false');b.title=muted?'Turn sound on':'Mute sound';$('soundIcon').textContent=muted?'🔇':'🔊';$('soundLabel').textContent=muted?'Muted':'Sound on'}
function ensureAudio(){if(muted)return null;try{const AC=window.AudioContext||window.webkitAudioContext;if(!AC)return null;if(!audioCtx)audioCtx=new AC();if(audioCtx.state==='suspended')audioCtx.resume();return audioCtx}catch(e){return null}}
function tone(freq,dur,vol=.055,type='sine',delay=0,endFreq=null){const ac=ensureAudio();if(!ac)return;const now=ac.currentTime+delay,o=ac.createOscillator(),g=ac.createGain();o.type=type;o.frequency.setValueAtTime(freq,now);if(endFreq)o.frequency.exponentialRampToValueAtTime(Math.max(25,endFreq),now+dur);g.gain.setValueAtTime(.0001,now);g.gain.exponentialRampToValueAtTime(vol,now+.008);g.gain.exponentialRampToValueAtTime(.0001,now+dur);o.connect(g).connect(ac.destination);o.start(now);o.stop(now+dur+.02)}
function noise(dur=.075,vol=.035,delay=0){const ac=ensureAudio();if(!ac)return;const len=Math.max(1,Math.floor(ac.sampleRate*dur)),buf=ac.createBuffer(1,len,ac.sampleRate),d=buf.getChannelData(0);for(let i=0;i<len;i++)d[i]=(Math.random()*2-1)*(1-i/len);const src=ac.createBufferSource(),f=ac.createBiquadFilter(),g=ac.createGain(),now=ac.currentTime+delay;f.type='bandpass';f.frequency.value=1700;f.Q.value=.7;g.gain.setValueAtTime(vol,now);g.gain.exponentialRampToValueAtTime(.0001,now+dur);src.buffer=buf;src.connect(f).connect(g).connect(ac.destination);src.start(now)}
function sfxFlip(delay=0){if(muted)return;noise(.085,.032,delay);tone(240,.055,.018,'triangle',delay+.015,155)}
function sfxCorrect(){if(muted)return;tone(590,.12,.047,'sine',0,720);tone(880,.16,.038,'sine',.085,1040)}
function sfxWrong(){if(muted)return;tone(185,.17,.05,'triangle',0,105);tone(116,.18,.032,'square',.055,78)}
function sfxTie(){if(muted)return;tone(440,.11,.035,'sine',0,440);tone(440,.11,.035,'sine',.12,440)}
function sfxStreak(){if(muted)return;tone(740,.08,.035,'sine',0,880);tone(990,.1,.035,'sine',.07,1180);tone(1320,.14,.03,'sine',.14,1480)}
function toggleSound(){muted=!muted;try{localStorage.setItem('acidBattleMuted',muted?'1':'0')}catch(e){}if(!muted)ensureAudio();updateSoundButton()}
function acidById(id,list){return list.find(a=>a.id===id)}
function currentList(){return solvent==='water'?(args.water||[]):(args.dmso||[])}
function deckIds(){if(solvent!=='water')return null;if(deckChoice==='25')return args.core25||[]; if(deckChoice==='50')return args.extended50||[]; return null}
function buildPool(){const list=currentList();if(deckChoice==='all'){pool=list.slice();return}const requested=Number(deckChoice);if(solvent==='water'){const ids=deckIds();pool=ids?ids.map(id=>acidById(id,list)).filter(Boolean):list.slice(0,requested)}else{pool=list.slice(0,Math.min(requested,list.length))}}
function refreshDeckControls(){const n=currentList().length;document.querySelectorAll('[data-deck]').forEach(b=>{const need=b.dataset.deck==='all'?0:Number(b.dataset.deck);const disabled=need>n;b.disabled=disabled;b.classList.toggle('disabled',disabled)});$('allCount').textContent=n+' acids';if((deckChoice==='25'&&n<25)||(deckChoice==='50'&&n<50)){deckChoice='all'};document.querySelectorAll('[data-deck]').forEach(b=>b.classList.toggle('active',b.dataset.deck===deckChoice));$('pending').style.display='none';$('start').disabled=n<2}
function setSolvent(v){solvent=v;document.querySelectorAll('[data-solvent]').forEach(b=>b.classList.toggle('active',b.dataset.solvent===v));refreshDeckControls();setHeight()}
function setDeck(v){const btn=document.querySelector('[data-deck="'+v+'"]');if(btn&&btn.disabled)return;deckChoice=v;document.querySelectorAll('[data-deck]').forEach(b=>b.classList.toggle('active',b.dataset.deck===v))}
function pairKey(a,b){return [a.id,b.id].sort().join('|')}
function newPair(){buildPool(); if(pool.length<2)return; let a,b,key,tries=0; do{a=pool[Math.floor(Math.random()*pool.length)];do{b=pool[Math.floor(Math.random()*pool.length)]}while(b.id===a.id);key=pairKey(a,b);tries++}while(recentPairs.includes(key)&&tries<80);recentPairs.push(key);if(recentPairs.length>Math.min(18,pool.length*2))recentPairs.shift();pair=Math.random()<.5?[a,b]:[b,a];locked=false;renderPair()}
function renderMol(acid,i){const box=$('structure'+i);if(acid.image){box.innerHTML='<img alt="'+esc(acid.name)+' structure" src="'+acid.image+'">'}else{box.innerHTML='<div class="formula-fallback">'+esc(acid.ref)+'</div>'}}
function renderPair(){for(let i=0;i<2;i++){const a=pair[i],c=$('card'+i);c.className='acid-card '+(i===0?'deal-left':'deal-right');renderMol(a,i);$('name'+i).textContent=a.name;$('formula'+i).textContent=a.ref;$('pka'+i).textContent=a.pka_text||String(a.pka);$('est'+i).textContent=a.estimated?'* estimated / extrapolated on this scale':'';$('reveal'+i).classList.remove('show')}sfxFlip(0);sfxFlip(.075);document.querySelectorAll('.solvLabel').forEach(x=>x.textContent=solvent==='water'?'H₂O':'DMSO');$('feedback').className='feedback';$('feedback').textContent='Choose a contender.';$('explain').textContent='Lower pKa means the stronger acid.';$('next').style.display='none';$('roundHud').textContent=round;setTimeout(()=>{for(let i=0;i<2;i++)$('card'+i).classList.remove('deal-left','deal-right')},380);setHeight()}
function strengthCompare(a,b){if(a.pka==null&&b.pka==null)return 0;if(a.pka==null)return -1;if(b.pka==null)return 1;return a.pka-b.pka}
function sparks(card){const arena=$('arena'),r=card.getBoundingClientRect(),ar=arena.getBoundingClientRect();for(let n=0;n<16;n++){const s=document.createElement('span');s.className='spark';s.style.left=(r.left-ar.left+r.width/2)+'px';s.style.top=(r.top-ar.top+45)+'px';const ang=Math.random()*Math.PI*2,dist=28+Math.random()*75;s.style.setProperty('--dx',(Math.cos(ang)*dist)+'px');s.style.setProperty('--dy',(Math.sin(ang)*dist)+'px');arena.appendChild(s);setTimeout(()=>s.remove(),700)}}
function choose(i){if(locked)return;locked=true;ensureAudio();const a=pair[0],b=pair[1],cmp=strengthCompare(a,b);let winners=cmp<0?[0]:cmp>0?[1]:[0,1];const correct=winners.includes(i);for(let j=0;j<2;j++){$('card'+j).classList.add('locked','flipping')}sfxFlip(0);sfxFlip(.065);
setTimeout(()=>{for(let j=0;j<2;j++)$('reveal'+j).classList.add('show')},190);
setTimeout(()=>{for(let j=0;j<2;j++){$('card'+j).classList.remove('flipping');if(winners.includes(j))$('card'+j).classList.add(winners.length===2?'tie':'correct')}if(!correct)$('card'+i).classList.add('wrong');if(winners.length===2){score++;streak++;$('feedback').className='feedback tie';$('feedback').textContent='Tie — same reference pKa.';$('explain').textContent=a.pka_text+' vs '+b.pka_text+' on the '+(solvent==='water'?'water':'DMSO')+' scale.';sfxTie()}else if(correct){score++;streak++;$('feedback').className='feedback good';$('feedback').textContent='Correct — '+pair[winners[0]].name+' wins.';let d=(a.pka!=null&&b.pka!=null)?Math.abs(a.pka-b.pka):null;$('explain').textContent=d==null?'The reference table ranks it as the stronger acid.':'ΔpKa = '+d.toFixed(d<1?2:1).replace(/\.0$/,'')+'. Lower pKa means greater acidity.';sparks($('card'+winners[0]));if(streak>0&&streak%5===0)sfxStreak();else sfxCorrect()}else{streak=0;$('feedback').className='feedback bad';$('feedback').textContent='Not this time — '+pair[winners[0]].name+' is stronger.';$('explain').textContent='Compare the revealed pKa values: the lower value wins.';sfxWrong()}$('scoreHud').textContent=score;$('streakHud').textContent=streak;$('next').style.display='block';setHeight()},440)}
function start(){ensureAudio();buildPool();score=0;streak=0;round=1;recentPairs=[];$('setup').style.display='none';$('battle').style.display='block';$('solventHud').textContent=solvent==='water'?'H₂O':'DMSO';$('deckHud').textContent=pool.length;$('scoreHud').textContent='0';$('streakHud').textContent='0';newPair();setHeight()}
function resetSetup(){$('battle').style.display='none';$('setup').style.display='block';setHeight()}
document.querySelectorAll('[data-solvent]').forEach(b=>b.addEventListener('click',()=>setSolvent(b.dataset.solvent)));document.querySelectorAll('[data-deck]').forEach(b=>b.addEventListener('click',()=>setDeck(b.dataset.deck)));$('start').addEventListener('click',start);$('sound').addEventListener('click',toggleSound);$('card0').addEventListener('click',()=>choose(0));$('card1').addEventListener('click',()=>choose(1));$('next').addEventListener('click',()=>{round++;newPair()});$('change').addEventListener('click',resetSetup);
$('fullscreen').addEventListener('click',async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen()}catch(e){}setHeight()});document.addEventListener('fullscreenchange',()=>{$('fullscreen').textContent=document.fullscreenElement?'↙ Exit full screen':'⛶ Full screen';setHeight()});window.addEventListener('resize',setHeight);
loadSoundPref();window.addEventListener('message',e=>{if(!e.data||e.data.type!=='streamlit:render')return;args=e.data.args||{};setSolvent('water');setDeck('25');refreshDeckControls();setHeight()});send('streamlit:componentReady',{apiVersion:1});
})();
</script>
</body>
</html>'''


def acid_battle_component():
    component_dir = os.path.join(tempfile.gettempdir(), 'acid_battle_component_v003')
    os.makedirs(component_dir, exist_ok=True)
    index_path = os.path.join(component_dir, 'index.html')
    try:
        old = ''
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                old = f.read()
        if old != HTML:
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(HTML)
    except OSError:
        pass
    component = components.declare_component('acid_battle_component_v003', path=component_dir)
    component(
        water=WATER,
        dmso=DMSO,
        core25=CORE_25_IDS,
        extended50=EXTENDED_50_IDS,
        key='acid_battle_main',
        default=None,
    )

acid_battle_component()
