"""Fusionne tous les scénarios Make en un seul scénario actif (offre gratuite : 2 actifs max).
Le scénario 2 devient le « hub » : passage planifié (sans mode) = publication + relances,
lancements manuels avec data.mode = ajouter | stats | export_stats | voix | veille | analyse |
importer | exporter | maj | bilan | importer_json | plan | pages | lire | ecrire | test_mail."""
import json, re, sys
SP = '/tmp/claude-0/-home-claude/0d2ec442-8b50-5cf5-89e8-ff56ed7ae875/scratchpad/'
SB, GH, YT, ZE, GE, RS = 12067470, 12075389, 12069432, 12080150, 12068262, 12067592

def renum(flow, off):
    """Renumérote les modules (id + off) et toutes les références {{N.…}}, feeder, $lid."""
    ids = set()
    def collect(f):
        for m in f:
            ids.add(m['id'])
            for r in m.get('routes', []): collect(r['flow'])
            for e in m.get('onerror', []): ids.add(e['id'])
    collect(flow)
    s = json.dumps(flow, ensure_ascii=False)
    def rep(mo):
        n = int(mo.group(2))
        return mo.group(1) + (str(n + off) if n in ids else mo.group(2)) + mo.group(3)
    # références de mapping : 12.body, (12.data …, ;12.x, +12.x, get(12.
    s = re.sub(r'([\{\(;\s+]|^)(\d+)(\.)', rep, s)
    f = json.loads(s)
    def fix(fl):
        for m in fl:
            m['id'] += off
            if 'feeder' in m.get('parameters', {}): m['parameters']['feeder'] += off
            for r in m.get('routes', []): fix(r['flow'])
            for e in m.get('onerror', []): e['id'] += off
    fix(f)
    return f

def mode(v):
    return {"name": f"mode = {v}", "conditions": [[{"a": "{{var.input.mode}}", "o": "text:equal", "b": v}]]}

def with_filter(flow, flt):
    flow = json.loads(json.dumps(flow))
    first = flow[0]
    old_groups = []
    if 'filter' in first:  # on garde les conditions existantes, sauf l'ancien filtre sur var.input.mode
        old_groups = [[c for c in g if c.get('a') != '{{var.input.mode}}'] for g in first['filter']['conditions']]
        old_groups = [g for g in old_groups if g]
    if old_groups:
        first['filter'] = {"name": flt['name'] + ' + ' + first['filter']['name'],
                           "conditions": [flt['conditions'][0] + g for g in old_groups]}
    else:
        first['filter'] = flt
    return flow

sans_mode = {"name": "passage planifié (sans mode)", "conditions": [[{"a": "{{var.input.mode}}", "o": "notexist"}]]}

# --- flows d'origine ---------------------------------------------------------------
prospects_lot = [
 {"id": 21, "module": "supabase:makeAnApiCall", "version": 1, "parameters": {"__IMTCONN__": SB}, "mapper": {"url": "/rest/v1/rpc/prospects_lot", "method": "POST", "headers": [{"key": "Content-Type", "value": "application/json"}], "body": "{\"n\": 15}"}, "onerror": [{"id": 24, "module": "builtin:Ignore", "version": 1}]},
 {"id": 22, "module": "resend:makeAnApiCall", "version": 1, "parameters": {"__IMTCONN__": RS}, "filter": {"name": "Lot non vide", "conditions": [[{"a": "{{21.body.nb}}", "b": "0", "o": "number:greater"}]]}, "mapper": {"url": "/emails/batch", "method": "POST", "headers": [{"key": "Content-Type", "value": "application/json"}], "body": "{{21.body.batch_text}}"}},
 {"id": 23, "module": "supabase:makeAnApiCall", "version": 1, "parameters": {"__IMTCONN__": SB}, "filter": {"name": "Envoi réussi", "conditions": [[{"a": "{{22.statusCode}}", "b": "200", "o": "number:equal"}]]}, "mapper": {"url": "/rest/v1/rpc/prospects_marquer", "method": "POST", "headers": [{"key": "Content-Type", "value": "application/json"}], "body": "{\"ids_text\": \"{{21.body.ids_text}}\"}"}}]
