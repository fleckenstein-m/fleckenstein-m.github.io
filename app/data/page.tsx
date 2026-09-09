import data from '../generated/academic.json';
import {SiteFrame} from '../site-frame';
import type {Dataset} from '../types';

export const metadata = {title: 'Data | Matthias Fleckenstein'};

export default function DataPage() {
  const datasets = data.datasets as Dataset[];
  const papers = [...data.publications, ...data.other_publications];
  return <SiteFrame active="data"><main id="main" className="shell research-main data-main">
    <div className="page-heading"><p className="eyebrow">Research resources</p><h1>Data</h1></div>
    <p className="data-intro">Selected data and replication materials accompanying my research.</p>
    {datasets.length ? <div className="dataset-list">{datasets.map(item => {
      const paper = papers.find(p => p.id === item.paper_id)!;
      return <article key={item.id} id={item.id} className="dataset-entry">
        <h2>{item.title}</h2>
        <p className="dataset-paper">Associated paper: <a href={'/research/#'+paper.id}>{paper.title}</a></p>
        <p className="dataset-description">{item.description}</p>
        {item.updated && <p className="citation">Updated {item.updated}</p>}
        <div className="paper-links" aria-label={`Resources for ${item.title}`}>
          {item.files?.map(file => <a key={file.url} href={file.url} target="_blank" rel="noopener noreferrer">{file.label}</a>)}
          {item.replication_url && <a href={item.replication_url} target="_blank" rel="noopener noreferrer">Replication package</a>}
        </div>
        {item.citation && <p className="dataset-citation"><span>Please cite</span>{item.citation}</p>}
      </article>;
    })}</div> : <p className="data-empty">No datasets are posted yet.</p>}
  </main></SiteFrame>;
}
