#!/usr/bin/env python3
"""
whiteclock by https://askubuntu.com/users/81249/kenn atillakaraca@gmail.com 
Based on https://pygobject.readthedocs.io/en/latest/guide/cairo_integration.html, Wander Boessenkool's sphinX.py clock and cairo-demo/X11/cairo-demo.c and 
"""
import math
from datetime import datetime
import cairo
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib 
FPS = 4

# taken from https://github.com/s-zeid/bin/blob/main/display-transparent
def _drag_callback(window, event):
 """Called when the window is clicked on."""
 window.begin_move_drag(
  event.button,
  int(round(event.x + window.get_window().get_root_origin()[0])),
  int(round(event.y + window.get_window().get_root_origin()[1])),
  event.time
 )

# ticks method taken from https://codegolf.stackexchange.com/users/2381/luser-droog   xclock.c    
def ticks(ctx):
    #t = 12
    ctx.set_source_rgb(1, 1, 1)
    ctx.save()
    ctx.translate(100, 100)
    ctx.rotate(math.pi/12)
    for i in range(1, 13):
        #ctx.translate(50, 50)
        ctx.set_line_width(1)
        for j in range(4):
            ctx.rotate(math.pi/30)
            #ctx.translate(50, 50)
            ctx.move_to(50, 50)
            ctx.rel_line_to(2, 2)
            #ctx.close_path()
            ctx.stroke()
        
        ctx.set_line_width(3)

        ctx.rotate(math.pi/30)
        #ctx.translate(50, 50)
        ctx.move_to(50, 50)
        ctx.rel_line_to(2, 2)
        #ctx.stroke()

        #ctx.close_path()
        ctx.stroke()
    ctx.restore()    

#based on Mael Ponchant's algorithm https://stackoverflow.com/questions/58589643/cant-show-text-in-cairomm-gtkmm-context        
def face(ctx):
    ctx.translate(100, 100)
    #ctx.rotate(-math.pi/120)
    for i in range(1, 13):
        #ctx.translate(50, 50)
        #ctx.move_to(40, 60)
        ctx.move_to(58 * math.cos (2 * (i - 7.5) * 0.75 * math.pi / 9 + (0.75 * math.pi )) - 5, 58 * math.sin (2 * (i - 7.5) * 0.75 * math.pi / 9 + (0.75 * math.pi)) + 5);
        #ctx.move_to(58 * math.cos (2 * (i - 8) * 0.75 * math.pi / 9 + (0.75 * math.pi )) - 3, 58 * math.sin (2 * (i - 8) * 0.75 * math.pi / 9 + (0.75 * math.pi)) + 5);
        ctx.set_line_width(1)
        ctx.select_font_face("Serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(12)
        ctx.set_source_rgb(1, 1, 1)
        #ctx.move_to(40, 60)
        #ctx.rotate(j * - math.pi/30)
        ctx.show_text(str(i))  
         
# hands methon taken from Wander Boessenkool's sphinX.py clock  
def hands(ctx):

        ctx.set_source_rgba(1.0, 1.0, 1.0, 0.0)
        ctx.set_operator(cairo.OPERATOR_SOURCE)
        ctx.paint()
        ctx.set_operator(cairo.OPERATOR_CLEAR)
        ctx.set_operator(cairo.OPERATOR_OVER)
        ctx.translate(50, 50)
        ctx.scale(100 , 100)
        curtime = datetime.now()
        h = float(curtime.hour)
        m = float(curtime.minute)
        s = float(curtime.second)
        m += s / 60
        h += m / 60
        h = (h % 12) / 6 * math.pi
        m = m / 30 * math.pi
        s = s / 30 * math.pi

        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(0.5, 0.5)
        ctx.line_to(0.5 + 0.3 * math.sin(h), 0.5 - 0.3 * math.cos(h))
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.8)
        ctx.set_line_width(0.075)
        ctx.stroke_preserve()
        ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        ctx.set_line_width(0.05)
        ctx.stroke()
        ctx.move_to(0.5, 0.5)
        ctx.line_to(0.5 + 0.35 * math.sin(m), 0.5 - 0.35 * math.cos(m))
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.8)
        ctx.set_line_width(0.065)
        ctx.stroke_preserve()
        ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        ctx.set_line_width(0.04)
        ctx.stroke()
        ctx.move_to(0.5, 0.5)
        ctx.line_to(0.5 + 0.4 * math.sin(s), 0.5 - 0.4 * math.cos(s))
        ctx.set_source_rgba(0.0, 0.0, 0.0, 0.8)
        ctx.set_line_width(0.055)
        ctx.stroke_preserve()
        ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        ctx.set_line_width(0.03)
        ctx.stroke()
        ctx.move_to(0.55, 0.5)
        ctx.arc(0.5, 0.5, 0.05, 0, 2 * math.pi)
        ctx.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        ctx.fill_preserve()
        ctx.set_line_width(0.015)
        ctx.set_source_rgba(0.0, 0.0, 0.0, 1.0)
        ctx.stroke()

def circle(ctx):
    #ctx.move_to(50, 50)
    #ctx.translate(100, 100)
    ctx.arc(100, 100, 75, 0, 4 * math.pi/2)
    #ctx.set_source_rgb(0, 0, 0)
    #ctx.set_line_width(0.04)
    #ctx.stroke()

def draw(da, ctx):

    #ctx.set_line_width(SIZE / 4)
    ctx.set_tolerance(0.1)
    #stroke_shapes(ctx, 0, 9 * SIZE)
    ctx.save()
    ctx.new_path()
    #ctx.translate(3 * SIZE, 0)
    #arc(ctx)
    hands(ctx)
    ctx.restore()
    circle(ctx)
    ticks(ctx)
    face(ctx)
    #hands(ctx)
    #ctx.arc(50, 50, 50, 0, 4 * math.pi/2)    
    ctx.stroke()

# to update the screen, taken from http://bazaar.launchpad.net/~macslow/cairo-countdown/trunk/view/head:/countdown.py    
def onTimeout (widget):
    widget.queue_draw ()
    return True


def main():
    win = Gtk.Window(title="Hayriye Saati")
    #win.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
    #win.connect('button-press-event', buttonpress)
     # Make the window draggable
    screen = win.get_screen()
    rgba = screen.get_rgba_visual()
    win.set_visual(rgba)
    win.connect("button-press-event", _drag_callback)
    win.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
    #win.set_type_hint (Gdk.WindowTypeHint.DOCK)
    win.connect('destroy', lambda w: Gtk.main_quit())
    win.set_default_size(200, 200)
    win.set_app_paintable (True)
    win.set_decorated (False)
    win.set_skip_taskbar_hint (True)
    drawingarea = Gtk.DrawingArea()
    win.add(drawingarea)
    drawingarea.connect('draw', draw)
    timeoutId = GLib.timeout_add (1000 / FPS, onTimeout, win)
    win.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()
