import data from '../generated/academic.json';
import {SiteFrame, Arrow} from '../site-frame';
import type {CourseLink} from '../types';

export const metadata = {title: 'Teaching | Matthias Fleckenstein'};

export default function Teaching() {
  const courses = data.course_links as CourseLink[];
  const terms = [...new Set(courses.map(course => course.term))];
  return <SiteFrame active="teaching"><main id="main" className="shell research-main teaching-main">
    <div className="page-heading"><p className="eyebrow">Courses & materials</p><h1>Teaching</h1></div>
    {terms.map(term => <section className="course-term" key={term}>
      <h2>{term}</h2>
      <div className="course-list">{courses.filter(course => course.term === term).map(course => <article className="course-entry" id={course.id} key={course.id}>
        <div><p className="course-code">{course.code}</p><h3><a href={course.url} target="_blank" rel="noopener noreferrer">{course.title}</a></h3></div>
        <a className="text-link course-link" href={course.url} target="_blank" rel="noopener noreferrer" aria-label={`Course website for ${course.code}, ${course.term}`}>Course website <Arrow/></a>
      </article>)}</div>
    </section>)}
    {!courses.length && <p className="data-empty">No course websites are posted yet.</p>}
  </main></SiteFrame>;
}
