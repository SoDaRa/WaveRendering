# Image tag declarations
image bg sunset =               "images/bgs/sunset.jpg"
image wave set =                WaveImage("images/bgs/sunset.jpg", 20, 10, 0.99, 20, -1, 450, False, True, 1, True, True)
image earthbbg =                TranslateImage(Transform(MeltImage("images/bgs/BG2.png", speed = 50, amp = 50, horizontal=True),xzoom=5,yzoom = 2.8125, nearest=True), True, False)
image interleavedbbg =          Transform(WaveImage("images/bgs/BG4.png",double = "interleaved"), zoom=2.8125, nearest = True)
image interleavedbbg double =   Transform(WaveImage("images/bgs/BG4Rings.png",double = True), zoom=2.8125, nearest = True)
image rotate_img =              WaveImageUnRotate("images/nito.webp", amp = 20,strip_height = 10, speed=25)
image sine_ext =                WaveImage("images/nito.webp", amp = 20, sine_extreme = True, damp = 0.995)

image interleaved_solid =   "#600000"
image pal_solid =           "#203830"
image empty_solid =         "#aaa"

label start:
    scene pal_solid
    show pal_cycle
    "Here is an example of palette cycling using a background pulled from Earthbound."
    "It's a bit cumbersome to setup but definitely doable."

    scene earthbbg
    "Here is an example of the melt effect with some translation applied."
    "Looks pretty interesting."
    scene interleaved_solid
    show interleavedbbg
    "Here is an interleaved background image."
    show interleavedbbg double
    "And here's what happens if we modify it a bit and flip each wave!"
    scene bg sunset
    show wave set
    "Here is an example of using the melt effect to create water distortion over a sunset."
    window hide
    pause
    window show
    "The dampening is used to help decrease the effect as we approach the horizon."
    scene empty_solid
    show rotate_img:
        yoffset -50 # Just to help center it a bit.
    "Here is an example of rotating the strips in real time."
    "The strip height has been increased to help it run smoother."
    "You may want to have a check to reduce it further if you release on mobile."
    hide rotate_img
    show sine_ext
    "Here's an example of the effect coming and going due to another sine wave."
    hide sine_ext
    "And of course, I can extend all of these effects into text tags."
    "{wave=s100-}It's likely harder to read but is quite neat.{/wave}"
    "{wave=s100-v}Can even be used vertically if one wishes.{/wave}"
    "{wave}{color=#f00}And can be used{/color} {b}with other text styling{/b} {u}tags.{/u}{/wave}"
    "{wave=a20-s50-vmd}Or to really distort it. {/wave}"
    "Thank you for checking out this project and hope it was interesting!"
    "The source code for this can be found in the game folder in the .rpy files."
    "wave_renderer.rpy handles the wave effects while palette_cycling.rpy has the palette cycling one."
    "Credits to image sources can be found in the About screen."
    return
