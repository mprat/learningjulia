---
layout: post
title:  "Image tilings and arrays"
date:   2017-02-22 20:00:04 -0500
---

In this notebook I decided to get more familiar with Julia basic functions, arrays, and operations by giving myself a small computational photography challenge! And on a suggestion, I played with the [Interact.jl](https://github.com/JuliaGizmos/Interact.jl) package too.

<!--more-->

I've included the notebook I used for my image tiling manipulation, ending with playing with the [Interact.jl](https://github.com/JuliaGizmos/Interact.jl) library.

# My notebook

{% include notebook.html name='02-image-tiling-and-colors' %}

The widget in the last output of the notebook did not render properly, so I'm including a screenshot here:

![Interact.jl widget]({{ site.baseurl }}/assets/imgs/02-widget.jpg)

# Random memory initialization

In line 4 (`In[4]:`), an uninitialized array takes random memory and random values. I don't fully understand where this memory comes from, but I'm pretty sure it has to do with most-recently accessed memory. When I was running on my local machine, line 2 (`In[2]:`) loaded the original image of the lighthouse we saw in [my first post]({% post_url 2017-02-20-getting-started-with-images %}). So when line 4 (creating a random uninitialized array) was executed, I got this pretty lighthouse artifact! You can see it is different image than came up in the second run of the notebook rendered above!

![Random memory initialization]({{ site.baseurl }}/assets/imgs/02-random-memory.jpg)

# Jupyter notebook rendering aside

As another aside, in rendering the Jupyter notebook, the Interact library created widgets that generated custom Javascript during the `nbconvert` phase. I just removed that entire script section from the generated HTML, which is why I had to include a screenshot of the final widget at the end. I'm sorry for that ugliness - Jupyter and nbconvert are fantastic projects, they just can't possibly cover all use cases!

Any comments for me?