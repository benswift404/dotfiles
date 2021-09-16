# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List  # noqa: F401
import os
import subprocess
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal, logger

mod = "mod4"
terminal = "alacritty"

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "r", lazy.spawn("rofi -show run"), desc="Run rofi"),
    Key([mod, "control"], "p", lazy.spawn("xfce4-screenshooter -f ~/Screenshots/%Y-%m-%T-screenshot.png"), desc="Take a screenshot"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),

    Key([mod], "w", lazy.spawn("slock"), desc="Lock Screen"),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "f", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
]

group_names = [("一", {'layout': 'columns'}),
               ("二", {'layout': 'columns'}),
               ("三", {'layout': 'columns'}),
               ("四", {'layout': 'columns'}),
               ("五", {'layout': 'columns'}),
               ("六", {'layout': 'floating'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

layout_theme = {
    "border_width": 5,
    "margin": 8,
    "border_focus": "#bd93f9",
    "border_normal": "#44475a",
}

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(),
    layout.Floating(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.TextBox("歡迎回來, 班傑明",
                    name="name",
                    font="Source Han Sans TW Bold",
                    background="#bd93f9",
                    padding=40,
                    ),
                widget.Sep(
                    linewidth=0,
                    padding=24
                ),
                # widget.CurrentLayout(),
                widget.WindowName(
                    font="Source Xode Pro Bold",
                ),
                # widget.Chord(
                #     chords_colors={
                #         'launch': ("#ff0000", "#ffffff"),
                #     },
                #     name_transform=lambda name: name.upper(),
                # ),
                # widget.Spacer(),
                widget.GroupBox(
                    active='#bd93f9',
                    inactive='#f8f8f2',
                    highlight_color='#191919',
                    highlight_method='line',
                    #this_current_screen_border='#f8f8f2',
                    #other_current_screen_border='#f8f8f2',
                    this_current_screen_border = '#f8f8f2',
                    this_screen_border ='#f8f8f2',
                    other_current_screen_border ='#f8f8f2',
                    other_screen_border ='#f8f8f2',

                ),
                widget.Spacer(),
                widget.TextBox(
                    " ",
                    name="ethernet",
                    padding=0,
                    fontsize=25,
                    #background="#ffb86c",
                    foreground="#ffb86c",
                ),
                widget.Net(
                    # interface = "enp6s0",
                    font="Source Code Pro Bold",
                    format = '{down} ↓↑ {up}',
                    padding=0,
                    #background="#ffb86c",
                ),
                widget.Sep(
                    linewidth=2,
                    size_percent=50,
                    padding=20
                ),
                widget.TextBox(
                    "  ",
                    name="cpu",
                    padding=0,
                    fontsize=25,
                    #background="#ffb86c",
                    foreground="#ff79c6",
                ),
                widget.CPU(
                    font="Source Code Pro Bold",
                    padding=0,
                    #background="#ff79c6",
                ),
                widget.Sep(
                    linewidth=2,
                    size_percent=50,
                    padding=20
                ),
                widget.TextBox(
                    " ",
                    name="memory",
                    padding=0,
                    fontsize=25,
                    #background="#ffb86c",
                    foreground="#8be9fd",
                ),
                widget.Memory(
                    font="Source Code Pro Bold",
                    padding=0,
                    #background="#8be9fd",
                ),
                widget.Sep(
                    linewidth=0,
                    padding=15
                ),
                widget.Systray(),
                widget.Clock(format='%m-%d-%Y %a %I:%M %p',
                    font="Source Code Pro Bold",
                    padding=6,
                    background="#ff5555",
                ),
            ],
            30,
            margin=8,
            background="#191919",
        ),
        bottom=bar.Bar(
            [
                #widget.Spacer(),
                widget.TextBox(
                    "",
                    name="arch",
                    padding=12,
                    fontsize=30,
                    background="#44475a",
                    foreground="#8be9fd",
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(terminal + ' -e python3 development/arch.py')},
                ),
                widget.TextBox(
                    "",
                    name="firefox",
                    padding=10,
                    fontsize=30,
                    #background="#ffb86c",
                    foreground="#ffb86c",
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('firefox')},
                ),
                widget.TextBox(
                    "",
                    name="code",
                    padding=10,
                    fontsize=30,
                    #background="#ffb86c",
                    foreground="#8be9fd",
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('code')},
                ),
                widget.TextBox(
                    "",
                    name="thunar",
                    padding=10,
                    fontsize=30,
                    #background="#ffb86c",
                    foreground="#bd93f9",
                    mouse_callbacks={'Button1': lambda: qtile.cmd_spawn('thunar')},
                ),
                widget.Spacer(),
            ],
            35,
            margin=[0,880,8,880],
            background="#191919",
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
], **layout_theme)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "qtile"
