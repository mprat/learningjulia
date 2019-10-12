---
layout: post
title:  "A Basic RNN"
date:   2019-10-11
mathjax: on
widgets: false
---

In the epic adventure of audio processing and neural networks with Julia, the theme of today is RNNs! I'll walk through how I built my first basic RNN in Julia with [Flux.jl](https://github.com/FluxML/Flux.jl). This is all in pursuit of the Trebekian project.

<!--more-->

* TOC
{:toc}

# The Project

As I described in [my previous post]({% post_url 2019-10-09-julia-1.2 %}), the project I am working on is called Trebekian, where I want to augment my partner's [CLI trivia app](https://github.com/rdeits/Trivia.jl) by having the voice of Alex Trebek read the questions out loud. Thus, [Trebekian.jl](https://github.com/mprat/Trebekian.jl) was born.

# Flux and a Basic RNN

Today, I learned how to use Flux (the all-Julia neural network package) to train an RNN that has a very simple task: provide the sum of all elements in the provided array.

## RNNs: An Aside

What is an RNN? It stands for a "recurrent neural network" - basically, an RNN is a fully-connected or dense unit that has state. When fed a sequence of inputs, it does a linear operation ($$\text{output} = W \cdot \text{input} + b$$), but then feeds the output as an input into the next input. So the output at time step $$t + 1$$ are a function of the inputs, the weights and biases, and the output at time $$t$$.

The classic RNN unit is typically diagrammed like this:

![RNN]({{ site.baseurl }}/assets/imgs/RNN.svg)

Where the function $$W$$ can really be anything! In the case of a classic "RNN" people usually mean a linear unit like $$Wx + b$$ with some kind of activation function.

There is, of course, a whole field of research devoted to studying RNNs and their theory and application, but for the purposes of this project, we aren't going to go too far down the rabbit hole (yet). Suffice it to say that the basic "recurrent" structure of an RNN can take many forms. If you're looking for more reading material, take a look at LSTMs (which are used for sequence-to-sequence models in computer vision) and GRUs (which are used heavily in audio processing). There are many many others, and I encourage you to do some of your own research to learn more.

## Why RNNs

For Trebekian, we want to use an RNN because the goal is to take a sequence of data (i.e. a sentence) and turn it into another sequence (i.e. audio). To do this, we know we will need some kind of "hidden state" that is offered by a recurrent model. It's going to be fun to figure out exactly what will work for this application, but I know for sure it will be a recurrent model!

# RNNs in Julia

As always, to learn more about this topic, I start with a simple example that I know can be solved by an RNN. The test case we will work with is formulated quite simply: given a variable-length input array, calculate the sum of the inputs. This is really easy to test, easy to generate training data for, and is a REALLY simple linear function that can be expressed by a linear unit. So, we start with all the machinery!

## Generate Data

First we want to generate some sample train and test data. In Julia this is pretty straightforward to do:

{% highlight julia %}
function generate_data(num_samples)
  train_data = [rand(1.0:10.0, rand(2:7)) for i in 1:num_samples]
  train_labels = (v -> sum(v)).(train_data)

  test_data = 2 .* train_data
  test_labels = 2 .* train_labels

  train_data, train_labels, test_data, test_labels
end
{% endhighlight %}

We take some shortcuts by generating only random small arrays that contain the values 1 to 10, and of variable lengths from 2 to 7. Since the task we're trying to learn is fairly simple, we take it! For the test data we just take what we already generated and multiply both the training vectors and the training outputs by 2 - we know it will still work! To also keep it simple we generate the same amount of training and testing data - normally this won't be the case, but in this situation where data is easy to come by, we take it!

The syntax `(v -> sum(v)).(train_data)` uses an anonymous function (`(v -> sum(v))`) and the dot operator to apply that summation function to each of the arrays in our training data.

## Create The Model

