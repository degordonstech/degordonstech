"""Draws the HIRE ME profile artwork in the style of a GitHub contribution grid.

Run it to regenerate both themes:

    python art/make-hire-me.py

It writes art/hire-me-dark.svg and art/hire-me-light.svg. The grid is
decoration, not contribution data, and the artwork says so.
"""

from pathlib import Path
import random

# 5-row pixel glyphs. 1 = lit cell.
GLYPHS = {
    'H': ['10001', '10001', '11111', '10001', '10001'],
    'I': ['111', '010', '010', '010', '111'],
    'R': ['11110', '10001', '11110', '10010', '10001'],
    'E': ['11111', '10000', '11110', '10000', '11111'],
    'M': ['10001', '11011', '10101', '10001', '10001'],
    ' ': ['000', '000', '000', '000', '000'],
}

THEMES = {
    'dark': {
        'bg': '#0d1117', 'border': '#30363d', 'empty': '#161b22',
        'levels': ['#0e4429', '#006d32', '#26a641', '#39d353'],
        'text': '#e6edf3', 'muted': '#7d8590', 'dot': '#39d353',
    },
    'light': {
        'bg': '#ffffff', 'border': '#d0d7de', 'empty': '#ebedf0',
        'levels': ['#9be9a8', '#40c463', '#30a14e', '#216e39'],
        'text': '#1f2328', 'muted': '#656d76', 'dot': '#2da44e',
    },
}

COLS, ROWS = 53, 7          # one year of weeks, seven days
CELL, GAP = 10, 3
PAD = 24
HEADER, FOOTER = 38, 18
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


def lit_cells(word):
    """Map the word onto the grid, centred, on rows 1 to 5."""
    columns = []
    for i, ch in enumerate(word):
        glyph = GLYPHS[ch]
        width = len(glyph[0])
        for x in range(width):
            columns.append([row[x] == '1' for row in glyph])
        if i < len(word) - 1 and ch != ' ' and word[i + 1] != ' ':
            columns.append([False] * 5)       # one blank column between letters
    left = (COLS - len(columns)) // 2
    lit_cells.span = (left - 2, left + len(columns) + 1)
    lit = set()
    for x, col in enumerate(columns):
        for y, on in enumerate(col):
            if on:
                lit.add((left + x, y + 1))
    return lit


def draw(theme, word='HIRE ME'):
    t = THEMES[theme]
    lit = lit_cells(word)
    rng = random.Random(7)                   # same "noise" every time
    grid_w = COLS * (CELL + GAP) - GAP
    grid_h = ROWS * (CELL + GAP) - GAP
    width = grid_w + PAD * 2
    height = HEADER + grid_h + FOOTER + PAD

    cells = []
    for x in range(COLS):
        for y in range(ROWS):
            in_word = lit_cells.span[0] <= x <= lit_cells.span[1] and 1 <= y <= 5
            if (x, y) in lit:
                fill = t['levels'][3]            # letters in one colour so they read as text
            elif not in_word and rng.random() < 0.12:
                fill = t['levels'][0]            # faint background activity
            else:
                fill = t['empty']
            cx = PAD + x * (CELL + GAP)
            cy = HEADER + y * (CELL + GAP)
            cells.append(f'<rect x="{cx}" y="{cy}" width="{CELL}" height="{CELL}" rx="2" fill="{fill}"/>')

    legend_x = width - PAD - (4 * (CELL + GAP) - GAP)
    legend = ''.join(
        f'<rect x="{legend_x + i * (CELL + GAP)}" y="{height - PAD - 1}" width="{CELL}" height="{CELL}" rx="2" fill="{c}"/>'
        for i, c in enumerate(t['levels'])
    )
    foot_y = height - PAD + 8

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Hire me, drawn as a contribution grid">
  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" fill="{t['bg']}" stroke="{t['border']}"/>
  <circle cx="{PAD + 4}" cy="21" r="4" fill="{t['dot']}"/>
  <text x="{PAD + 14}" y="25" font-family="{FONT}" font-size="12" fill="{t['text']}">@degordonstech</text>
  <text x="{width - PAD}" y="25" font-family="{FONT}" font-size="11" fill="{t['muted']}" text-anchor="end" letter-spacing="1">OPEN TO WORK</text>
  {''.join(cells)}
  <text x="{PAD}" y="{foot_y}" font-family="{FONT}" font-size="11" fill="{t['muted']}">Contribution-style artwork, not activity data</text>
  {legend}
</svg>
'''


if __name__ == '__main__':
    here = Path(__file__).parent
    for name in THEMES:
        (here / f'hire-me-{name}.svg').write_text(draw(name), encoding='utf-8')
        print('wrote', here / f'hire-me-{name}.svg')
