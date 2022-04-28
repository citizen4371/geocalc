# geocalc - HTTP service for geometric calculations

Currently only calculates intersection over union of two bounding boxes.

## Requirements

- Python 3.7+

- pip

- git

- setuptools (optional)

## Installation

First, clone this repository.

<div class="termy">
  
```console
$ git clone git@github.com:citizen4371/geocalc.git
$ cd geocalc
```

</div>

Service can be started as a python module:
<div class="termy">

```console
$ python -m geocalc
```

</div>

You can check that it's working it by visiting http://localhost:8000/

### Docker

Dockerfile is provided as well, you can build docker image:

<div class="termy">

```console
$ docker build -t geocalc .
```

</div>

Then start the container:

<div class="termy">

```console
$ docker run -d --name geocalc -p 8000:8000 geocalc
```

</div>

## Usage

When the service is running, swagger api documentation is available at `/docs` endpoint.</br></br>

The only  calculation endpoint currently available is `/calculations/iou` which performs intersection over union.</br>
Coordinates of the two boxes should be passed to it as query params (2 lists of 4 float values): </br>
`?box1=[top-left x]&box1=[top-left y]&box1=[bottom-right x]&box1=[bottom-right y]&box2=[top-left x]&box2=[top-left y]&box2=[bottom-right x]&box2=[bottom-right y]`</br></br>
Convention for positive x-axis direction is left to right, y-axis - bottom to top.