Next, we want to actually create our model. This is part of the "magic" of machine learning, since you have to formulate your model correctly or you will get non-sensical data. With [Flux](https://github.com/FluxML/Flux.jl) we certainly have enough functions to get us started, so the model I chose to start with is this one:

{% highlight julia %}
using Flux

simple_rnn = Flux.RNN(1, 1, (x -> x))
{% endhighlight %}

What this does is create a single linear RNN unit taking one element at a time and producing one element for each input. We want one-input-to-one-output because we want to make an accumulator - for each input, the output should contain the sum of it and all previous inputs.

The model feeds the output back to itself with (in this case) no activation function applied to the output (before it is fed back to itself). The default activation function is a `tanh` function in Flux, but that clips the output to between -1 and 1, which is not good if you're trying to make a summation RNN! So instead, we provide the RNN unit from Flux an anonymous function as an activation that does nothing to the input - it just passes the output directly forward to the next unit. This is pretty atypical of neural network design, but the good part here is that we know something about our problem - we know that we want a summation machine, so we know it would be pretty easy to learn without any complicated activation functions, and in fact, impossible with the default one! Later down in this post I'll show you what happens if you try to train this with the default `tanh` activation function...

There's a whole theory of activation functions that I won't get into here. That's one of those rabbit holes we might dive into further into the journey of Trebekian, but not at this point!

Now to actually evaluate the model on a sequence of inputs, you have to call it like this:

{% highlight julia %}
julia> simple_rnn.([1, 2, 3])
{% endhighlight %}

Notice the dot notation here - since our RNN only takes one input at a time, we need to apply the RNN on the sequence of inputs we provide one at a time. Then, if we take the last element of the output (after it has seen the entire sequence) we expect to see the sum of all the inputs.

## Train! and Evaluate

Now that we've defined our model we set up the training and evaluation. This is probably the least code I've ever used to set up a training and evaluation in any language I've done neural networks with...

{% highlight julia %}
using Flux: @epochs

num_samples = 1000
num_epochs = 50

# generate our test data with the data generation function from above
train_data, train_labels, test_data, test_labels = generate_data(num_samples)
simple_rnn = Flux.RNN(1, 1, (x -> x))

function eval_model(x)
  out = simple_rnn.(x)[end]
  Flux.reset!(simple_rnn)
  out
end

loss(x, y) = abs(sum((eval_model(x) .- y)))

ps = Flux.params(simple_rnn)

# use the ADAM optimizer. It's a pretty good one!
opt = Flux.ADAM()

println("Training loss before = ", sum(loss.(train_data, train_labels)))
println("Test loss before = ", sum(loss.(test_data, test_labels)))

# callback function during training
evalcb() = @show(sum(loss.(test_data, test_labels)))

@epochs num_epochs Flux.train!(loss, ps, zip(train_data, train_labels), opt, cb = Flux.throttle(evalcb, 1))

# after training, evaluate the loss
println("Test loss after = ", sum(loss.(test_data, test_labels)))
{% endhighlight %}

Now, the only weirdness is this bit:

```
function eval_model(x)
  out = simple_rnn.(x)[end]
  Flux.reset!(simple_rnn)
  out
end
```

There are 2 important things to note:

1. When you call an RNN on an input sequence, it will produce an output for each input (because it has to feed it back to itself). So if you want to make a "many to one" more, or a model where you generate a single output for a variable-length input, you have to take the last element (in Julia, with the `[end]` syntax) to use as your output. And we again use the dot notation to apply the model, like we discussed above.
2. You have to call `Flux.reset!(simple_rnn)` after every forward pass / evaluation call. Because an RNN has hidden state, you want to make sure that you don't pollute any future calls to the RNN with this hidden state. See this [Flux documentation page](https://fluxml.ai/Flux.jl/stable/models/recurrence/#Truncating-Gradients-1) for more information.

During training we use an evaluation callback (throttled at max 1 / second) to display the output.

The loss function I chose for this implementation was a simple absolute value difference loss to keep it simple. Much like activation functions, there is a whole theory of loss functions and it really depends on your problem for which one is most appropriate. In our simple case, we keep it simple!

Putting it all together, here is what the output looks like after we run that code snippet in the Julia shell:

```
Training loss before = 55217.345537789966 (tracked)
Test loss before = 94049.80539624124 (tracked)
[ Info: Epoch 1
sum(loss.(test_data, test_labels)) = 93804.66858509867 (tracked)
[ Info: Epoch 2
sum(loss.(test_data, test_labels)) = 12159.511678479557 (tracked)
[ Info: Epoch 3
sum(loss.(test_data, test_labels)) = 8576.120354854142 (tracked)
[ Info: Epoch 4
sum(loss.(test_data, test_labels)) = 5690.999849859255 (tracked)
[ Info: Epoch 5
sum(loss.(test_data, test_labels)) = 3116.2798290993724 (tracked)
[ Info: Epoch 6
sum(loss.(test_data, test_labels)) = 1236.2371627322057 (tracked)
[ Info: Epoch 7
sum(loss.(test_data, test_labels)) = 647.9433550823187 (tracked)
[ Info: Epoch 8
sum(loss.(test_data, test_labels)) = 560.9731228928553 (tracked)
[ Info: Epoch 9
sum(loss.(test_data, test_labels)) = 329.70988278656426 (tracked)
[ Info: Epoch 10
sum(loss.(test_data, test_labels)) = 414.3748623363597 (tracked)
[ Info: Epoch 11
sum(loss.(test_data, test_labels)) = 272.77977394696893 (tracked)
[ Info: Epoch 12
sum(loss.(test_data, test_labels)) = 328.3123554838486 (tracked)
[ Info: Epoch 13
sum(loss.(test_data, test_labels)) = 242.4203668107719 (tracked)
[ Info: Epoch 14
sum(loss.(test_data, test_labels)) = 218.60153886368636 (tracked)
[ Info: Epoch 15
sum(loss.(test_data, test_labels)) = 253.86385772098487 (tracked)
[ Info: Epoch 16
sum(loss.(test_data, test_labels)) = 122.21473555253418 (tracked)
[ Info: Epoch 17
sum(loss.(test_data, test_labels)) = 112.17151257920302 (tracked)
[ Info: Epoch 18
sum(loss.(test_data, test_labels)) = 59.315820365915805 (tracked)
[ Info: Epoch 19
sum(loss.(test_data, test_labels)) = 80.86340671284957 (tracked)
[ Info: Epoch 20
sum(loss.(test_data, test_labels)) = 56.31063887725306 (tracked)
[ Info: Epoch 21
sum(loss.(test_data, test_labels)) = 76.6685032420411 (tracked)
[ Info: Epoch 22
sum(loss.(test_data, test_labels)) = 31.083147771133483 (tracked)
[ Info: Epoch 23
sum(loss.(test_data, test_labels)) = 16.74637425520851 (tracked)
[ Info: Epoch 24
sum(loss.(test_data, test_labels)) = 77.01847954680784 (tracked)
[ Info: Epoch 25
sum(loss.(test_data, test_labels)) = 15.370755358095774 (tracked)
[ Info: Epoch 26
sum(loss.(test_data, test_labels)) = 130.08021926044637 (tracked)
[ Info: Epoch 27
sum(loss.(test_data, test_labels)) = 128.75033937485176 (tracked)
[ Info: Epoch 28
sum(loss.(test_data, test_labels)) = 91.12742710739198 (tracked)
[ Info: Epoch 29
sum(loss.(test_data, test_labels)) = 89.87023473923429 (tracked)
[ Info: Epoch 30
sum(loss.(test_data, test_labels)) = 158.50912426059236 (tracked)
[ Info: Epoch 31
sum(loss.(test_data, test_labels)) = 29.45693041628419 (tracked)
[ Info: Epoch 32
sum(loss.(test_data, test_labels)) = 105.69801396269521 (tracked)
[ Info: Epoch 33
sum(loss.(test_data, test_labels)) = 172.5401606984177 (tracked)
[ Info: Epoch 34
sum(loss.(test_data, test_labels)) = 12.815772419050736 (tracked)
[ Info: Epoch 35
sum(loss.(test_data, test_labels)) = 25.23781677126996 (tracked)
[ Info: Epoch 36
sum(loss.(test_data, test_labels)) = 30.23609685178663 (tracked)
[ Info: Epoch 37
sum(loss.(test_data, test_labels)) = 25.49028534974471 (tracked)
[ Info: Epoch 38
sum(loss.(test_data, test_labels)) = 68.95778844912086 (tracked)
[ Info: Epoch 39
sum(loss.(test_data, test_labels)) = 117.24532600063654 (tracked)
[ Info: Epoch 40
sum(loss.(test_data, test_labels)) = 23.103795825171595 (tracked)
[ Info: Epoch 41
sum(loss.(test_data, test_labels)) = 132.91250068756722 (tracked)
[ Info: Epoch 42
sum(loss.(test_data, test_labels)) = 28.780922677236568 (tracked)
[ Info: Epoch 43
sum(loss.(test_data, test_labels)) = 25.806662467489737 (tracked)
[ Info: Epoch 44
sum(loss.(test_data, test_labels)) = 105.77374438451754 (tracked)
[ Info: Epoch 45
sum(loss.(test_data, test_labels)) = 14.471225800954223 (tracked)
[ Info: Epoch 46
sum(loss.(test_data, test_labels)) = 67.57839085268583 (tracked)
[ Info: Epoch 47
sum(loss.(test_data, test_labels)) = 14.271042475914427 (tracked)
[ Info: Epoch 48
sum(loss.(test_data, test_labels)) = 20.822220602624686 (tracked)
[ Info: Epoch 49
sum(loss.(test_data, test_labels)) = 35.281069472306996 (tracked)
[ Info: Epoch 50
sum(loss.(test_data, test_labels)) = 46.27433474390857 (tracked)
Test loss after = 44.424693127695676 (tracked)
```

And when we test the model on some inputs, here's what we get. It's amazing how we made an adder RNN that can operate on negative numbers, even when there are no negative numbers in our dataset!

{% highlight julia %}
julia> eval_model([1, 2, 3])
Tracked 1×1 Array{Float32,2}:
 6.0188646f0

julia> eval_model([1, -2, 30])
Tracked 1×1 Array{Float32,2}:
 29.037376f0

julia> eval_model([1, 0, 30])
Tracked 1×1 Array{Float32,2}:
 31.038675f0

julia> eval_model([1, 1, 1])
Tracked 1×1 Array{Float32,2}:
 3.0166523f
{% endhighlight %}

# Incorrect Models

Above, I alluded to model selection as being an important part of machine learning. I am constantly reminded of this in my day job (I do computer vision, software, machine learning, data analysis for robotics) and was reminded of it again here. Before I looked at the Flux definition of an RNN, I didn't realize that the default activation function was `tanh`, which clips the function to the range `[-1, 1]`. Running the same training / evaluation code above but with this model:

{% highlight julia %}
simple_rnn = Flux.RNN(1, 1)
{% endhighlight %}

Yielded some fantastically poor results:

```
Training loss before = 25779.026819202103 (tracked)
Test loss before = 50528.06475943625 (tracked)
[ Info: Epoch 1
sum(loss.(test_data, test_labels)) = 50520.94230701844 (tracked)
[ Info: Epoch 2
sum(loss.(test_data, test_labels)) = 48654.89364155943 (tracked)
[ Info: Epoch 3
sum(loss.(test_data, test_labels)) = 48647.24435190139 (tracked)
[ Info: Epoch 4
sum(loss.(test_data, test_labels)) = 48644.77063770764 (tracked)
[ Info: Epoch 5
sum(loss.(test_data, test_labels)) = 48643.60112418384 (tracked)
[ Info: Epoch 6
sum(loss.(test_data, test_labels)) = 48642.96202919946 (tracked)
[ Info: Epoch 7
sum(loss.(test_data, test_labels)) = 48642.5878624949 (tracked)
[ Info: Epoch 8
sum(loss.(test_data, test_labels)) = 48642.36151888183 (tracked)
[ Info: Epoch 9
sum(loss.(test_data, test_labels)) = 48642.222615282604 (tracked)
[ Info: Epoch 10
sum(loss.(test_data, test_labels)) = 48642.13694385092 (tracked)
[ Info: Epoch 11
sum(loss.(test_data, test_labels)) = 48642.084075882245 (tracked)
[ Info: Epoch 12
sum(loss.(test_data, test_labels)) = 48642.0515033255 (tracked)
[ Info: Epoch 13
sum(loss.(test_data, test_labels)) = 48642.03148004183 (tracked)
[ Info: Epoch 14
sum(loss.(test_data, test_labels)) = 48642.019201353156 (tracked)
[ Info: Epoch 15
sum(loss.(test_data, test_labels)) = 48642.01168961853 (tracked)
[ Info: Epoch 16
sum(loss.(test_data, test_labels)) = 48642.0071039518 (tracked)
[ Info: Epoch 17
sum(loss.(test_data, test_labels)) = 48642.00431001056 (tracked)
[ Info: Epoch 18
sum(loss.(test_data, test_labels)) = 48642.00261078987 (tracked)
[ Info: Epoch 19
sum(loss.(test_data, test_labels)) = 48642.001579098454 (tracked)
[ Info: Epoch 20
sum(loss.(test_data, test_labels)) = 48642.00095367056 (tracked)
[ Info: Epoch 21
sum(loss.(test_data, test_labels)) = 48642.00057510369 (tracked)
[ Info: Epoch 22
sum(loss.(test_data, test_labels)) = 48642.0003463085 (tracked)
[ Info: Epoch 23
sum(loss.(test_data, test_labels)) = 48642.00020822942 (tracked)
[ Info: Epoch 24
sum(loss.(test_data, test_labels)) = 48642.00012501622 (tracked)
[ Info: Epoch 25
sum(loss.(test_data, test_labels)) = 48642.00007494745 (tracked)
[ Info: Epoch 26
sum(loss.(test_data, test_labels)) = 48642.000044863176 (tracked)
[ Info: Epoch 27
sum(loss.(test_data, test_labels)) = 48642.00002681499 (tracked)
[ Info: Epoch 28
sum(loss.(test_data, test_labels)) = 48642.000016004866 (tracked)
[ Info: Epoch 29
sum(loss.(test_data, test_labels)) = 48642.000009539996 (tracked)
[ Info: Epoch 30
sum(loss.(test_data, test_labels)) = 48642.00000567951 (tracked)
[ Info: Epoch 31
sum(loss.(test_data, test_labels)) = 48642.00000337845 (tracked)
[ Info: Epoch 32
sum(loss.(test_data, test_labels)) = 48642.0000020087 (tracked)
[ Info: Epoch 33
sum(loss.(test_data, test_labels)) = 48642.00000119481 (tracked)
[ Info: Epoch 34
sum(loss.(test_data, test_labels)) = 48642.00000071163 (tracked)
[ Info: Epoch 35
sum(loss.(test_data, test_labels)) = 48642.000000425585 (tracked)
[ Info: Epoch 36
sum(loss.(test_data, test_labels)) = 48642.000000256 (tracked)
[ Info: Epoch 37
sum(loss.(test_data, test_labels)) = 48642.00000015527 (tracked)
[ Info: Epoch 38
sum(loss.(test_data, test_labels)) = 48642.00000009584 (tracked)
[ Info: Epoch 39
sum(loss.(test_data, test_labels)) = 48642.00000006016 (tracked)
[ Info: Epoch 40
sum(loss.(test_data, test_labels)) = 48642.00000003875 (tracked)
[ Info: Epoch 41
sum(loss.(test_data, test_labels)) = 48642.000000025655 (tracked)
[ Info: Epoch 42
sum(loss.(test_data, test_labels)) = 48642.0000000178 (tracked)
[ Info: Epoch 43
sum(loss.(test_data, test_labels)) = 48642.00000001263 (tracked)
[ Info: Epoch 44
sum(loss.(test_data, test_labels)) = 48642.00000000949 (tracked)
[ Info: Epoch 45
sum(loss.(test_data, test_labels)) = 48642.000000007145 (tracked)
[ Info: Epoch 46
sum(loss.(test_data, test_labels)) = 48642.00000000572 (tracked)
[ Info: Epoch 47
sum(loss.(test_data, test_labels)) = 48642.00000000478 (tracked)
[ Info: Epoch 48
sum(loss.(test_data, test_labels)) = 48642.00000000396 (tracked)
[ Info: Epoch 49
sum(loss.(test_data, test_labels)) = 48642.000000003405 (tracked)
[ Info: Epoch 50
sum(loss.(test_data, test_labels)) = 48642.000000002816 (tracked)
Test loss after = 48642.000000002576 (tracked)
```

Note how the loss was not going down. If we evaluate the model we just trained on the entire test dataset, you see that everything has the max value it can possibly have - 1:

```
julia> eval_model.(test_data)
1000-element Array{TrackedArray{…,Array{Float64,2}},1}:
 [1.0] (tracked)               
 [0.9999999999733875] (tracked)
 [1.0] (tracked)               
 [1.0] (tracked)               
 [1.0] (tracked)               
 [1.0] (tracked)               
 [1.0] (tracked)               
 [1.0] (tracked)               
 [1.0] (tracked)               
 [0.999999999999973] (tracked) 
 [1.0] (tracked)               
 [1.0] (tracked)               
 [1.0] (tracked)               
 [1.0] (tracked)               
 [1.0] (tracked)               
 [1.0] (tracked)               
 [1.0] (tracked)               
 [0.9999999999733875] (tracked)
 [1.0] (tracked)               
 [1.0] (tracked)               
 ⋮                             
 [1.0] (tracked)               
 [1.0] (tracked)               
 [1.0] (tracked)               
 [1.0] (tracked)               
 [0.9999999999733875] (tracked)
 [0.9999999999733875] (tracked)
 [1.0] (tracked)               
 [0.999999999999973] (tracked) 
 [1.0] (tracked)               
 [1.0] (tracked)               
 [1.0] (tracked)               
 [1.0] (tracked)               
 [1.0] (tracked)               
 [1.0] (tracked)               
 [0.9999999999733875] (tracked)
 [1.0] (tracked)               
 [1.0] (tracked)               
 [1.0] (tracked)               
 [1.0] (tracked)
```

This clue led me to dive into the Flux RNN implementation to figure out how to supply a custom (in this case no) activation function.

# The Code

If you want to see the code, check out my implementation of a Basic RNN in the Trebekian repository: https://github.com/mprat/Trebekian.jl/blob/0cdcd33880dd3fc9cc49f3a143f212968f918d91/BasicRNN.jl

Happy Julia-ing!
