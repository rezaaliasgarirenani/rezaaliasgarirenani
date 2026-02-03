#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "${script_dir}/export.tex" ]; then
  default_tex="${script_dir}/export.tex"
else
  default_tex="${script_dir}/latex_template.tex"
fi
default_out="${script_dir}/thesis.docx"
default_bib="${script_dir}/references.bib"

the_tex="${1:-$default_tex}"
out_docx="${2:-$default_out}"
bib_file="${3:-$default_bib}"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Error: pandoc not found in PATH." >&2
  echo "Install pandoc, then rerun this script." >&2
  exit 1
fi

if [ ! -f "$the_tex" ]; then
  echo "Error: LaTeX file not found: $the_tex" >&2
  exit 1
fi

tex_dir="$(cd "$(dirname "$the_tex")" && pwd)"
tmp_tex="$(mktemp "${tex_dir}/.pandoc-export.XXXXXX.tex")"
cleanup() {
  rm -f "$tmp_tex"
}
trap cleanup EXIT

# Pandoc ignores many LaTeX-only commands. This light preprocess improves TOC
# and removes commands that confuse the Word output.
sed -E \
  -e 's/\\section\\*[{]([^}]*)[}]/\\\\section{\\1}/g' \
  -e 's/\\subsection\\*[{]([^}]*)[}]/\\\\subsection{\\1}/g' \
  -e 's/\\subsubsection\\*[{]([^}]*)[}]/\\\\subsubsection{\\1}/g' \
  -e '/^[[:space:]]*\\\\tableofcontents/d' \
  -e '/^[[:space:]]*\\\\listoffigures/d' \
  -e '/^[[:space:]]*\\\\listoftables/d' \
  -e '/^[[:space:]]*\\\\addcontentsline[{]toc[}][{]section[}][{].*[}]/d' \
  -e '/^[[:space:]]*\\\\printbibliography/d' \
  -e '/^[[:space:]]*\\\\nocite[{].*[}]/d' \
  "$the_tex" > "$tmp_tex"

if [ ! -f "$bib_file" ]; then
  echo "Warning: bibliography file not found: $bib_file" >&2
  echo "Proceeding without bibliography." >&2
  bib_arg=()
else
  bib_arg=(--bibliography="$bib_file")
fi

ref_doc="${script_dir}/reference.docx"
if [ -f "$ref_doc" ]; then
  ref_arg=(--reference-doc="$ref_doc")
else
  ref_arg=()
fi

resource_path="$tex_dir"
if [ "$tex_dir" != "$script_dir" ]; then
  resource_path="$resource_path:$script_dir"
fi

(cd "$tex_dir" && pandoc "$tmp_tex" \
  --from=latex --to=docx --standalone \
  --toc --toc-depth=3 \
  --citeproc \
  "${bib_arg[@]}" \
  "${ref_arg[@]}" \
  --resource-path="$resource_path" \
  -M nocite='@*' \
  -o "$out_docx")

echo "Wrote: $out_docx"
