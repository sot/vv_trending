#!/usr/bin/env python

import os
import argparse
import numpy as np
import matplotlib
if __name__ == '__main__':
    matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.mpl as mpl
import matplotlib.cm as cm

from Chandra.Time import DateTime

from mica.vv import get_rms_data


def get_options():
    parser = argparse.ArgumentParser(
        description="Update VV/Aspect Solution resid plots")
    parser.add_argument("--outdir",
                        default="/proj/sot/ska/www/ASPECT/vv_rms/",
                        help="directory for plots")
    opt = parser.parse_args()
    return opt


def mission_plots(rms_data):
    norm = mpl.colors.LogNorm()
    my_cm = cm.jet
    figsize = (5, 4)
    data = rms_data
    notfid = data['type'] != 'FID'
    reasonable = ((data['dz_rms'] > 0) & (data['dz_rms'] < 1))
    last_year = data['tstart'] > DateTime(-365).secs

    hist2d_fig = plt.figure(figsize=figsize)
    H, xedges, yedges = np.histogram2d(
        DateTime(data[notfid & reasonable]['tstart']).frac_year,
        data[notfid & reasonable]['dz_rms'],
        bins=100, range=[[2007, DateTime().frac_year + .25], [0.0, 0.30]])
    #ax1 = hist2d_fig.add_axes([0.125, 0.12, 0.70, 0.78])
    ax1 = hist2d_fig.add_axes([0.14, 0.14, 0.70, 0.78])
    #ax1 = subplot(111)
    ax1.pcolorfast(xedges, yedges, H.T, cmap=my_cm, norm=norm)
    plt.grid()
    plt.ylabel("Star Resid RMS in Z (arcsec)")
    plt.xlabel("Time (Cal Year)")
    plt.suptitle("RMS vs Time")
    plt.xticks(rotation='60')
    ax1.xaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%d'))

    ax2 = hist2d_fig.add_axes([0.85, 0.14, 0.015, 0.78])
    tick_locs = [norm.vmin, 2, 5, 10, norm.vmax]
    cb = mpl.colorbar.ColorbarBase(ax2,
                                   cmap=my_cm,
                                   norm=norm,
                                   orientation='vertical')
    cb.locator = mpl.ticker.FixedLocator(tick_locs)
    cb.formatter = mpl.ticker.FormatStrFormatter("%d")
    plt.ylabel("N stars")
    cb.update_ticks()

    mag_resid_fig = plt.figure(figsize=figsize)
    year_2007 = ((data['tstart'] < DateTime('2008:001').secs)
                 & (data['tstart'] > DateTime('2007:001').secs))
    cmap_blue = matplotlib.colors.ListedColormap(['white', 'blue'])
    cmap_red = matplotlib.colors.ListedColormap(['white', 'red'])
    cmap_blue._init()
    cmap_red._init()
    # set the white to have alpha 0 and everything else to a half
    cmap_blue._lut[:, -1] = [0, 1, 0, 1, 1]
    cmap_red._lut[:, -1] = [0, .8, 0, .8, .8]
    bounds = ([0, 1, 10])
    norm_blue = matplotlib.colors.BoundaryNorm(bounds, cmap_blue.N, 256)
    norm_red = matplotlib.colors.BoundaryNorm(bounds, cmap_red.N, 256)
    ax2 = mag_resid_fig.add_axes([0.14, 0.12, 0.70, 0.78])
    h2, x2, y2 = np.histogram2d(data[notfid & reasonable & year_2007]['mag_med'],
                                data[notfid & reasonable & year_2007]['dz_rms'], 
                                bins=100, range=[[5,11], [0, .3]])
    h1, x1, y1 = np.histogram2d(data[notfid & reasonable & last_year]['mag_med'], 
                                data[notfid & reasonable & last_year]['dz_rms'],
                                bins=100, range=[[5,11], [0, .3]])
    ax2.pcolorfast(x2, y2, h2.T, cmap=cmap_blue, norm=norm_blue)
    ax2.pcolorfast(x1, y1, h1.T, cmap=cmap_red, norm=norm_red)
    plt.grid()
    plt.title("RMS vs mag: year 2007 (blue), past year (red)")
    plt.xlabel("Median Mag.")
    plt.ylabel("Star Resid RMS in Z (arcsec)")


    return dict(hist2d_fig=hist2d_fig,
                mag_vs_resid=mag_resid_fig)


if __name__ == '__main__':
    opt = get_options()
    if not os.path.exists(opt.outdir):
        os.makedirs(opt.outdir)

    rms_data = get_rms_data()
    # Filter in place to only use default data in plots
    rms_data = rms_data[rms_data['isdefault'] == 1]
    figures = mission_plots(rms_data)
    for fig in figures:
        plt.figure(figures[fig].number)
        plt.savefig(os.path.join(opt.outdir,
                                 "{}.png".format(fig)))
