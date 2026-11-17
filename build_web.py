"""Build Eslam's portfolio page from the single source: resume.yaml."""
from pathlib import Path
from html import escape

HERE = Path(__file__).parent


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return value[1:-1].replace('\\"', '"').replace('\\\\', '\\')
    return value


def load_resume(path):
    """Parse the small YAML subset used by resume.yaml (no dependencies)."""
    data = {}
    section = item = subsection = None
    last_entry = None
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        indent = len(raw) - len(raw.lstrip(' '))
        if indent == 0:
            key, _, value = line.partition(':')
            section = key.strip()
            data[section] = unquote(value) if value.strip() else ({} if section == 'education' else [])
            item = subsection = None
        elif indent == 2 and line.startswith('- '):
            item = {}
            if isinstance(data.get(section), list):
                data[section].append(item)
            subsection = None
            key, _, value = line[2:].partition(':')
            if value.strip():
                item[key.strip()] = unquote(value)
        elif indent == 2 and isinstance(data.get(section), dict):
            key, _, value = line.partition(':')
            data[section][key.strip()] = unquote(value)
        elif indent == 4:
            key, _, value = line.partition(':')
            key = key.strip()
            if key == 'bullets':
                item['bullets'] = []
                subsection = 'bullets'
            elif not value.strip():
                item[key] = []
                subsection = key
            else:
                item[key] = unquote(value)
                subsection = None
        elif indent == 6 and line.startswith('- ') and subsection == 'positions':
            key, _, value = line[2:].partition(':')
            entry = {key.strip(): unquote(value)}
            item.setdefault(subsection, []).append(entry)
            last_entry = entry
        elif indent == 8 and subsection == 'positions' and last_entry is not None:
            key, _, value = line.partition(':')
            last_entry[key.strip()] = unquote(value)
        elif indent >= 6 and line.startswith('- '):
            item.setdefault(subsection, []).append(unquote(line[2:]))
    return data


def roles_line(r):
    """Company-level role line; tolerates single-role and multi-position companies."""
    if 'positions' in r:
        return ' · '.join(p['role'] + ' (' + p['dates'] + ')' for p in r['positions'])
    return r['role']


def role_title_html(r):
    if 'positions' in r:
        rows = ''.join('<span class="pos"><strong>' + escape(p['role']) + '</strong> ' +
                       '<em>' + escape(p['dates']) + '</em></span>' for p in r['positions'])
        return rows + '<span class="loc">' + escape(r['location']) + '</span>'
    return (escape(r['role']) + ' <span class="loc">/ ' + escape(r['location']) + '</span>')


def role_html(r):
    return ('<article class="role"><div class="role-head"><h3>' + escape(r['company']) +
            '</h3><span>' + escape(r['dates']) + '</span></div><div class="role-title">' +
            role_title_html(r) + '</div>' +
            ('<p class="pref">' + escape(r['pref']) + '</p>' if r.get('pref') else '') + '<ul>' +
            ''.join('<li>' + escape(x) + '</li>' for x in r.get('bullets', [])) + '</ul></article>')


def mini_html(r):
    return ('<p class="mini"><strong>' + escape(r['company']) + '</strong> — ' +
            escape(roles_line(r)) + ' · ' + escape(r['location']) +
            '<span>' + escape(r['dates']) + '</span></p>')


def skills_html(items):
    return ''.join('<p class="skills-line"><span class="skills-label">' + escape(s['label']) +
                   ':</span> ' + escape(s['values']) + '</p>' for s in items)


data = load_resume(HERE / 'resume.yaml')
education = data['education']
links = data.get('links', [])
links_block = ''.join('<a href="' + escape(l['url']) + '" rel="me">' + escape(l['label']) +
                      '</a>' for l in links)
is_full = lambda r: r.get('detail', 'full') == 'full'
full_roles = [r for r in data['experience'] if is_full(r)]
compact_roles = [r for r in data['experience'] if not is_full(r)]
roles_block = ''.join(role_html(r) for r in full_roles)
compact_block = ''.join(mini_html(r) for r in compact_roles)
skills_block = skills_html(data['skills'])

