"""Render the shared academic record using the MIT-licensed CleanCV template."""
from pathlib import Path
import os, shutil, subprocess, re

def tex(value):
    replacements={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','–':'--','—':'---'}
    replacements['†']=r'\textsuperscript{\dag}'
    return ''.join(replacements.get(c,c) for c in str(value))

def inline(value):
    """Render Markdown links from source text, escaping all ordinary text."""
    parts=[];pos=0
    for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)',str(value)):
        parts += [tex(str(value)[pos:m.start()]),r'\href{'+tex(m[2])+'}{'+tex(m[1])+'}'];pos=m.end()
    return ''.join(parts)+tex(str(value)[pos:])

def paper_list(records):
    lines=[r'\begin{enumerate}[leftmargin=1.6em,label={\arabic*.},itemsep=0.75em,parsep=0pt]']
    for paper in records:
        title=tex(paper['title'])
        if paper.get('url'):title=r'\href{'+tex(paper['url'])+'}{'+title+'}'
        lines += [r'\needspace{6\baselineskip}',r'\item\begin{samepage} '+title+r'\\',r'With '+tex(paper['coauthors'])+'.']
        if paper.get('journal'):lines.append(r'\\\emph{'+tex(paper['journal'])+'}, '+tex(paper['citation']))
        elif paper.get('status'):lines.append(r'\\'+tex(paper['status']))
        if paper.get('note'):lines.append(r'\\'+tex(paper['note']))
        if paper.get('award'):lines.append(r'\\\emph{'+tex(paper['award'])+'}')
        for recognition in paper.get('recognition',[]):lines.append(r'\\'+tex(recognition))
        for media in paper.get('media',[]):lines.append(r'\\{\small\href{'+tex(media['url'])+'}{'+tex(media['label'])+'}, '+tex(media['date'])+'}')
        lines.append(r'\end{samepage}')
    return lines+[r'\end{enumerate}']

def record_section(title,records):
    lines=[r'\section*{'+tex(title)+'}']
    for item in records:
        lines += [r'\needspace{4\baselineskip}']
        if item.get('text') or item.get('items'):
            lines.append(r'\textbf{'+inline(item['title'])+r'}\par')
            if item.get('text'):lines.append(inline(item['text'])+r'\par')
            if item.get('items'):
                lines.append(r'\begin{itemize}[leftmargin=1.3em,itemsep=0.2em]')
                lines.extend(r'\item '+inline(x) for x in item['items'])
                lines.append(r'\end{itemize}')
        else:lines.append(inline(item['title'])+r'\par')
        lines.append(r'\medskip')
    return lines

def render_cv(data, root):
    work=root/'work'/'cv';work.mkdir(parents=True,exist_ok=True)
    shutil.copy2(root/'templates'/'cleancv'/'cleancv.sty',work/'cleancv.sty')
    p=data['profile']
    lines=[r'\documentclass[letterpaper,11pt]{article}',r'\usepackage{cleancv}',r'\usepackage{needspace}',
      r'\hypersetup{pdftitle={Matthias Fleckenstein - Curriculum Vitae},pdfauthor={Matthias Fleckenstein}}',
      r'\fancyfoot[R]{\footnotesize Record updated: '+tex(p['updated'])+'}',
      r'\begin{document}',r'\cvname{'+tex(p['name'])+'}',r'\begin{center}\small',
      tex(p['role'])+r'\enspace | \enspace '+tex(p['institution'])+r'\\[3pt]',
      r'\faHome\space\href{'+p['website']+'}{'+tex(p['website'].split('://')[-1].removeprefix('www.'))+r'}\quad '+r'\faEnvelope\space\href{mailto:'+p['email']+'}{'+tex(p['email'])+r'}\quad\faPhone\space '+tex(p['phone'])+r'\\[3pt]',tex(p['school'])+r'\\',tex(p['office']+', '+p['address']),r'\end{center}',
      r'\section*{Employment}']
    for e in data['employment']:
        lines.extend([r'\needspace{5\baselineskip}',r'\textbf{'+tex(e['institution'])+r'}\par'])
        for r in e['roles']:lines.append(tex(r['title'])+r'\hfill '+tex(r['dates'])+r'\par')
        lines.append(r'\medskip')
    lines.append(r'\section*{Education}')
    for e in data['education']:
        lines += [r'\needspace{4\baselineskip}',r'\textbf{'+tex(e['institution'])+r'}\hfill '+tex(e['year'])+r'\\',tex(e['degree'])+r'\par\medskip']
    lines += [r'\section*{Published and Forthcoming Papers}']
    lines += paper_list([x for x in data['publications'] if x['type']=='published'])
    lines += [r'\section*{Non-Refereed Publications}']+paper_list(data['other_publications'])
    lines += [r'\section*{Working Papers}']+paper_list([x for x in data['publications'] if x['type']=='working'])
    lines += record_section('Citations',data['citations'])
    lines += [r'\section*{Invited Seminars and Conference Presentations}']
    papers={x['id']:x for x in data['publications']}
    for item in data['presentations']:
        title=item.get('title_at_presentation',papers[item['paper_id']]['title'])
        lines += [r'\needspace{6\baselineskip}',r'\textbf{'+tex(title)+r'}\par']
        for category in ['conferences','seminars']:
            if item.get(category):lines.append(r'\emph{'+category.capitalize()+':} '+tex(item[category])+r'\par')
        lines.append(r'\medskip')
    lines.append(r'{\small '+tex(data['presentations_note'])+r'}\par')
    lines += record_section('Invited Discussions',data['discussions'])
    lines.append(r'{\small '+tex(data['discussions_note'])+r'}\par')
    for title,key in [('Teaching','teaching'),('Honors and Awards','awards'),('Service to the Profession','professional_service'),('Service to the University','university_service'),('Additional Information','additional_information')]:
        lines += record_section(title,data[key])
    lines.append(r'\end{document}')
    (work/'cv.tex').write_text('\n'.join(lines),encoding='utf-8')
    engine=os.environ.get('ACADEMIC_LATEX') or shutil.which('pdflatex')
    if not engine:raise RuntimeError('Install a LaTeX distribution or set ACADEMIC_LATEX to pdflatex.')
    for _ in range(2):
        result=subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error','-no-shell-escape','cv.tex'],cwd=work,capture_output=True,text=True,encoding='utf-8',errors='replace')
        (work/'compile-output.txt').write_text(result.stdout+result.stderr,encoding='utf-8')
        if result.returncode:raise RuntimeError('CleanCV compilation failed. See work/cv/compile-output.txt\n'+result.stdout[-2500:])
    output=root/'public'/'Matthias-Fleckenstein-CV.pdf'
    shutil.copy2(work/'cv.pdf',output)
    # Keep previous review links working while the website uses the stable CV URL.
    shutil.copy2(output,root/'public'/'Matthias-Fleckenstein-CV-proof.pdf')
    print('Generated complete CleanCV:',output)
