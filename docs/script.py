# corrected script.py
import re
import os
import subprocess

# Map admonition types to box names
ADMONITION_MAP = {
    'note': 'notebox',
    'tip': 'tipbox',
    'info': 'infobox',
    'warning': 'warningbox',
    'danger': 'dangerbox'
}

def escape_latex(text: str) -> str:
    """Escape special LaTeX characters for normal text (not for verbatim/code)."""
    chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
    }
    return ''.join(chars.get(c, c) for c in text)

def process_inline(text: str) -> str:
    """
    Robust version:
    - Converts <br>, <br/>, <br /> into real LaTeX line breaks
    - Handles bold, italic and inline code
    - Never leaves the placeholder in the output
    """
    if not text:
        return text

    # --- Step 1: normalize all HTML line breaks to a unique placeholder ---
    text = re.sub(r'<br\s*/?>', '§BR§', text, flags=re.IGNORECASE)

    # --- Step 2: escape LaTeX special characters ---
    escaped = escape_latex(text)

    # --- Step 3: restore the real line-break command ---
    # We do it twice (once before and once after markdown processing)
    # to be 100 % sure the placeholder never survives
    escaped = escaped.replace('§BR§', r'\\')

    # --- Step 4: inline code `code` ---
    def repl_code(m):
        return r'\passthrough{' + m.group(1) + '}'
    escaped = re.sub(r'`([^`]+)`', repl_code, escaped)

    # --- Step 5: bold **text** ---
    def repl_bold(m):
        return r'\textbf{' + m.group(1) + '}'
    escaped = re.sub(r'\*\*([^*]+)\*\*', repl_bold, escaped)

    # --- Step 6: italic *text* ---
    def repl_italic(m):
        return r'\emph{' + m.group(1) + '}'
    escaped = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', repl_italic, escaped)

    # --- Final safety net ---
    escaped = escaped.replace('§BR§', r'\\')   # in case anything re-introduced it

    return escaped

def parse_table(table_lines, short_thresh=25):
    """Simple, robust parse: first small columns -> 'l' (natural width), else -> 'Y' (flexible/wrapping).
    Requires ltablex + \\keepXColumns in LaTeX preamble.
    """
    if not table_lines:
        return []

    # keep non-empty lines (preserve order)
    clean_lines = [ln.rstrip('\n') for ln in table_lines if ln.strip() != '']
    if len(clean_lines) < 2:
        return []

    # parse header: strip outer '|' if present, then split on '|' allowing spaces
    header_line = clean_lines[0].strip()
    header_cells = [c.strip() for c in re.split(r'\s*\|\s*', header_line.strip('| ')) if (c.strip() != '' or header_line.count('|')>0)]
    num_cols = len(header_cells)
    if num_cols == 0:
        return []

    # parse body rows (lines after the separator at index 1)
    rows = []
    for line in clean_lines[2:]:
        s = line.strip()
        cells = [c.strip() for c in re.split(r'\s*\|\s*', s.strip('| '))]
        # pad or truncate to match num_cols
        if len(cells) < num_cols:
            cells += [''] * (num_cols - len(cells))
        elif len(cells) > num_cols:
            cells = cells[:num_cols]
        rows.append(cells)

    # compute max length per column (header + rows)
    max_lens = [len(h) for h in header_cells]
    for r in rows:
        for i, c in enumerate(r):
            if i < num_cols:
                max_lens[i] = max(max_lens[i], len(c))

    # decide column types: small -> l, otherwise -> Y
    col_types = []
    for ml in max_lens:
        if ml <= short_thresh:
            col_types.append('l')
        else:
            col_types.append('Y')

    # build colspec
    colspec = '@{}' + ''.join(col_types) + '@{}'

    # build latex lines
    latex = []
    latex.append(f'\\begin{{tabularx}}{{\\textwidth}}{{{colspec}}}')
    latex.append('\\toprule')

    # header (process inline)
    header_proc = [f"\\makecell[l]{{{process_inline(c)}}}" for c in header_cells]
    header_line_tex = ' & '.join(header_proc) + ' \\\\ \\midrule'
    latex.append(header_line_tex)
    latex.append('\\endfirsthead')
    latex.append('\\toprule')
    latex.append(header_line_tex)
    latex.append('\\endhead')

    # footers
    latex.append('\\midrule\\multicolumn{' + str(num_cols) + '}{r}{\\textit{Continued on next page}}\\\\')
    latex.append('\\endfoot')
    latex.append('\\bottomrule')
    latex.append('\\endlastfoot')

    # rows
    for idx, r in enumerate(rows):
        # ensure length
        cells = r[:num_cols] + [''] * max(0, num_cols - len(r))
        cells_proc = [process_inline(c) for c in cells]
        color = '\\rowcolor{tableEven}' if idx % 2 == 0 else '\\rowcolor{tableOdd}'
        latex.append(color)
        latex.append(' & '.join(cells_proc) + ' \\\\')

    latex.append('\\end{tabularx}')
    return latex
