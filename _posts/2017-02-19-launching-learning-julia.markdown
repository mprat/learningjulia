---
layout: post
title:  "Launching Learning Julia"
date:   2017-02-19
---

I am launching this blog to document and share my experience learning the [Julia](http://julialang.org) programming language. My learning style is to learn by doing - I'm sure the things I do at first will be wrong, against code style, and inefficient. But that is the best way to learn: you try something out, realize it doesn't work, and end up learning something.

<!--more-->

My background is in computer vision and image processing, so the challenges I will set for myself will be based around images. Eventually, I hope to move on to neural networks, data science, and other machine learning. But you have to start somewhere, and start small.

This blog is powered by [Jekyll](http://jekyllrb.com), and the source code is fully open-source, hosted on my [Github account](http://github.com/mprat/learningjulia), so you can follow along in source code as well.

So let's dive right in!

# Installing Julia, using Notebooks

First I had to install Julia to my local computer. I am doing my development on an Ubuntu 16.04 system with a Kubuntu skin - if I include screenshots, they will be from this computer. And any operating-system-specific information will be about Linux.

First, I went to [the official download page](http://julialang.org/downloads/) and downloaded the 64-bit tar file of Julia 0.5.0 and untar it:

{% highlight bash %}
tar -xvf ~/Downloads/julia-0.5.0-linux-x86_64.tar.gz
{% endhighlight %}

I also added the location of the binary `julia` to my PATH, so when I run `julia` from the command line, I start the Julia REPL.

{% highlight bash %}
export PATH=$PATH:$HOME/Documents/software/julia-3c9d75391c/bin/
{% endhighlight %}

Now to install the IJulia notebooks, first start the REPL, and install the package:

{% highlight julia %}
julia> Pkg.add("IJulia")
{% endhighlight %}

The concept of adding a package and installing a package is one and the same - if your program needs a package, just add it. If you don't have this package, it will be downloaded and compiled. If you have an outdated version of the package, you will get a message that tells you exactly how to update:

{% highlight julia %}
INFO: Nothing to be done
INFO: METADATA is out-of-date — you may not have the latest version of IJulia
INFO: Use `Pkg.update()` to get the latest versions of your packages

julia> Pkg.update()
{% endhighlight %}

And once that finishes, start the IJulia notebook from the local directory:

{% highlight julia %}
julia> using IJulia();
julia> notebook(dir=".");
{% endhighlight %}

I had the problem of "authentication" with my IJulia notebooks, shown in this screenshot: 

![Token error in IJulia notebooks]({{ site.baseurl }}/assets/imgs/notebook-token.jpg)

I got the token by running `jupyter notebook list` in my terminal and copying the token into the password box.

I will do most of my learning using IJulia notebooks - I am already familiar with [Jupyter notebooks](http://jupyter.org). They are fantastic for getting immediate feedback (and plotting!) from a REPL. If and when it comes time to make a new package, I will learn how that system works as well. I will start with baby steps, and go from there.

# Posting notebooks on this blog

The source code for all the notebooks (the `.ipynb` files) are posted at the [Github repository](http://github.com/mprat/learningjulia/tree/master/_includes/notebooks/) in their original form, so you can download and look at those as well.

The awesome thing about IJulia notebooks is that you can export them into `.html` format to embed into a blog. Once finished with the notebook and ready for export, just run `nbconvert`:

{% highlight bash %}
jupyter nbconvert --execute --allow-errors \
	--output-dir=../_includes/notebooks/ \
	--to=html --template=basic.tpl NOTEBOOK_NAME.ipynb
{% endhighlight %}

This will do a few things:

1. Execute the notebook (and continue the process even if a cell contains an error)
2. Output to HTML and save to the `_includes/notebooks/` folder with no formatting (using the example code above, it will be saved to `NOTEBOOK_NAME.html`)

Next, create the post with the correct front-matter and any text outside of what the notebook HTML will generate. Lastly, simply include the notebook, like so:

{% highlight jekyll %}
include _notebooks/NOTEBOOK_NAME.html
{% endhighlight %}

## Notebook Rendering Aside

There is one annoying post-processing step (which I will eventually write a post-processor for in Jupyter, but for now am content doing it manually). when Julia renders inline SVGs, it includes an HTML line `DOCTYPE`, which does not get rendered properly by Jinja templates on the Jekyll include. So I manually delete the `DOCTYPE` line in the `NOTEBOOK_NAME.html` rendering, and the SVGs get rendered properly.

A second annoyance is that I had to create a custom [nbconvert template file](https://github.com/mprat/learningjulia/blob/master/notebooks/basic.tpl) based off of the `basic.tpl` file provided. I wanted to make sure that all the output cells in my notebook were annotated with the `Out[]` tag, and the easiest way to do that was to modify the template a little bit.

I hope you enjoy following me on my journey through Julia. I know I will enjoy sharing it with you.