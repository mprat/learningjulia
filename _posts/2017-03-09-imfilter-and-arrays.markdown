---
layout: post
title:  "imfilter and arrays"
date:   2017-03-09
mathjax: true
---

Whereas in [my last post]({% post_url 2017-02-25-blurring-and-manipulation %}) I manually wrote a blur kernel and code to convolve an image, I didn't want to do that every time an image convolution came up. So in this post I learned about the `imfilter` function from the [ImageFiltering.jl](https://github.com/JuliaImages/ImageFiltering.jl) package. I also learned about the `@time` macro and had a small aside on array creation.

<!--more-->

I've included my notebook here. You can see the original [on Github](https://github.com/mprat/learningjulia/blob/master/notebooks/04-imfilter.ipynb) if you like.

If you want, you can skip to some headers below:

* [Setup](#Setup)
* [Sobel kernels](#Sobel-kernels)
* [The `imfilter` functions](#The-imfilter-function)
* [Sobel kernel to edge map](#Sobel-to-edges)
* [Separable kernels](#Separable-kernels)
* [Factoring kernels](#Factoring-Kernels)
* [No Opencv...](#The-notable-lack-of-OpenCV)
* [Timings](#Timings)
* [Wrapping up with gradients](#Wrapping-up-with-gradients)
* [An aside on array notation](#An-aside-on-array-notation)

{% include notebook.html name='04-imfilter' %}

## Final thoughts

I suspect there will be a lot from [the ImageFiltering.jl package](https://github.com/JuliaImages/ImageFiltering.jl) in my future... it implements nice things like smart image padding, kernel factorization, and smart filtering. And the package author is active on Github, answering questions and closing issues as needed.

Thank you for reading, as usual! I would love to hear from you if you have any suggestions, comments, or ideas for what I should learn next.
