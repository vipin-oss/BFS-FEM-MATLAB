# Overleaf / LaTeX entry point

This repository root is itself a compilable LaTeX project:

| File | What it is |
|---|---|
| `main.tex` | the manuscript source, `amsart`, 23 pages |
| `References.bib` | 27 entries, all verified |
| `figures/*.pdf` | the four figures, ready for `pdflatex` (no SVG conversion needed) |

Everything else in the repository (the ZIPs, `REPRODUCIBILITY/`, `AUDIT/`) is supporting material and is ignored by the compiler.

## Compile locally

```
pdflatex main.tex
bibtex   main
pdflatex main.tex
pdflatex main.tex
```

Expected: 23 pages, 27 references, 7 tables, 4 figures, 2 appendices.

## Packages

`amsart` with `amsmath`, `amssymb`, `amsthm`, `booktabs`, `array`, `graphicx`, `microtype`, `geometry`, `hyperref`, and `\bibliographystyle{amsplain}`. All are in a standard TeX Live and on Overleaf.

## Notes

* The figures ship as PDF because `pdflatex` cannot include SVG. The vector sources are in the submission package under `MANUSCRIPT/figures/*.svg`; the PDFs here were converted from them and are visually identical.
* `main.tex` is generated from the Markdown sources in the submission package (`REPRODUCIBILITY/source_manuscript/`). Edit the Markdown and rebuild if you want the change to survive a regeneration; editing `main.tex` directly is fine for a one-off.
* The source has been validated structurally (0 problems: balanced environments and braces, every `\ref`/`\label` and `\cite`/entry resolved, every table row counted, every `\includegraphics` target present) but was **not** run through a TeX engine in the environment where it was produced. This is the first thing to do on Overleaf.

## Pull it into Overleaf

Overleaf's Git bridge is a *single-branch* remote (`main` only) with its own history, so a plain
`git pull` from this repository into Overleaf is not possible. Push this project into the Overleaf
remote instead:

**1. Get a Git token.** Overleaf → *Account Settings* → *Git integration* → *Create token*.
The token is the password; the username is `git`.

**2. Make a clean copy of just the manuscript** (recommended, so the Overleaf file tree holds only
the paper):

```bash
git clone --depth 1 --branch arena/c72d7f5d-bfs-fem-matlab \
  https://github.com/vipin-oss/BFS-FEM-MATLAB.git bfswork
mkdir overleaf-src && cp -r bfswork/main.tex bfswork/References.bib bfswork/figures overleaf-src/
cd overleaf-src && git init -b main && git add . && git commit -m "Manuscript V19"
git remote add overleaf https://git.overleaf.com/<PROJECT_ID>
git push --force overleaf main
```

`<PROJECT_ID>` is the string in your project URL, `https://www.overleaf.com/project/<PROJECT_ID>`.
Push with `--force` because the Overleaf repository has an unrelated first commit; label a version in
Overleaf's History first if you want a backup. Pushing updates the project immediately — reload it and
compile.

**3. Or push the whole repository** (adds the audit package and the ZIPs to the Overleaf tree; the
compiler ignores them):

```bash
git clone --depth 1 --branch arena/c72d7f5d-bfs-fem-matlab \
  https://github.com/vipin-oss/BFS-FEM-MATLAB.git
cd BFS-FEM-MATLAB
git remote add overleaf https://git.overleaf.com/<PROJECT_ID>
git push --force overleaf HEAD:main
```

**4. Or, without a terminal:** *New Project* → *Upload Project* → upload
`Overleaf_Manuscript_V19.zip` (at the repository root). Its top level is exactly `main.tex`,
`References.bib` and `figures/`, ready to compile.

Then: *Menu* → *Settings* → *Main document* = `main.tex`; compiler = pdfLaTeX; press Recompile.
