---
layout: post
title:  "Image Stitching: Part 2"
date:   2018-08-25
mathjax: true
widgets: false
published: true
---

This is Part 2 of 2 in my posts about how to stitch two images together using Julia. It's rough around the edges, since I'm learning how to do this myself. In [Part 1]({% post_url 2017-03-26-image-stitching-part-1 %}) I talked about finding keypoints, descriptors, and matching two images together. This time, in Part 2, I'll talk about how to estimate the image transformation and how to actually do the stitching.

<!--more-->

## Updating Julia versions

For Part 2 of image stitching, I upgraded to Julia 0.6.0. The process was quite painless - download the `.tar.gz` file from the [julialang.org](http://julialang.org), extract it, and add the `bin/` directory from the extracted archive into my path, as I described in my [initial post about setting up Julia]({% post_url 2017-02-19-launching-learning-julia %}).

Because I wanted to use the latest versions of some packages (and in Julia, they change often!) I had to do some updates before launching the Jupyter Notebook:

```;
>>> Pkg.update();
>>> using IJulia;
>>> notebook(dir="notebooks/", detached=true);
```

I also had to make sure to change my Jupyter kernel to Julia 0.6.0 - in the menu bar at the top of the page, click on "Kernel" --> "Change Kernel" --> "Julia 0.6.0". No reason to stay stuck to old code!

## Updating some image drawing functions

One of the packages that I had to image ([ImageDraw](https://github.com/JuliaImages/ImageDraw.jl), used for drawing shapes on images), updated their API for drawing lines. There is no longer a syntactic sugar called `line` for drawing lines on images; instead, there is a single `draw` method that accepts targets and `Drawable` objects. I changed my previous code:

```
line!(grid, m[1], m[2] + offset)
```

to

```
draw!(grid, LineSegment(m[1], m[2] + offset))
```

And everything worked great.

I've included my notebook here. You can see the original [on Github](https://github.com/mprat/learningjulia/blob/master/notebooks/06-image-stitching-part-2.ipynb) if you like.

You can also skip to any of the headers below:

* [Calculate Transformation](#Calculate-Transformation)
* [Transform Image](#Transform-Image)
* [RANSAC: Improving Homography Estimation](#RANSAC-Improving-Homography-Estimation)
* [Merging Images](#Merging-Images)
* [Conclusion and Summary](#Conclusion-and-Summary)

{% include notebook.html name='06-image-stitching-part-2' %}

## Final thoughts

This notebook was a long time coming (almost a year between parts 1 and 2!) but I'm glad I finally did it. It was tons of fun, and in a future notebook I want to do automatic panorama stitching with multiple images instead of just two! Hopefully this will be equally painless. I am sold on using Julia for image processing - lightning fast, easy to prototype, and easy to get things done!

Thank you for reading, as usual! I would love to hear from you if you have any suggestions, comments, or ideas for what I should learn next.

Here are the ideas I already have:
* Explore more sophisticated methods of image stitching (for example, mean pixel value across multiple pixels, bilaterial filtering, edge smoothing)
* Learning how to fix the warning I see from the `ImageDraw` package
* Multiple-image panorama stitching (instead of just two images)
* Your idea here!
