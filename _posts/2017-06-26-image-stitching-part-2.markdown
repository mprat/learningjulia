---
layout: post
title:  "Image Stitching: Part 2"
date:   2017-06-26
mathjax: true
widgets: true
---

This is Part 2 of 2 in my posts about how to stitch two images together using Julia. It's rough around the edges, since I'm learning how to do this myself. In [Part 1]({% post_url 2017-03-26-image-stitching-part-2 %}) I talked about finding keypoints, descriptors, and matching two images together. This time, in Part 2, I'll talk about how to estimate the image transformation and how to actually do the stitching.

## Updating Julia versions

For Part 2 of image stitching, I upgraded to Julia 0.6.0. The process was quite painless - download the `.tar.gz` file from the [julialang.org](http://julialang.org), extract it, and add the `bin/` directory from the extracted archive into my path, as I described in my [initial post about setting up Julia]({% post_url 2017-02-19-launching-learning-julia %}).

Because I wanted to use the latest versions of some packages (and in Julia, they change often!) I had to do some updates before launching the Jupyter Notebook:

```
>>> Pkg.add("IJulia");
>>> Pkg.clone("https://github.com/JuliaImages/ImageFeatures.jl");
>>> Pkg.add("Images");
>>> Pkg.clone("https://github.com/JuliaImages/ImageDraw.jl");
>>> Pkg.add("FileIO");
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

BELOW THIS IS OLD STUFF

<!--more-->

I've included my notebook here. You can see the original [on Github](https://github.com/mprat/learningjulia/blob/master/notebooks/05-image-stitching-part-1.ipynb) if you like.

_Note: There are a number of places where I've included the Jupyter Notebook widgets in the rendering below. You can click buttons and slide sliders, but it does not affect the output. It's fun to play with the widgets though!_

You can also skip to any of the headers below:

* [Setting up and loading images](#Setting-up-and-loading-images)
* [Extracting feature points](#Extracting-Feature-Points)
* [Visualizing keypoints](#Visualizing-keypoints)
* [Calculating descriptors](#Calculating-descriptors)
* [Matching keypoints and descriptors](#Matching-keypoints)
* [The end result](#The-end-result)

{% include notebook.html name='05-image-stitching-part-1' %}

## Final thoughts

Extracting image features is a tricky business, and it is often dependent on the domain, type of image, white balance, etc. Before neural networks became popular, these manual orientation and gradient methods were all the rage. In computational photography and graphics, these methods are still going strong because they yield great results. I would be interested, when I'm more familiar with Julia, to dive into using a neural-network-based approach to extracting and matching keypoints between images. Who knows where my next project will take me!

Thank you for reading, as usual! I would love to hear from you if you have any suggestions, comments, or ideas for what I should learn next.
