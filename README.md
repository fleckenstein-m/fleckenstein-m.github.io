# Maintaining the academic website and CV

Edit [content/academic.md](content/academic.md) to update the website and full CleanCV PDF. Store downloadable files in `public/`. Everything else is generated or controls the design.

Project folder on this computer: `F:\AcademicWebpage\github-pages-migration`. Use its `master` branch for routine updates.

The [public website](https://www.mfleckenstein.com/) is live on GitHub Pages at **https://www.mfleckenstein.com/**. The address without `www` redirects to it. The installed [Academic website workflow](.github/workflows/pages.yml) builds and checks updates to `master`; publication requires a manual run with **Publish this build to the public academic website** checked. Building locally does not publish. See [the GitHub Pages guide](docs/GITHUB-PAGES.md#routine-updates-after-migration) for routine updates and rollback instructions.

The [private design preview](https://matthias-fleckenstein-design-proof.magicmaze.chatgpt.site/) remains separate. Maintain this GitHub checkout as the authoritative source; edits do not automatically synchronize to the old design-proof folder or its hosted preview.

The custom domain was connected on September 10, 2026. IONOS manages the domain registration and DNS; GitHub Pages serves the website and its HTTPS certificate. The repository variable `ACADEMIC_SITE_URL` is set to `https://www.mfleckenstein.com/`, and `profile.website` in the main content file supplies the CV's website link. Ordinary content updates need no DNS changes. See [the saved domain configuration](docs/GITHUB-PAGES.md#custom-domain-configuration) for the exact settings and the IONOS `www` checkbox detail.

## 1. What goes where

| Change | Location in academic.md | Appears in |
| --- | --- | --- |
| Contact details and position | `profile` | Website and CV, where applicable |
| LinkedIn, Twitter / X, and other social profiles | `social_links` | Website footer |
| Employment and education | `employment`, `education` | CV |
| Research description | Prose after the closing `---` | Homepage and website description |
| Featured publications and working papers | `homepage` | Homepage only |
| Published and working papers | `publications` | Research page and CV |
| Book chapters and other publications | `other_publications` | Research page and CV |
| Abstracts | Paper's `abstract` | Research page, expandable |
| Publisher or repository link | Paper's `url` | Visible research link and linked CV title |
| Author's paper PDF | Paper's `pdf` | Visible research link |
| Internet Appendix | Paper's `appendix` | Visible research link |
| Media coverage | Paper's `media` | Visible research links and CV |
| Data and replication materials | `datasets` | Data page and a link from the related paper |
| Presentations and discussions | `presentations`, `discussions` | CV |
| Course website links | `course_links` | Teaching page |
| Full teaching history, awards, service | Corresponding named sections | CV |
| Citation counts | `citations` | CV |
| Record update date | `profile.updated` | CV page and PDF |

Paper PDFs, appendices, and datasets supplement the website. They do not add lines to the CV or replace publisher links. The CV retains its existing layout and bibliographic entries.

Presentations and discussions appear in the downloadable CV. The Teaching page lists selected course websites; the full teaching history remains in the CV.

## 2. Understand the master file

The file is Markdown with structured YAML between two `---` lines. Your research description follows the second line:

```yaml
---
profile:
  name: Matthias Fleckenstein
  # Other existing profile fields remain here.
publications:
  # Paper entries remain here.
# Other existing sections remain here.
---
Your research description goes here as plain prose.
```

This is a structural illustration, not a replacement for your complete file.

- Copy a similar existing entry and edit its fields.
- Preserve indentation; use spaces, not tabs.
- Quote text containing a colon, for example `title: "A Title: With a Subtitle"`.
- Use `>-` for long paragraphs, indenting the following lines by two additional spaces.
- Keep each section heading only once. Duplicate headings are rejected rather than silently replacing an earlier list.
- Omit an optional field when it has no value; do not add a blank link.
- Entries appear in file order. They are not automatically sorted by date.
- Keep IDs stable when a paper title or status changes.
- Do not edit `app/generated/academic.json`, `work/cv/cv.tex`, exported HTML, or the generated PDF.

## 3. Add a new working paper

Add an entry under the existing `publications:` heading. The following example is fictional; replace the details and omit the URL until you have one:

```yaml
- id: financial-frictions-and-arbitrage
  title: Financial Frictions and Arbitrage
  type: working
  coauthors: Jane Smith and John Doe
  status: Working paper.
  url: https://example.com/paper
  abstract: >-
    We study how financial frictions affect arbitrage
    activity and asset prices.
```

`id` must be unique and use lowercase letters, numbers, and hyphens. Presentations and data records refer to it. The website supports papers without coauthors; the current CV renderer still expects the `coauthors` field, so ask for the small CV adjustment before adding a solo-authored paper.

Use `status` for an R&R and `note` for information such as a previous title:

```yaml
  status: Revise and Resubmit at Journal of Financial Economics.
  note: Previously titled An Earlier Title.
```

Keep all bibliographic fields as part of the same paper entry.

## 4. Move a paper to published or forthcoming

Edit the existing entry; do not create a second copy. Keep its `id`, title, coauthors, abstract, local file fields, and media list. Update these fields:

```yaml
  type: published
  year: 2027
  journal: Journal of Financial Economics
  citation: Forthcoming.
```

Remove the stale working-paper or R&R `status`. Update `url` to the publisher's page or DOI. Once available, replace `Forthcoming.` with the final volume, issue, and page details.

Move the entry to the desired position among published papers. If it was featured under `homepage.working_papers`, remove it from that list and optionally add its ID under `homepage.publications`. The build rejects a paper whose category no longer matches its homepage selection.

### Choose the homepage's recent papers

The homepage has two matching sections: **Recent publications** and **Recent working papers**, with up to two papers in each. The `homepage` section near the top of academic.md controls the selections independently of the Research page and CV ordering:

```yaml
homepage:
  publications:
  - do-municipal-bond-investors-pay-a-convenience-premium-to-avoid-taxes
  - treasury-richness
  working_papers:
  - the-puzzling-internal-inconsistencies-in-term-structures-of-bank-cd-rates
  - fixed-floating-interest-rate-parity
```

To feature another paper, replace an ID in the relevant list with that paper's existing ID. Change the list order to change the display order. The title, coauthors, journal, year, and working-paper status are taken from the paper record; do not duplicate them here. New papers are not automatically featured when these lists are present. Use `[]` to hide a section, or one ID to show a single paper. If a list is omitted, it defaults to the first two papers in that category.

These are editorial selections: choose the newest or most recently revised work you want to highlight. Working-paper revision dates are not consistently recorded, so the site does not attempt to infer recency from titles or statuses.

## 5. Add a local paper PDF or Internet Appendix

Keep `url` as the publisher/repository link. Add `pdf` and `appendix` alongside it:

```yaml
  url: https://doi.org/your-real-doi
  pdf: /papers/treasury-richness.pdf
  appendix: /appendices/treasury-richness-internet-appendix.pdf
```

Replace the example DOI with the real URL. Add only fields whose files you have copied into the project.

| File on this computer | Value in academic.md |
| --- | --- |
| `F:\AcademicWebpage\github-pages-migration\public\papers\treasury-richness.pdf` | `/papers/treasury-richness.pdf` |
| `F:\AcademicWebpage\github-pages-migration\public\appendices\treasury-richness-internet-appendix.pdf` | `/appendices/treasury-richness-internet-appendix.pdf` |

The `public` folder is the website root, so **do not include `public` in the link**. Do not use an `E:\` or `F:\` path in a URL. Files elsewhere on your computer are not automatically copied or synchronized.

The Research page shows **Published version**, **Paper PDF**, and **Internet Appendix** whenever their respective fields are present. Working papers use **Working paper** for the main external link. The abstract control contains only the abstract. Media coverage stays visible beneath the resource links.

Local filenames must match exactly, including capitalization. Prefer lowercase names with hyphens and no spaces. The build checks file existence, exact capitalization, and the PDF header before generating the outputs. It also rejects unsupported URL schemes and paths outside `public/`.

Both `pdf` and `appendix` may alternatively use an external HTTP(S) URL. The build does not fetch external URLs to verify availability.

To update a paper while keeping its link stable, replace the file using the same filename and rebuild. To preserve a dated version, add a new filename and update the field. Every file in `public/` is included in the deployed website, even if no page links to it; keep only material intended for website distribution there.

## 6. Add media coverage

Add to the paper's existing `media:` list, or create it if absent:

```yaml
  media:
  - label: Publication Name
    url: https://example.com/article
    date: September 9, 2026.
```

Use the real outlet, link, and date. These entries appear outside the abstract on the Research page and in the CV. Keep `date` because the CV uses it.

## 7. Add data or a replication package

The first dataset is the Figure 2 TIPS–Treasury mispricing series. This is its actual entry under `datasets:` in academic.md:

```yaml
datasets:
- id: tips-treasury-mispricing
  paper_id: the-tips-treasury-bond-puzzle
  title: TIPS–Treasury Mispricing
  description: >-
    Time series of the average TIPS-Treasury mispricing, measured in basis points,
    across the pairs included in the sample, where the average is weighted by the
    notional amount of the TIPS issue. Data plotted in Figure 2 of the paper.
  files:
  - label: Download data (Excel)
    url: /data/FLL_2014_JF.xlsx
```

The file lives at `F:\AcademicWebpage\github-pages-migration\public\data\FLL_2014_JF.xlsx`. Its website path is `/data/FLL_2014_JF.xlsx`: omit `public` and retain the exact filename capitalization. The dataset description is displayed as written, and **Associated paper** links to the paper identified by `paper_id`.

### Add another dataset

1. Copy the new file into `public/data/`. You can create a subfolder for a paper, such as `public/data/treasury-richness/`, to keep its data and documentation together.
2. Copy an existing dataset entry under the same `datasets:` heading. Keep that heading only once and retain the other entries.
3. Give the new dataset a unique `id`, set `paper_id` to its paper's existing ID, and replace the title and description. Include units, weighting, sample coverage, or a figure/table reference when useful.
4. Update each file's `label` and `url`. A file in `public/data/treasury-richness/series.csv` uses `/data/treasury-richness/series.csv`.
5. Save academic.md and run `npm run build`. During an existing local preview, `npm run content` refreshes the data. Check the Data entry, its paper association, and the download before publishing.
6. Publish through the current hosting workflow. Copying a file or rebuilding locally does not update the hosted website by itself.

Dataset entries appear in file order. Put a new entry first if you want it listed first. Replacing a file using the same filename keeps its website link stable; rebuild and publish after replacing it.

The Data page supports downloadable Excel, CSV, Stata, PDF, ZIP, and other file formats. Files are served as supplied; publishing does not modify spreadsheet contents. External HTTP(S) links also work in `files`.

To provide additional formats or a data dictionary, append more entries under the dataset's `files` list. Add an optional `replication_url` for a repository or ZIP package, `updated` for a stated revision date, or `citation` for the text users should cite.

- `paper_id` must match a paper in `publications` or `other_publications`.
- `id` is the dataset's own unique identifier and determines its page anchor.
- `title` and `description` are required.
- `updated` and `citation` are optional text. Quote an ISO date such as `"2026-09-09"` to keep it text.
- Each `files` entry needs `label` and `url`.
- `replication_url` is optional and can point to an external repository or a local ZIP file.
- At least one file or replication link is required. Keep unpublished drafts outside the `datasets` list.

For a replication package only, omit `files` and retain `replication_url`. For data without replication materials, omit `replication_url`.

Adding a dataset automatically adds **Data & replication** to the related paper on the Research page. The Data entry links back to that paper. Multiple datasets may reference the same paper; the research link goes to the first of them in file order.

For small selected datasets, local files are convenient. For substantial replication archives, prefer linking to the journal's repository or an archival repository. This keeps the website lightweight and gives the package a stable independent location. GitHub Pages has a [1 GB published-site limit](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits).

## 8. Add a presentation

Presentations are grouped by paper. Under `presentations:`, find the paper's entry and append the new event to `conferences` or `seminars`. If it has no entry yet:

```yaml
- paper_id: treasury-richness
  conferences: Conference Name (2027)
  seminars: University Name (2027), Another University (2027)
```

Keep one group per paper rather than creating another entry for each talk. The CV obtains the title from the paper record. Use `title_at_presentation` only to preserve a historical title when appropriate.

Your existing convention uses `†` for a coauthor's presentation. The explanatory `presentations_note` appears in the CV.

## 9. Add a discussion

Under `discussions:`, add the newest event at the top:

```yaml
- title: Western Finance Association (2027)
  text: "Paper Title by Jane Smith and John Doe"
```

This appears in the CV. There is currently no dedicated discussion-slides field or discussions website page. Do not add a `slides` field expecting it to display automatically.

## 10. Update teaching, awards, and service

### Add a course website to the Teaching page

Under the existing `course_links:` heading in academic.md, add a new entry. For example:

```yaml
- id: financial-data-analytics-spring-2027
  code: FINC 672
  title: Financial Data Analytics
  term: Spring 2027
  url: https://example.com/your-course-website/
```

Replace the example URL with the actual course website. All five fields are required. Use a unique ID for each course offering, usually including its semester and year. The link must be a full HTTP(S) URL; the course website stays at its existing address and is not copied into the academic site.

The Teaching page groups entries by the exact `term` text. Put new courses at the top of the list to show the newest semester first; courses within a semester follow their file order. Use the same term spelling for courses that belong together. Keep older links to retain an archive, or remove their `course_links` entries to stop displaying them. This does not delete the linked course website.

The initial Spring 2026 entries are **FINC 409 / 609 — Fixed Income Securities** and **FINC 672 — Financial Data Analytics**. The fixed-income URL contains `FINC462-662`, but its current page title and the CV use FINC 409/609; the website label follows the course page.

Save academic.md, run `npm run build`, and review `/teaching/`. During an existing local preview, use `npm run content` to refresh the content. Publishing is still a separate step, described in [the migration guide](docs/GITHUB-PAGES.md).

`course_links` controls the website links only. Add the course to `teaching` below it as well if it belongs in the CV history. Both are maintained in this same master file.

### Update the CV's teaching history

For teaching, add a course under the existing institution's `items:` list:

```yaml
- title: University of Delaware (Instructor)
  items:
  - "FINC 672: Financial Data Analytics (MS; Spring 2027)"
  # Keep the other existing courses below it.
```

For an award, add under `awards:`:

```yaml
- title: Awarding Organization (2027)
  text: Name of Award
```

For service, edit the appropriate entry under `professional_service:` or `university_service:`. For example, append a journal to the referee list or add:

```yaml
- title: Committee Name (2027–Present)
  text: Committee member
```

Update employment and education using the existing institution, role, degree, and date fields. These sections remain part of the CV.

## 11. Update the research description, dates, and social links

Edit the plain prose after the final `---` to change the homepage research description. Your September 9, 2026 revision is preserved. The description is treated as plain text, not as a full Markdown document.

Near the top, change the record date when appropriate:

```yaml
  updated: September 2026
```

This date is manual. Citation counts have their own dates under `citations`; update those only when you refresh the counts. Neither date is silently replaced with the build date.

### Footer social links

Edit `social_links` near the top of `content/academic.md`. These appear as small text links beside **Get in touch** in the footer of every page:

```yaml
social_links:
- label: LinkedIn
  url: https://www.linkedin.com/in/matthias-fleckenstein-a327915/
- label: Twitter / X
  url: https://x.com/m_fleckenstein
```

Change a label or URL, reorder entries, or copy an entry to add another profile. Use a complete `https://` URL. Remove an entry to hide that link; use `social_links: []` to hide all social links. These settings apply only to the website footer. Rebuild and publish using the instructions below.

## 12. Build and preview on this computer

Open PowerShell:

```powershell
Set-Location 'F:\AcademicWebpage\github-pages-migration'
npm run build
```

This validates content and local references, generates the full CleanCV PDF and website data, and exports the site to `dist/client/`. The PDF is [public/Matthias-Fleckenstein-CV.pdf](public/Matthias-Fleckenstein-CV.pdf). The old `Matthias-Fleckenstein-CV-proof.pdf` filename remains as a compatibility copy.

To preview the website:

```powershell
npm run dev
```

Open the local address printed in the terminal (usually `http://localhost:3000/`). Stop the preview with **Ctrl+C**.

If the preview is already running when you edit academic.md, run this in a second terminal in the same project folder:

```powershell
npm run content
```

That refreshes website data and the PDF. Refresh the browser or reopen the PDF if it still shows a cached version. Run `npm run build` before publication.

Review the changed Research/Data entries, open new downloads, and check the affected CV pages. **None of these commands publishes.** After committing and pushing to `master`, open GitHub's **Actions → Academic website → Run workflow**, select **master**, check **Publish this build to the public academic website**, and start the run. Wait for both **build** and **deploy** to succeed.

For a fresh checkout on this computer, install the local dependencies once before building:

```powershell
npm ci
& 'C:\Users\mflecken\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -m pip install --target scripts/vendor -r requirements.txt
```

The `scripts/vendor` folder is ignored by Git. The build wrapper selects the same bundled Python installation automatically. On another computer, follow Section 13 instead.

### If something fails

| Message or symptom | What to check |
| --- | --- |
| Invalid YAML | Indentation; quote text containing colons; keep the two `---` delimiters |
| Duplicate field or ID | Keep one section heading and one unique ID per record |
| Local file is missing | Copy it into the matching location under `public/` |
| Filename capitalization | Match the file and link exactly |
| Unknown paper_id | Copy the paper's existing ID exactly |
| Data entry has no resources | Add a real file/link or leave the draft out of the list |
| CleanCV compilation failed | Inspect `work/cv/compile-output.txt`; verify MiKTeX/TeX Live is installed |
| Content changed locally but not online | Rebuild, review, then publish through the configured hosting workflow |

## 13. Setup on another computer

Install Node.js compatible with the locked project (Node 24 is recommended), Python 3.10+ with pip, and a LaTeX distribution with pdfLaTeX. From the project folder:

```powershell
npm ci
python -m pip install -r requirements.txt
npm run build
```

The wrappers prefer the bundled Python/Node runtimes when present on this computer. Otherwise they use the normal Python/Node installations. Set `ACADEMIC_PYTHON` or `ACADEMIC_LATEX` to a specific executable if needed. LaTeX package requirements are described in [templates/cleancv/README.md](templates/cleancv/README.md).

For maintenance checks, `python scripts/test_content_model.py` tests resource validation. `python scripts/verify_record.py` checks the CV's text against the generated record and requires `pdfplumber` as an additional verification dependency. These checks do not publish anything.

## 14. Project map and migration history

| Path | Purpose |
| --- | --- |
| `content/academic.md` | Main editable content |
| `public/papers/` | Author paper PDFs |
| `public/appendices/` | Internet Appendices |
| `public/data/` | Selected datasets and documentation |
| `public/portrait.jpg` | Homepage portrait |
| `app/` | Website layout and page templates |
| `scripts/content_model.py` | Content and local-file validation |
| `scripts/build_clean_cv.py` | CV generation |
| `templates/cleancv/` | Unmodified MIT-licensed CleanCV style |
| `work/cv/` | Generated LaTeX and compilation logs |
| `dist/client/` | Generated deployable website |
| `.github/workflows/pages.yml` | Installed GitHub build and manual publishing workflow |
| `docs/GITHUB-PAGES.md` | Migration record, routine publishing, and rollback instructions |
| `docs/pages-workflow.example.yml` | Reference copy of the installed workflow; keep it synchronized |

The original August 2026 CV was migrated in full: 10 published/forthcoming papers, 7 working papers, 1 book chapter, 14 presentation groups, 21 discussions, 29 teaching entries, 8 awards, citation totals with their source dates, service, and additional information. These are historical migration totals, not limits on future entries.

The original `E:\Research\Tenure\CurriculumVitae\MarkdownCV` directory remains unchanged. Going forward, maintain this project's academic.md; changes to the old index.md do not synchronize into it.

## What “design-proof” means

“Design proof” was the name given to the separate site used to develop and review this replacement. The current implementation is functional, including the CV, paper downloads, Data, and Teaching pages. The phrase is a name, not a limitation of the website.

The private preview address is hosted by Sites and is restricted to your account. The public GitHub Pages website is now live at `https://www.mfleckenstein.com/`; the original GitHub address also redirects to the custom domain. The original design-proof folder can remain as a reference; use `F:\AcademicWebpage\github-pages-migration\content\academic.md` for future public-site updates. The local folder name has no effect on the public URL.
