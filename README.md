# Polymede

A simple query language for JSON documents.

## Installation

````
pip install polymede
````

You can then start polymede from the console:

````
polymede [OPTIONS] [QUERY]
````


## Examples

mydata.json

```` json
{
  "items": [{
    "foo": "bar"
  },
  {
    "bar": "baz"
  },
  {
    "bar": "boom"
  },
  {
    "bam": 12
  }]
}
````

Querying data:

```` shell
> load "mydata.json"

# Result:
true


> find "items.*"

# Result:
[
  {
    "foo": "bar"
  },
  {
    "bar": "baz"
  },
  {
    "bar": "boom"
  },
  {
    "bam": 12
  }
]


> find "items.(1-2)"

# Result:
[
  {
    "bar": "baz"
  },
  {
    "bar": "boom"
  },
]


> find "items.*" where "bar" = "boom"

# Result:
[
  {
    "bar": "boom"
  },
]


> count "items.*"

# Result:
4
````
