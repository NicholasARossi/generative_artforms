import pandas as pd

header = """<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd" >

<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">

<metadata>

</metadata>
<defs>
<font id="danxianziti SVG" horiz-adv-x="378" >
<font-face
font-family="danxianziti SVG"
units-per-em="1000"
ascent="800"
descent="-200"
cap-height="500"
x-height="300"
/>
<missing-glyph horiz-adv-x="800"/>
"""
footer = """
</font>
</defs>
</svg>"""

x_advance = 1000


def convert_string_strokes(strokes):
    running_string = ''
    for stroke in strokes:
        current_stroke = ''
        for i, substroke in enumerate(stroke):
            if i == 0:
                current_stroke += f'M {substroke[0]} {substroke[1]} '
            else:
                current_stroke += f'L {substroke[0]} {substroke[1]} '
        running_string += current_stroke
    return running_string


def convert_full_entry(row):
    return f'<glyph unicode="{row.character}" glyph-name="{row.character}" horiz-adv-x="{x_advance}" d="{row.combined_lines}" /> \n'


def main():
    ### this graphics.txt file should be coming from https://github.com/skishore/makemeahanzi

    df = pd.read_json('graphics.txt', lines=True)
    df['combined_lines'] = df.medians.apply(convert_string_strokes)
    df['full_entries'] = df.apply(lambda x: convert_full_entry(x), axis=1)
    with open('danxianziti.svg', 'w') as f:
        f.write(header)
        for entry in df['full_entries'].values:
            f.write(entry)
        f.write(footer)