plan = [
 {"id": 30, "module": "supabase:makeAnApiCall", "version": 1, "parameters": {"__IMTCONN__": SB}, "mapper": {"url": "/rest/v1/rpc/plan_du_jour", "method": "POST", "headers": [{"key": "Content-Type", "value": "application/json"}], "body": "{}"}},
 {"id": 31, "module": "resend:sendAnEmail", "version": 1, "parameters": {"__IMTCONN__": RS}, "filter": {"name": "Quelque chose à valider", "conditions": [[{"a": "{{30.body.nb}}", "b": "0", "o": "number:greater"}]]}, "mapper": {"to": ["prouessia.contact@gmail.com"], "from": "Prouessia <reels@prouessia.fr>", "html": "{{30.body.html}}", "subject": "{{30.body.sujet}}", "sendEmailAs": "html"}}]
publication = [
 {"id": 1, "mapper": {"limit": 10, "table": "social_posts", "search": [[{"a": "status", "b": "valide", "o": "text:eq."}]]}, "module": "supabase:searchRows", "version": 1, "parameters": {"__IMTCONN__": SB}},
 {"id": 4, "filter": {"name": "Validé et à l'heure", "conditions": [[{"a": "{{1.status}}", "b": "valide", "o": "text:equal"}, {"a": "{{1.scheduled_at}}", "b": "{{addMinutes(now; 30)}}", "o": "date:lessorequal"}]]}, "mapper": {"id": "{{1.id}}", "table": "social_posts", "status": "en_publication"}, "module": "supabase:upsertARecord", "version": 1, "parameters": {"__IMTCONN__": SB}},
 {"id": 5, "mapper": {"video": "{{1.video_path}}", "content": "{{1.caption}}", "accountid": "6ad4e37eebbb709cd6908c42", "scheduledFor": "{{formatDate(addMinutes(now; 2); \"YYYY-MM-DDTHH:mm:ss.SSS[Z]\"; \"UTC\")}}"}, "module": "make-nodes-late:addInstagramReel", "version": 1, "parameters": {"__IMTCONN__": ZE}},
 {"id": 6, "mapper": {"video": "{{1.video_path}}", "content": "{{1.caption}}", "accountid": "6ad4e1fa979e52960a8126ab", "allow_duet": False, "allow_stitch": False, "scheduledFor": "{{formatDate(addMinutes(now; 2); \"YYYY-MM-DDTHH:mm:ss.SSS[Z]\"; \"UTC\")}}", "privacy_level": "PUBLIC_TO_EVERYONE", "allow_comments": True, "is_made_with_ai": False}, "module": "make-nodes-late:addTiktokPost", "version": 1, "parameters": {"__IMTCONN__": ZE}},
 {"id": 7, "mapper": {"url": "{{1.video_path}}", "shareCookies": False, "stopOnHttpError": True}, "module": "http:DownloadFile", "version": 4, "parameters": {"authenticationType": "noAuth"}},
 {"id": 8, "mapper": {"data": "{{7.data}}", "title": "{{substring(1.hook; 0; 90)}} #Shorts", "fileName": "{{7.fileName}}", "categoryId": "26", "description": "{{1.caption}}", "privacyStatus": "public", "containsSyntheticMedia": False, "selfDeclaredMadeForKids": False}, "module": "youtube:uploadVideo", "version": 4, "parameters": {"__IMTCONN__": YT}},
 {"id": 9, "mapper": {"id": "{{1.id}}", "table": "social_posts", "status": "publie", "platform_ids": "{\"instagram\":\"{{5.post.`_id`}}\",\"tiktok\":\"{{6.post.`_id`}}\",\"youtube\":\"{{8.id}}\"}"}, "module": "supabase:upsertARecord", "version": 1, "parameters": {"__IMTCONN__": SB}},
 {"id": 11, "filter": {"name": "Commentaire présent", "conditions": [[{"a": "{{1.pinned_comment}}", "o": "exist"}]]}, "mapper": {"qs": [{"key": "part", "value": "snippet"}], "url": "/v3/commentThreads", "body": {"snippet": {"videoId": "{{8.id}}", "topLevelComment": {"snippet": {"textOriginal": "{{1.pinned_comment}}"}}}}, "method": "POST", "headers": [{"key": "Content-Type", "value": "application/json"}]}, "module": "youtube:universal", "onerror": [{"id": 12, "module": "builtin:Ignore", "version": 1}], "version": 4, "parameters": {"__IMTCONN__": YT}}]
