import click
import rasterio
import numpy as np
from rasterio.enums import Resampling

from raster_plaster.merge import merge


RESAMPLING_METHODS = [str(s).split('.')[1] for s in Resampling]


@click.command()
@click.argument('rasters', type=click.Path(exists=True), nargs=-1)
@click.option('--output', '-o', type=click.Path(), required=True, help='Name of output raster')
@click.option('--feather-radius', type=int, default=4, show_default=True)
@click.option('--resample-to', type=int, default=1,
              help='Which raster to resample to, if resolutions differ')
@click.option('--resample-method', type=click.Choice(RESAMPLING_METHODS),
              default='nearest', show_default=True)
def cli(rasters, output, feather_radius=4, resample_to=1, resample_method='bilinear'):
    if 1 > resample_to > len(rasters):
        click.abort('--resample-to out of range')
    if feather_radius < 1:
        click.abort('--feather-radius must be a positive integer')

    resampling = Resampling[resample_method]
    srcs = [rasterio.open(f) for f in rasters]
    res = srcs[resample_to - 1].res

    out_img, _ = merge(srcs, res=res, resampling=resampling)
    profile = srcs[0].profile
    profile.update(
        dtype=np.float32,
        nodata=np.nan
    )
    with rasterio.open(output, 'w', **profile) as dst:
        dst.write(out_img)