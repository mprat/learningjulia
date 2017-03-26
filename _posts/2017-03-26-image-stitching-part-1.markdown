---
layout: post
title:  "Image Stitching: Part 1"
date:   2017-03-26
mathjax: true
---

This is Part 1 of 2 in my posts about how to stitch two images together using Julia. It's rough around the edges, since I'm learning how to do this myself. In Part 1 I talk about finding keypoints, descriptors, and matching two images together. Next time, I'll talk about how to estimate the image transformation and how to actually do the stitching.

<!--more-->

I've included my notebook here. You can see the original [on Github](https://github.com/mprat/learningjulia/blob/master/notebooks/05-image-stitching-part-1.ipynb) if you like.

You can also skip to any of the headers below:

* [Setting up and loading images](#Setting-up-and-loading-images)
* [Extracting feature points](#Extracting-feature-points)
* [Visualizing keypoints](#Visualizing-keypoints)
* [Calculating descriptors](#Calculating-descriptors)
* [Matching keypoints and descriptors](#Matching-keypoints-and-descriptors)
* [The end result](#The-end-result)

{% include notebook.html name='05-image-stitching-part-1' %}

## Final thoughts

Extracting image features is a tricky business, and it is often dependent on the domain, type of image, white balance, etc. Before neural networks became popular, these manual orientation and gradient methods were all the rage. In computational photography and graphics, these methods are still going strong because they yield great results. I would be interested, when I'm more familiar with Julia, to dive into using a neural-network-based approach to extracting and matching keypoints between images. Who knows where my next project will take me!

Thank you for reading, as usual! I would love to hear from you if you have any suggestions, comments, or ideas for what I should learn next.
