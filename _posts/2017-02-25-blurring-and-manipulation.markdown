---
layout: post
title:  "Blurring and manipulation"
date:   2017-02-24
---

Now that I've been able to load an image and play with some colors, I wanted to implement some basic image manipulation functionality: blurring. To handle out-of-bounds errors when back-projecting to the input image, I learned about image overloading, played with the [Interpolations.jl](https://github.com/tlycken/Interpolations.jl) package, and generated some really trippy mirror art.

<!--more-->

Here is my notebook, annotated with my findings and pretty pictures.

If you want, you can skip to some headers below:

* [Generating kernels](#Generating-kernels)
* [Basic blurring](#Putting-it-all-together:-blurring)
* [Interpolations.jl](#Interpolating-nearest-neighbors-with-the-Interpolations-package)
* [Mirror interpolation](#Creating-a-custom-implementation-of-mirror-interpolation)
* [Aside: broadcasting linear interpolations](#An-aside-on-broadcasting-linear-interpolations)

{% include notebook.html name='03-image-manipulation' %}

## Incorrect code

I wanted to share a wrong piece of code and the resulting image with you. I ended up going with a different structure for my final implementation, as you can see from the notebook above, but a question for you: can you find my bug?

Here is the code:

{% highlight julia %}
function getindex(im::InterpImage, xrange::UnitRange, yrange::UnitRange)
	new_xrange = [];
	if xrange.stop < size(im.img, 1)
		new_xrange = xrange;
	else
		new_xrange = vcat(
			xrange.start:(xrange.stop - size(im.img, 1)),
			size(im.img, 1):-1:1)
	end

	new_yrange = [];
	if yrange.stop < size(im.img, 2)
		new_yrange = yrange;
	else
		new_yrange = vcat(
			yrange.start:(yrange.stop - size(im.img, 2)),
			size(im.img, 2):-1:1)
	end

	return im.img[new_xrange, new_yrange];
end
{% endhighlight %}

And it produces this output:

![backwards lighthouse]({{ site.baseurl }}/assets/imgs/03-mirror-image-image.jpg)

Maybe _THIS_ one should be _Lighthouseception_.

_Hint: start and stop indices are difficult to get right_.

Any comments for me?