ajouter = [
 {"id": 3, "mapper": {"url": "https://raw.githubusercontent.com/PROUESSIA/prouessia-reels/main/{{var.input.video_file}}", "shareCookies": False, "stopOnHttpError": True}, "module": "http:DownloadFile", "version": 4, "parameters": {"authenticationType": "noAuth"}},
 {"id": 4, "mapper": {"upsert": True, "bucketID": "reels", "file_data": "{{3.data}}", "file_name": "{{var.input.video_file}}"}, "module": "supabase:uploadAFile", "version": 1, "parameters": {"__IMTCONN__": SB}},
 {"id": 1, "mapper": {"hook": "{{var.input.hook}}", "table": "social_posts", "topic": "{{var.input.topic}}", "series": "{{var.input.series}}", "status": "a_valider", "caption": "{{var.input.caption}}", "cover_path": "https://raw.githubusercontent.com/PROUESSIA/prouessia-reels/main/{{var.input.cover_file}}", "video_path": "https://qibubxxhvhghktlpvrls.supabase.co/storage/v1/object/public/reels/{{var.input.video_file}}", "scheduled_at": "{{var.input.scheduled_at}}", "pinned_comment": "{{var.input.pinned_comment}}", "sources_pdf_path": "https://github.com/PROUESSIA/prouessia-reels/blob/main/{{var.input.sources_file}}"}, "module": "supabase:createARow", "version": 1, "parameters": {"__IMTCONN__": SB}}]
stats = json.load(open(SP + 'stats.json'))
export = json.load(open(SP + 'export.json'))
voix = [
 {"id": 1, "mapper": {"url": "/v1beta/models/{{ifempty(var.input.model; \"gemini-3.8-flash-tts\")}}:generateContent", "body": "{\"contents\":[{\"parts\":[{\"text\":\"{{replace(replace(replace(\"### DIRECTOR'S NOTES (do not read aloud)\" + newline + var.input.style + newline + newline + \"### TRANSCRIPT (read only this, in French)\" + newline + var.input.text; \"\\\\\"; \"\\\\\\\\\"); \"\\\"\"; \"\\\\\\\"\"); newline; \"\\\\n\")}}\"}]}],\"generationConfig\":{\"responseModalities\":[\"AUDIO\"],\"speechConfig\":{\"voiceConfig\":{\"prebuiltVoiceConfig\":{\"voiceName\":\"{{ifempty(var.input.voice; \"Elio\")}}\"}}}}}", "method": "POST", "headers": [{"key": "Content-Type", "value": "application/json"}]}, "module": "gemini-ai:makeApiCall", "version": 1, "parameters": {"__IMTCONN__": GE}},
 {"id": 2, "mapper": {"url": "/repos/PROUESSIA/prouessia-reels/contents/{{var.input.path}}", "body": {"branch": "main", "content": "{{base64(get(get(1.body.candidates; 1).content.parts; 1).inlineData.data + \"|\" + 1.statusCode)}}", "message": "voix {{var.input.path}}"}, "method": "PUT"}, "module": "github:makeRestApiCall", "version": 4, "parameters": {"__IMTCONN__": GH}}]
v7 = json.load(open(SP + 'bp7.json'))['flow'][0]['routes']
veille, analyse = v7[0]['flow'], v7[1]['flow']
outils = json.load(open(SP + 'bp-prosp.json'))['flow'][0]['routes']
o_imp, o_exp, o_maj, o_bil, o_json = [r['flow'] for r in outils]

# mode pages : lit des fiches publiques d'annuaires (URL séparées par des virgules) et écrit leur texte dans le dépôt
pages = [
 {"id": 1, "module": "builtin:BasicFeeder", "version": 1, "mapper": {"array": "{{split(var.input.payload; \",\")}}"}},
 {"id": 2, "module": "http:MakeRequest", "version": 4, "parameters": {"authenticationType": "noAuth", "tlsType": ""},
  "mapper": {"url": "{{trim(1.value)}}", "method": "get", "contentType": "", "parseResponse": False, "stopOnHttpError": False, "timeout": 40,
             "allowRedirects": True, "shareCookies": False, "requestCompressedContent": True},
  "onerror": [{"id": 5, "module": "builtin:Ignore", "version": 1}]},
 {"id": 3, "module": "util:TextAggregator", "version": 1, "parameters": {"feeder": 1, "rowSeparator": "\n"},
  "mapper": {"value": "=== {{trim(1.value)}} [{{2.statusCode}}]\n{{substring(if(var.input.style; 2.data; stripHTML(2.data)); ifempty(var.input.after; 0); ifempty(var.input.n; 200000))}}"}},
 {"id": 4, "module": "github:makeRestApiCall", "version": 4, "parameters": {"__IMTCONN__": GH},
  "mapper": {"url": "/repos/PROUESSIA/prouessia-reels/contents/{{var.input.path}}", "method": "PUT",
             "body": {"branch": "main", "message": "pages annuaire", "content": "{{base64(3.text)}}"}}}]

