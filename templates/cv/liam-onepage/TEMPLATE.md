# Template: liam-onepage

- **Type:** CV
- **Source extension:** .tex
- **Engine/toolchain:** pdflatex (display label only)
- **Page limit:** 1 page
- **Fonts:** Computer Modern (LaTeX default - no external font files, nothing to install)
- **Class/packages:** `article` (letterpaper, 11pt) with `fullpage`, `titlesec`, `marvosym`, `enumitem`, `hyperref`, `fancyhdr`, `tabularx`, `latexsym`, `babel`, and `\input{glyphtounicode}` - all standard. Based on Jake Gutierrez's MIT-licensed resume template (https://github.com/sb2nov/resume).

## Compile command

    cd cv && pdflatex -interaction=nonstopmode <file>.tex

`pdflatex` is correct here and must not be swapped for `lualatex`. The template
uses no `fontspec` and loads no font files by path, so the stock guidance's
`fontawesome5`/lualatex warning does not apply. It also sets the pdftex
primitive `\pdfgentounicode=1`, which is what makes the text layer extract
cleanly for ATS parsers.

## Style rules

- **Hard 1-page limit.** This is an internship-oriented resume; a second page is a failure, not a near-miss. Cut by relevance (see the stock guidance's relevance-weighted cutting rules), never by shrinking geometry or `\vspace`.
- **Section order:** Professional Summary, Professional Experience, Leadership Experience, Education, Projects, Skills, Certifications. Reorder only when a posting makes a different order clearly stronger; keep Professional Summary first always.
- **Monochrome.** No color. Section headings are small-caps with a full-width horizontal rule, produced by the `\titleformat` block. Do not introduce a color scheme.
- **Custom macros do the layout.** Use `\resumeSubheading{title}{dates}{org}{location}`, `\resumeItem{...}`, `\resumeProjectHeading{name | stack}{dates}`, and the `\resumeSubHeadingListStart/End` and `\resumeItemListStart/End` wrappers. Do not hand-roll `itemize` blocks; the negative `\vspace` values inside these macros are what keep the density correct.
- **Bullets:** 3 per role, 2 per project. Each bullet leads with a past-tense outcome verb and carries a concrete number, tool, or measurable result wherever one honestly exists.
- **Date format:** `Month YYYY - Month YYYY`, or `Month YYYY - Present` for current roles. See the pitfall below.
- **Header:** single centered block - name, then `City, Country | phone | email | LinkedIn | Personal Site | GitHub` separated by `$|$`. The email must stay printed as literal text (not hidden behind link text) so ATS extraction finds it.

## Known pitfalls

- **Date arguments must use a single ASCII hyphen, never `--`.** LaTeX ligatures `--` into an en-dash (U+2013). Verified on this template: a `--` date extracts from the PDF text layer as `June 2024 <U+2013> August 2026`, and parsers that split ranges only on ASCII `-` see no range at all. The failure is completely silent - the PDF looks perfect. The skeleton is already fixed; keep it that way when filling it in. `--` remains correct in prose (e.g. a numeric range like `10--20`).
- **`fancyhdr` emits a `\footskip is too small (0.0pt)` warning** on every compile. Harmless and expected - the template clears headers and footers deliberately. Do not "fix" it.
- **`LaTeX Font Warning: Some font shapes were not available, defaults substituted.`** is also expected (small-caps bold in section headings). No visual defect.
- **First compile on a fresh MiKTeX may fail on a missing `hyperref` dependency** (`kvdefinekeys.sty`). Fix once with `mpm --require=kvdefinekeys`, or enable on-the-fly installs with `initexmf --set-config-value "[MPM]AutoInstall=1"`.
- **`\resumeItem` content sits inside braces**, so a bullet beginning with `[` is safe. But a bare `\item [text]` outside these macros would be read by LaTeX as an optional item label - always go through `\resumeItem{...}`.
- **Each bullet marker extracts as one U+FFFD replacement character, and this is expected.** `pdftotext` yields one `�` at the start of every bullet line because the Computer Modern bullet glyph comes from the math symbol font (`cmsy10`) and has no Unicode mapping, which `\pdfgentounicode=1` does not cover. **Verified harmless:** the marker is decorative, carries no information, and no replacement character ever appears adjacent to a letter, so no word is corrupted. It is the same class of noise as the stock template's fontawesome icon glyphs, which `05-cv-templates.md` also calls harmless. During ATS verification, expect a replacement-character count equal to the number of bullets and do not treat it as a failure. The check that matters is whether any `�` sits *next to a letter* - that would mean real text loss. Do not "fix" this by changing the list marker; it would alter the visual design for no parsing benefit.
