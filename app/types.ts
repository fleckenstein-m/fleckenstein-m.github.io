export type CourseLink = {
  id: string;
  code: string;
  title: string;
  term: string;
  url: string;
};

export type Paper = {
  id: string;
  title: string;
  type?: string;
  coauthors?: string;
  year?: number;
  journal?: string;
  citation?: string;
  status?: string;
  note?: string;
  url?: string;
  pdf?: string;
  appendix?: string;
  abstract?: string;
  award?: string;
  media?: {label: string; url: string; date?: string}[];
};

export type Dataset = {
  id: string;
  paper_id: string;
  title: string;
  description: string;
  updated?: string;
  citation?: string;
  files?: {label: string; url: string}[];
  replication_url?: string;
};
