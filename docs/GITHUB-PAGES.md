# Step-by-step migration to GitHub Pages

This guide moves the new academic website to your existing public repository. **These migration steps have not been executed.** The existing GitHub homepage, course websites, and DNS remain unchanged.

Prepared September 9, 2026. The public repository was checked: it is `fleckenstein-m/fleckenstein-m.github.io`, its default branch is `master`, and Pages is enabled. The actual Pages publishing source and custom-domain setting require checking in your signed-in repository settings.

## What “design-proof” means

The name was chosen for the separate site where we developed and reviewed the replacement. The implementation is functional: it generates the website and full CV and serves paper PDFs, Data, and Teaching pages.

The current `matthias-fleckenstein-design-proof.magicmaze.chatgpt.site` address is a private Sites publication restricted to your account. It is not the existing GitHub homepage. On GitHub Pages, the same built website can use `https://fleckenstein-m.github.io/` or your verified custom domain. The words `design-proof` do not have to appear in the public address or page titles.

The local folder `F:\AcademicWebpage\design-proof` can retain its name. A folder name does not determine the public address. Keep the private preview available for review during migration; there is no need to rename it to launch on GitHub.

## The recommended approach

Retain the existing GitHub repository and its history. Prepare the new source on a separate branch. GitHub Actions builds the website and CV together and publishes only `dist/client/`.

Use the supplied [workflow template](pages-workflow.example.yml). It checks pull requests and pushes to `master`. Public deployment happens only when you run it manually from `master` with **Publish** selected. This makes the first launch and subsequent publication decisions explicit.

The template is stored under `docs/` and is inactive. It has not run on a GitHub runner. The first pull-request build below is the required check of the Linux/LaTeX setup before public cutover. No new paid service, database, or always-running server is required by this website architecture.

## Step 1 — Record the current setup

