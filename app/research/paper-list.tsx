'use client';
import {useEffect, useState} from 'react';
import {Accordion, AccordionItem, AccordionTrigger, AccordionContent} from '@/components/ui/accordion';
import type {Paper} from '../types';

export function PaperList({papers, dataLinks = {}}: {papers: Paper[], dataLinks?: Record<string, string>}) {
  const [open, setOpen] = useState<string[]>([]);
  useEffect(() => {
    const show = () => {
      const id = window.location.hash.slice(1);
      if (papers.some(p => p.id === id)) setOpen(v => v.includes(id) ? v : [...v, id]);
    };
    show();
    window.addEventListener('hashchange', show);
    return () => window.removeEventListener('hashchange', show);
  }, [papers]);

  return <Accordion multiple value={open} onValueChange={setOpen} className="paper-list">
    {papers.map(p => <AccordionItem key={p.id} value={p.id} id={p.id} className="paper-entry">
      <div className="paper-summary">
        <h3 className="paper-title">{p.title}</h3>
        {p.coauthors && <p className="coauthors">With {p.coauthors}</p>}
        <p className="paper-meta">
          {p.journal ? <><span className="journal">{p.journal}</span>{p.year && <span>{p.year}</span>}</> : <span className="working-status">{p.status}</span>}
          {p.award && <span className="award">{p.award}</span>}
        </p>
        {p.citation && <p className="citation">{p.citation}</p>}
        {p.note && <p className="citation">{p.note}</p>}
      </div>
      <div className="paper-links" aria-label={`Resources for ${p.title}`}>
        {p.url && <a href={p.url} target="_blank" rel="noopener noreferrer">{p.type === 'working' ? 'Working paper' : 'Published version'}</a>}
        {p.pdf && <a href={p.pdf} target="_blank" rel="noopener noreferrer">Paper PDF</a>}
        {p.appendix && <a href={p.appendix} target="_blank" rel="noopener noreferrer">Internet Appendix</a>}
        {dataLinks[p.id] && <a href={dataLinks[p.id]}>Data & replication</a>}
      </div>
      {!!p.media?.length && <div className="paper-media"><span className="media-label">Media coverage</span><ul>
        {p.media.map(m => <li key={m.url}><a href={m.url} target="_blank" rel="noopener noreferrer">{m.label}</a>{m.date && <span className="media-date">{m.date}</span>}</li>)}
      </ul></div>}
      {p.abstract && <><AccordionTrigger className="paper-trigger"><span>Abstract</span></AccordionTrigger>
        <AccordionContent className="paper-detail"><p className="abstract">{p.abstract}</p></AccordionContent></>}
    </AccordionItem>)}
  </Accordion>;
}
