### How to run Hw3

#### Choose A Protocol

In the `config.in` file,

pick your idea protocol under the field `TCP`

```sh
PROTOCOL=ABP
```
or
```sh
PROTOCOL=GBN
```
or
```sh
PROTOCOL=SR
```


#### Single

```sh=
bash hw3_1_topo.sh
```

in the mininet cli

```sh=
source command_12.sh 
```
---
#### Linear

```sh=
bash hw3_2_topo.sh
```

in the mininet cli

```sh=
source command_12.sh 
```
---
 
## Tree

```sh=
bash hw3_3_topo.sh
```

in the mininet cli

```sh=
source command_3.sh
``` 
---

#### Router

One can close the router using ROUTER=FALSE under the field `TCP`

[Algorithm Ref](https://web.eecs.umich.edu/~sugih/courses/eecs489/lectures/26-FlowControl+ARQ.pdf)
