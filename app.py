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
        img = Draw.MolToImage(mol, size=(520, 320), kekulize=True, fitImage=True)
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
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<style>
:root{
  --ink:#e4eef4;--muted:#8da5b5;--blue:#78c7ff;--deep:#07111a;--panel:#142635;
  --line:#405c70;--cream:#fffaf0;--cream2:#f0e5c9;--good:#72e49a;--bad:#ff7c7c;
  --gold:#ffd36a;--felt:#19453f;--felt2:#0f312e;--cpu:#90aabb;--player:#68b5e7;
}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
.sr-only{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important}
button:focus-visible,input:focus-visible,.card.selectable:focus-visible,[tabindex]:focus-visible{outline:3px solid #fff!important;outline-offset:3px!important;box-shadow:0 0 0 6px #126ca1!important}
button:disabled{cursor:not-allowed}
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
.card{position:relative;width:100%;aspect-ratio:.72;border:2px solid #c5a85c;border-radius:13px;background:linear-gradient(180deg,#fffefa,#f5ecd7);box-shadow:0 5px 12px rgba(0,0,0,.24);padding:7px;display:flex;flex-direction:column;overflow:hidden;transition:transform .14s ease,box-shadow .14s ease,border-color .14s ease;transform-style:preserve-3d}.card.cpu{border-color:#8ba4b6}.card.player-center{border-color:#4a86b8}.card.selectable{cursor:pointer}.card.selectable:hover,.card.selectable:focus-visible{transform:translateY(-5px);border-color:#4aa7e1;box-shadow:0 9px 18px rgba(0,0,0,.30)}.card.locked{cursor:default;opacity:.68}.card.deal{animation:deal .32s cubic-bezier(.2,.8,.2,1)}.card.flip{animation:flip .62s cubic-bezier(.45,.05,.2,1);transform-origin:center center;backface-visibility:hidden}.card.win{animation:winPulse .36s alternate 2;border-color:#63d889;box-shadow:0 0 0 4px rgba(105,224,145,.16),0 8px 18px rgba(0,0,0,.26)}.card.loss{animation:wrongShake .22s linear 2;border-color:#ef7272}.card.tie{border-color:#ffd36a;box-shadow:0 0 0 4px rgba(255,211,106,.14),0 8px 18px rgba(0,0,0,.26)}
@keyframes deal{0%{opacity:0;transform:translateY(-28px) scale(.96)}100%{opacity:1;transform:none}}@keyframes flip{0%{transform:perspective(850px) rotateY(0deg) scale(1)}44%{transform:perspective(850px) rotateY(88deg) scale(.97)}50%{transform:perspective(850px) rotateY(92deg) scale(.97)}56%{transform:perspective(850px) rotateY(88deg) scale(.97)}100%{transform:perspective(850px) rotateY(0deg) scale(1)}}@keyframes winPulse{to{transform:translateY(-5px) scale(1.015);filter:brightness(1.05)}}@keyframes wrongShake{25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}
.card-title{position:absolute;top:7px;left:7px;right:7px;height:29px;font-weight:950;font-size:clamp(10px,1.05vw,14px);line-height:1.08;text-align:center;display:flex;align-items:center;justify-content:center;color:#172033;overflow:hidden;z-index:2}.structure-frame{position:absolute;left:7px;right:7px;top:39px;bottom:36px;display:flex;align-items:center;justify-content:center;min-width:0;min-height:0;overflow:hidden;background:#fff;border-radius:7px;z-index:1}.structure-frame img{display:block!important;width:100%!important;height:100%!important;min-width:100%!important;max-width:100%!important;object-fit:contain!important;margin:0!important;flex:none!important;background:#fff}.formula-fallback{width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:#fff;border-radius:7px;color:#182737;font-weight:950;font-size:clamp(18px,2vw,27px);padding:8px;text-align:center}.pka{position:absolute;left:7px;right:7px;bottom:8px;height:23px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:950;color:#5d4817;z-index:2}.pka.hidden{color:#8b7c5b}.estimate{position:absolute;left:7px;right:7px;bottom:1px;font-size:8px;color:#806c42;text-align:center;height:9px;z-index:2}.empty-card{width:100%;aspect-ratio:.72;border:2px dashed rgba(255,255,255,.28);border-radius:12px;display:flex;align-items:center;justify-content:center;color:rgba(255,255,255,.62);font-size:11px;font-weight:850;text-align:center;padding:8px}
.result-box{align-self:center;min-height:166px;border-radius:14px;background:rgba(255,255,255,.96);border:1px solid #d0dde4;box-shadow:0 4px 12px rgba(0,0,0,.17);padding:13px 15px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}.result-head{font-size:17px;font-weight:1000;color:#173d61;margin-bottom:6px}.result-head.win{color:#166534}.result-head.loss{color:#9f1239}.result-head.tie{color:#6b5b20}.capture-note{font-size:11px;font-weight:900;color:#294e68;margin:1px 0 7px}.result-detail{font-size:10px;line-height:1.35;color:#40586d;max-width:410px}.next-note{font-size:9px;color:#72879a;margin-top:7px}.war-pot{display:flex;flex-direction:column;align-items:center;justify-content:center;color:#fff;font-weight:950;font-size:9px;gap:3px}.pot-count{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#7c5a22;border:2px solid #d8b66a;font-size:14px;box-shadow:0 2px 7px rgba(0,0,0,.25)}
.hand-area{position:relative;display:grid;grid-template-columns:1fr 150px;gap:10px;align-items:end;margin-top:11px}.hand-wrap{min-width:0}.hand-title{font-size:11px;font-weight:950;color:#e1f0f5;margin:0 0 6px 3px}.hand{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:7px;height:clamp(165px,21vw,215px)}.hand-slot{min-width:0;min-height:0}.hand .card{height:100%;aspect-ratio:auto}.hand .card-title{font-size:clamp(9px,.92vw,12px);height:25px;top:6px}.hand .structure-frame{top:34px;bottom:32px}.hand .pka{bottom:6px}.player-piles .pile{color:#d7eaf5}.footer-note{text-align:center;color:#6f8b9b;font-size:9px;padding:0 12px 11px}.gameover{display:none;position:absolute;z-index:10;inset:0;background:rgba(4,13,20,.91);backdrop-filter:blur(5px);align-items:center;justify-content:center;padding:25px}.gameover.show{display:flex}.gameover-card{max-width:480px;width:100%;text-align:center;border:2px solid #57788d;border-radius:19px;background:linear-gradient(180deg,#173044,#0c1d29);box-shadow:0 24px 50px rgba(0,0,0,.5);padding:28px}.gameover-title{font-size:34px;font-weight:1000;margin-bottom:8px}.gameover-sub{color:#a8c1d0;line-height:1.45}.gameover-actions{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:18px}.primary{border:2px solid #915d12;background:linear-gradient(180deg,#ffe297,#dfa938);color:#352308;border-radius:12px;padding:12px;font-weight:1000;cursor:pointer}
.spark{position:absolute;width:7px;height:7px;border-radius:50%;background:#fff4b5;box-shadow:0 0 7px #fff,0 0 16px #ffe089;pointer-events:none;animation:spark .72s ease-out forwards}@keyframes spark{to{transform:translate(var(--dx),var(--dy)) scale(.1);opacity:0}}
@media(max-width:900px){.setup-grid{grid-template-columns:1fr}.hero-copy{max-width:none}.table-grid{grid-template-columns:120px minmax(135px,180px) minmax(190px,1fr) minmax(135px,180px) 50px}.hand-area{grid-template-columns:1fr 120px}.deck-stack{width:44px;height:62px}}
@media(max-width:680px){#app{padding:7px}.topbar{margin-bottom:7px}.brandmark{width:37px;height:37px}.brand h1{font-size:18px}.brand small{display:none}.ghost{min-height:40px;padding:8px 10px}.sound-btn{min-width:42px}.sound-label{display:none}.setup{padding:17px 12px}.choice-row.three{grid-template-columns:1fr}.hud{grid-template-columns:1fr auto;padding:8px}.battle-title{display:none}.hud-left,.hud-right{gap:4px}.hud-right{justify-content:flex-end}.pill{font-size:9px;padding:5px 7px}.table{margin:7px;padding:8px;min-height:0}.table-grid{grid-template-columns:72px minmax(112px,1fr) minmax(135px,1.15fr) 38px;grid-template-areas:"cpiles cpu result pot";gap:5px;min-height:230px}.cpu-piles{grid-area:cpiles;grid-template-columns:1fr;gap:3px}.cpu-card-holder{grid-area:cpu}.result-box{grid-area:result;min-height:122px;padding:8px}.player-center-holder{display:none}.war-pot{grid-area:pot}.deck-stack{width:32px;height:45px}.pile-count{font-size:11px}.pile-label{font-size:8px}.card{padding:4px;border-radius:9px}.card-title{font-size:9px;height:21px;top:4px;left:4px;right:4px}.structure-frame{left:4px;right:4px;top:28px;bottom:29px}.pka{left:4px;right:4px;bottom:5px;font-size:10px;height:19px}.estimate{left:4px;right:4px;bottom:0;font-size:7px}.hand .structure-frame{top:28px;bottom:29px}.hand .card-title{top:4px;height:21px}.result-head{font-size:12px}.capture-note,.result-detail{font-size:8.5px}.next-note{display:none}.hand-area{display:block;margin-top:8px}.player-piles{display:none}.hand{display:flex;height:166px;overflow-x:auto;gap:7px;scroll-snap-type:x mandatory;padding:0 2px 5px}.hand-slot{flex:0 0 132px;scroll-snap-align:start}.hand .card-title{font-size:9px}.hand-title{font-size:10px}.footer-note{padding-bottom:8px}.gameover-actions{grid-template-columns:1fr}}
.entry{padding:clamp(20px,4vw,48px);position:relative;z-index:2}
.entry-actions{display:grid;gap:11px}.entry-btn{width:100%;border:1px solid #49697e;border-radius:14px;background:#102b3b;color:#e7f4fb;padding:16px 14px;text-align:left;cursor:pointer;box-shadow:inset 0 -3px 0 rgba(0,0,0,.18);transition:.14s ease}.entry-btn:hover{transform:translateY(-2px);filter:brightness(1.08)}.entry-btn strong{display:block;font-size:17px;letter-spacing:.02em}.entry-btn span{display:block;color:#9db9c9;font-size:12px;margin-top:4px;line-height:1.4}.entry-btn.primary-entry{background:linear-gradient(180deg,#193f56,#102b3b);border-color:#6aa8cc}.entry-btn.guest-entry{background:#12242f}.disabled-look{opacity:.68}
.auth-panel{display:none}.auth-note{font-size:12px;line-height:1.45;color:#a9c4d3;background:#0e202d;border:1px solid #37566a;border-radius:11px;padding:10px 11px;margin-bottom:11px}.auth-note b{color:#fff}.form-label{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.10em;color:#84b5d0;font-weight:950;margin:10px 0 6px}.auth-input{width:100%;border:1px solid #44687d;border-radius:11px;background:#071821;color:#eef8fd;padding:13px 12px;font-size:16px;outline:none}.auth-input:focus{border-color:#7cc8f1;box-shadow:0 0 0 3px rgba(120,199,255,.12)}.pin-input{letter-spacing:.35em;font-weight:950}.auth-buttons{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:12px}.auth-buttons button{min-height:48px}.auth-message{min-height:19px;margin-top:9px;font-size:11px;color:#a9c4d3}.auth-message.error{color:#ff9b9b}.auth-message.working{color:#ffd36a}.tiny-link{margin-top:9px;border:0;background:transparent;color:#9fc8dd;text-decoration:underline;cursor:pointer;padding:4px 0;font-weight:750}.config-note{display:none;margin-top:11px;padding:9px 10px;border:1px solid #7a6135;border-radius:10px;background:#2a2112;color:#e5c985;font-size:11px;line-height:1.4}
.mode-chip{display:inline-flex;align-items:center;gap:7px;margin-top:12px;border:1px solid #486a7e;border-radius:999px;background:#0c1d28;padding:8px 11px;color:#9db8c8;font-size:12px}.mode-chip b{color:#fff}.setup-status{min-height:18px;color:#ffab8f;font-size:11px;margin-top:8px;line-height:1.3}.profile-stats{font-size:10px;color:#9cc6dc;margin-left:5px}.saved-note{color:#9bb7c7;font-size:11px}
.strategy-feedback{margin-top:8px;border-radius:9px;padding:8px 9px;font-size:10.5px;line-height:1.4;font-weight:700}.strategy-feedback.good{border:1px solid rgba(114,228,154,.65);background:#183a28;color:#d8ffe4}.strategy-feedback.bad{border:2px solid #ffd36a;background:#302307;color:#fff9e8;box-shadow:inset 0 0 0 1px rgba(255,255,255,.04)}.strategy-feedback.bad .strategy-label{display:block;color:#ffe38a;font-weight:1000;letter-spacing:.04em;margin-bottom:2px}
.lb-overlay{position:fixed;inset:0;z-index:100;background:rgba(2,8,12,.78);display:none;align-items:center;justify-content:center;padding:14px}.lb-overlay.show{display:flex}.lb-card{width:min(720px,96vw);max-height:88vh;overflow:auto;border:2px solid #4c6b80;border-radius:20px;background:linear-gradient(180deg,#142b3a,#081721);box-shadow:0 24px 60px rgba(0,0,0,.55);padding:16px}.lb-top{display:flex;justify-content:space-between;gap:10px;align-items:center}.lb-title{font-size:23px;font-weight:1000}.lb-sub{color:#8faabb;font-size:11px;margin-top:3px}.lb-controls{display:flex;gap:7px}.lb-tabs{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:14px 0 10px}.lb-tab{border:1px solid #416076;background:#0d202c;color:#b8cfdb;border-radius:11px;padding:11px;font-weight:900;cursor:pointer}.lb-tab.active{background:#d5edf9;color:#09283a;border-color:#8acdf2}.leaderboard-loading,.leaderboard-empty{padding:30px 12px;text-align:center;color:#9fb6c5}.lb-row{display:grid;grid-template-columns:42px 1fr 95px 100px;gap:8px;align-items:center;padding:9px 8px;border-bottom:1px solid rgba(118,153,174,.17);font-size:13px}.lb-row span:nth-child(3),.lb-row span:nth-child(4){text-align:right;font-variant-numeric:tabular-nums}.lb-row.lb-head{color:#89aabd;text-transform:uppercase;font-size:10px;font-weight:950;letter-spacing:.08em}.lb-row.mine{background:rgba(120,199,255,.09);border-radius:8px}.lb-row small{color:#77c8f8;font-weight:900}.lb-foot{margin-top:10px;color:#809cac;font-size:10px;line-height:1.4}
.a11y-overlay{position:fixed;inset:0;z-index:120;background:rgba(2,8,12,.82);display:none;align-items:center;justify-content:center;padding:14px}.a11y-overlay.show{display:flex}.a11y-card{width:min(680px,96vw);max-height:90vh;overflow:auto;border:2px solid #5f8195;border-radius:20px;background:linear-gradient(180deg,#142b3a,#081721);box-shadow:0 24px 60px rgba(0,0,0,.58);padding:20px}.a11y-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px}.a11y-title{font-size:24px;font-weight:1000}.a11y-copy{color:#b7cbd7;line-height:1.55;font-size:14px}.a11y-list{padding-left:22px;color:#c6d9e4;line-height:1.55}.a11y-controls{display:grid;gap:10px;margin-top:16px}.a11y-toggle{display:flex;justify-content:space-between;align-items:center;gap:14px;width:100%;border:1px solid #55788d;background:#0c202c;color:#e5f1f7;border-radius:12px;padding:13px 14px;text-align:left;cursor:pointer}.a11y-toggle strong{display:block}.a11y-toggle span{color:#a9c4d3;font-size:11px;line-height:1.35}.toggle-state{flex:none;border-radius:999px;padding:5px 9px;background:#253d4b;color:#fff!important;font-weight:950}.a11y-toggle[aria-pressed="true"] .toggle-state{background:#d5edf9;color:#09283a!important}.next-trick-wrap{margin-top:9px}.next-trick-btn{width:100%;min-height:44px}.reduce-motion *,html.reduce-motion *{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important;scroll-behavior:auto!important}.reduce-motion .spark,html.reduce-motion .spark{display:none!important}
@media(max-width:680px){.topbar{flex-wrap:wrap}.top-actions{width:100%;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px}.top-actions .ghost{width:100%;min-width:0}.top-actions #profile{max-width:none;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.entry{padding:17px 12px}.auth-buttons{grid-template-columns:1fr}.lb-overlay{padding:7px}.lb-card{padding:12px;border-radius:15px;max-height:92vh}.lb-title{font-size:19px}.lb-row{grid-template-columns:30px 1fr 64px 70px;font-size:11px;padding:8px 4px}.lb-controls .sound-label{display:none}.profile-stats{display:none}.strategy-feedback{font-size:10px;padding:7px 8px}}
@media(max-width:680px){.a11y-card{padding:15px;border-radius:15px}.a11y-title{font-size:20px}.a11y-copy,.a11y-list{font-size:13px}}
</style>
</head>
<body>
<div id="srAnnouncer" class="sr-only" role="status" aria-live="polite" aria-atomic="true"></div>
<main id="app">
  <header class="topbar">
    <div class="brand"><div class="brandmark">⚗️</div><div><h1>ACID BATTLE</h1><small>Physical Organic Chemistry</small></div></div>
    <div class="top-actions">
      <button class="ghost" id="profile" style="display:none" title="Switch player"></button>
      <button type="button" class="ghost" id="leaderboardBtn" aria-haspopup="dialog">🏆 Leaderboards</button>
      <button type="button" class="ghost" id="accessibilityBtn" aria-haspopup="dialog">♿ Accessibility</button>
      <button type="button" class="ghost sound-btn" id="sound" aria-label="Mute sound"><span class="sound-icon" id="soundIcon">🔊</span> <span class="sound-label" id="soundLabel">Sound on</span></button>
      <button type="button" class="ghost" id="fullscreen" aria-label="Enter full screen">⛶ Full screen</button>
    </div>
  </header>

  <div class="machine">
    <div class="rivets"></div>
    <section class="entry" id="entry" aria-labelledby="entryTitle">
      <div class="setup-grid">
        <div>
          <div class="hero-kicker">Physical organic chemistry</div>
          <h2 class="hero-title" id="entryTitle">ACID<br>BATTLE</h2>
          <div class="hero-copy">Play freely as a guest, or create a player profile to save your wins and optimal-move strategy record to the class leaderboards.</div>
          <div class="rule-chip"><b>LOWER pKa WINS</b><span>•</span><span>play smart, not just strong</span></div>
        </div>
        <div class="console">
          <div class="screen">
            <div id="entryChoices">
              <div class="screen-title">Choose how to play</div>
              <div class="entry-actions">
                <button type="button" class="entry-btn guest-entry" id="entryGuest"><strong>PLAY AS GUEST</strong><span>Practice normally. Strategy feedback is shown, but nothing is saved.</span></button>
                <button type="button" class="entry-btn primary-entry" id="entryPlayer"><strong>SIGN IN / CREATE PLAYER</strong><span>Save wins and optimal-move percentage to the class leaderboards.</span></button>
              </div>
              <div class="config-note" id="leaderboardConfigNote">Player accounts are not configured yet on this deployment. Guest play is available.</div>
            </div>
            <div class="auth-panel" id="authPanel" aria-labelledby="authTitle">
              <div class="screen-title" id="authTitle">Player profile</div>
              <div class="auth-note" id="authHelp">Use a <b>nickname</b>, not your full name. <b>Remember your nickname and 4-digit PIN.</b> You need both to return to the same score record. There is no PIN recovery.</div>
              <label class="form-label" for="nicknameInput">Nickname</label>
              <input class="auth-input" id="nicknameInput" maxlength="20" autocomplete="username" aria-describedby="authHelp authMessage" placeholder="e.g. AcidMaster">
              <label class="form-label" for="pinInput">4-digit PIN</label>
              <input class="auth-input pin-input" id="pinInput" maxlength="4" inputmode="numeric" aria-describedby="authHelp authMessage" pattern="[0-9]*" autocomplete="current-password" type="password" placeholder="••••">
              <div class="auth-buttons"><button class="ghost" id="signIn">SIGN IN</button><button class="start" id="createPlayer" style="margin-top:0">CREATE PLAYER</button></div>
              <div class="auth-message" id="authMessage" role="status" aria-live="polite" aria-atomic="true"></div>
              <button type="button" class="tiny-link" id="authBack">← Back to Guest / Player choice</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="setup" id="setup" style="display:none" aria-labelledby="setupTitle">
      <div class="setup-grid">
        <div>
          <div class="hero-kicker">War-style pKa card game</div>
          <h2 class="hero-title" id="setupTitle">Choose your hand.<br>Capture the deck.</h2>
          <div class="hero-copy">The computer reveals an acid. You choose one acid from your five-card hand to fight it. The lower pKa wins the trick and captures the cards. Each acid type starts with one copy on each side, so both players begin with the same chemistry deck.</div>
          <div class="rule-chip"><b>LOWER pKa WINS</b><span>•</span><span>ties build the war pot</span></div>
          <div class="mode-chip" id="modeChip"></div>
        </div>
        <div class="console">
          <div class="screen">
            <div class="screen-title" id="solventLabel">Solvent / pKa scale</div>
            <div class="choice-row" role="group" aria-labelledby="solventLabel">
              <button type="button" class="select-btn active" data-solvent="water" aria-pressed="true">H₂O<span>water reference scale</span></button>
              <button type="button" class="select-btn" data-solvent="dmso" aria-pressed="false">DMSO<span>DMSO reference scale</span></button>
            </div>
            <div class="separator"></div>
            <div class="screen-title" id="deckLabel">Acid deck</div>
            <div class="choice-row three" role="group" aria-labelledby="deckLabel">
              <button type="button" class="select-btn active" data-deck="25" aria-pressed="true">25 acids<span>core deck</span></button>
              <button type="button" class="select-btn" data-deck="50" aria-pressed="false">50 acids<span>extended deck</span></button>
              <button type="button" class="select-btn" data-deck="all" aria-pressed="false">WHOLE LIST<span id="allCount">63 acids</span></button>
            </div>
            <div class="pool-note" id="poolNote">Every selected acid appears once in the physical battle deck. An odd-sized deck is split as evenly as possible.</div>
            <button type="button" class="start" id="start">DEAL THE CARDS</button>
            <div class="setup-status" id="setupStatus" role="status" aria-live="polite"></div>
          </div>
        </div>
      </div>
    </section>

    <section class="battle" id="battle" aria-label="Acid Battle game">
      <div class="hud" aria-label="Game status">
        <div class="hud-left">
          <span class="pill"><b id="solventHud">H₂O</b></span>
          <span class="pill"><b id="deckHud">25</b> cards</span>
          <span class="pill">Trick <b id="trickHud">1</b></span>
          <span class="pill">War pot <b id="potHud">0</b></span>
          <span class="pill">Player <b id="playerHud">Guest</b></span>
          <span class="pill">Strategy <b id="strategyHud">—</b></span>
        </div>
        <div class="battle-title">LOWER pKa WINS • CAPTURE THE WHOLE DECK</div>
        <div class="hud-right"><button type="button" class="ghost" id="change">Change deck</button></div>
      </div>

      <div class="table" id="table">
        <div class="table-grid">
          <div class="pile-cluster cpu-piles">
            <div class="pile"><div class="deck-stack"><div class="deck-card"></div><div class="deck-card"></div><div class="deck-card"></div></div><div class="pile-count" id="cpuDrawCount">0</div><div class="pile-label">CPU DRAW</div></div>
            <div class="pile won"><div class="deck-stack"><div class="deck-card"></div><div class="deck-card"></div><div class="deck-card"></div></div><div class="pile-count" id="cpuWonCount">0</div><div class="pile-label">CPU WON</div></div>
          </div>
          <div class="cpu-card-holder" id="cpuCard"></div>
          <div class="result-box" id="resultBox" role="status" aria-live="polite" aria-atomic="true" tabindex="-1"></div>
          <div class="player-center-holder" id="playerCenter"></div>
          <div class="war-pot"><div class="pot-count" id="potCount">0</div><div>WAR POT</div></div>
        </div>

        <div class="hand-area">
          <div class="hand-wrap"><div class="hand-title" id="handLabel">YOUR HAND — CHOOSE ONE CARD</div><div class="hand" id="hand" role="group" aria-labelledby="handLabel"></div></div>
          <div class="pile-cluster player-piles">
            <div class="pile"><div class="deck-stack"><div class="deck-card"></div><div class="deck-card"></div><div class="deck-card"></div></div><div class="pile-count" id="drawCount">0</div><div class="pile-label">YOUR DRAW</div></div>
            <div class="pile won"><div class="deck-stack"><div class="deck-card"></div><div class="deck-card"></div><div class="deck-card"></div></div><div class="pile-count" id="wonCount">0</div><div class="pile-label">YOUR WON</div></div>
          </div>
        </div>

        <div class="gameover" id="gameover" role="dialog" aria-modal="true" aria-labelledby="gameoverTitle"><div class="gameover-card" tabindex="-1" id="gameoverCard"><div class="gameover-title" id="gameoverTitle"></div><div class="gameover-sub" id="gameoverSub"></div><div class="gameover-actions"><button type="button" class="primary" id="again">BATTLE AGAIN</button><button type="button" class="ghost" id="newDeck">CHANGE DECK</button></div></div></div>
      </div>
      <div class="footer-note">pKa values are revealed only after you commit a card. Close values within 0.20 pKa units are treated as a tie.</div>
    </section>

    <div class="lb-overlay" id="leaderboardModal" role="dialog" aria-modal="true" aria-labelledby="leaderboardTitle">
      <div class="lb-card" tabindex="-1" id="leaderboardCard">
        <div class="lb-top">
          <div><div class="lb-title" id="leaderboardTitle">Acid Battle Leaderboards</div><div class="lb-sub">Wins and strategy are tracked separately.</div></div>
          <div class="lb-controls"><button type="button" class="ghost" id="leaderboardRefresh" aria-label="Refresh leaderboard">↻</button><button type="button" class="ghost" id="leaderboardClose" aria-label="Close leaderboards">✕</button></div>
        </div>
        <div class="lb-tabs" role="tablist" aria-label="Leaderboard type"><button type="button" class="lb-tab active" role="tab" aria-selected="true" data-lb="wins">🏆 WINS</button><button type="button" class="lb-tab" role="tab" aria-selected="false" data-lb="strategy">🎯 STRATEGY</button></div>
        <div id="leaderboardBody"></div>
        <div class="lb-foot">Strategy ranks optimal-move percentage and requires at least 20 recorded moves. Moves are recorded as they are played, including moves from unfinished games. A win counts only when a game is completed.</div>
      </div>
    </div>

    <div class="a11y-overlay" id="accessibilityModal" role="dialog" aria-modal="true" aria-labelledby="accessibilityTitle">
      <div class="a11y-card" id="accessibilityCard" tabindex="-1">
        <div class="a11y-head">
          <div><div class="a11y-title" id="accessibilityTitle">Accessibility</div><div class="lb-sub">Options for keyboard, motion, audio, zoom, and result timing.</div></div>
          <button type="button" class="ghost" id="accessibilityClose" aria-label="Close accessibility options">✕</button>
        </div>
        <div class="a11y-copy">Acid Battle is designed to be playable without a mouse. All game information is provided in text as well as visually or by sound.</div>
        <ul class="a11y-list">
          <li>Use <b>Tab</b> or <b>Shift+Tab</b> to move between controls and acid cards.</li>
          <li>Use <b>Enter</b> or <b>Space</b> to play a focused acid card.</li>
          <li>Sound is optional and can be muted from the top bar.</li>
          <li>Browser zoom and pinch-to-zoom are supported.</li>
          <li>Correct, incorrect, tie, and strategy results are always written in text; color and sound are not the only cues.</li>
          <li>Reduce motion is OFF by default. Turn it ON here if you prefer fewer animations.</li>
        </ul>
        <div class="a11y-controls">
          <button type="button" class="a11y-toggle" id="motionToggle" aria-pressed="false"><span><strong>Reduce motion</strong>ON removes card flips, shakes, sparks, and most transitions. OFF restores full game animation.</span><span class="toggle-state" id="motionState">OFF</span></button>
          <button type="button" class="a11y-toggle" id="manualToggle" aria-pressed="false"><span><strong>Manual result advance</strong>Keep each result on screen until you choose Next trick.</span><span class="toggle-state" id="manualState">OFF</span></button>
        </div>
        <div class="a11y-copy" style="margin-top:15px">If you encounter an accessibility problem, contact your course instructor so an alternative can be provided.</div>
      </div>
    </div>
  </div>
</main>

<script>
(function(){
const args=__ACID_BATTLE_DATA__;
let solvent='water', deckChoice='25', pool=[];
let hand=[], playerDraw=[], playerWon=[], cpuDraw=[], cpuWon=[], cpuCurrent=null, warPot=[];
let turn=0, waiting=false, gameOver=false, timer=null, audioCtx=null, muted=false, lastPlayed=null;
let reduceMotion=false, manualAdvance=false, modalReturnFocus=null;
let playerMode='entry', playerNickname='', sessionToken='', currentGameId=null;
let gameMoves=0, gameOptimal=0, pendingMoves=new Map(), movePromises=new Set();
let persistentStats={wins:0,moves:0,optimal_moves:0,optimal_pct:null};
let leaderboardRows=[], leaderboardMode='wins';
const HAND_SIZE=5, TIE_TOL=0.20, HOLD_MS=3600, STRATEGY_MIN=20;
const $=id=>document.getElementById(id);
function send(type,data){window.parent.postMessage(Object.assign({isStreamlitMessage:true,type:type},data||{}),'*')}
function setHeight(){setTimeout(()=>send('streamlit:setFrameHeight',{height:Math.max(document.body.scrollHeight+6,620)}),20)}
function announce(text){const a=$('srAnnouncer');if(!a)return;a.textContent='';setTimeout(()=>{a.textContent=String(text||'')},20)}
function readPref(key){try{return localStorage.getItem(key)}catch(e){return null}}
function writePref(key,val){try{localStorage.setItem(key,val?'1':'0')}catch(e){}}
function loadAccessibilityPrefs(){const r=readPref('acidBattleReduceMotion'),m=readPref('acidBattleManualAdvance');reduceMotion=r==='1';manualAdvance=m==='1';applyAccessibilityPrefs()}
function applyAccessibilityPrefs(){document.documentElement.classList.toggle('reduce-motion',reduceMotion);$('motionToggle').setAttribute('aria-pressed',reduceMotion?'true':'false');$('motionState').textContent=reduceMotion?'ON':'OFF';$('manualToggle').setAttribute('aria-pressed',manualAdvance?'true':'false');$('manualState').textContent=manualAdvance?'ON':'OFF'}
function toggleMotion(){reduceMotion=!reduceMotion;writePref('acidBattleReduceMotion',reduceMotion);applyAccessibilityPrefs();announce('Reduce motion '+(reduceMotion?'on':'off'))}
function toggleManual(){manualAdvance=!manualAdvance;writePref('acidBattleManualAdvance',manualAdvance);applyAccessibilityPrefs();announce('Manual result advance '+(manualAdvance?'on':'off'))}
function openAccessibility(){modalReturnFocus=document.activeElement;$('accessibilityModal').classList.add('show');$('accessibilityCard').focus();setHeight()}
function closeAccessibility(){$('accessibilityModal').classList.remove('show');if(modalReturnFocus&&modalReturnFocus.focus)modalReturnFocus.focus();setHeight()}
function esc(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function shuffle(a){for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a}
function apiReady(){return !!(args.supabase_url&&args.supabase_key&&args.course_code)}
function loadSoundPref(){try{muted=localStorage.getItem('acidBattleMuted')==='1'}catch(e){muted=false}updateSoundButton()}
function updateSoundButton(){const b=$('sound');b.classList.toggle('muted',muted);b.setAttribute('aria-pressed',muted?'true':'false');b.title=muted?'Turn sound on':'Mute sound';b.setAttribute('aria-label',muted?'Turn sound on':'Mute sound');$('soundIcon').textContent=muted?'🔇':'🔊';$('soundLabel').textContent=muted?'Muted':'Sound on'}
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

async function rpc(name,body,keepalive=false){
  if(!apiReady())throw new Error('Leaderboard service is not configured.');
  const headers={'Content-Type':'application/json','Accept':'application/json','apikey':args.supabase_key};
  if(String(args.supabase_key).split('.').length===3)headers['Authorization']='Bearer '+args.supabase_key;
  const response=await fetch(String(args.supabase_url).replace(/\/$/,'')+'/rest/v1/rpc/'+name,{method:'POST',headers,body:JSON.stringify(body||{}),keepalive:!!keepalive});
  const raw=await response.text();
  let data=null;
  if(raw){try{data=JSON.parse(raw)}catch(e){data=raw}}
  if(!response.ok){const detail=(data&&data.message)||raw||('HTTP '+response.status);throw new Error(detail)}
  if(typeof data==='string'&&data.trim().startsWith('{')){try{data=JSON.parse(data)}catch(e){}}
  return data;
}
function setAuthMessage(text,kind=''){const box=$('authMessage');box.textContent=text||'';box.className='auth-message'+(kind?' '+kind:'')}
function savedNickname(){try{return localStorage.getItem('acidBattleNickname')||''}catch(e){return ''}}
function saveNickname(n){try{localStorage.setItem('acidBattleNickname',n)}catch(e){}}
function clientNicknameAllowed(name){
  const n=String(name||'').trim();
  if(n.length<3||n.length>20||!/^[A-Za-z0-9 _-]+$/.test(n))return false;
  let x=n.toLowerCase().replace(/[^a-z0-9]/g,'').replace(/0/g,'o').replace(/1/g,'i').replace(/3/g,'e').replace(/4/g,'a').replace(/5/g,'s').replace(/7/g,'t');
  if(/(fuck|shit|cunt|nigg|fagg|bitch|whore|slut|penis|vagina|pussy|cock)/.test(x))return false;
  if(['admin','administrator','professor','instructor','teacher','moderator'].includes(x))return false;
  return true;
}
function authErrorMessage(code){
  const map={nickname_taken:'That nickname is already in use. Sign in if it is yours, or choose another nickname.',nickname_not_allowed:'Please choose a different nickname.',pin_invalid:'The PIN must be exactly 4 digits.',invalid_login:'Nickname or PIN is incorrect.',session_expired:'Your player session expired. Please sign in again.',course_not_configured:'The course leaderboard is not configured.',game_settings_invalid:'Those game settings could not be saved.'};
  return map[code]||'Could not connect to the leaderboard. Please try again.';
}
function showAuth(){
  $('entryChoices').style.display='none';$('authPanel').style.display='block';
  $('nicknameInput').value=savedNickname();$('pinInput').value='';setAuthMessage('');$('nicknameInput').focus();setHeight();
}
function hideAuth(){$('authPanel').style.display='none';$('entryChoices').style.display='block';setAuthMessage('');setHeight()}
function updateModeUI(){
  const chip=$('modeChip'),profile=$('profile');
  if(playerMode==='player'){
    chip.innerHTML='<b>'+esc(playerNickname)+'</b><span>• scores saved</span>';
    profile.style.display='inline-flex';profile.innerHTML='👤 '+esc(playerNickname)+' <span class="profile-stats">🏆 '+Number(persistentStats.wins||0)+' · 🎯 '+(persistentStats.optimal_pct==null?'—':persistentStats.optimal_pct+'%')+'</span>';
  }else if(playerMode==='guest'){
    chip.innerHTML='<b>Guest</b><span>• practice only — scores are not saved</span>';
    profile.style.display='inline-flex';profile.innerHTML='👤 Guest';
  }else profile.style.display='none';
}
function goToSetup(){
  $('entry').style.display='none';$('battle').style.display='none';$('setup').style.display='block';$('gameover').classList.remove('show');updateModeUI();refreshDeckControls();setHeight();
}
function enterGuest(){playerMode='guest';playerNickname='';sessionToken='';currentGameId=null;persistentStats={wins:0,moves:0,optimal_moves:0,optimal_pct:null};goToSetup()}
function enterPlayer(data){
  playerMode='player';playerNickname=data.nickname||$('nicknameInput').value.trim();sessionToken=data.session_token||'';currentGameId=null;
  persistentStats={wins:Number(data.wins||0),moves:Number(data.moves||0),optimal_moves:Number(data.optimal_moves||0),optimal_pct:data.optimal_pct==null?null:Number(data.optimal_pct)};
  saveNickname(playerNickname);goToSetup();
}
async function authPlayer(action){
  if(!apiReady()){setAuthMessage('Leaderboard setup is incomplete. Guest play is still available.','error');return}
  const nickname=$('nicknameInput').value.trim(),pin=$('pinInput').value.trim();
  if(!clientNicknameAllowed(nickname)){setAuthMessage('Use 3–20 letters/numbers/spaces/_/-. Please choose an appropriate nickname.','error');return}
  if(!/^\d{4}$/.test(pin)){setAuthMessage('Enter a 4-digit PIN.','error');return}
  $('signIn').disabled=true;$('createPlayer').disabled=true;setAuthMessage(action==='create'?'Creating player…':'Signing in…','working');
  try{
    const fn=action==='create'?'acid_create_player':'acid_login_player';
    const data=await rpc(fn,{p_course_code:args.course_code,p_nickname:nickname,p_pin:pin});
    if(!data||data.ok!==true){setAuthMessage(authErrorMessage(data&&data.error),'error');return}
    enterPlayer(data);
  }catch(e){setAuthMessage('Could not reach the leaderboard. '+e.message,'error')}
  finally{$('signIn').disabled=false;$('createPlayer').disabled=false;setHeight()}
}
function switchPlayer(){
  if(timer){clearTimeout(timer);timer=null} waiting=false;gameOver=false;currentGameId=null;playerMode='entry';playerNickname='';sessionToken='';
  $('battle').style.display='none';$('setup').style.display='none';$('entry').style.display='block';$('gameover').classList.remove('show');$('profile').style.display='none';hideAuth();setHeight();
}
async function refreshMyStats(){
  if(playerMode!=='player'||!sessionToken)return;
  try{const d=await rpc('acid_my_stats',{p_course_code:args.course_code,p_session_token:sessionToken});if(d&&d.ok){persistentStats={wins:Number(d.wins||0),moves:Number(d.moves||0),optimal_moves:Number(d.optimal_moves||0),optimal_pct:d.optimal_pct==null?null:Number(d.optimal_pct)};updateModeUI()}}
  catch(e){}
}

function currentList(){return solvent==='water'?(args.water||[]):(args.dmso||[])}
function buildPool(){const list=currentList();if(deckChoice==='all'){pool=list.slice();return}const n=Math.min(Number(deckChoice),list.length);pool=shuffle(list.slice()).slice(0,n)}
function refreshDeckControls(){const n=currentList().length;document.querySelectorAll('[data-deck]').forEach(b=>{const need=b.dataset.deck==='all'?0:Number(b.dataset.deck),disabled=need>n;b.disabled=disabled;b.classList.toggle('disabled',disabled);b.setAttribute('aria-disabled',disabled?'true':'false')});$('allCount').textContent=n+' acids';if((deckChoice==='25'&&n<25)||(deckChoice==='50'&&n<50))deckChoice='all';document.querySelectorAll('[data-deck]').forEach(b=>{const active=b.dataset.deck===deckChoice;b.classList.toggle('active',active);b.setAttribute('aria-pressed',active?'true':'false')});const selected=(deckChoice==='all')?n:Number(deckChoice);$('poolNote').textContent=(n<25?'This solvent currently has '+n+' reference acids, so the whole-list deck is used. ':'')+selected+' acid types = '+(selected*2)+' physical cards. For 25- and 50-acid games, a new random set of acid types is chosen for every battle. Both sides receive the same selected acid set, then the decks are shuffled independently.'}
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
function cardValue(c){return c?(c.pka==null?Number(c.pka_sort):Number(c.pka)):Infinity}
function wouldWin(c,opp){if(!c||!opp)return false;if(c.pka!=null&&opp.pka!=null)return Number(c.pka)<Number(opp.pka)-TIE_TOL-1e-12;return cardValue(c)<cardValue(opp)}
function analyzeOptimal(cards,opp,chosenId){
  const winners=cards.filter(c=>wouldWin(c,opp));const candidates=winners.length?winners:cards.slice();
  if(!candidates.length)return{optimal:true,best:[],canWin:false};
  const bestValue=Math.max(...candidates.map(cardValue));const best=candidates.filter(c=>Math.abs(cardValue(c)-bestValue)<1e-9);
  return{optimal:best.some(c=>c.instance_id===chosenId),best,canWin:winners.length>0};
}
function strategyHtml(a){
  if(!a)return'';
  if(a.optimal)return'<div class="strategy-feedback good">🎯 Optimal move</div>';
  const b=a.best&&a.best[0];if(!b)return'';
  const why=a.canWin?'weakest acid in your hand that still wins':'best sacrifice: least acidic card in your hand';
  return'<div class="strategy-feedback bad"><span class="strategy-label">⚠ NOT OPTIMAL</span>Best play was <b>'+esc(b.name)+'</b> (pKa '+esc(pkaText(b))+') — '+why+'.</div>';
}
function cardNode(card,kind='hand',reveal=false,selectable=false){
  if(!card){const e=document.createElement('div');e.className='empty-card';e.textContent='card played';e.setAttribute('aria-hidden','true');return e}
  const el=document.createElement('div');el.className='card '+(kind||'')+(selectable?' selectable':'');el.dataset.id=card.instance_id||'';
  const label=(card.name||'Acid')+(reveal?(', pKa '+pkaText(card)+(card.estimated?', estimated or extrapolated':'')):', pKa hidden')+(selectable?'. Press Enter or Space to play this card.':'');
  el.setAttribute('aria-label',label);
  if(selectable){el.setAttribute('role','button');el.tabIndex=0;el.onclick=()=>playCard(card.instance_id,el);el.addEventListener('keydown',e=>{if((e.key==='Enter'||e.key===' ')&&!e.repeat){e.preventDefault();playCard(card.instance_id,el)}})}
  const t=document.createElement('div');t.className='card-title';t.textContent=card.name||'';el.appendChild(t);
  const sf=document.createElement('div');sf.className='structure-frame';if(card.image){const img=document.createElement('img');img.src=card.image;img.alt='';img.setAttribute('aria-hidden','true');img.draggable=false;sf.appendChild(img)}else{const f=document.createElement('div');f.className='formula-fallback';f.textContent=formula(card);f.setAttribute('aria-hidden','true');sf.appendChild(f)}el.appendChild(sf);
  const p=document.createElement('div');p.className='pka'+(reveal?'':' hidden');p.textContent=reveal?('pKa '+pkaText(card)):'pKa ?';el.appendChild(p);const est=document.createElement('div');est.className='estimate';est.textContent=reveal&&card.estimated?'* estimated / extrapolated':'';el.appendChild(est);return el
}
function renderPiles(){$('drawCount').textContent=playerDraw.length;$('wonCount').textContent=playerWon.length;$('cpuDrawCount').textContent=cpuDraw.length;$('cpuWonCount').textContent=cpuWon.length;$('potCount').textContent=warPot.length;$('potHud').textContent=warPot.length;$('trickHud').textContent=turn+1;$('strategyHud').textContent=gameMoves?Math.round(100*gameOptimal/gameMoves)+'%':'—'}
function renderIdle(){renderPiles();const cpu=$('cpuCard');cpu.innerHTML='';const node=cardNode(cpuCurrent,'cpu',false,false);node.classList.add('deal');cpu.appendChild(node);setTimeout(()=>node.classList.remove('deal'),350);const pc=$('playerCenter');pc.innerHTML='';pc.appendChild(cardNode(null));const rb=$('resultBox');rb.innerHTML='<div class="result-head">Computer has played</div><div class="result-detail">Choose the acid you want to commit. If you can win, conserve strength by using the weakest acid that still wins; if you cannot win, sacrifice your least acidic card.</div>';const h=$('hand');h.innerHTML='';hand.forEach(c=>{const slot=document.createElement('div');slot.className='hand-slot';slot.appendChild(cardNode(c,'hand',false,true));h.appendChild(slot)});while(h.children.length<HAND_SIZE){const slot=document.createElement('div');slot.className='hand-slot';slot.appendChild(cardNode(null));h.appendChild(slot)}sfxDeal();flushPendingMoves();announce('Computer played '+(cpuCurrent?cpuCurrent.name:'an acid')+'. Choose a card from your hand.');setHeight()}
function renderResult(player,opp,winner,delta,captureCount,analysis){renderPiles();const cpu=$('cpuCard');cpu.innerHTML='';const cn=cardNode(opp,'cpu',true,false);cn.classList.add('flip');cpu.appendChild(cn);const pc=$('playerCenter');pc.innerHTML='';const pn=cardNode(player,'player-center',true,false);pn.classList.add('flip');pc.appendChild(pn);const h=$('hand');h.innerHTML='';hand.forEach(c=>{const slot=document.createElement('div');slot.className='hand-slot';const n=cardNode(c,'hand',false,false);n.classList.add('locked');slot.appendChild(n);h.appendChild(slot)});while(h.children.length<HAND_SIZE){const slot=document.createElement('div');slot.className='hand-slot';slot.appendChild(cardNode(null));h.appendChild(slot)};sfxFlip();setTimeout(()=>{cn.classList.remove('flip');pn.classList.remove('flip');if(winner==='player'){pn.classList.add('win');cn.classList.add('loss')}else if(winner==='computer'){cn.classList.add('win');pn.classList.add('loss')}else{cn.classList.add('tie');pn.classList.add('tie')}},640);const rb=$('resultBox');let head='',cls='',capture='',detail='';if(winner==='player'){head='You win the trick';cls='win';capture='You capture '+captureCount+' card'+(captureCount===1?'':'s')+'.';detail=pkaText(player)+' vs '+pkaText(opp)+' — '+(delta==null?'the reference table ranks the winner as the stronger acid.':'lower pKa wins.');if(captureCount>=6)sfxCaptureBig();else sfxWin();sparks(pn)}else if(winner==='computer'){head='Computer wins the trick';cls='loss';capture='CPU captures '+captureCount+' card'+(captureCount===1?'':'s')+'.';detail=pkaText(player)+' vs '+pkaText(opp)+' — '+(delta==null?'the reference table ranks the winner as the stronger acid.':'lower pKa wins.');sfxLoss()}else{head='Tie — cards go to the war pot';cls='tie';capture='The pot now holds '+(warPot.length+2)+' cards. The next winner takes them all.';detail=(delta!=null&&delta<=1e-12)?'Same reference pKa.':('ΔpKa = '+Number(delta).toFixed(2)+'; differences ≤ '+TIE_TOL.toFixed(2)+' are treated as a tie.');sfxTie()}rb.innerHTML='<div class="result-head '+cls+'">'+head+'</div><div class="capture-note">'+capture+'</div><div class="result-detail">'+detail+'</div>'+strategyHtml(analysis)+'<div class="next-note">'+(manualAdvance?'Result will remain until you choose Next trick.':'Cards move to the winner’s pile, then the next trick is dealt…')+'</div><div class="next-trick-wrap"><button type="button" class="primary next-trick-btn" id="nextTrickBtn">NEXT TRICK</button></div>';announce(head+'. '+capture+' '+detail+' '+(analysis&&analysis.optimal?'Optimal move.':'Strategy feedback available on screen.'));setHeight()}
function sparks(card){if(reduceMotion)return;const table=$('table'),r=card.getBoundingClientRect(),tr=table.getBoundingClientRect();for(let n=0;n<20;n++){const s=document.createElement('span');s.className='spark';s.style.left=(r.left-tr.left+r.width/2)+'px';s.style.top=(r.top-tr.top+35)+'px';const a=Math.random()*Math.PI*2,d=34+Math.random()*86;s.style.setProperty('--dx',(Math.cos(a)*d)+'px');s.style.setProperty('--dy',(Math.sin(a)*d)+'px');table.appendChild(s);setTimeout(()=>s.remove(),820)}}
function trackPromise(p){movePromises.add(p);p.finally(()=>movePromises.delete(p));return p}
function recordPersistentMove(moveNo,optimal){
  if(playerMode!=='player'||!currentGameId||!sessionToken)return;
  const payload={p_course_code:args.course_code,p_session_token:sessionToken,p_game_id:currentGameId,p_move_number:moveNo,p_optimal:!!optimal};
  const pr=rpc('acid_record_move',payload,true).then(d=>{if(!d||d.ok!==true)throw new Error((d&&d.error)||'move_not_saved');pendingMoves.delete(moveNo)}).catch(()=>pendingMoves.set(moveNo,payload));
  trackPromise(pr);
}
async function flushPendingMoves(){
  if(playerMode!=='player'||pendingMoves.size===0)return;
  const entries=[...pendingMoves.entries()];
  for(const [n,payload] of entries){try{const d=await rpc('acid_record_move',payload,true);if(d&&d.ok)pendingMoves.delete(n)}catch(e){}}
}
function playCard(id,clicked){
  if(waiting||gameOver||!cpuCurrent)return;ensureAudio();const idx=hand.findIndex(c=>c.instance_id===id);if(idx<0)return;
  const snapshot=hand.slice(),opp=cpuCurrent,analysis=analyzeOptimal(snapshot,opp,id);gameMoves++;if(analysis.optimal)gameOptimal++;recordPersistentMove(gameMoves,analysis.optimal);
  waiting=true;const player=hand.splice(idx,1)[0];cpuCurrent=null;lastPlayed={player,opp};const numericBoth=(player.pka!=null&&opp.pka!=null);const delta=numericBoth?Math.abs(Number(player.pka)-Number(opp.pka)):null;let winner='tie';if(!numericBoth){winner=Number(player.pka_sort)<Number(opp.pka_sort)?'player':'computer'}else if(delta>TIE_TOL+1e-12){winner=Number(player.pka)<Number(opp.pka)?'player':'computer'};const captureCount=winner==='tie'?0:warPot.length+2;renderResult(player,opp,winner,delta,captureCount,analysis);if(timer)clearTimeout(timer);timer=null;const next=$('nextTrickBtn');if(next)next.addEventListener('click',()=>{if(timer){clearTimeout(timer);timer=null}advance(player,opp,winner)});if(!manualAdvance)timer=setTimeout(()=>advance(player,opp,winner),HOLD_MS)
}
function advance(player,opp,winner){if(!waiting)return;if(winner==='player'){playerWon.push(...warPot.splice(0),player,opp)}else if(winner==='computer'){cpuWon.push(...warPot.splice(0),player,opp)}else{warPot.push(player,opp)}turn++;waiting=false;lastPlayed=null;refillHand();prepareCpu();const p=playerTotal(false),c=cpuTotal(false);if(p<=0||c<=0){if(p<=0&&c>0)cpuWon.push(...warPot.splice(0));else if(c<=0&&p>0)playerWon.push(...warPot.splice(0));finishGame(p,c);return}renderIdle()}
async function finishPersistentGame(won){
  if(playerMode!=='player'||!currentGameId)return;
  await Promise.allSettled([...movePromises]);await flushPendingMoves();
  try{await rpc('acid_finish_game',{p_course_code:args.course_code,p_session_token:sessionToken,p_game_id:currentGameId,p_won:!!won},true);await refreshMyStats()}catch(e){}
  currentGameId=null;
}
function finishGame(p,c){gameOver=true;renderPiles();let title,sub,won=false;if(p<=0&&c<=0){title='DRAW';sub='Both sides ran out of cards at the same time.'}else if(p<=0){title='CPU WINS';sub='The computer captured the battle deck.'}else{title='YOU WIN';sub='You captured the battle deck.';won=true}const pct=gameMoves?Math.round(1000*gameOptimal/gameMoves)/10:0;$('gameoverTitle').textContent=title;$('gameoverSub').innerHTML=esc(sub)+'<br>Tricks played: '+turn+' · Strategy: <b>'+gameOptimal+'/'+gameMoves+' optimal ('+pct+'%)</b>.'+(playerMode==='player'?'<br><span class="saved-note">Moves are saved as you play; completed wins count on the Wins leaderboard.</span>':'<br><span class="saved-note">Guest game — nothing was saved.</span>');$('gameover').classList.add('show');announce(title+'. '+sub+' Strategy '+gameOptimal+' of '+gameMoves+' optimal.');setTimeout(()=>$('gameoverCard').focus(),20);if(won)sfxCaptureBig();else sfxLoss();finishPersistentGame(won);setHeight()}
async function startBattle(){
  ensureAudio();$('start').disabled=true;$('setupStatus').textContent='';
  if(playerMode==='player'){
    try{const d=await rpc('acid_start_game',{p_course_code:args.course_code,p_session_token:sessionToken,p_solvent:solvent,p_deck_size:deckChoice});if(!d||!d.ok){$('setupStatus').textContent=authErrorMessage(d&&d.error);$('start').disabled=false;return}currentGameId=d.game_id}catch(e){$('setupStatus').textContent='Could not start a saved game. Check the leaderboard connection or use Guest mode.';$('start').disabled=false;return}
  }else currentGameId=null;
  const [p,c]=makeDeal();hand=[];playerDraw=p;playerWon=[];cpuDraw=c;cpuWon=[];cpuCurrent=null;warPot=[];turn=0;waiting=false;gameOver=false;lastPlayed=null;gameMoves=0;gameOptimal=0;pendingMoves.clear();movePromises.clear();if(timer){clearTimeout(timer);timer=null}$('setup').style.display='none';$('battle').style.display='block';$('gameover').classList.remove('show');$('solventHud').textContent=solvent==='water'?'H₂O':'DMSO';$('deckHud').textContent=pool.length+' acids';$('playerHud').textContent=playerMode==='player'?playerNickname:'Guest';$('start').disabled=false;refillHand();prepareCpu();renderIdle()
}
function backToSetup(){if(timer){clearTimeout(timer);timer=null}$('battle').style.display='none';$('setup').style.display='block';$('gameover').classList.remove('show');refreshDeckControls();setHeight()}
function battleAgain(){startBattle()}

async function loadLeaderboard(){
  const body=$('leaderboardBody');body.innerHTML='<div class="leaderboard-loading">Loading leaderboard…</div>';
  if(!apiReady()){body.innerHTML='<div class="leaderboard-empty">Leaderboard setup is not complete yet. Guest play still works.</div>';return}
  try{const rows=await rpc('acid_leaderboard',{p_course_code:args.course_code});leaderboardRows=Array.isArray(rows)?rows:[];renderLeaderboard()}catch(e){body.innerHTML='<div class="leaderboard-empty">Could not load the leaderboard.</div>'}
}
function renderLeaderboard(){
  const body=$('leaderboardBody');let rows=leaderboardRows.slice();
  if(leaderboardMode==='wins')rows=rows.filter(r=>Number(r.wins||0)>0).sort((a,b)=>Number(b.wins||0)-Number(a.wins||0)||(Number(b.optimal_pct||0)-Number(a.optimal_pct||0))||Number(b.moves||0)-Number(a.moves||0));
  else rows=rows.filter(r=>Number(r.moves||0)>=STRATEGY_MIN).sort((a,b)=>Number(b.optimal_pct||0)-Number(a.optimal_pct||0)||Number(b.moves||0)-Number(a.moves||0)||Number(b.wins||0)-Number(a.wins||0));
  if(!rows.length){body.innerHTML='<div class="leaderboard-empty">'+(leaderboardMode==='wins'?'No completed wins yet.':'No player has reached '+STRATEGY_MIN+' recorded moves yet.')+'</div>';return}
  const head=leaderboardMode==='wins'?'<div class="lb-row lb-head"><span>#</span><span>Player</span><span>Wins</span><span>Optimal</span></div>':'<div class="lb-row lb-head"><span>#</span><span>Player</span><span>Optimal</span><span>Moves</span></div>';
  body.innerHTML=head+rows.slice(0,50).map((r,i)=>{const mine=playerMode==='player'&&String(r.nickname).toLowerCase()===String(playerNickname).toLowerCase();return'<div class="lb-row'+(mine?' mine':'')+'"><span>'+(i+1)+'</span><span>'+esc(r.nickname)+(mine?' <small>you</small>':'')+'</span><span>'+(leaderboardMode==='wins'?Number(r.wins||0):(r.optimal_pct==null?'—':Number(r.optimal_pct).toFixed(1)+'%'))+'</span><span>'+(leaderboardMode==='wins'?(r.optimal_pct==null?'—':Number(r.optimal_pct).toFixed(1)+'%'):Number(r.moves||0))+'</span></div>'}).join('');
}
function openLeaderboard(){modalReturnFocus=document.activeElement;leaderboardMode='wins';document.querySelectorAll('[data-lb]').forEach(b=>{const active=b.dataset.lb==='wins';b.classList.toggle('active',active);b.setAttribute('aria-selected',active?'true':'false')});$('leaderboardModal').classList.add('show');$('leaderboardCard').focus();loadLeaderboard();setHeight()}
function closeLeaderboard(){$('leaderboardModal').classList.remove('show');if(modalReturnFocus&&modalReturnFocus.focus)modalReturnFocus.focus();setHeight()}

$('entryGuest').addEventListener('click',enterGuest);$('entryPlayer').addEventListener('click',showAuth);$('authBack').addEventListener('click',hideAuth);$('signIn').addEventListener('click',()=>authPlayer('login'));$('createPlayer').addEventListener('click',()=>authPlayer('create'));
$('pinInput').addEventListener('input',e=>{e.target.value=e.target.value.replace(/\D/g,'').slice(0,4)});$('pinInput').addEventListener('keydown',e=>{if(e.key==='Enter')authPlayer('login')});
$('setup').addEventListener('click',e=>{const solventButton=e.target.closest('button[data-solvent]');if(solventButton){setSolvent(solventButton.dataset.solvent);return}const deckButton=e.target.closest('button[data-deck]');if(deckButton){setDeck(deckButton.dataset.deck);return}});
$('start').addEventListener('click',startBattle);$('sound').addEventListener('click',toggleSound);$('accessibilityBtn').addEventListener('click',openAccessibility);$('accessibilityClose').addEventListener('click',closeAccessibility);$('motionToggle').addEventListener('click',toggleMotion);$('manualToggle').addEventListener('click',toggleManual);$('accessibilityModal').addEventListener('click',e=>{if(e.target===$('accessibilityModal'))closeAccessibility()});$('change').addEventListener('click',backToSetup);$('newDeck').addEventListener('click',backToSetup);$('again').addEventListener('click',battleAgain);$('profile').addEventListener('click',switchPlayer);$('leaderboardBtn').addEventListener('click',openLeaderboard);$('leaderboardClose').addEventListener('click',closeLeaderboard);$('leaderboardRefresh').addEventListener('click',loadLeaderboard);
document.querySelectorAll('[data-lb]').forEach(b=>b.addEventListener('click',()=>{leaderboardMode=b.dataset.lb;document.querySelectorAll('[data-lb]').forEach(x=>{const active=x===b;x.classList.toggle('active',active);x.setAttribute('aria-selected',active?'true':'false')});renderLeaderboard()}));$('leaderboardModal').addEventListener('click',e=>{if(e.target===$('leaderboardModal'))closeLeaderboard()});document.addEventListener('keydown',e=>{if(e.key==='Escape'){if($('accessibilityModal').classList.contains('show'))closeAccessibility();else if($('leaderboardModal').classList.contains('show'))closeLeaderboard()}});
$('fullscreen').addEventListener('click',async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen()}catch(e){}setHeight()});document.addEventListener('fullscreenchange',()=>{const fs=!!document.fullscreenElement;$('fullscreen').textContent=fs?'↙ Exit full screen':'⛶ Full screen';$('fullscreen').setAttribute('aria-label',fs?'Exit full screen':'Enter full screen');setHeight()});window.addEventListener('resize',setHeight);document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='hidden')flushPendingMoves()});

loadSoundPref();loadAccessibilityPrefs();$('nicknameInput').value=savedNickname();if(!apiReady()){$('leaderboardConfigNote').style.display='block';$('entryPlayer').classList.add('disabled-look')}setSolvent('water');setDeck('25');refreshDeckControls();setHeight();
})();

</script>
</body>
</html>'''



def _secret_value(name: str) -> str:
    try:
        return str(st.secrets[name]).strip()
    except (KeyError, FileNotFoundError):
        return ""


def acid_battle_component():
    # Only the publishable/anon key is sent to the browser. Never expose the
    # SUPABASE_SECRET_KEY/service-role key in the HTML component.
    public_key = _secret_value("SUPABASE_PUBLISHABLE_KEY") or _secret_value("SUPABASE_ANON_KEY")
    payload = {
        "water": WATER,
        "dmso": DMSO,
        "core25": CORE_25_IDS,
        "extended50": EXTENDED_50_IDS,
        "supabase_url": _secret_value("SUPABASE_URL"),
        "supabase_key": public_key,
        "course_code": _secret_value("COURSE_CODE"),
    }
    html = HTML.replace("__ACID_BATTLE_DATA__", json.dumps(payload, ensure_ascii=False))
    components.html(html, height=1080, scrolling=False)


acid_battle_component()