css = ':root{--ink:#172d45;--muted:#526173;--accent:#a86717;--paper:#fffdf8;--line:#d9dfe4}*{box-sizing:border-box}body{margin:0;background:#e9edf0;color:var(--ink);font-family:Arial,sans-serif;line-height:1.6}main{max-width:960px;margin:48px auto;background:var(--paper);padding:64px 76px;box-shadow:0 12px 60px #172d4512}.eyebrow{text-transform:uppercase;letter-spacing:.22em;font-size:12px;color:var(--accent);font-weight:700}h1{font-size:clamp(32px,5vw,54px);line-height:1.08;letter-spacing:-.045em;margin:16px 0}header{border-top:6px solid var(--ink);padding-top:28px;padding-bottom:28px;border-bottom:1px solid var(--line)}.headline{font-size:22px;margin:0 0 18px;color:var(--muted)}.contact{display:flex;flex-wrap:wrap;gap:8px 22px;font-size:14px}a{color:inherit;text-underline-offset:4px}a:focus-visible{outline:3px solid var(--accent);outline-offset:4px}.intro{font-size:17px;margin:28px 0 32px;max-width:74ch}h2{font-size:12px;text-transform:uppercase;letter-spacing:.2em;color:var(--accent);border-bottom:1px solid var(--line);padding-bottom:10px;margin:32px 0 20px}.role{margin:0 0 28px;break-inside:avoid}.role-head{display:flex;justify-content:space-between;align-items:baseline;gap:16px}.role-head span{font-size:13px;color:var(--muted);white-space:nowrap}h3{font-size:23px;margin:0;letter-spacing:-.02em}.role-title{font-weight:700;margin:3px 0 10px;font-size:14px}.role-title .loc{font-weight:400;color:var(--muted)}.role-title .pos{display:flex;justify-content:space-between;gap:16px;font-weight:400;max-width:420px}.role-title .pos em{font-style:normal;color:var(--muted);font-size:13px;white-space:nowrap}.role-title .pos+.loc{margin-top:6px;display:block}.pref{font-size:13.5px;font-style:italic;color:var(--muted);margin:0 0 10px;max-width:70ch}ul{padding-left:19px;margin:0}li{padding-left:3px;margin:6px 0;font-size:14px;color:#263a4c}li::marker{color:var(--accent)}.mini{display:flex;justify-content:space-between;gap:16px;font-size:14px;color:var(--muted);margin:0 0 8px}.mini strong{color:var(--ink)}.mini span{white-space:nowrap}.skills{font-size:14px}.skills-line{margin:0 0 8px}.skills-label{font-weight:700;color:var(--ink)}.education{display:flex;justify-content:space-between;gap:24px;font-size:14px}footer{font-size:12px;color:var(--muted);border-top:1px solid var(--line);margin-top:32px;padding-top:16px}.print-button{position:fixed;right:24px;bottom:24px;border:0;border-radius:6px;padding:14px 20px;background:var(--ink);color:white;cursor:pointer;font:inherit}@media(max-width:650px){main{margin:0;padding:32px 24px}.role-head,.education{display:block}.contact{display:grid;gap:6px}.print-button{position:static;margin:16px 24px}}@page{size:A4;margin:16mm 17mm}@media print{body{background:white}main{margin:0;padding:0;max-width:none;box-shadow:none;background:white}header{padding-top:12px;padding-bottom:16px}h1{font-size:34px}.headline{font-size:18px}.intro{font-size:11px;margin:16px 0}h2{margin:18px 0 12px}h3{font-size:16px}.role{margin-bottom:17px}.role-title,.role-head span,li,.skills,.education,.contact{font-size:10px}li{margin:3px 0;line-height:1.45}.print-button{display:none}footer{font-size:9px}}'

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{escape(data['name'])} — {escape(data['title'])} specializing in backend systems, integrations and developer experience."><title>{escape(data['name'])} — {escape(data['title'])}</title><style>
{css}
</style></head><body><main><header><div class="eyebrow">{escape(data['eyebrow'])}</div><h1>{escape(data['name'])}</h1><p class="headline">{escape(data['title'])}</p><div class="contact"><span>{escape(data['location'])}</span><a href="mailto:{escape(data['email'])}">{escape(data['email'])}</a><a href="tel:{escape(data['phone_link'])}">{escape(data['phone'])}</a>{links_block}</div></header><p class="intro">{escape(data['intro'])}</p><section aria-labelledby="experience"><h2 id="experience">Professional experience</h2>{roles_block}</section>{"<section aria-labelledby=\"earlier\"><h2 id=\"earlier\">Earlier experience</h2>" + compact_block + "</section>" if compact_roles else ""}<section aria-labelledby="skills"><h2 id="skills">Technical skills</h2><div class="skills">{skills_block}</div></section><section aria-labelledby="education"><h2 id="education">Education</h2><div class="education"><strong>{escape(education['degree'])} · {escape(education['school'])}</strong><span>{escape(education['dates'])} · {escape(education['location'])}</span></div></section></main><button class="print-button" onclick="window.print()">Print / Save PDF</button></body></html>'''

(HERE / 'index.html').write_text(html)
print(f'Built index.html: {len(full_roles)} full roles, {len(compact_roles)} compact roles, {len(data["skills"])} skill groups')
