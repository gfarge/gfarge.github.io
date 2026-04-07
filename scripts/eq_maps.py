"""
Earthquake–station geometry maps for the earthquake-sounds page.

Outputs (relative to this script):
  ../files/figures/map_tam_sumatra.png
  ../files/figures/map_inu_nagoya.png

Station coordinates from GEOSCOPE / FDSN:
  TAM  Tamanrasset, Algeria     22.79149 N   5.52838 E
  INU  Inuyama, Japan           35.35    N 137.029   E

Earthquake coordinates:
  Sumatra-Andaman 2004-12-26 M9.1   3.295 N  95.982 E
  Nagoya (user-provided)            35.307 N 137.091 E
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import to_rgba
from matplotlib.patches import Rectangle
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from pyproj import Geod

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR    = os.path.join(SCRIPT_DIR, '..', 'files', 'figures')

# ── Palette ────────────────────────────────────────────────────────────────
LAND  = "#d6da8b"
SEA   = "#a4d8ff"
STA   = 'royalblue'
EQ    = 'crimson'
URBAN = "#adadad"
FS    = 12   # base font size

_geod = Geod(ellps='WGS84')


# ── Geodesy ─────────────────────────────────────────────────────────────────

def dist_and_mid(lat1, lon1, lat2, lon2):
    """Return (distance_km, mid_lat, mid_lon) along the geodesic."""
    az, _, d_m = _geod.inv(lon1, lat1, lon2, lat2)
    mlon, mlat, _ = _geod.fwd(lon1, lat1, az, d_m / 2.0)
    return d_m / 1000.0, mlat, mlon


# ── Helpers ────────────────────────────────────────────────────────────────

def base_map(ax, extent, urban_res='10m'):
    ax.set_facecolor(SEA)
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND,      facecolor=LAND, zorder=1)
    ax.add_feature(cfeature.COASTLINE, linewidth=0.4, edgecolor='#888888', zorder=2)
    ax.add_feature(cfeature.BORDERS,   linewidth=0.2, edgecolor='#aaaaaa', zorder=2)
    ax.add_feature(
        cfeature.NaturalEarthFeature('cultural', 'urban_areas', urban_res),
        facecolor=URBAN, edgecolor='none', zorder=3)


def add_gridlines(ax, xlocs, ylocs):
    gl = ax.gridlines(draw_labels=True, x_inline=False, y_inline=False,
                      linewidth=0.4, color='gray', alpha=0.4, linestyle='--')
    gl.xlocator     = mticker.FixedLocator(xlocs)
    gl.ylocator     = mticker.FixedLocator(ylocs)
    gl.top_labels   = False
    gl.right_labels = False
    gl.xlabel_style = {'size': FS - 1}
    gl.ylabel_style = {'size': FS - 1}


def add_scale_bar(ax, length_km, x0_frac=0.05, y0_frac=0.06):
    ext = ax.get_extent(ccrs.PlateCarree())
    lon_min, lon_max, lat_min, lat_max = ext
    lat_bar = lat_min + (lat_max - lat_min) * y0_frac
    lon_bar = lon_min + (lon_max - lon_min) * x0_frac
    d_lon   = length_km / (111.32 * np.cos(np.radians(lat_bar)))
    ax.plot([lon_bar, lon_bar + d_lon], [lat_bar, lat_bar],
            color='#333333', linewidth=2.5, solid_capstyle='butt',
            transform=ccrs.PlateCarree(), zorder=10)
    ax.text(lon_bar + d_lon / 2,
            lat_bar + (lat_max - lat_min) * 0.025,
            f'{length_km} km',
            ha='center', va='bottom', color='#333333', fontsize=FS - 1,
            transform=ccrs.PlateCarree(), zorder=10)


def plot_station(ax, lon, lat, label, dx=0.0, dy=0.0, ha='left'):
    ax.plot(lon, lat, marker='v', color=STA, markersize=8, linestyle='none',
            markeredgewidth=0, transform=ccrs.PlateCarree(), zorder=7)
    ax.text(lon + dx, lat + dy, label, color=STA, fontsize=FS,
            va='center', ha=ha, transform=ccrs.PlateCarree(), zorder=8,
            fontweight='bold')


def plot_eq(ax, lon, lat, label, dx=0.0, dy=0.0, ha='left'):
    ax.plot(lon, lat, marker='*', color=EQ, markersize=12, linestyle='none',
            markeredgewidth=0, transform=ccrs.PlateCarree(), zorder=7)
    ax.text(lon + dx, lat + dy, label, color=EQ, fontsize=FS,
            va='center', ha=ha, transform=ccrs.PlateCarree(), zorder=8,
            fontweight='bold')


def add_geodetic_line(ax, lat1, lon1, lat2, lon2, lbl_offset=(0, 0)):
    """Dotted geodetic line with a distance label at the midpoint."""
    d_km, m_lat, m_lon = dist_and_mid(lat1, lon1, lat2, lon2)
    ax.plot([lon1, lon2], [lat1, lat2],
            color='#555555', linewidth=0.9, linestyle=':',
            transform=ccrs.Geodetic(), zorder=5)
    ax.text(m_lon + lbl_offset[0], m_lat + lbl_offset[1],
            f'{d_km:.0f} km',
            color='#333333', fontsize=FS - 1, ha='center', va='center',
            transform=ccrs.PlateCarree(), zorder=9,
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1.5))


def add_japan_inset(ax, main_extent):
    """Floating top-left inset: Japan outline + red box for the zoomed region."""
    shp = shpreader.natural_earth(resolution='50m', category='cultural',
                                  name='admin_0_countries')
    japan = next(
        (r.geometry for r in shpreader.Reader(shp).records()
         if r.attributes['NAME'] == 'Japan'),
        None)
    if japan is None:
        return

    # Plain axes, transparent background, no frame
    axins = ax.inset_axes([0.02, 0.5, 0.1, 0.40])
    axins.axis('off')
    axins.patch.set_alpha(0)

    # Draw Japan polygons in geographic lat/lon
    polys = list(japan.geoms) if hasattr(japan, 'geoms') else [japan]
    for poly in polys:
        xs, ys = poly.exterior.xy
        axins.fill(xs, ys, color='k', linewidth=0, zorder=1)

    axins.set_xlim(128, 148)
    axins.set_ylim(29, 46)
    axins.set_aspect('equal')

    # Red box indicating the zoomed region
    ln, lx, la, lb = main_extent
    axins.add_patch(Rectangle((ln, la), lx - ln, lb - la,
                               linewidth=1.0, edgecolor='crimson',
                               facecolor='crimson', zorder=3))


# ── Map 1: TAM / Sumatra-Andaman 2004 ─────────────────────────────────────
tam_lat, tam_lon = 22.79149, 5.52838
sa_lat,  sa_lon  = 3.295, 95.982

fig, ax = plt.subplots(figsize=(6, 3.5),
                       subplot_kw={'projection': ccrs.PlateCarree()})
base_map(ax, extent=[-8, 104, -7, 32], urban_res='50m')
add_gridlines(ax,
              xlocs=list(range(0, 110, 20)),
              ylocs=list(range(-10, 35, 10)))
plot_station(ax, tam_lon, tam_lat, 'TAM',          dx=1.5,  dy=0.5)
# EQ label to the left so it stays within the frame
plot_eq(     ax, sa_lon,  sa_lat,  'Sumatra (2004)', dx=-1.5, dy=0.5, ha='right')
# Geodetic line; label offset upward from the midpoint
add_geodetic_line(ax, tam_lat, tam_lon, sa_lat, sa_lon, lbl_offset=(0, 2.5))
# No scale bar for this map

plt.tight_layout(pad=0.5)
out1 = os.path.join(FIG_DIR, 'map_tam_sumatra.png')
plt.savefig(out1, dpi=150, bbox_inches='tight')
plt.close()
print(f'Saved {out1}')


# ── Map 2: INU / Nagoya earthquake ────────────────────────────────────────
inu_lat, inu_lon = 35.35,  137.029
eq2_lat, eq2_lon = 35.307, 137.091

# lon 136-138 (2°) × lat 34.6-35.85 (1.25°) → clearly wider than taller
main_extent = [135.9, 138.1, 34.9, 35.6]

fig, ax = plt.subplots(figsize=(6, 4.2),
                       subplot_kw={'projection': ccrs.PlateCarree()})
base_map(ax, extent=main_extent)
add_gridlines(ax,
              xlocs=[136, 137, 138],
              ylocs=[35, 35.5])

# INU and the EQ are only ~7 km apart; stagger labels to avoid overlap
# INU: upper-left of the marker
plot_station(ax, inu_lon, inu_lat, 'INU', dx=-0.03, dy=0.05, ha='right')
# Nagoya EQ: lower-right of the marker
plot_eq(ax, eq2_lon, eq2_lat, 'Nagoya EQ', dx=0.03,  dy=-0.06, ha='left')
# Distance label: offset to the right of midpoint, above the EQ label
add_geodetic_line(ax, inu_lat, inu_lon, eq2_lat, eq2_lon,
                  lbl_offset=(0.11, 0.03))

add_scale_bar(ax, 50)
add_japan_inset(ax, main_extent)

plt.tight_layout(pad=0.5)
out2 = os.path.join(FIG_DIR, 'map_inu_nagoya.png')
plt.savefig(out2, dpi=150, bbox_inches='tight')
plt.close()
print(f'Saved {out2}')
