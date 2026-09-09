import type {Metadata} from 'next';
import './globals.css';
import data from './generated/academic.json';
const publicSite = process.env.ACADEMIC_PUBLIC_SITE === 'true';
export const metadata:Metadata={title:`${data.profile.name} | ${data.profile.role}`,description:data.biography,metadataBase:new URL(process.env.ACADEMIC_SITE_URL || 'https://fleckenstein-m.github.io/'),robots:{index:publicSite,follow:publicSite}};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