1. Sign into GitHub and open [the homepage repository](https://github.com/fleckenstein-m/fleckenstein-m.github.io).
2. Open **Settings → Pages**.
3. Record the current **Source**. If it says **Deploy from a branch**, record both the branch and folder (for example, `master` and `/ (root)`). Do not assume those values without checking.
4. Record the **Custom domain** field and whether **Enforce HTTPS** is enabled.
5. Open your current public homepage and record its final browser address. If you use `www.mfleckenstein.com`, confirm whether it is the actual Pages custom domain or a separate redirect.
6. Record the domain provider's current DNS configuration if a custom domain is involved.

The September 9 public repository listing contains no root CNAME file. That alone does not establish whether a domain is configured elsewhere. Use Settings → Pages as the source of truth.

These are read-only checks. Do not change the publishing source or DNS yet.

## Step 2 — Create a migration checkout and rollback tag

Open PowerShell. These commands create a new checkout; they do not overwrite the old MarkdownCV folder or the current design-proof project. If the destination folder or branch/tag already exists, inspect and resume it rather than deleting it or repeating these commands blindly.

```powershell
Set-Location 'F:\AcademicWebpage'
git clone https://github.com/fleckenstein-m/fleckenstein-m.github.io.git github-pages-migration
Set-Location 'F:\AcademicWebpage\github-pages-migration'
git switch master
git pull --ff-only
git tag before-academic-redesign-2026-09-09
git push origin before-academic-redesign-2026-09-09
git switch -c academic-redesign
```

Git may ask you to sign into GitHub. Use your normal account authentication; do not put a password or token in the commands.

The tag preserves the pre-migration source. Also retain the publishing-source and domain settings from Step 1, because reverting code alone does not undo a Pages configuration change.

## Step 3 — Copy the reviewed new source

First make sure the design-proof checkout contains your latest saved work and a successful build:

```powershell
Set-Location 'F:\AcademicWebpage\design-proof'
git status --short
npm run build
```

The next command exports the latest committed version. If `git status` shows uncommitted changes that you want to migrate, save and commit them in this project first. Do not proceed with an older snapshot by accident.

Export the tracked source and expand it into the migration branch:

```powershell
git archive --format=zip --output='F:/AcademicWebpage/academic-site-source.zip' HEAD
Expand-Archive -LiteralPath 'F:\AcademicWebpage\academic-site-source.zip' -DestinationPath 'F:\AcademicWebpage\github-pages-migration' -Force
Set-Location 'F:\AcademicWebpage\github-pages-migration'
```

This preserves the migration checkout's `.git` directory because `git archive` does not contain Git's internal history. It also excludes ignored dependencies and temporary files.

Remove only the copied Sites manifest from the new GitHub checkout; GitHub does not use it. Keep the original manifest in the design-proof checkout:

```powershell
Remove-Item -LiteralPath 'F:\AcademicWebpage\github-pages-migration\.openai\hosting.json'
```

The remaining old root files, such as `index.md`, `index.html`, and `makefile`, are historical at this point. They will not be part of the new `dist/client/` publication. Maintain `content/academic.md` for the new site; do not continue editing the old root index.md expecting changes to appear.

## Step 4 — Preserve existing download URLs

Existing CV PDFs are already public under their current filenames. Copy them into the new `public` folder so links from emails, search results, and other sites keep working:

```powershell
Get-ChildItem -LiteralPath 'F:\AcademicWebpage\github-pages-migration' -File -Filter '*.pdf' |
    Copy-Item -Destination 'F:\AcademicWebpage\github-pages-migration\public'
```

The new website's current CV remains `/Matthias-Fleckenstein-CV.pdf`. Keep dated legacy filenames attached to their original documents; do not substitute a new CV under an old date.

Review other important old public paths. To preserve any of them, copy the relevant file into the same relative path under `public/`. Root `index.html` is replaced by the newly generated homepage.

Do not move or rename the repositories hosting `FINC462-662-SP2026` and `FINC672-SP2026`. The Teaching page links to them at their existing addresses. Check those links after the academic-site launch as part of the final verification.

## Step 5 — Install the prepared workflow on the migration branch

In the migration checkout:

```powershell
New-Item -ItemType Directory -Path '.github\workflows' -Force
Copy-Item -LiteralPath 'docs\pages-workflow.example.yml' -Destination '.github\workflows\pages.yml'
```

The template:

- Uses the confirmed `master` branch. Update all branch references if you deliberately change the repository's default branch later.
- Installs Node, Python, pdfLaTeX, the CleanCV font packages, and `texlive-bibtex-extra`, which supplies the template's required `biblatex.sty`. Checks that the key LaTeX packages are present before building.
- Runs content checks, builds both outputs, checks TypeScript, and audits CV completeness.
- Verifies all generated pages and local file references through the project's build script.
- Uploads only `dist/client/`.
- Deploys only a manually requested publishing run from `master` after its build succeeds.

GitHub's [custom Pages workflows documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) describes this artifact-based publication method. Runtime setup follows the official [Node setup action](https://github.com/actions/setup-node) and [Python setup action](https://github.com/actions/setup-python).

## Step 6 — Set the final site address for public builds

In the homepage repository, open **Settings → Secrets and variables → Actions → Variables**. Create a repository variable:

- **Name:** `ACADEMIC_SITE_URL`
- **Value:** the verified final HTTPS address, including its scheme; for example `https://www.mfleckenstein.com/` if that is the domain confirmed in Step 1.

If you intend to use the standard GitHub address, set `https://fleckenstein-m.github.io/`, or omit the variable and use the template's default.

This is a public address, so use a repository variable rather than a secret. This variable supplies the site's metadata base. It does not configure DNS or attach a domain to Pages.

The template automatically sets `ACADEMIC_PUBLIC_SITE=true` for an approved publishing run. That enables search indexing in the generated page metadata. Local builds and the private Sites preview remain `noindex` by default. No page-template edits are needed to switch this behavior.

## Step 7 — Review locally and open a pull request

In `F:\AcademicWebpage\github-pages-migration`:

```powershell
npm ci
python -m pip install -r requirements.txt pdfplumber
npm run build
npm run dev
```

The existing LaTeX installation on this computer is used for the local CV. Open the preview address printed in the terminal. Review Home, Research, Data, Teaching, and CV. Test the paper download, both course links, and any newly added data. Check the current and legacy CV files.

Stop the preview with **Ctrl+C**, then review the changes before committing:

```powershell
git status --short
git diff --stat
git add .
git commit -m "Prepare redesigned academic website and CV"
git push -u origin academic-redesign
```

On GitHub, open a pull request from `academic-redesign` into `master`. Wait for the **Academic website / build** check to pass. Review the changed files and the generated artifact. A missing LaTeX package, broken local resource reference, or compilation failure must be fixed on this branch and checked again.

The first runner build verifies the prepared workflow in the real GitHub environment. It may take longer because it installs the font packages. A successful local build does not substitute for this check.

## Step 8 — Change the Pages publishing source and merge

This is the start of public cutover. Proceed after the migration pull request and its checks are approved for launch.

1. Open **Settings → Pages** in the homepage repository.
2. Under **Build and deployment → Source**, select **GitHub Actions**.
3. Preserve the domain recorded in Step 1. If the domain is already attached to this same Pages site, do not remove it or change DNS merely because the build system changed.
4. Merge the reviewed `academic-redesign` pull request into `master`.
5. Wait for the push build to pass. The template's push build does not publish by itself.

The old branch-and-folder publishing method is replaced by the new workflow. See GitHub's [publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

If you use a custom domain, its authoritative setting is **Settings → Pages → Custom domain**. GitHub's custom-workflow publication does not require a CNAME file; an existing one is ignored for that purpose. If the custom domain is not yet configured, follow [GitHub's domain setup instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) before treating the address as ready.

