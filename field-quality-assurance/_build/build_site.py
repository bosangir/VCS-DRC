# -*- coding: utf-8 -*-
"""Build the training website (one page, French and English) from guide_text.py and the training files.
Usage: python _build/build_site.py <training_folder> <out_folder>
The output folder can be published as it is (GitHub Pages: the docs/ folder of the repository)."""
import html
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guide_text import EN, FR  # noqa: E402

SRC, OUT = sys.argv[1:3]
A = os.path.join(OUT, 'assets')
os.makedirs(A, exist_ok=True)
COPY = {
    '01_Key_messages_by_role/Messages_cles_qualite_donnees_par_role_FR.docx': 'Messages_cles_qualite_donnees_par_role_FR.docx',
    '01_Key_messages_by_role/Key_messages_quality_data_by_role_EN.docx': 'Key_messages_quality_data_by_role_EN.docx',
    '04_Segment_protocol_demo/segment_protocol_demo.html': 'segment_protocol_demo.html',
}
for lang in ('fr', 'en'):
    L = lang.upper()
    for ext in ('png', 'pdf'):
        COPY[f'03_Process_infographic/Process_infographic_{L}.{ext}'] = f'Process_infographic_{L}.{ext}'
    for m in ('correct', 'errors'):
        COPY[f'04_Segment_protocol_demo/fig_{m}_{lang}.png'] = f'fig_{m}_{lang}.png'
for s, d in COPY.items():
    shutil.copyfile(os.path.join(SRC, s), os.path.join(A, d))
open(os.path.join(OUT, '.nojekyll'), 'w').close()

e = html.escape