def parse_md_to_latex(md_lines):
    """Parse Markdown lines to LaTeX."""
    latex_lines = []
    i = 0
    n = len(md_lines)

    # Skip frontmatter only at the very top
    if i < n and md_lines[i].strip() == '---':
        i += 1
        while i < n and md_lines[i].strip() != '---':
            i += 1
        if i < n and md_lines[i].strip() == '---':
            i += 1  # skip closing ---

    in_code = False
    code_lang = ''
    code_lines = []
    in_table = False
    table_lines = []
    in_admonition = False
    admonition_class = ''
    admonition_title = ''
    admonition_lines = []
    in_list = False
    list_type = ''  # 'item' or 'enum'
    in_details = False
    details_summary_raw = ''
    details_lines = []

    while i < n:
        line = md_lines[i].rstrip('\n')
        stripped = line.strip()

        # Code block handling
        if in_code:
            if stripped.startswith('```'):
                # end code block
                in_code = False
                # Use minted verbatim environment - do NOT escape code content
                latex_lines.append(f'\\begin{{minted}}{{{code_lang}}}')
                latex_lines += code_lines
                latex_lines.append('\\end{minted}')
                code_lines = []
            else:
                # preserve original code line (do NOT escape)
                code_lines.append(line)
            i += 1
            continue

        # Table continuation
        if in_table:
            if not stripped.startswith('|') and stripped != '':
                # finish table
                in_table = False
                latex_lines += parse_table(table_lines)
                table_lines = []
                # do not consume this line here (re-process it in outer loop)
                continue
            else:
                table_lines.append(line)
                i += 1
                continue

        # Admonition body
        if in_admonition:
            if stripped == ':::':
                in_admonition = False
                title_esc = escape_latex(admonition_title)
                # Automatically add the correct emoji + space before the title
                if admonition_class == "tip":
                    emoji = "\\bulb~"
                elif admonition_class == "note":
                    emoji = "\\note~"
                elif admonition_class == "info":
                    emoji = "\\info~"
                elif admonition_class == "warning":
                    emoji = "\\warning~"
                elif admonition_class == "danger":
                    emoji = "\\fire~"
                else:
                    emoji = ""

                full_title = f"{emoji}\\textbf{{{title_esc}}} :"
                box_name = ADMONITION_MAP.get(admonition_class, 'infobox')
                latex_lines.append(f'\\begin{{{box_name}}}{{\\textbf{{{full_title}}}}}')
                # recursively parse the lines inside admonition
                inner = parse_md_to_latex(admonition_lines)
                latex_lines += inner
                latex_lines.append(f'\\end{{{box_name}}}')
                admonition_lines = []
            else:
                admonition_lines.append(line)
            i += 1
            continue

        # Details block body
        if in_details:
            if stripped.startswith('</details>'):
                in_details = False

                # Convert summary markdown to LaTeX (bold, inline code, etc.)
                title_tex = process_inline(details_summary_raw) if details_summary_raw else 'Details'

                # Remove any literal <div> / </div> lines from the captured details content
                cleaned_details = [ln for ln in details_lines if ln.strip().lower() not in ('<div>', '</div>')]

                # Render as a subsubsection (normal section, no box)
                latex_lines.append('')
                latex_lines.append(f'\\subsubsection{{{title_tex}}}')

                # Parse the cleaned inner lines (recursive)
                inner = parse_md_to_latex(cleaned_details)
                latex_lines += inner

                # reset
                details_lines = []
                i += 1
            else:
                details_lines.append(line)
            i += 1
            continue


        # Headings (strip manual numbers like "1. ", "2. ")
        if stripped.startswith('# '):
            raw = stripped[2:].strip()
            text = re.sub(r'^\d+\.\s*', '', raw)
            latex_lines.append(f'\\section{{{process_inline(text)}}}')
            i += 1
            continue
        if stripped.startswith('## '):
            raw = stripped[3:].strip()
            text = re.sub(r'^\d+\.\s*', '', raw)
            latex_lines.append(f'\\subsection{{{process_inline(text)}}}')
            i += 1
            continue
        if stripped.startswith('### '):
            raw = stripped[4:].strip()
            text = re.sub(r'^\d+\.\s*', '', raw)
            latex_lines.append(f'\\subsubsection{{{process_inline(text)}}}')
            i += 1
            continue

        # Code block start
        if stripped.startswith('```'):
            in_code = True
            code_lang = stripped[3:].strip() or 'text'
            code_lines = []
            i += 1
            continue

        # Admonition start (:::note Title)
        match = re.match(r'^:::(\w+)\s*(.*)$', stripped)
        if match:
            # Close any open list before starting admonition
            if in_list:
                if list_type == 'item':
                    latex_lines.append('\\end{itemize}')
                else:
                    latex_lines.append('\\end{enumerate}')
                in_list = False

            in_admonition = True
            admonition_class = match.group(1).lower()
            admonition_title = match.group(2).strip()
            admonition_lines = []
            i += 1
            continue

        # Table start detection (header line + separator)
        if stripped.startswith('|') and i+1 < n and re.match(r'^\|?[-:\s|]+\|?$', md_lines[i+1].strip()):
            in_table = True
            table_lines = [line]
            i += 1
            continue

        # Unordered lists
        if stripped.startswith('- '):
            if not in_list or list_type != 'item':
                if in_list:
                    # close previous list
                    if list_type == 'item':
                        latex_lines.append('\\end{itemize}')
                    else:
                        latex_lines.append('\\end{enumerate}')
                in_list = True
                list_type = 'item'
                latex_lines.append('\\begin{itemize}')
            text = stripped[2:].strip()
            latex_lines.append(f'\\item {process_inline(text)}')
            i += 1
            continue

        # Ordered lists
        if re.match(r'^\d+\.\s', stripped):
            if not in_list or list_type != 'enum':
                if in_list:
                    # close previous list
                    if list_type == 'item':
                        latex_lines.append('\\end{itemize}')
                    else:
                        latex_lines.append('\\end{enumerate}')
                in_list = True
                list_type = 'enum'
                latex_lines.append('\\begin{enumerate}')
            text = re.sub(r'^\d+\.\s+', '', stripped)
            latex_lines.append(f'\\item {process_inline(text)}')
            i += 1
            continue

        # Blockquotes (> text) - ADD THIS SECTION HERE
        if stripped.startswith('> '):
            # Close any open list first
            if in_list:
                if list_type == 'item':
                    latex_lines.append('\\end{itemize}')
                else:
                    latex_lines.append('\\end{enumerate}')
                in_list = False

            # Collect all consecutive blockquote lines
            quote_lines = []
            while i < n and md_lines[i].strip().startswith('> '):
                quote_text = md_lines[i].strip()[2:].strip()  # Remove "> " prefix
                quote_lines.append(quote_text)
                i += 1

            # Process the blockquote content
            latex_lines.append('\\begin{blockquote}')
            for qline in quote_lines:
                if qline:  # non-empty line
                    latex_lines.append(process_inline(qline))
                else:  # blank line within quote
                    latex_lines.append('')
            latex_lines.append('\\end{blockquote}')
            continue

        # End list on blank line or non-list
        if in_list and stripped != '' and not stripped.startswith('- ') and not re.match(r'^\d+\.\s', stripped):
            if list_type == 'item':
                latex_lines.append('\\end{itemize}')
            else:
                latex_lines.append('\\end{enumerate}')
            in_list = False
            # continue parsing this same line (do NOT increment i here)
            continue

        # Details start (<details> with optional <summary> on next line)
        if stripped.startswith('<details>'):
            in_details = True
            details_lines = []
            details_summary_raw = ''
            i += 1

            # If the next line contains <summary> ... </summary> (possibly multiline), capture it cleanly.
            if i < n and '<summary>' in md_lines[i]:
                # collect lines until a closing </summary> appears (handles multiline summary)
                summ_parts = []
                while i < n and '</summary>' not in md_lines[i]:
                    summ_parts.append(md_lines[i].strip())
                    i += 1
                if i < n:
                    # append the line containing the closing tag too
                    summ_parts.append(md_lines[i].strip())
                    i += 1

                # join and remove summary tags and any inner HTML tags
                summary_raw = ' '.join(summ_parts)
                summary_raw = re.sub(r'</?summary>', '', summary_raw, flags=re.I).strip()
                # remove any remaining HTML tags like <strong>, <div> etc.
                summary_raw = re.sub(r'<[^>]+>', '', summary_raw).strip()
                details_summary_raw = summary_raw
            continue


        # Horizontal rule
        if stripped == '---':
            i += 1
            continue

        # Paragraphs / plain text
        if stripped:
            latex_lines.append(process_inline(stripped))
        else:
            latex_lines.append('')

        i += 1

    # Close any open environments
    if in_list:
        if list_type == 'item':
            latex_lines.append('\\end{itemize}')
        else:
            latex_lines.append('\\end{enumerate}')
    if in_table:
        latex_lines += parse_table(table_lines)
    if in_admonition:
        title_esc = escape_latex(admonition_title)
        # Automatically add the correct emoji + space before the title
        if admonition_class == "tip":
            emoji = "\\tipemoji~"
        elif admonition_class == "note":
            emoji = "\\noteemoji~"
        elif admonition_class == "info":
            emoji = "\\infoemoji~"
        elif admonition_class == "warning":
            emoji = "\\warningemoji~"
        elif admonition_class == "danger":
            emoji = "\\dangeremoji~"
        else:
            emoji = ""

        full_title = f"{emoji}\\textbf{{{title_esc}}}"
        box_name = ADMONITION_MAP.get(admonition_class, 'infobox')
        latex_lines.append(f'\\begin{{{box_name}}}{{\\textbf{{{full_title}}}}}')
        latex_lines.append(f'\\end{{{box_name}}}')
    if in_details:
        summary_esc = escape_latex(details_summary_raw)
        latex_lines.append(f'\\begin{{tcolorbox}}[title={{ \\textbf{{{summary_esc}}} }}]')
        latex_lines += parse_md_to_latex(details_lines)
        latex_lines.append('\\end{tcolorbox}')

    return latex_lines