# mode lire : GET /rest/v1/<query> (lecture de la table prospects) ; mode ecrire : upsert de prospects par SIREN
lire = [
 {"id": 1, "module": "supabase:makeAnApiCall", "version": 1, "parameters": {"__IMTCONN__": SB},
  "mapper": {"url": "/rest/v1/{{var.input.query}}", "method": "GET", "headers": [{"key": "Accept", "value": "text/csv"}]}},
 {"id": 2, "module": "github:makeRestApiCall", "version": 4, "parameters": {"__IMTCONN__": GH},
  "mapper": {"url": "/repos/PROUESSIA/prouessia-reels/contents/{{var.input.path}}", "method": "PUT",
             "body": {"branch": "main", "message": "lecture prospects", "content": "{{base64(1.statusCode + newline + toString(1.body))}}"}}}]
ecrire = [
 {"id": 1, "module": "supabase:makeAnApiCall", "version": 1, "parameters": {"__IMTCONN__": SB},
  "mapper": {"url": "/rest/v1/prospects?on_conflict=siren", "method": "POST", "body": "{{var.input.payload}}",
             "headers": [{"key": "Content-Type", "value": "application/json"}, {"key": "Prefer", "value": "resolution=merge-duplicates,return=minimal"}]}},
 {"id": 2, "module": "github:makeRestApiCall", "version": 4, "parameters": {"__IMTCONN__": GH},
  "mapper": {"url": "/repos/PROUESSIA/prouessia-reels/contents/{{var.input.path}}", "method": "PUT",
             "body": {"branch": "main", "message": "ecriture prospects", "content": "{{base64(1.statusCode + newline + toString(1.body))}}"}}}]

# mode test_mail : envoie un exemple d'e-mail UNIQUEMENT aux deux boîtes de la fondatrice (destinataires figés)
test_mail = [
 {"id": 1, "module": "resend:sendAnEmail", "version": 1, "parameters": {"__IMTCONN__": RS},
  "mapper": {"to": ["prouessia.contact@gmail.com", "rimbaabou9@gmail.com"], "from": "Prouessia <contact@prouessia.fr>", "replyTo": ["contact@prouessia.fr"],
             "subject": "{{var.input.hook}}", "html": "{{var.input.text}}", "sendEmailAs": "html"}}]

# mode copier : télécharge un fichier public (video_url) et le range dans le dépôt (path)
copier = [
 {"id": 1, "module": "http:DownloadFile", "version": 4, "parameters": {"authenticationType": "noAuth"},
  "mapper": {"url": "{{var.input.video_url}}", "shareCookies": False, "stopOnHttpError": True}},
 {"id": 2, "module": "github:makeRestApiCall", "version": 4, "parameters": {"__IMTCONN__": GH},
  "mapper": {"url": "/repos/PROUESSIA/prouessia-reels/contents/{{var.input.path}}", "method": "PUT",
             "body": {"branch": "main", "message": "copie {{var.input.path}}", "content": "{{base64(1.data)}}"}}}]

# mode comptes : liste des comptes connectés à Zernio (plateforme, id, nom) écrite dans le dépôt
comptes = [
 {"id": 1, "module": "make-nodes-late:getSocialAccounts", "version": 1, "parameters": {"__IMTCONN__": ZE}, "mapper": {"profileid": "6ad4b6cfee58f47508be0456"}},
 {"id": 2, "module": "util:TextAggregator", "version": 1, "parameters": {"feeder": 1, "rowSeparator": "\n"},
  "mapper": {"value": "{{1.platform}} | {{1._id}} | {{1.displayName}} | {{1.username}} | actif {{1.isActive}}"}},
 {"id": 3, "module": "github:makeRestApiCall", "version": 4, "parameters": {"__IMTCONN__": GH},
  "mapper": {"url": "/repos/PROUESSIA/prouessia-reels/contents/{{var.input.path}}", "method": "PUT",
             "body": {"branch": "main", "message": "comptes zernio", "content": "{{base64(2.text)}}"}}}]

