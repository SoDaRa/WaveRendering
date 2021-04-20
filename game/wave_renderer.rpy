"""
 Wave Rendering Ren'Py Module
 2021 Daniel Westfall <SoDaRa2595@gmail.com>

 http://twitter.com/sodara9
 I'd appreciate being given credit if you do end up using this! :D Would really
 make my day to know I helped some people out!
 http://opensource.org/licenses/mit-license.php
 Github: https://github.com/SoDaRa/WaveRendering
 itch.io: https://wattson.itch.io/renpy-wave-rendering
"""
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


init python:
    import math
    # Helps set up the range of for loops
    def get_wave_range(width, height, start, end, direction, horizontal):
        if start == -1:
            if direction:
                start = 0
            else:
                if horizontal:
                    start = int(height)
                else:
                    start = int(width)
        if end == -1:
            if direction:
                if horizontal:
                    end = int(height)
                else:
                    end = int(width)
            else:
                end = 0
        # If start and end wouldn't make sense given the direction, we'll flip it to not cause an infinite loop
        if direction and start > end:
            start, end = end, start
        elif not direction and end > start:
            start, end = end, start
        return start, end

    class WaveImage(renpy.Displayable):
        # disp:         (String) Filename of the image to show.
        # freq:         (float) Freqency of the sine wave
        # amp:          (int) How far the lines move
        # damp:         (float) The value extreme approaches as the strip process continues
        # speed:        (float) How fast the sine wave moves with time
        # start:        (int) Which y/x it'll start on. -1 To start at edge
        # end:          (int) Which y/x it'll end on. -1 To end at edge
        # direction:    (bool) True to go left to right/top to bottom. False for reverse
        # horizontal:   (bool) True for strips to be horizontal. False for vertical.
        # strip_height: (int) Height of each strip. SHOULD NEVER BE < 1
        # double:       (bool/String) Whether strips will have double drawn on opposite side of wave. "interleaved" will make it apply interleaving of waves
        #                             Can help cover up holes if a background.
        # melt:         (bool/String) Whether to render with offset in which strip is rendered in place of the current one. The Vertical Oscillation effect in Earthbound
        #                             "wrap" will make it pull strips from the other end of the range if at the edge of the image.
        # sine_extreme: (bool) Whether extreme's starting value should be dictated by a sine wave.
        def __init__(self, disp, freq=10, amp=20, damp=1.0, speed=25, start=-1, end=-1, direction=True, horizontal=True, strip_height=1, double=False, melt = False, sine_extreme = False, *args, **kwargs):
            super(WaveImage, self).__init__(*args, **kwargs)
            self.height = 0
            # If disp is a string, it should be a file name that can be converted into an image.
            if isinstance(disp, (str, unicode)):
                self.child = Image(disp)
            else: # Otherwise we'll treat it as a displayable
                self.child = disp
            self.freq = freq
            self.amp = amp
            self.damp = damp
            self.speed = speed
            self.start = start
            self.end = end
            if direction:
                self.step = strip_height
            else:
                self.step = -1 * strip_height
            self.hori = horizontal
            self.direction = direction
            self.s_height = strip_height
            self.double = double
            self.melt = melt
            self.s_e = sine_extreme

        def render(self, width, height, st, at):
            extreme_start = 1.0 # Used to affect how much the wave offset is applied.
            if self.s_e:
                # Lots of ways you may want this function to work. But you should aim to keep the value of extreme between 0.0 and 1.0 for this
                # I decided on this one since it gives some time off at 0 with longer time on at 1
                extreme_start = min((math.sin(st/2) + 1.0) / 2.0, 1.0)
            extreme = extreme_start
            child_render = renpy.render(self.child, width, height, st, at) # The render we'll be distorting.
            if self.height == 0: # If this is out first time, then we need to update our width, height, start and end
                self.width, self.height = child_render.get_size()
                self.start, self.end = get_wave_range(self.width, self.height, self.start, self.end, self.direction, self.hori)

            render = renpy.Render(self.width, self.height) # The render we'll be putting strips onto
            step_num = float(self.start - self.end) / self.step
            step_count = 1
            if self.hori:
                for y in range(self.start, self.end, self.step):
                    curr_offset = int(math.sin((1.0/self.freq) * (y+(st * self.speed))) * self.amp) * extreme # Get the offset we'll work with for this line
                                                                                                              # The melt and line offset share the same wave
                                                                                                              # but could be broken up if one wished.
                                                                                                              # I chose to share it for simplicity.
                    if self.melt: # Use the offset in the subsurface process if we want to apply vertical oscillation
                        if self.melt == "wrap":
                            yoffset = int((y+curr_offset) % self.height)
                        else:
                            yoffset = int(y+curr_offset)
                        curr_surface = child_render.subsurface((0,yoffset,self.width,self.s_height))
                    else:
                        curr_surface = child_render.subsurface((0,y,self.width,self.s_height))
                    if self.double == "interleaved": # Apply interleaving if specified
                        if y % 2 == 0:
                            render.subpixel_blit(curr_surface, (curr_offset, y))
                        else:
                            render.subpixel_blit(curr_surface, (-curr_offset, y))
                    else:
                        render.subpixel_blit(curr_surface, (curr_offset, y)) # Apply our base offset
                        if self.double:
                            render.subpixel_blit(curr_surface, (-curr_offset, y))
                    if int(self.damp) != 1:
                        extreme = extreme_start - (step_count * ((self.damp - extreme_start) / step_num)) # Change how extreme the wave amplitude will be next round.
                        step_count += 1
            else:
                for x in range(self.start, self.end, self.step): # Same as above but vertically
                    curr_offset = int(math.sin((1.0/self.freq) * (x+(st * self.speed))) * self.amp) * extreme
                    if self.melt:
                        if self.melt == "wrap":
                            xoffset = int((x+curr_offset) % self.width)
                        else:
                            xoffset = int(x+curr_offset)
                        curr_surface = child_render.subsurface((xoffset,0,self.s_height,self.height))
                    else:
                        curr_surface = child_render.subsurface((x,0,self.s_height,self.height))
                    if self.double == "interleaved":
                        if x % 2 == 0:
                            render.subpixel_blit(curr_surface, (x, curr_offset))
                        else:
                            render.subpixel_blit(curr_surface, (x, -curr_offset))
                    else:
                        render.subpixel_blit(curr_surface, (x, curr_offset))
                        if self.double:
                            render.subpixel_blit(curr_surface, (x, -curr_offset))
                    if int(self.damp) != 1:
                        extreme = extreme_start - step_count * ((self.damp - extreme_start) / step_num)
                        step_count += 1

            renpy.redraw(self, 0)   # Request redraw
            return render           # Output our new render
    class MeltImage(renpy.Displayable):
        # Specialized version of WaveImage that only does Melting
        # disp:         (String) Filename of the image to show.
        # freq:         (int) Freqency of the sine wave
        # amp:          (int) How far the lines move
        # speed:        (int) How fast the sine wave moves with time
        # strip_height: (int) Height of each strip. SHOULD NEVER BE < 1
        #                     Can help cover up holes if a background.
        # wrap:         (bool) Whether it will pull strips from the other end of the range if at the edge of the image.
        def __init__(self, disp, freq=10, amp=20, speed=25, strip_height=1, horizontal = True, wrap = True, *args, **kwargs):
            super(MeltImage, self).__init__(*args, **kwargs)
            self.width, self.height = 0,0
            self.child = Image(disp)
            self.freq = freq
            self.amp = amp
            self.speed = speed
            self.s_height = strip_height
            self.hori = horizontal
            self.wrap = wrap
        def render(self, width, height, st, at):
            child_render = renpy.render(self.child, self.width, self.height, st, at)
            self.width, self.height = child_render.get_size()
            render = renpy.Render(self.width, self.height)
            if self.hori:
                for y in range(int(self.height)):
                    curr_offset = int(math.sin((1.0/self.freq) * (y+(st * self.speed))) * self.amp)
                    if self.wrap:
                        yoffset = int((y+curr_offset) % self.height)
                    else:
                        yoffset = int(y+curr_offset)
                    curr_surface = child_render.subsurface((0,yoffset,self.width,self.s_height))
                    render.subpixel_blit(curr_surface, (0, y))
            else:
                for x in range(int(self.width)):
                    curr_offset = int(math.sin((1.0/self.freq) * (x+(st * self.speed))) * self.amp)
                    if self.wrap:
                        xoffset = int((x+curr_offset) % self.width)
                    else:
                        xoffset = int(x+curr_offset)
                    curr_surface = child_render.subsurface((xoffset,0,self.s_height,self.height))
                    render.subpixel_blit(curr_surface, (x, 0))

            renpy.redraw(self, 0)   # Request redraw
            return render           # Output our new, beautiful, render
    class TranslateImage(renpy.Displayable):
        # Translates an displayable's render across the screen in a loop
        # Displayable should loop smoothly already and be sized for the screen/area it is to be rendered
        # Could probably have a speed parameter added to affect how fast the motion is
        # Or parameters to instruct it to apply certain kinds of motion or paths
        def __init__(self, disp, horizontal=True, vertical=False, *args, **kwargs):
            super(TranslateImage, self).__init__(*args, **kwargs)
            self.width, self.height = 0,0
            self.child = disp
            self.hori = horizontal
            self.vert = vertical
        def render(self, width, height, st, at):
            x,y = 0,0
            child_render = renpy.render(self.child, self.width, self.height, st, at)
            self.width, self.height = child_render.get_size()
            render = renpy.Render(self.width, self.height)
            # Get current offset within range of height and width
            if self.vert:
                y = int((st/.05) % self.height)
            if self.hori:
                x = int((st/.05) % self.width)
            render.blit(child_render, (x,y))
            # Duplicate render based on parameters
            if self.hori:
                render.blit(child_render, (x-self.width, y))
            if self.vert:
                render.blit(child_render, (x, y-self.height))
            # If going at a diagonal, then copy a render diagonal to original
            if self.hori and self.vert:
                render.blit(child_render, (x-self.width, y-self.height))
            return render

    class WaveImageRotate(renpy.Displayable):
        # Identical to WaveImage, but applies a rotation to the image render supplied by WaveImageUnRotate
        # and uses the time supplied by WaveImageUnRotate as well to ensure they stay in sync.
        def __init__(self, disp, freq=10, amp=20, damp=1.0, start=-1, end=-1, direction=True, horizontal=True, strip_height=1, double=False, melt = False, sine_extreme = False, *args, **kwargs):
            super(WaveImageRotate, self).__init__(*args, **kwargs)
            self.height = 0
            self.child = Image(disp)
            self.freq = freq
            self.amp = amp
            self.damp = damp
            self.start = start
            self.end = end
            if direction:
                self.step = strip_height
            else:
                self.step = -1 * strip_height
            self.hori = horizontal
            self.direction = direction
            self.s_height = strip_height
            self.double = double
            self.melt = melt
            self.s_e = sine_extreme
            self.rotate = 0
            self.time = 0

        def render(self, width, height, st, at):
            extreme_start = 1.0
            if self.s_e:
                extreme_start = min((math.sin(st/2) + 1.0) / 2.0, 1.0)
            extreme = extreme_start
            t = Transform(child=self.child, rotate = self.rotate)
            child_render = renpy.render(t, width, height, st, at)
            if self.height == 0:
                self.width, self.height = child_render.get_size()
                self.start, self.end = get_wave_range(self.width, self.height, self.start, self.end, self.direction, self.hori)

            render = renpy.Render(self.width, self.height)
            step_num = float(self.start - self.end) / self.step
            step_count = 1
            if self.hori:
                for y in range(self.start, self.end,self.step):
                    curr_offset = int(math.sin((1.0/self.freq) * (y+self.time)) * self.amp) * extreme
                    if self.melt:
                        curr_surface = child_render.subsurface((0,y+curr_offset,self.width,self.s_height))
                    else:
                        curr_surface = child_render.subsurface((0,y,self.width,self.s_height))
                    render.blit(curr_surface, (curr_offset, y))
                    if self.double:
                        render.blit(curr_surface, (-curr_offset, y))
                    if int(self.damp) != 1:
                        extreme = extreme_start - (step_count * ((self.damp - extreme_start) / step_num))
                        step_count += 1
            else:
                for x in range(self.start, self.end,self.step):
                    curr_offset = int(math.sin((1.0/self.freq) * (x+self.time)) * self.amp) * extreme
                    if self.melt:
                        curr_surface = child_render.subsurface((x+curr_offset,0,self.s_height,self.height))
                    else:
                        curr_surface = child_render.subsurface((x,0,self.s_height,self.height))
                    render.blit(curr_surface, (x, curr_offset))
                    if self.double:
                        render.blit(curr_surface, (x, -curr_offset))
                    if int(self.damp) != 1:
                        extreme = extreme_start - (step_count * ((self.damp - extreme_start) / step_num))
                        step_count += 1
            return render           # Output our new, beautiful, render

        # How WaveImageUnRotate communicates with us
        def set_rotate_time(self, new_angle, new_time):
            self.rotate = new_angle
            self.time = new_time
    class WaveImageUnRotate(renpy.Displayable):
        # Works with WaveImageRotate to rotate a displayable wave render.
        # Takes the rotated render supplied by WaveImageRotate and rotates it back to 0 degrees.
        def __init__(self, disp, freq=10, amp=20, damp=1.0, speed=25, start=-1, end=-1, direction=True, horizontal=True, strip_height=1, double=False, melt=False, sine_extreme = False,*args, **kwargs):
            super(WaveImageUnRotate, self).__init__(*args, **kwargs)
            self.width, self.height = 0,0
            self.speed = speed
            self.child = WaveImageRotate(disp, freq, amp, damp, start, end, direction, horizontal, strip_height, double, melt, sine_extreme, *args, **kwargs)
        def render(self, width, height, st, at):
            st = st * self.speed
            angle = st % 360
            self.child.set_rotate_time(angle, st)
            t = Transform(child=self.child, rotate = -1 * angle)
            child_render = renpy.render(t, self.width, self.height, st, at)
            self.width, self.height = child_render.get_size()
            renpy.redraw(self, 0)   # Request redraw
            return child_render           # Output our new, beautiful, render

    # Applies wavy effects to text.
    # Accepts arguments for amp, freq, speed, strip_height, horizontal, double(no interleaved) and melt
    # The following must be paired with a float or int parameter
    # 'a' for amp (int)
    # 'f' for freq (float)
    # 's' for speed (float)
    # 'h' for strip_height (int)
    # The following enable an effect if they are included.
    # 'v' to enable vertical wave
    # 'd' for double render
    # 'm' for melt render
    # Separate number arguments with a '-'.
    # Example: "{wave=a10-f0.9-s2.5-h5-vdm}"
    def wavy_tag(tag, argument, contents):
        new_list = [ ]
        amp, freq, speed, strip_height, hori, double, melt = 10, 20, 25, 1, True, False, False
        if 'v' in argument:
            hori = False
        if 'd' in argument:
            double = True
        if 'm' in argument:
            melt = True
        argument = argument.split('-')
        for arg in argument:
            if 'a' in arg and arg[1:].isdigit():
                amp = int(arg[1:])
            if 'f' in arg:
                freq = float(arg[1:])
            if 's' in arg:
                speed = float(arg[1:])
            if 'h' in arg and arg[1:].isdigit():
                strip_height = int(arg[1:])
        my_style = DispTextStyle() # Defined in kinetic_text_tags.rpy. Used for style information preservation.
        for kind,text in contents:
            if kind == renpy.TEXT_TEXT:
                text = Text(my_style.apply_style(text))
                char_disp = WaveImage(text, amp = amp, freq=freq, speed = speed, strip_height = strip_height, horizontal = hori, double=double, melt=melt)
                new_list.append((renpy.TEXT_DISPLAYABLE, char_disp))
            elif kind == renpy.TEXT_TAG:
                if not my_style.add_tags(text):
                    new_list.append((kind, text))
            else:
                new_list.append((kind,text))
        return new_list

    config.custom_text_tags["wave"] = wavy_tag
