import data from '../generated/academic.json';
import { SiteFrame } from '../site-frame';
import { PaperList } from './paper-list';
import type {Dataset} from '../types';
export const metadata = {title:'Research | Matthias Fleckenstein'};
export default function Research(){
  const published=data.publications.filter(p=>p.type==='published');
  const working=data.publications.filter(p=>p.type==='working');
  const dataLinks: Record<string,string> = {};
  for (const item of data.datasets as Dataset[]) {
    if (!dataLinks[item.paper_id]) dataLinks[item.paper_id] = '/data/#'+item.id;
  }
  return <SiteFrame active="research"><main id="main" className="shell research-main">
    <div className="page-heading"><p className="eyebrow">Publications & working papers</p><h1>Research</h1></div>
    <nav className="section-nav" aria-label="Research sections"><a href="#publications">Published & forthcoming <span>{published.length}</span></a><a href="#working-papers">Working papers <span>{working.length}</span></a><a href="#other-publications">Other publications <span>{data.other_publications.length}</span></a></nav>
    <section id="publications" className="paper-section"><h2>Published & forthcoming</h2><PaperList papers={published} dataLinks={dataLinks}/></section>
    <section id="working-papers" className="paper-section"><h2>Working papers</h2><PaperList papers={working} dataLinks={dataLinks}/></section>
    <section id="other-publications" className="paper-section"><h2>Other publications</h2><PaperList papers={data.other_publications} dataLinks={dataLinks}/></section>
  </main></SiteFrame>
}
