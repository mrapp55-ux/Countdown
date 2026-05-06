"""
Countdown Chart Implementation

This script creates a visual countdown chart using Matplotlib, highlighting specific days
(Mondays and Wednesdays) from May 1, 2026, to September 30, 2026. The chart uses bars
to represent days, with different styles indicating past, present, and future dates.

Key features:
- Green bars for Mondays and Wednesdays (tall for emphasis)
- Red bars for other days (short)
- Visual differentiation for past (hollow), today (half-filled), and future (solid) key days
- Month separators and labels
- Interactive refresh button
"""

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Button
from datetime import date, timedelta

START = date(2026, 5, 1)
END = date(2026, 9, 30)

SHORT_H = 1.0
TALL_H = 3.0
BAR_W = 0.7
GREEN = '#2ecc71'
RED = '#e74c3c'


def build_days():
    days = []
    d = START
    while d <= END:
        days.append(d)
        d += timedelta(days=1)
    return days


def draw_chart(ax):
    ax.clear()
    today = date.today()
    days = build_days()

    for i, d in enumerate(days):
        is_key = d.weekday() in (0, 2)
        if is_key:
            if d < today:
                ax.add_patch(mpatches.Rectangle(
                    (i - BAR_W / 2, 0), BAR_W, TALL_H,
                    linewidth=1.5, edgecolor=GREEN, facecolor='none'
                ))
            elif d == today:
                half = TALL_H / 2
                ax.add_patch(mpatches.Rectangle(
                    (i - BAR_W / 2, 0), BAR_W, half,
                    linewidth=0, facecolor=GREEN
                ))
                ax.add_patch(mpatches.Rectangle(
                    (i - BAR_W / 2, half), BAR_W, half,
                    linewidth=1.5, edgecolor=GREEN, facecolor='none'
                ))
            else:
                ax.add_patch(mpatches.Rectangle(
                    (i - BAR_W / 2, 0), BAR_W, TALL_H,
                    linewidth=0, facecolor=GREEN
                ))
        else:
            ax.add_patch(mpatches.Rectangle(
                (i - BAR_W / 2, 0), BAR_W, SHORT_H,
                linewidth=0, facecolor=RED
            ))

    month_groups = {}
    for i, d in enumerate(days):
        if d.month not in month_groups:
            month_groups[d.month] = {'start': i, 'end': i, 'label': d.strftime('%B')}
        month_groups[d.month]['end'] = i

    tick_pos = []
    tick_labels = []
    for _, info in sorted(month_groups.items()):
        mid = (info['start'] + info['end']) / 2
        tick_pos.append(mid)
        tick_labels.append(info['label'])
        if info['start'] > 0:
            ax.axvline(
                info['start'] - 0.5,
                color='#777777',
                linewidth=1.5,
                linestyle='--',
                alpha=0.7,
                zorder=0
            )

    ax.set_xlim(-1, len(days))
    ax.set_ylim(0, TALL_H + 0.4)
    ax.set_aspect('auto')
    ax.set_xticks(tick_pos)
    ax.set_xticklabels(tick_labels, fontsize=12, ha='center')
    ax.set_yticks([])
    ax.set_title(
        f'Countdown  |  May – September 2026    (today: {today.strftime("%d %b %Y")})',
        fontsize=13, pad=12
    )

    for spine in ('top', 'right', 'left'):
        ax.spines[spine].set_visible(False)


fig, ax = plt.subplots(figsize=(18, 4))
fig.canvas.manager.set_window_title('Countdown Chart')
plt.subplots_adjust(bottom=0.18, left=0.02, right=0.98, top=0.90)

# Initial draw
draw_chart(ax)

ax_btn = fig.add_axes([0.82, 0.02, 0.14, 0.08])
btn = Button(ax_btn, 'Refresh', color='#eeeeee', hovercolor='#cccccc')
btn.on_clicked(lambda event: draw_chart(ax))

plt.show()