def T(fr, en, tag='span', cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<{tag} data-l="fr"{c}>{fr}</{tag}><{tag} data-l="en"{c}>{en}</{tag}>'


def both(key, fn):
    """render a guide_text entry in both languages with fn(value) -> html"""
    return f'<div data-l="fr">{fn(FR[key])}</div><div data-l="en">{fn(EN[key])}</div>'


def table(cols, rows, cls=''):
    h = ''.join(f'<th>{e(c)}</th>' for c in cols)
    b = ''.join('<tr>' + ''.join(f'<td>{e(x)}</td>' for x in r) + '</tr>' for r in rows)
    return f'<div class="tw"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


# ------------------------------------------------------------------ sections
NAV = [('start', 'Commencer ici', 'Start here'), ('process', 'Le processus', 'The process'),
       ('segments', 'Scénarios animés', 'Animated scenarios'), ('slides', 'Diaporama', 'Slide deck'), ('videos', 'Vidéos', 'Videos'),
       ('card', 'Dates de carte', 'Card dates'),
       ('duration', 'Durée active', 'Active duration'), ('roles', 'Par rôle', 'By role'),
       ('codes', 'Codes et alertes', 'Codes and alerts'), ('selfcheck', 'Auto-contrôle', 'Self-check'),
       ('files', 'Téléchargements', 'Downloads')]
nav = ''.join(f'<a href="#{i}">{T(fr, en)}</a>' for i, fr, en in NAV)


def six(d):
    return '<ol class="six">' + ''.join(f'<li><b>{e(a)}</b> {e(b)}</li>' for a, b in d) + '</ol>'


def paras(d):
    return ''.join(f'<p>{e(x)}</p>' for x in d)


start = f'''
<section id="start">
<h2>{T('Six messages pour tout le monde', 'Six messages for everyone')}</h2>
{both('five', six)}
<details class="why"><summary>{T('Pourquoi c\'est important', 'Why this matters')}</summary>{both('why', paras)}</details>
</section>'''

process = f'''
<section id="process">
<h2>{T('Le processus, de la préparation aux contrôles indépendants', 'The process, from preparation to independent checks')}</h2>
<p>{T("Dix étapes, les lignes rouges et qui fait quoi. Imprimez l'affiche en A3 ou partagez l'image sur WhatsApp.",
      'Ten steps, the red lines and who does what. Print the poster in A3 or share the image on WhatsApp.')}</p>
<figure class="poster">
<img data-l="fr" src="assets/Process_infographic_FR.png" alt="Affiche du processus de collecte et de contrôle qualité" loading="lazy">
<img data-l="en" src="assets/Process_infographic_EN.png" alt="Poster of the data collection and quality assurance process" loading="lazy">
</figure>
<p class="btns">
<a class="btn" data-l="fr" href="assets/Process_infographic_FR.pdf" download>Télécharger l'affiche (PDF)</a>
<a class="btn" data-l="en" href="assets/Process_infographic_EN.pdf" download>Download the poster (PDF)</a>
</p>
</section>'''

SCN = [('basic', 'Parcours de base', 'Basic canvassing', 'A · PSU 1'), ('quota1', 'Cible atteinte dans le segment 1', 'Target reached in Segment 1', 'A · PSU 1'),
       ('flood', 'Segment inondé', 'Flooded segment', 'D1 · PSU 2'), ('empty', 'Segment sans habitation', 'Uninhabited segment', 'C1 · PSU 1'),
       ('river', 'Segment derrière la rivière', 'Segment across the river', 'E3 · PSU 2'), ('danger', 'Insécurité pendant le travail', 'Insecurity during work', 'J + F1 · PSU 2'),
       ('swamp', 'Marais dans une partie du segment', 'Swamp in part of a segment', 'J + D2 · PSU 2'), ('two', 'Deux enquêteurs dans un PSU', 'Two enumerators in one PSU', 'blocs / blocks'),
       ('below', 'Cible non atteinte après tous les segments', 'Target not reached after every segment', 'PSU 6'), ('emptypsu', 'PSU entièrement vide', 'Entirely empty PSU', 'C1 · PSU 5'),
       ('g1', 'Décision sur image satellite', 'Decision from satellite imagery', 'G1 · PSU 2')]
VIDS = os.path.join(SRC, '07_Videos')
os.makedirs(os.path.join(A, 'videos'), exist_ok=True)
for f in os.listdir(VIDS) if os.path.isdir(VIDS) else []:
    if f.endswith('.mp4'):
        shutil.copyfile(os.path.join(VIDS, f), os.path.join(A, 'videos', f))
for f in os.listdir(os.path.join(SRC, '06_Slides')):
    if f.endswith('.pptx'):
        shutil.copyfile(os.path.join(SRC, '06_Slides', f), os.path.join(A, f))
shutil.copyfile(os.path.join(SRC, '06_Slides', 'canvassing_slides.html'), os.path.join(OUT, 'slides.html'))


def vid(sid, v):
    return ''.join(f'<video data-l="{l}" controls preload="metadata" src="assets/videos/{sid}_{v}_{l}.mp4"></video>' for l in ('fr', 'en'))


gallery = ''.join(f"""<div class="vcard"><h3>{i + 1}. {T(fr, en)} <span class="code">{c}</span></h3><div class="vpair">
<figure>{vid(sid, 'correct')}<figcaption class="okc">{T('Bonne pratique', 'Right practice')}</figcaption></figure>
<figure>{vid(sid, 'wrong')}<figcaption class="badc">{T('Ce qu\'il ne faut pas faire', 'What not to do')}</figcaption></figure></div></div>"""
                  for i, (sid, fr, en, c) in enumerate(SCN))

segments = f"""
<section id="segments">
<h2>{T('Le protocole des segments, en scénarios animés', 'The segment protocol, in animated scenarios')}</h2>
<p>{T("Onze situations du formulaire de disposition, chacune jouée deux fois : la bonne pratique, puis l'erreur. Choisissez un scénario à gauche, puis <b>Lecture</b> ou <b>Étape suivante</b>. Tout tient sur un écran.",
      'Eleven situations from the disposition form, each played twice: the right practice, then the mistake. Choose a scenario on the left, then <b>Play</b> or <b>Next step</b>. Everything fits on one screen.')}</p>
<p class="btns"><a class="btn" id="demo-open" href="assets/segment_protocol_demo.html?lang=fr" target="_blank" rel="noopener">{T('Ouvrir les scénarios en plein écran', 'Open the scenarios full screen')}</a>
<a class="btn ghost" href="slides.html" target="_blank" rel="noopener">{T('Ouvrir le diaporama de formation', 'Open the training slide deck')}</a></p>
<div class="frame tall"><iframe id="demo" title="Segment protocol scenarios" src="assets/segment_protocol_demo.html?lang=fr" loading="lazy"></iframe></div>
<p class="note">{T("L'ordre des segments est strict au Sankuru. Cible : 6 entretiens d'enfants de 12–23 mois par PSU, mais on finit toujours le segment en cours. Cible non atteinte après tous les segments : PSU code 6, jamais de travail hors du PSU.",
                   'Segment order is strict in Sankuru. Target: 6 interviews of children aged 12–23 months per PSU, but the segment in progress is always finished. Target not reached after every segment: PSU code 6, never work outside the PSU.')}</p>
</section>
<section id="slides">
<h2>{T('Diaporama : parcourir le PSU', 'Slide deck: canvassing the PSU')}</h2>
<p>{T("Le diaporama de la journée 2 : pourquoi le protocole, avant de partir, le balayage, l'éligibilité et la date de naissance (calendrier des événements locaux), les visites et revisites, les codes de disposition, puis chaque scénario en vidéo. Flèches du clavier pour avancer ; FR / EN en bas à droite.",
      'The Day 2 deck: why the protocol, before leaving, the sweep, eligibility and the date of birth (calendar of local events), visits and revisits, disposition codes, then each scenario on video. Arrow keys to move; FR / EN at the bottom right.')}</p>
<div class="frame"><iframe title="Slide deck" src="slides.html" loading="lazy"></iframe></div>
<p class="btns"><a class="btn" href="slides.html" target="_blank" rel="noopener">{T('Ouvrir le diaporama en plein écran', 'Open the slide deck full screen')}</a>
<a class="btn ghost" href="assets/Day 2 - Canvassing the PSU - Sankuru - Bernard.pptx" download>{T('Télécharger la version PowerPoint (avec vidéos)', 'Download the PowerPoint version (with videos)')}</a></p>
</section>
<section id="videos">
<h2>{T('Les scénarios en vidéo', 'The scenarios on video')}</h2>
<p>{T('Pour WhatsApp ou une projection sans internet : chaque vidéo dure moins d\'une minute.', 'For WhatsApp or showing offline: each video is under a minute.')}</p>
<div class="vgrid">{gallery}</div>
</section>"""

card = f'''
<section id="card">
<h2>{T('Contrôle des dates de la carte, comme dans la CAPI', 'Card date checks, as in the CAPI')}</h2>
<p>{T("La CAPI (version 006) compare les dates saisies et affiche un seul écran en fin de carte. Essayez un exemple ou changez une date : l'écran à droite montre ce que l'enquêteur verra.",
      'The CAPI (version 006) compares the dates entered and shows one screen at the end of the card. Try an example or change a date: the screen on the right shows what the enumerator will see.')}</p>
<div class="presets" id="presets"></div>
<div class="cardgrid">
<div class="cardbox">
<div class="dobrow"><label>{T('Date de naissance', 'Date of birth')} <input type="date" id="dob"></label></div>
<div class="tw"><table class="doses"><thead><tr><th>{T('Âge', 'Age')}</th><th>{T('Dose', 'Dose')}</th><th>{T('Sur la carte', 'On the card')}</th><th>Date</th></tr></thead><tbody id="doses"></tbody></table></div>
</div>
<div class="phone" aria-live="polite"><div class="phonebar">CAPI</div><div id="screen"></div></div>
</div>
<div class="tw"><table class="plain">
<thead><tr><th>{T('Contrôle', 'Check')}</th><th>{T('Ce qui le déclenche', 'What triggers it')}</th><th>{T("Ce que fait l'enquêteur", 'What the enumerator does')}</th></tr></thead>
<tbody>
<tr><td>{T('Date future', 'Future date')}</td><td>{T("Date après le jour de l'entretien", 'Date after the interview day')}</td><td>{T('Bloquant : la date ne peut pas être enregistrée. Revérifier la carte.', 'Blocking: the date cannot be saved. Recheck the card.')}</td></tr>
<tr><td>{T('Ordre de la série', 'Series order')}</td><td>{T('Dose suivante le même jour ou avant la précédente (ex. Penta 2 ≤ Penta 1)', 'Next dose on the same day as or before the previous one (e.g. Penta 2 ≤ Penta 1)')}</td><td>{T('Revérifier ; si la carte le montre, confirmer et commenter', 'Recheck; if the card shows it, confirm and comment')}</td></tr>
<tr><td>{T('Même âge, dates différentes', 'Same age, different dates')}</td><td>{T('Doses de 6, 10, 14 semaines ou 9 mois à des jours différents', 'Doses due at 6, 10, 14 weeks or 9 months on different days')}</td><td>{T('Revérifier et confirmer', 'Recheck and confirm')}</td></tr>
<tr><td>{T('Même âge, dose manquante', 'Same age, dose missing')}</td><td>{T('Une dose datée et une autre du même âge notée « Non »', 'One dose dated and another due at the same age recorded "No"')}</td><td>{T('Revérifier et confirmer', 'Recheck and confirm')}</td></tr>
<tr><td>{T('Avant la naissance', 'Before birth')}</td><td>{T('Date avant la date de naissance', 'Date before the date of birth')}</td><td>{T('Revérifier ; si la carte le montre, confirmer et commenter', 'Recheck; if the card shows it, confirm and comment')}</td></tr>
</tbody></table></div>
</section>'''

duration = f'''
<section id="duration">
<h2>{T("Durée active de l'entretien", 'Active interview duration')}</h2>
<p>{T("L'heure de fin moins l'heure de début ne mesure pas l'entretien : un formulaire peut rester ouvert toute la journée pour revenir au ménage. La CAPI version 006 compte seulement le temps où le formulaire est ouvert à l'écran, et fige ce compteur au consentement, au début et à la fin de chaque femme, et au résultat de la visite.",
      'End time minus start time does not measure the interview: a form may stay open all day to return to the household. CAPI version 006 counts only the time the form is open on screen, and freezes that counter at consent, at the start and end of each woman, and at the visit result.')}</p>
<div class="presets" id="dpresets"></div>
<div id="timeline"></div>
<div id="dvars"></div>
<p class="note">{T("<b>Consigne aux enquêteurs :</b> quand vous quittez un ménage, enregistrez et fermez le formulaire. Un formulaire laissé ouvert à l'écran continue de compter.",
                   '<b>Instruction to enumerators:</b> when you leave a household, save and close the form. A form left open on screen keeps counting.')}</p>
<details><summary>{T('Variables pour la gestion des données', 'Variables for data management')}</summary>
<div class="tw"><table class="plain"><thead><tr><th>{T('Variable', 'Variable')}</th><th>{T('Contenu', 'Content')}</th></tr></thead><tbody>
<tr><td><code>dur_active_s</code>, <code>dur_active_min</code></td><td>{T('Temps total du formulaire à l\'écran (secondes, minutes)', 'Total time the form was on screen (seconds, minutes)')}</td></tr>
<tr><td><code>dur_t_consent</code>, <code>dur_t_result</code></td><td>{T('Compteur figé au consentement (HHI09 = 1) et au résultat de la visite (HL16/HL17)', 'Counter frozen at consent (HHI09 = 1) and at the visit result (HL16/HL17)')}</td></tr>
<tr><td><code>dur_interview_min</code></td><td>{T('Minutes actives du consentement au résultat : la durée de l\'entretien à rapporter', 'Active minutes from consent to result: the interview duration to report')}</td></tr>
<tr><td><code>dur_cg_t1</code>, <code>dur_cg_t2</code>, <code>dur_cg_min</code></td><td>{T('Par mère/gardienne : de CB00 = 1 à IC04', 'Per mother/caregiver: from CB00 = 1 to IC04')}</td></tr>
<tr><td><code>flag_short_interview</code></td><td>{T('1 si un enfant a été interrogé et la durée est sous 15 min, ou sous 25 min avec un enfant de 12–23 mois (alertes A4/A5)', '1 if a child was interviewed and the duration is under 15 min, or under 25 min with a child aged 12–23 months (alerts A4/A5)')}</td></tr>
<tr><td><code>duration</code></td><td>{T('Ancien calcul VS01 moins PVT01B (heures saisies), gardé pour comparaison', 'Old calculation VS01 minus PVT01B (typed clock times), kept for comparison')}</td></tr>
<tr><td><code>text_audit</code></td><td>{T('Temps passé sur chaque question (déjà dans le formulaire)', 'Time spent on each question (already in the form)')}</td></tr>
</tbody></table></div></details>
</section>'''


def roles(d):
    tabs = ''.join(f'<button class="tab" data-r="{i}">{e(name)}</button>' for i, (name, _) in enumerate(d))
    panes = ''
    for i, (name, phases) in enumerate(d):
        cols = ''.join(f'<div class="phase"><h4>{e(ph)}</h4><ul>' + ''.join(f'<li>{e(x)}</li>' for x in items) + '</ul></div>' for ph, items in phases)
        panes += f'<div class="pane" data-r="{i}"><h3>{e(name)}</h3><div class="phases">{cols}</div></div>'
    return f'<div class="tabs">{tabs}</div>{panes}'


rolesec = f'''
<section id="roles">
<h2>{T('Ce que fait chaque rôle', 'What each role does')}</h2>
{both('roles', roles)}
</section>'''

codes = f'''
<section id="codes">
<h2>{T('Codes de disposition des segments', 'Segment disposition codes')}</h2>
{both('codes', lambda d: table(['Code', 'Signification' if d is FR['codes'] else 'Meaning', 'À utiliser quand' if d is FR['codes'] else 'Use it when'], d, 'codes'))}
{both('codes_note', lambda x: f'<p class="note">{e(x)}</p>')}
<h2>{T('Alertes automatiques et qui agit', 'Automatic alerts and who acts')}</h2>
<div data-l="fr">{table(FR['alerts_cols'], FR['alerts'])}</div><div data-l="en">{table(EN['alerts_cols'], EN['alerts'])}</div>
<h2>{T('Ce qui change après les réunions BGC des 13 et 16 novembre', 'What changes after the BGC meetings of 13 and 16 November')}</h2>
<div data-l="fr">{table(FR['bgc_cols'], FR['bgc'])}</div><div data-l="en">{table(EN['bgc_cols'], EN['bgc'])}</div>
</section>'''


def checklist(d):
    return '<ul class="check">' + ''.join(f'<li><label><input type="checkbox"> {e(x)}</label></li>' for x in d) + '</ul>'


selfcheck = f'''
<section id="selfcheck">
<h2>{T("Auto-contrôle quotidien de l'enquêteur", 'Enumerator daily self-check')}</h2>
{both('card_intro', lambda x: f'<p>{e(x)}</p>')}
{both('card', checklist)}
<p class="btns"><button class="btn ghost" onclick="window.print()">{T('Imprimer cette page', 'Print this page')}</button></p>
</section>'''

files = f'''
<section id="files">
<h2>{T('Téléchargements', 'Downloads')}</h2>
<ul class="files">
<li><a href="assets/Messages_cles_qualite_donnees_par_role_FR.docx" download>{T('Guide des messages clés par rôle (Word, français)', 'Key messages guide by role (Word, French)')}</a></li>
<li><a href="assets/Key_messages_quality_data_by_role_EN.docx" download>{T('Guide des messages clés par rôle (Word, anglais)', 'Key messages guide by role (Word, English)')}</a></li>
<li><a href="assets/Process_infographic_FR.pdf" download>{T('Affiche du processus (PDF, français)', 'Process poster (PDF, French)')}</a> · <a href="assets/Process_infographic_FR.png" download>PNG</a></li>
<li><a href="assets/Process_infographic_EN.pdf" download>{T('Affiche du processus (PDF, anglais)', 'Process poster (PDF, English)')}</a> · <a href="assets/Process_infographic_EN.png" download>PNG</a></li>
<li><a href="assets/Day 2 - Canvassing the PSU - Sankuru - Bernard.pptx" download>{T('Diaporama « Parcourir le PSU » (PowerPoint, anglais, avec vidéos)', 'Slide deck "Canvassing the PSU" (PowerPoint, English, with videos)')}</a></li>
<li><a href="slides.html" target="_blank" rel="noopener">{T('Diaporama web (français et anglais)', 'Web slide deck (French and English)')}</a></li>
<li><a href="assets/segment_protocol_demo.html" download>{T('Scénarios animés (fonctionne hors ligne)', 'Animated scenarios (works offline)')}</a></li>
</ul>
<p class="small">{T("Sources : Protocole d'étude Sankuru V1.0 (5 novembre 2026), SOP-01 Protocole compact des segments V1.0 (7 novembre 2026), Plan DQA V1.0, réunions BGC–UNIKIN des 13 et 16 novembre 2026. En cas de différence, le Protocole d'étude prévaut. Les PSU, segments et ménages des démonstrations sont simulés.",
                    'Sources: Sankuru Study Protocol V1.0 (5 November 2026), SOP-01 Compact Segment Protocol V1.0 (7 November 2026), DQA Plan V1.0, BGC–UNIKIN meetings of 13 and 16 November 2026. Where they differ, the Study Protocol governs. PSUs, segments and households in the demonstrations are simulated.')}</p>
</section>'''

CSS = r'''
:root{--ink:#1d2733;--muted:#55606e;--line:#d6dbe1;--bg:#ffffff;--soft:#f3f5f8;--acc:#1f4e79;--ok:#2e7d32;--bad:#b03a2e;--warn:#9a6700}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:64px}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 Arial,Helvetica,sans-serif}
html[lang=fr] [data-l=en],html[lang=en] [data-l=fr]{display:none!important}
header{background:var(--acc);color:#fff;padding:28px 16px 22px}
header .in,main,nav .in{max-width:1080px;margin:0 auto}
header h1{margin:0 0 6px;font-size:1.7rem;line-height:1.25}header p{margin:0;opacity:.92;max-width:760px}
.lang{float:right;display:flex;gap:4px}.lang button{background:transparent;color:#fff;border:1px solid #ffffff99;padding:4px 10px;border-radius:3px;cursor:pointer;font-weight:bold}
.lang button[aria-pressed=true]{background:#fff;color:var(--acc)}
nav{position:sticky;top:0;z-index:5;background:#fff;border-bottom:1px solid var(--line)}
nav .in{display:flex;gap:2px;overflow-x:auto;padding:0 8px}nav a{white-space:nowrap;padding:12px 10px;color:var(--ink);text-decoration:none;font-size:.92rem;border-bottom:3px solid transparent}
nav a:hover{border-bottom-color:var(--acc)}
main{padding:0 16px 40px}section{padding:34px 0 10px;border-bottom:1px solid var(--line)}section:last-child{border-bottom:0}
h2{font-size:1.35rem;margin:0 0 12px;color:var(--acc)}h3{font-size:1.1rem;margin:16px 0 8px}h4{margin:0 0 6px;font-size:.98rem}
p{max-width:820px}.small{font-size:.86rem;color:var(--muted)}
.note{background:var(--soft);border-left:4px solid var(--acc);padding:10px 14px;max-width:none}
ol.six{padding-left:0;list-style:none;counter-reset:s;display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px}
ol.six li{counter-increment:s;border:1px solid var(--line);border-radius:4px;padding:12px 14px 12px 52px;position:relative}
ol.six li:before{content:counter(s);position:absolute;left:14px;top:11px;width:26px;height:26px;border-radius:50%;background:var(--acc);color:#fff;text-align:center;line-height:26px;font-weight:bold}
ol.six b{display:block;margin-bottom:2px}
details{margin:12px 0}summary{cursor:pointer;color:var(--acc);font-weight:bold}
figure{margin:0}img{max-width:100%;height:auto;display:block}.poster img{border:1px solid var(--line)}
.btns{display:flex;flex-wrap:wrap;gap:8px}.btn{display:inline-block;background:var(--acc);color:#fff;text-decoration:none;padding:8px 14px;border-radius:3px;border:1px solid var(--acc);font:inherit;cursor:pointer}
.btn.ghost{background:#fff;color:var(--acc)}
.frame{border:1px solid var(--line);border-radius:4px;overflow:hidden}.frame iframe{width:100%;aspect-ratio:16/9;height:auto;border:0;display:block}
.frame.tall iframe{aspect-ratio:auto;height:min(82vh,780px)}
.vgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(470px,1fr));gap:14px}.vcard{border:1px solid var(--line);border-radius:4px;padding:10px 12px}
.vcard h3{margin:0 0 8px;font-size:1rem}.vcard .code{font-weight:400;color:var(--muted);font-size:.85rem;margin-left:6px}
.vpair{display:grid;grid-template-columns:1fr 1fr;gap:8px}.vpair video{width:100%;display:block;border:1px solid var(--line);background:#f4f6f9}
.okc{color:var(--ok);font-weight:700}.badc{color:var(--bad);font-weight:700}
.two{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:16px 0}.two figure{border:1px solid var(--line);padding:8px}figcaption{font-size:.9rem;color:var(--muted);margin-top:6px}
.tw{overflow-x:auto;margin:10px 0}table{border-collapse:collapse;width:100%;font-size:.93rem}th,td{border:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}th{background:var(--soft)}
table.codes td:first-child{font-weight:bold;text-align:center;width:52px}
.presets{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 12px}.presets button{background:#fff;border:1px solid var(--line);padding:6px 10px;border-radius:3px;cursor:pointer;font:inherit;font-size:.9rem}
.presets button[aria-pressed=true]{border-color:var(--acc);background:var(--acc);color:#fff}
.cardgrid{display:grid;grid-template-columns:1.35fr 1fr;gap:18px;align-items:start}
.cardbox{border:1px solid var(--line);border-radius:4px;padding:10px;background:#fbfcfd}
table.doses td,table.doses th{padding:3px 6px}table.doses select,table.doses input,.dobrow input{font:inherit;font-size:.88rem;padding:2px}
table.doses tr.hit td{background:#fdf1e7}table.doses tr.fut td{background:#fbe3e0}table.doses td.age{color:var(--muted);font-size:.85rem}
.dobrow{margin-bottom:8px}
.phone{border:10px solid #2b2f36;border-radius:22px;background:#fff;min-height:380px;position:sticky;top:70px}
.phonebar{background:#2b2f36;color:#fff;font-size:.75rem;padding:0 0 6px;text-align:center}
#screen{padding:12px;font-size:.92rem}#screen h5{margin:0 0 8px;font-size:.95rem}#screen ul{padding-left:18px;margin:6px 0}
.ok{color:var(--ok)}.bad{color:var(--bad)}.warn{color:var(--warn)}.box{border:1px solid var(--line);padding:8px;border-radius:3px;margin-top:8px;background:var(--soft)}
#timeline svg{width:100%;height:auto;display:block;border:1px solid var(--line);border-radius:4px;background:#fff}
#dvars{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:8px;margin:12px 0}
#dvars div{border:1px solid var(--line);border-radius:4px;padding:8px 10px}#dvars b{display:block;font-size:1.3rem}#dvars code{font-size:.8rem;color:var(--muted)}
.tabs{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:6px}.tab{background:#fff;border:1px solid var(--line);padding:7px 12px;border-radius:3px;cursor:pointer;font:inherit}
.tab[aria-pressed=true]{background:var(--acc);color:#fff;border-color:var(--acc)}
.pane{display:none}.pane.on{display:block}.phases{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}
.phase{border:1px solid var(--line);border-radius:4px;padding:10px 12px}.phase ul{padding-left:18px;margin:0}.phase li{margin:4px 0}
ul.check{list-style:none;padding:0;columns:2;column-gap:24px}ul.check li{break-inside:avoid;margin:0 0 8px}ul.check input{transform:scale(1.2);margin-right:6px}
ul.files li{margin:6px 0}code{font-family:Consolas,monospace;font-size:.88em}
footer{background:var(--soft);padding:18px 16px;font-size:.85rem;color:var(--muted)}footer .in{max-width:1080px;margin:0 auto}
@media (max-width:760px){.two,.cardgrid{grid-template-columns:1fr}.phone{position:static}.frame.tall iframe{height:70vh}.vgrid{grid-template-columns:1fr}.vpair{grid-template-columns:1fr}ul.check{columns:1}header h1{font-size:1.35rem}}
@media print{nav,header .lang,.frame,.btns,#segments,#slides,#videos,#card,#duration,#process{display:none}section{page-break-inside:avoid}}
'''

JS = r'''
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
let LANG=(location.hash.match(/lang=(fr|en)/)||[])[1]||(new URLSearchParams(location.search).get('lang'))||'fr';
const t=(fr,en)=>LANG==='fr'?fr:en;
function setLang(l){LANG=l;document.documentElement.lang=l;$$('.lang button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.lang===l));
 const src='assets/segment_protocol_demo.html?lang='+l;const f=$('#demo');if(f&&!f.src.endsWith(src))f.src=src;$('#demo-open').href=src;
 try{localStorage.setItem("lang",l)}catch(e){};if(card[1])drawDoses();renderCard();renderDur();presetButtons();}
// ---------------- roles tabs
$$('.tabs').forEach(tb=>{const bs=[...tb.querySelectorAll('.tab')];const panes=[...tb.parentElement.querySelectorAll('.pane')];
 const pick=i=>{bs.forEach((b,j)=>b.setAttribute('aria-pressed',i===j));panes.forEach((p,j)=>p.classList.toggle('on',i===j));};
 bs.forEach((b,i)=>b.onclick=()=>pick(i));pick(2);});
// ---------------- card date demo (same rules as CAPI 006)
const DOSES=[[1,'BCG','birth'],[2,'VPO0','birth'],[3,'VPO1','6w'],[4,'Penta1','6w'],[5,'PCV1','6w'],[6,'Rota1','6w'],[7,'VPO2','10w'],[8,'Penta2','10w'],[9,'PCV2','10w'],[10,'Rota2','10w'],
 [11,'VPO3','14w'],[12,'VPI','14w'],[13,'Penta3','14w'],[14,'PCV3','14w'],[15,'Rota3','14w'],[16,'VAR','9m'],[17,'VAA','9m']];
const AGE={birth:['Naissance','Birth'],'6w':['6 semaines','6 weeks'],'10w':['10 semaines','10 weeks'],'14w':['14 semaines','14 weeks'],'9m':['9 mois','9 months']};
const SERIES=[[2,3],[3,7],[7,11],[4,8],[8,13],[5,9],[9,14],[6,10],[10,15]];
const SAME=[['6w',[3,4,5,6]],['10w',[7,8,9,10]],['14w',[11,12,13,14,15]],['9m',[16,17]]];
const NAME=Object.fromEntries(DOSES.map(d=>[d[0],d[1]]));
const DOB='2025-03-03',BASE={1:'2025-03-03',2:'2025-03-03',3:'2025-04-14',4:'2025-04-14',5:'2025-04-14',6:'2025-04-14',7:'2025-05-12',8:'2025-05-12',9:'2025-05-12',10:'2025-05-12',
 11:'2025-06-09',12:'2025-06-09',13:'2025-06-09',14:'2025-06-09',15:'2025-06-09',16:'2025-12-03',17:'2025-12-03'};
const PRESETS=[
 ['Carte correcte','Clean card',{}],
 ['Penta 1 et Penta 2 le même jour','Penta 1 and Penta 2 on the same day',{8:'2025-04-14'}],
 ['Penta 2 avant Penta 1','Penta 2 before Penta 1',{4:'2025-05-12',8:'2025-04-14'}],
 ['Doses de 6 semaines à des jours différents','6-week doses on different days',{5:'2025-04-21'}],
 ['PCV 1 « Non », Penta 1 daté','PCV 1 "No", Penta 1 dated',{5:'n'}],
 ['BCG avant la naissance','BCG before birth',{1:'2025-02-20'}],
 ['Date dans le futur','Date in the future',{13:'2027-01-05'}],
 ['Coches sans date','Ticks without dates',{3:'i',4:'i',5:'i',6:'i'}]];
let card={},cur=0;
function load(i){cur=i;card={};for(const [id] of DOSES){const v=(PRESETS[i][2][id]!==undefined)?PRESETS[i][2][id]:BASE[id];card[id]=(v==='n'||v==='i')?{s:v,d:''}:{s:'d',d:v};}$('#dob').value=DOB;drawDoses();renderCard();presetButtons();}
function presetButtons(){const p=$('#presets');if(!p)return;p.innerHTML='';PRESETS.forEach((x,i)=>{const b=document.createElement('button');b.textContent=t(x[0],x[1]);b.setAttribute('aria-pressed',i===cur);b.onclick=()=>load(i);p.appendChild(b);});
 const d=$('#dpresets');if(!d)return;d.innerHTML='';DUR.forEach((x,i)=>{const b=document.createElement('button');b.textContent=t(x.fr,x.en);b.setAttribute('aria-pressed',i===dcur);b.onclick=()=>{dcur=i;renderDur();presetButtons();};d.appendChild(b);});}
function drawDoses(){const tb=$('#doses');tb.innerHTML='';let last='';for(const [id,n,a] of DOSES){const tr=document.createElement('tr');tr.id='r'+id;const c=card[id];
 tr.innerHTML=`<td class="age">${a!==last?`<span data-l="fr">${AGE[a][0]}</span><span data-l="en">${AGE[a][1]}</span>`:''}</td><td>${n}</td>
 <td><select aria-label="${n}"><option value="d">${t('Date écrite','Date written')}</option><option value="i">${t('Coche / date incomplète','Tick / date incomplete')}</option><option value="n">${t('Non','No')}</option></select></td>
 <td><input type="date" aria-label="${n} date" value="${c.d}"></td>`;last=a;
 const sel=tr.querySelector('select'),inp=tr.querySelector('input');sel.value=c.s;inp.disabled=c.s!=='d';
 sel.onchange=()=>{c.s=sel.value;inp.disabled=c.s!=='d';if(c.s!=='d'){c.d='';inp.value='';}renderCard();};inp.oninput=()=>{c.d=inp.value;renderCard();};tb.appendChild(tr);}}
function renderCard(){if(!$('#screen'))return;if(!card[1])return load(0);const today=new Date().toISOString().slice(0,10),dob=$('#dob').value;const D=i=>card[i].s==='d'?card[i].d:'';
 $$('#doses tr').forEach(r=>r.classList.remove('hit','fut'));const hit=i=>$('#r'+i)&&$('#r'+i).classList.add('hit');
 const fut=DOSES.map(d=>d[0]).filter(i=>D(i)&&D(i)>today);
 if(fut.length){fut.forEach(i=>$('#r'+i).classList.add('fut'));$('#screen').innerHTML=`<h5 class="bad">${t('Date refusée','Date refused')}</h5><p>${NAME[fut[0]]} : ${t("La date ne peut pas être après aujourd'hui. Revérifiez la carte.",'The date cannot be after today. Recheck the card.')}</p><p class="small">${t("L'enquêteur ne peut pas avancer tant que la date n'est pas corrigée.",'The enumerator cannot move on until the date is corrected.')}</p>`;return;}
 const order=[],same=[],miss=[];let before=[];
 for(const [a,b] of SERIES)if(D(a)&&D(b)&&D(b)<=D(a)){order.push(t(`${NAME[b]} le même jour ou avant ${NAME[a]}`,`${NAME[b]} on the same day as or before ${NAME[a]}`));hit(a);hit(b);}
 for(const [age,g] of SAME){const ds=new Set(g.map(D).filter(Boolean));if(ds.size>1){same.push(t(`Doses de ${AGE[age][0]} à des dates différentes`,`${AGE[age][1]} doses on different dates`));g.forEach(i=>D(i)&&hit(i));}
  if(g.some(i=>card[i].s==='d')&&g.some(i=>card[i].s==='n')){miss.push(t(`Doses de ${AGE[age][0]} : une datée, une autre « Non »`,`${AGE[age][1]} doses: one dated, another "No"`));g.forEach(hit);}}
 if(dob)before=DOSES.map(d=>d[0]).filter(i=>D(i)&&D(i)<dob);before.forEach(hit);
 const inc=DOSES.filter(d=>card[d[0]].s==='i').length;const n=order.length+same.length+miss.length+(before.length?1:0);
 let h='';if(!n){h=`<h5 class="ok">${t('Aucun écran de vérification','No check screen')}</h5><p>${t('Les dates sont cohérentes. La CAPI passe à la question suivante.','The dates are consistent. The CAPI moves to the next question.')}</p>`;}
 else{h=`<h5>${t('Vérification des dates de la carte','Card date check')}</h5><ul>`+[...order,...same,...miss].map(x=>`<li>${x}</li>`).join('')+(before.length?`<li>${t('Date avant la naissance','Date before birth')} : ${before.map(i=>NAME[i]).join(', ')}</li>`:'')+'</ul>'+
  `<div class="box"><label><input type="checkbox"> ${t("J'ai revérifié la carte : ces dates sont bien celles écrites sur la carte","I rechecked the card: these dates are as written on the card")}</label></div>`+
  ((order.length||before.length)?`<div class="box"><span class="warn">${t('Commentaire obligatoire','Comment required')}</span> : ${t('décrivez ce que montre la carte.','describe what the card shows.')}</div>`:`<p class="small">${t('Pas de commentaire obligatoire pour ces contrôles.','No comment required for these checks.')}</p>`)+
  `<p class="small">${t("Si une date a été mal saisie, revenez en arrière et corrigez-la : l'écran disparaît.","If a date was entered wrongly, go back and correct it: the screen disappears.")}</p>`;}
 if(inc)h+=`<p class="small">${t('Doses avec coche ou date incomplète','Doses with a tick or incomplete date')} : ${inc}. ${t('Autorisé si c\'est vrai ; le taux par enquêteur est suivi.','Allowed when true; the rate per enumerator is tracked.')}</p>`;
 $('#screen').innerHTML=h;}
// ---------------- duration demo
const DUR=[
 {fr:'Entretien normal, formulaire fermé en partant',en:'Normal interview, form closed when leaving',kid1223:1,seg:[['open',0,6],['int',6,38],['closed',38,260],['open',260,262]],cons:6,res:38,cg:[[9,36]]},
 {fr:'Formulaire laissé ouvert à l\'écran pendant une attente',en:'Form left open on screen during a wait',kid1223:1,seg:[['open',0,5],['int',5,22],['wait',22,82],['int',82,96],['closed',96,260],['open',260,262]],cons:5,res:96,cg:[[8,94]]},
 {fr:'Entretien trop rapide (alerte A4/A5)',en:'Interview too fast (alert A4/A5)',kid1223:1,seg:[['open',0,3],['int',3,15],['closed',15,260],['open',260,261]],cons:3,res:15,cg:[[4,14]]},
 {fr:'Enfant de 0–11 mois seulement, 18 minutes',en:'Child aged 0–11 months only, 18 minutes',kid1223:0,seg:[['open',0,4],['int',4,22],['closed',22,260],['open',260,262]],cons:4,res:22,cg:[[6,21]]}];
let dcur=0;
function hm(m){const h=8+Math.floor((m+5)/60),mm=(m+5)%60;return `${String(h).padStart(2,'0')}:${String(mm).padStart(2,'0')}`;}
function renderDur(){const el=$('#timeline');if(!el)return;const s=DUR[dcur],W=1000,X=m=>40+m*(W-80)/262;
 const col={open:'#7a9cc6',int:'#1f4e79',wait:'#c98a2b',closed:'#e3e7ec'};
 let g='';for(const [k,a,b] of s.seg){g+=`<rect x="${X(a)}" y="58" width="${Math.max(2,X(b)-X(a))}" height="34" fill="${col[k]}"/>`;}
 const mark=(m,lab,y)=>`<line x1="${X(m)}" x2="${X(m)}" y1="50" y2="100" stroke="#b03a2e" stroke-width="2"/><text x="${X(m)}" y="${y}" font-size="13" text-anchor="middle" fill="#b03a2e">${lab}</text>`;
 g+=mark(s.cons,t('consentement','consent'),44)+mark(s.res,t('résultat','result'),118);
 for(const [a,b] of s.cg){g+=`<rect x="${X(a)}" y="128" width="${X(b)-X(a)}" height="10" fill="#2e7d32"/><text x="${X(a)}" y="152" font-size="12" fill="#2e7d32">${t('femme 1','woman 1')}</text>`;}
 for(let m=0;m<=240;m+=60)g+=`<text x="${X(m)}" y="178" font-size="12" text-anchor="middle" fill="#55606e">${hm(m)}</text>`;
 const leg=[['int',t("À l'écran : entretien",'On screen: interview')],['open',t("À l'écran : ouverture, fin",'On screen: opening, closing')],['wait',t("À l'écran : attente (compte quand même)",'On screen: waiting (still counts)')],['closed',t('Formulaire fermé (ne compte pas)','Form closed (does not count)')]];
 leg.forEach(([k,l],i)=>{const lx=40+(i%2)*460,ly=196+Math.floor(i/2)*22;g+=`<rect x="${lx}" y="${ly}" width="14" height="14" fill="${col[k]}" stroke="#999"/><text x="${lx+20}" y="${ly+12}" font-size="13" fill="#1d2733">${l}</text>`;});
 el.innerHTML=`<svg viewBox="0 0 ${W} 244" role="img" aria-label="timeline"><text x="40" y="22" font-size="14" fill="#1d2733">${t('Heure sur la montre : ','Wall clock: ')}${hm(0)} → ${hm(s.seg[s.seg.length-1][2])}</text>${g}</svg>`;
 const active=s.seg.filter(x=>x[0]!=='closed').reduce((a,x)=>a+x[2]-x[1],0),im=s.res-s.cons,cgm=s.cg[0][1]-s.cg[0][0],wall=s.seg[s.seg.length-1][2];
 const flag=(im<15||(s.kid1223&&im<25))?1:0;
 const card=(lab,v,code,cls='')=>`<div><span>${lab}</span><b class="${cls}">${v}</b><code>${code}</code></div>`;
 $('#dvars').innerHTML=card(t('Fin moins début (ancien)','End minus start (old)'),`${Math.floor(wall/60)} h ${wall%60} min`,'duration','bad')+card(t('Temps à l\'écran','Time on screen'),active+' min','dur_active_min')+
  card(t('Durée de l\'entretien','Interview duration'),im+' min','dur_interview_min')+card(t('Femme 1','Woman 1'),cgm+' min','dur_cg_min_1')+
  card(t('Signal entretien court','Short-interview flag'),flag?t('Oui','Yes'):t('Non','No'),'flag_short_interview',flag?'bad':'ok');}
// ---------------- init
$$('.lang button').forEach(b=>b.onclick=()=>setLang(b.dataset.lang));
$('#dob')&&($('#dob').oninput=renderCard);
try{const s=localStorage.getItem('lang');if(s&&!location.search.includes('lang='))LANG=s;}catch(e){}
load(0);setLang(LANG);
if(location.hash.length>1){const el=document.getElementById(location.hash.slice(1));if(el)setTimeout(()=>el.scrollIntoView(),60);}
'''

page = f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Qualité des données Sankuru</title>
<meta name="description" content="Supports de formation : collecte de données et assurance qualité, enquête de couverture vaccinale Sankuru (UNIKIN), novembre 2026.">
<style>{CSS}</style></head>
<body>
<header><div class="in">
<div class="lang"><button data-lang="fr" aria-pressed="true">FR</button><button data-lang="en" aria-pressed="false">EN</button></div>
<h1>{T('Données de qualité, PSU parcouru en entier', 'Quality data, every PSU fully covered')}</h1>
<p>{T("Formation à la collecte de données et à l'assurance qualité pour les coordinateurs, superviseurs, chefs d'équipe, enquêteurs, gestionnaires de données et l'équipe qualité. Enquête de couverture vaccinale du Sankuru, UNIKIN, novembre 2026.",
      'Training in data collection and quality assurance for coordinators, supervisors, team chiefs, enumerators, data managers and the quality team. Sankuru vaccination coverage survey, UNIKIN, November 2026.')}</p>
</div></header>
<nav aria-label="Sections"><div class="in">{nav}</div></nav>
<main>{start}{process}{segments}{card}{duration}{rolesec}{codes}{selfcheck}{files}</main>
<footer><div class="in">{T("Préparé par UNIKIN pour l'enquête de couverture vaccinale du Sankuru. À lire avec le Protocole d'étude V1.0, la SOP-01 V1.0 et le Plan DQA V1.0.",
                            'Prepared by UNIKIN for the Sankuru vaccination coverage survey. Read with Study Protocol V1.0, SOP-01 V1.0 and DQA Plan V1.0.')}</div></footer>
<script>{JS}</script>
</body></html>'''
import re  # noqa: E402
from PIL import Image  # noqa: E402


def sized(m):
    w, h = Image.open(os.path.join(OUT, m[1])).size
    return f'<img width="{w}" height="{h}" src="{m[1]}"'


page = re.sub(r'<img src="(assets/[^"]+\.png)"', sized, page.replace('<img data-l="fr" src=', '<img src=').replace('<img data-l="en" src=', '<img src='))
page = re.sub(r'<img (width="\d+" height="\d+" src="assets/[^"]+_(fr|FR|en|EN)\.png")', lambda m: f'<img data-l="{m[2].lower()}" {m[1]}', page)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page)
print('site written to', OUT)
