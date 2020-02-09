---
layout: post
title:  "Collaborating on a Julia Project"
date:   2020-02-09
mathjax: on
widgets: false
---

For personal projects, I tend to skip around a lot and not focus on one thing, so today's post is a break from the [Trebekian.jl](https://github.com/mprat/Trebekian.jl) project from the previous post. Instead, I want to talk a little bit about how to collaborate on a Julia project with other people.

<!--more-->

* TOC
{:toc}

# Why Collaboration

Collaborating on a project is the best way to accelerate development. Different people bring different skills to the table, and with combined brains and powers, the end result becomes easier to achieve.

# Collaboration Software

There are so many blogs and resources out there about collaboration software, specifically focused on task, time, and issue management. While this is all valuable, as a home-hacker-and-tinkerer, I care more about the nuts and bolts of HOW to collaborate and less about how to divvy up tasks. If we're working on a personal project, we're doing it for fun and likely not trying to reach some lofty milestones.

For tinkering, I've settled on the following tools as critical (with helpful input from my [most frequent collaboration partner](https://blog.robindeits.com)).

* `git` for version control - most repositories are hosted on Github. If we need a private repository for some reason we will either (a) set up a private Github repo or (b) set up a private repository on Bitbucket. Gitlab is a strong contender in the space as well, but we both have active Github profiles and it's easier to manage repositories in one place than 3. To be effective at working with others I always make sure I have `git` installed on my machine in whatever environment I'm working with.
* `jupyter notebook` for scripts and tinkering - I've written about [jupyter notebooks](http://jupyter.org/) before, namely on [my first post of this blog]({% post_url 2017-02-19-launching-learning-julia %}). It's a great way to have an interactive shell that can do inline visualizations. It's the bread-and-butter of modern computer science tinkering.

# Install Jupyter Notebook and the Julia Kernel

I was recently setting up a new collaboration environment on a [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install-win10) machine, which is basically Linux, so I had to learn how to do all these steps from scratch. Because `jupyter notebook` can run multiple different kernels (i.e. Julia, Python, R, etc.) I wanted to install it globally in my workspace. On Linux (or WSL), you need to install the core, client, and notebook packages:

```
sudo apt install jupyter-core jupyter-client jupyter-notebook
```

Now from a shell you can run `jupyter notebook` and launch the notebook!

Now we need to make sure we can run a Julia kernel through `jupyter notebook`. To do this, we need to install `IJulia` through our Julia package manager.

You have 2 options for this. (a) install it globally on your Julia installation, or (b) install it per-project. I personally installed it globally for my Julia installation because I use it in every project, so it saves me pain and time. Installing `IJulia` hooks up your `jupyter` installation to a Julia kernel, which lets us actually run Julia through `jupyter notebook`.

```
[mprat@DESKTOP-RUH3B2E] [3d-jigsaw (master *=)]$ julia

               _
   _       _ _(_)_     |  Documentation: https://docs.julialang.org
  (_)     | (_) (_)    |
   _ _   _| |_  __ _   |  Type "?" for help, "]?" for Pkg help.
  | | | | | | |/ _` |  |
  | | |_| | | | (_| |  |  Version 1.3.1 (2019-12-30)  
 _/ |\__'_|_|_|\__'_|  |  Official https://julialang.org/ release
|__/                   |

julia>

(v1.3) pkg> add IJulia
Updating registry at `~/.julia/registries/General`
Updating git-repo `https://github.com/JuliaRegistries/General.git
Resolving package versions...
Updating `~/.julia/environments/v1.3/Project.toml`
[no changes]
Updating `~/.julia/environments/v1.3/Manifest.toml`
[no changes]

(v1.3) pkg>  
```

Now to actually build the kernel and have it all work, you should also build it:

```
(v1.3) pkg> build IJulia 
```

After this step is done, we can launch `jupyter notebook` from the command-line and have it use the appropriate Julia kernel.

Next up, opening our project!

# Opening A Julia Package to Tinker With

To actually start tinkering with our Julia project, we need to first clone it from whereever we're working from to have a copy of it locally.

```
git clone WHATEVER
```

Next we open `jupyter notebook` from the repo you just cloned. If we've properly set up `IJulia` and `jupyter`, it will launch a `jupyter notebook` and you can open a new or existing notebook to work on.

Next, activate the project's Julia environment from it's `Project.toml` file. From `jupyter notebook` you can do:

```
using Pkg
Pkg.activate(@__DIR__)
Pkg.resolve()
```

What this does is install all the packages from the cloned project's `Manitest.toml` into a local virtual environment of Julia packages. If you are NOT using `jupyter notebook` you can also do this from the Julia package shell:

```
(v1.3) pkg> activate .

Activating environment at `/mnt/c/Users/mprat/Documents/repos/3d-jigsaw/Project.toml`

(3d-jigsaw) pkg> resolve

Resolving package versions...
Updating `/mnt/c/Users/mprat/Documents/repos/3d-jigsaw/Project.toml`
[no changes]
Updating `/mnt/c/Users/mprat/Documents/repos/3d-jigsaw/Manifest.toml`
[no changes]

(3d-jigsaw) pkg>  
```

# Tinker!

Now the environment is all set up to tinker! Yay =D
