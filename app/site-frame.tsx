import data from './generated/academic.json';
export function Arrow(){return <span aria-hidden="true">↗</span>}
export function SiteFrame({children,active}:{children:React.ReactNode,active:string}){
  return <>
    <a className="skip-link" href="#main">Skip to content</a>
    <header className="site-header"><div className="shell header-inner">
      <a href="/" className="wordmark"><span className="monogram" aria-hidden="true">MF</span><span>{data.profile.name}</span></a>
      <nav aria-label="Main navigation">{[['home','/','Home'],['research','/research/','Research'],['data','/data/','Data'],['teaching','/teaching/','Teaching'],['cv','/cv/','CV']].map(([id,href,label])=><a key={id} href={href} aria-current={active===id?'page':undefined}>{label}</a>)}</nav>
    </div></header>
    {children}
    <footer className="site-footer shell">
      <span>{data.profile.name} <span className="footer-dot">·</span> {data.profile.institution}</span>
      <nav className="footer-links" aria-label="Contact and social profiles">
        <a href={'mailto:'+data.profile.email}>Get in touch <Arrow/></a>
        {data.social_links.map(link=><a key={link.url} href={link.url} target="_blank" rel="noopener noreferrer">{link.label}</a>)}
      </nav>
    </footer>
  </>;
}
