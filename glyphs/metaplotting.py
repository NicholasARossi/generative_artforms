
from glyphs.core import GlyphPath,GridExplorer
from glyphs.visualization import render_multipath_lines
import numpy as np
import pandas as pd
from tqdm import tqdm
import os

def main(size):
    # generate plots

    explorer = GridExplorer(size)
    explorer.explore_closed_cylces()
    explorer.save_cycles_to_csv(save_location=f'grid_size_{size}_skeletons.csv')


    successful_cylces = []
    glyph_path_list = []

    index = 0
    target_value = 10000
    with tqdm(total=target_value) as pbar:
        while len(successful_cylces) < target_value:
            index = (index + 1) % len(explorer.all_paths)

            rotations = np.random.choice(2, size ** 2).reshape((size, size))
            glyph_path = GlyphPath(explorer.all_paths[index], rotations)
            glyph_path.run_all()
            result_series = glyph_path.return_series()
            if not result_series['is_crossing']:
                successful_cylces.append(result_series)
                glyph_path_list.append(glyph_path)
                pbar.update(1)
    result_df = pd.DataFrame(successful_cylces)
    result_df['glyph_objects'] = glyph_path_list

    sorted_df = result_df.sort_values(by='solidity')
    glyphs = sorted_df.tail(800)['glyph_objects'].values.tolist()
    render_multipath_lines(glyphs, save_location=f'solidity_{size}_800.svg')


    sorted_df = result_df.sort_values(by='concavity')
    glyphs = sorted_df.tail(800)['glyph_objects'].values.tolist()
    render_multipath_lines(glyphs, save_location=f'concavity_{size}_800.svg')


if __name__ == '__main__':
    main(5)