## Step 9 — Publish the first public version

1. Open the repository's **Actions** tab.
2. Select **Academic website**.
3. Choose **Run workflow**.
4. Select branch **master**.
5. Select **Publish this build to the public academic website**.
6. Start the run and wait for both **build** and **deploy** to succeed.
7. Open the URL in the deployment result.

The **Run workflow** control becomes available after the workflow file exists on the default branch. If GitHub requires approval for the `github-pages` environment, approve that deployment after checking the run.

A failed build does not proceed to deployment. Inspect and fix the failing step; do not upload a partial output folder by hand.

## Step 10 — Verify the actual public site

Check the final public address, not the private Sites preview:

- `/` and `/index.html`: updated homepage and both recent-paper sections.
- `/research/`: publisher links and the TIPS–Treasury Paper PDF.
- `/data/`: selected resources or the truthful empty state.
- `/teaching/`: the two Spring 2026 course websites.
- `/cv/` and `/Matthias-Fleckenstein-CV.pdf`: complete current CV.
- Important old PDF filenames retained in Step 4.
- HTTPS and the intended custom domain, if used.

Confirm a public publishing build does not contain `noindex` in the homepage's robots metadata. Search engines may take time to reflect a successfully published change.

## Routine updates after migration

Use the GitHub checkout as the authoritative project after launch. You can continue using the private preview when needed, but do not independently edit two diverging copies of academic.md.

1. Pull the latest `master` into `F:\AcademicWebpage\github-pages-migration`.
2. Edit `content/academic.md`; add files under `public/` when needed.
3. Build and review.
4. Commit and push, or use a pull request for review.
5. Wait for the automatic build check.
6. Run **Academic website** manually from `master` with **Publish** selected.
7. Confirm deployment success before treating the update as live.

Initially, manual publication is the recommended setting. Later we can configure successful updates to `master` to publish automatically. That would require changing the workflow's deployment condition and public-build flag together; adding a push trigger alone is insufficient.

If you want a more permanent local folder name, rename the GitHub checkout after closing any processes using it and update your saved project path. This has no effect on the public domain. There is no need to rename the existing GitHub repository.

## Rollback

For a problem in an ordinary content update, revert the offending commit on a branch, merge it, and run a new public deployment. Avoid force-pushing the repository history.

For rollback of the initial migration:

1. Preserve the current failed/new state in Git.
2. Use the recorded tag `before-academic-redesign-2026-09-09` to prepare a branch containing the previous site's files.
3. If Step 1 recorded **Deploy from a branch**, restore that publishing mode and select the rollback branch and original folder. Confirm the old site deploys before declaring rollback complete.
4. If Step 1 recorded a custom workflow, restore that workflow and its previous publication configuration instead.
5. Keep the custom domain and HTTPS settings consistent with the recorded configuration.

The old source tag and Pages settings are both needed for a reliable full rollback. Reverting source while leaving an incompatible publishing configuration can prevent the old site from returning.

## Size and scope

The academic homepage repository is the migration target; the two course repositories remain separate. Small paper PDFs, appendices, and selected datasets fit naturally under `public/`. For large replication packages, prefer a link to the journal's or an archival repository.

GitHub Pages currently limits a published site to 1 GB. See [Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits). Avoid accumulating large replication archives in the website's Git history.