routes = [
 (with_filter(prospects_lot, sans_mode), 0),
 (with_filter(publication, sans_mode), 100),
 (with_filter(plan, mode('plan')), 200),
 (with_filter(ajouter, mode('ajouter')), 300),
 (with_filter(stats, mode('stats')), 400),
 (with_filter(export, mode('export_stats')), 500),
 (with_filter(voix, mode('voix')), 600),
 (with_filter(veille, mode('veille')), 700),
 (with_filter(analyse, mode('analyse')), 800),
 (with_filter(o_imp, mode('importer')), 900),
 (with_filter(o_exp, mode('exporter')), 1000),
 (with_filter(o_maj, mode('maj')), 1100),
 (with_filter(o_bil, mode('bilan')), 1200),
 (with_filter(o_json, mode('importer_json')), 1300),
 (with_filter(pages, mode('pages')), 1400),
 (with_filter(lire, mode('lire')), 1500),
 (with_filter(ecrire, mode('ecrire')), 1600),
 (with_filter(test_mail, mode('test_mail')), 1700),
 (with_filter(copier, mode('copier')), 1800),
 (with_filter(comptes, mode('comptes')), 1900),
]
# les flows 7 et outils filtraient déjà sur var.input.mode (recherche/analyse/importer…) : on retire ce doublon
def strip_old(flow):
    f = flow[0]
    if 'filter' in f and ' + ' in f['filter']['name']:
        f['filter']['conditions'] = [[c for c in grp if not (c['a'] == '{{var.input.mode}}' and c['b'] in ('recherche', 'analyse', 'importer', 'exporter', 'maj', 'bilan', 'importer_json'))] for grp in f['filter']['conditions']]
    return flow
flows = [{"flow": renum(f, off)} for f, off in routes]
names = ['mode', 'plan', 'series', 'topic', 'hook', 'caption', 'pinned_comment', 'video_file', 'cover_file', 'sources_file', 'scheduled_at',
         'text', 'style', 'path', 'voice', 'model', 'query', 'after', 'video_url', 'departement', 'page', 'n', 'payload']
bp = {"name": "Prouessia · hub (publication, Reels, stats, veille, prospection)", "metadata": {"instant": False, "version": 1},
      "interface": {"input": [{"name": n, "type": "text", "required": False} for n in names], "output": []},
      "flow": [{"id": 5000, "module": "builtin:BasicRouter", "version": 1, "routes": flows}]}
# Reels prévus plus tard dans la journée (18 h) : seconde branche, programmée à l'heure exacte
import copy
pub = flows[1]['flow']
assert pub[0]['id'] == 101
maintenant = pub[1:]
plus_tard = copy.deepcopy(maintenant)
txt = json.dumps(plus_tard)
for i in (104, 105, 106, 107, 108, 109, 111, 112):
    txt = txt.replace('"id": %d' % i, '"id": %d' % (i + 20)).replace('{{%d.' % i, '{{%d.' % (i + 20))
txt = txt.replace('formatDate(addMinutes(now; 2); \\"YYYY', 'formatDate(101.scheduled_at; \\"YYYY')
plus_tard = json.loads(txt)
plus_tard[0]['filter'] = {"name": "Validé, prévu plus tard aujourd'hui", "conditions": [[{"a": "{{101.status}}", "b": "valide", "o": "text:equal"}, {"a": "{{101.scheduled_at}}", "b": "{{addMinutes(now; 30)}}", "o": "date:greater"}, {"a": "{{101.scheduled_at}}", "b": "{{addHours(now; 12)}}", "o": "date:lessorequal"}]]}
yt = [m for m in plus_tard if m['module'] == 'youtube:uploadVideo'][0]
yt['mapper']['privacyStatus'] = 'private'
yt['mapper']['publishAt'] = '{{formatDate(101.scheduled_at; "YYYY-MM-DDTHH:mm:ss.SSS[Z]"; "UTC")}}'
assert 'addMinutes(now; 2)' not in json.dumps(plus_tard)
flows[1]['flow'] = [pub[0], {"id": 150, "module": "builtin:BasicRouter", "version": 1, "routes": [{"flow": maintenant}, {"flow": plus_tard}]}]
json.dump(bp, open(SP + 'hub.json', 'w'), ensure_ascii=False)
s = json.dumps(bp, ensure_ascii=False)
print(len(s), 'caractères', s.count('"module"'), 'modules')
