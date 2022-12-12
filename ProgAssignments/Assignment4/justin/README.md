1. Deploy the delay you like by referencing the json-liked object 

```jsonld=
{
"C": 
  {"R1":"10.0.10.239" eth1, 
   "R2":"10.0.11.214" eth2, 
   "R3":"10.0.12.247" eth3},
"R1": 
  {"R2":"10.0.16.165" eth3,
   "R4":"10.0.13.171" eth2,
   "C":"10.0.10.235"},
"R2": 
  {"S": "10.0.15.82",  eth2
   "R3":"10.0.17.234", eth4
   "R1":"10.0.16.161", eth3
   "C":"10.0.11.208"},
"R3": {"R5":"10.0.14.30" eth2,"R2":"10.0.17.232", "C":"10.0.12.242"},
"R4": {"S":"10.0.18.17" eth2, "R1":"10.0.13.168"},
"R5": {"S":"10.0.19.80" eth1, "R3":"10.0.14.27"},
"S": {"R4":"10.0.18.14", "R5":"10.0.19.78", "R2":"10.0.15.84"}
}
```

2. add delay to the container on each or specific service(s)
```sh=
docker exec -it <justinContainer> tc qdisc change dev eth<the network you want> root netem delay 100ms
```

3. At cc@master, RUN
```sh=
cd justin/
python3 controller.py
```

4. At every hop on the path, go to the specific nodes & RUN
```sh=
docker cp justin/route.js <justinContainer>:NWClass_Justin
docker exec -it <justinContainer> /bin/bash
```

```jsonld=
{
"C": "worker10",
"S": "worker9",
"R1": "worker1",
"R2": "worker2",
"R3": "worker3",
"R4": "worker4",
"R5": "worker5"
}
```

5. In each container, start running client/router/server
```sh=
python3 client.py -i 10 
# or
python3 router.py
# or
python3 server.py
```

6. collect latency data at client side

