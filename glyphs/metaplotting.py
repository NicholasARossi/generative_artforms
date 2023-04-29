
from glyphs.core import GlyphPath,GridExplorer
from glyphs.visualization import render_multipath_fill
import numpy as np
import pandas as pd


def main(size):
    # generate plots

    explorer = GridExplorer(size)
    explorer.explore_closed_cylces()
    explorer.save_cycles_to_csv()

    successful_cylces = []
    counter_value = 0
    while len(successful_cylces) < 20:
        rotations = np.random.choice(2, size ** 2).reshape((size, size))
        glyph_path = GlyphPath(explorer.all_paths[counter_value], rotations)
        glyph_path.run_all()
        result_series = glyph_path.return_series()
        if result_series['not_crossing']:
            successful_cylces.append(result_series)

        counter_value += 1
    result_df = pd.DataFrame(successful_cylces)
    result_df.to_csv('results_df.csv')
    all_paths = list(result_df['all_points'].values)
    render_multipath_fill(all_paths,'glyph_figures/all_plots.png',annotate=True)

if __name__ == '__main__':
    main(3)