# Main
if __name__ == "__main__":
    import glob

    # Define your markdown files in order
    md_files = [
        'intro.md',
        'core-techniques/zero-few-shot.md',
        'core-techniques/cot.md',
        'core-techniques/chain-of-thought.md',
        'core-techniques/meta-prompting.md',
        'core-techniques/self-consistency.md',
        'core-techniques/gkp.md',
        'core-techniques/prompt-chaining.md',
        'core-techniques/tot.md',
        'core-techniques/rag.md',
        'core-techniques/art.md',
        'core-techniques/ape.md',
        'core-techniques/active-prompt.md',
        'core-techniques/dsp.md',
        'core-techniques/pal.md',
        'core-techniques/react.md',
        'core-techniques/reflexion.md',
        'core-techniques/multimodalcot.md',
        'ai-agents/introduction.md',
        'ai-agents/ai-workflows-vs-ai-agents.md',
        'ai-agents/context-engineering.md',
        'ai-agents/context-engineering-deep-dive.md',
        'ai-agents/function-calling.md',
        'ai-agents/deep-agents.md',
    ]

    template_path = 'template.tex'
    out_path = 'output.tex'

    # Check if template exists
    if not os.path.exists(template_path):
        print(f"Error: {template_path} not found.")
        raise SystemExit(1)

    # Process all markdown files
    all_body_lines = []

    for md_path in md_files:
        if not os.path.exists(md_path):
            print(f"Warning: {md_path} not found. Skipping.")
            continue

        print(f"Processing {md_path}...")

        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        md_lines = md_content.splitlines()

        # Parse this file
        body_lines = parse_md_to_latex(md_lines)

        # Add to combined output
        all_body_lines.extend(body_lines)

        # Add page break between files (optional, remove if not needed)
        all_body_lines.append('\\clearpage')

    # Combine all processed content
    body_latex = '\n'.join(all_body_lines)

    # Load template and insert body
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    tex = template.replace('$BODY$', body_latex)

    # Write output
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(tex)

    print(f'Generated {out_path}. Compiling...')

    # Compile twice for TOC
    for run in [1, 2]:
        print(f'\nCompilation run {run}/2...')
        result = subprocess.run(
            ['xelatex', '-shell-escape', '-interaction=nonstopmode', out_path],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Error during compilation run {run}:")
            print(result.stdout[-500:])  # Show last 500 chars of output
            break
    else:
        print(f'\n✓ PDF generated successfully: output.pdf')


