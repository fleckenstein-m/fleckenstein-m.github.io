import data from './generated/academic.json';
import { SiteFrame, Arrow } from './site-frame';
import type {Paper} from './types';

function FeaturedPapers({papers}: {papers: Paper[]}) {
  return <div className="selected-grid">{papers.map(p => <article className="selected-paper" key={p.id}>
    <p className={p.type === 'published' ? 'journal' : 'featured-status'}>
      {p.type === 'published' ? <>{p.journal}{p.year && <span> · {p.year}</span>}</> : (p.status || 'Working paper')}
    </p>
    <h3><a href={'/research/#'+p.id}>{p.title}</a></h3>
    {p.coauthors && <p className="coauthors">With {p.coauthors}</p>}
    <a className="text-link" href={'/research/#'+p.id}>Read more <Arrow/></a>
  </article>)}</div>;
}

export default function Home() {
  const p = data.profile;
  const papers = data.publications as Paper[];
  const recent = data.homepage.publications.map(id => papers.find(p => p.id === id)!);
  const working = data.homepage.working_papers.map(id => papers.find(p => p.id === id)!);
  return <SiteFrame active="home"><main id="main" className="shell">
    <section className="intro">
      <div className="portrait-column"><img className="portrait" src={p.portrait} width="250" height="375" alt={p.name}/><div className="portrait-caption"><span>{p.institution}</span><span>{p.school}</span></div></div>
      <div className="intro-copy"><p className="eyebrow">Finance · {p.institution}</p><h1>{p.name.split(' ')[0]}<br/>{p.name.split(' ').slice(1).join(' ')}</h1><p className="role">{p.role}</p><p className="biography">{data.biography}</p><div className="intro-actions"><a className="button primary" href="/research/">Explore research <Arrow/></a><a className="text-link" href="/cv/">Curriculum vitae <Arrow/></a></div><dl className="contact"><div><dt>Email</dt><dd><a href={'mailto:'+p.email}>{p.email}</a></dd></div><div><dt>Office</dt><dd>{p.office}<br/>{p.address}</dd></div></dl></div>
    </section>
    {!!recent.length && <section className="selected-section" aria-labelledby="recent-publications"><div className="section-heading"><h2 id="recent-publications">Recent publications</h2><a className="text-link" href="/research/#publications">All publications <Arrow/></a></div><FeaturedPapers papers={recent}/></section>}
    {!!working.length && <section className="selected-section" aria-labelledby="recent-working-papers"><div className="section-heading"><h2 id="recent-working-papers">Recent working papers</h2><a className="text-link" href="/research/#working-papers">All working papers <Arrow/></a></div><FeaturedPapers papers={working}/></section>}
  </main></SiteFrame>;
}

