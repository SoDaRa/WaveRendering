# Wave Rendering
 Module for Renpy to allow for distorting images and text with wavey effects

Ever wanted to make your images look trippy in Renpy?
Needed to make things look off?
Or just add some motion to some water?

![Example Wave](example_gif/WaveRenderingExample.gif)

I'm proud to share a neat little trick I've found with Ren'py. 
I don't consider this as useful as my kinetic text tags, but it's at least novel and useful for a couple while Ren'py 7.4 is getting optimized and fixed up.
This project was originally inspired by this video https://youtu.be/zjQik7uwLIQ on Earthbound battle background effects (hence the usage of them as examples in this demo). I wanted to see if I could come up with a way of doing it within Ren'py as well and think I came up with a pretty clever method.

## General Note
**This technique is made for people who have wanted to stick to Ren'py 7.3.5 or do not want to use the gl2 rendering that Ren'py 7.4 offers.** All of the effects this generates would in fact be much better handled by a shader. However, I've found their current implementation iffy lately. And this will work for anyone but at the cost of performance. Whenever I find the gl2 stuff to be working well, I'll likely release a shader that can do this much smoother and with a wider variety of options. 

## How it works
This works but having a class that breaks down an image into several strips. An offset is then applied to each strip before being built back together. It also allows for oscillation in terms of which strip is pulled from, which can be useful to simulate water refraction.

## Installation
Just take the [wave_renderer.rpy](https://github.com/SoDaRa/WaveRendering/blob/main/game/wave_renderer.rpy) and insert it into your project's game folder and should be all set to go. All documentation on the parameters for each of the classes and what they do is provided within the file.
    
## Limitations/Optimization
- **Breaking up a render into hundreds of strips can add considerable overhead to the rendering pipeline, and subsequently, LAG**. So it's recommended you try and reduce that number however possible. Some ways of doing this include:
   - Increasing the height of each strip will cut down substantially on the amount of time it takes to render, at the cost of some smoothness. But even increasing the strip height from 1 to 2 will half the amount of time it takes. 
       - **If you are building for mobile, you may want to have it automatically increase the strip height**. Or disable it for those platforms.
   - Make sure the strips are going across the smallest side. If an image is wider than it is tall, horizontal strips are recommended. And vertically if it's taller than it is wide.
   - Only strip as much as you need. If you only want to have the effect cover part of an image, then provide a start and end number so it only covers that range.
   - Applying this to a smaller image and then scaling it up to the size you want can help a lot. Especially if you're doing pixel art for your game since using nearest_neighbor during the zoom will keep each pixel crisp. 

## Support
This code will always be free. But if you'd like to support me you can consider buying it off itch here. https://wattson.itch.io/renpy-wave-rendering

## Bonus (Palette Cycling)
As this project was made to emulate the Earthbound battle backgrounds within Ren'py, I felt it incomplete without including Palette Cycling as well. Not sure how many people will find use out of that part. But I'm include it as a bonus. 

## Credits
- The team behind Minotaur Hotel for being cool with me using their sprite for demo purposes. Check 'em out at https://minoh.itch.io/minotaur-hotel
- Sunset Image borrowed from https://www.flickr.com/photos/rcweir/11074856536/ and modified to fit screen resolution and demonstrate melt effect.
- Earthbound backgrounds copyrighted to Nintendo. Please don't sue.
