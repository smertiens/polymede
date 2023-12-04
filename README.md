# Polymede

Status: pre-alpha, work in progress

A simple command-line tool to query data from JSON files.

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
{ "items": [
  { "foo": "bar" },
  { "bar": "baz" },
  { "bar": "boom" },
  { "bam": 12 }
]}
````

Querying data:

```` shell
> load "mydata.json"
# Result:
true

> find "items.*"
# Result:
[ { "foo": "bar" }, { "bar": "baz" }, { "bar": "boom" }, { "bam": 12 } ]

> find "items.(1-2)"
# Result:
[ { "bar": "baz" }, { "bar": "boom" } ]

> find "items.*" where "bar" = "boom"
# Result:
[ { "bar": "boom" } ]

> count "items.*"
# Result:
4
````


## Documentation

### Path Syntax



### Load Syntax

````
load "FILENAME" [as "FORMAT"]
````

### Find Syntax

````
find [(field1, field2, ...)] "pathstring" [WHERE "pathstring" OPERATOR value]
````

### Count Syntax

````
count [(field1, field2, ...)] "pathstring" [WHERE "pathstring" OPERATOR value]
````

