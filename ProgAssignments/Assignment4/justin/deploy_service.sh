#!/bin/bash
IMAGE=192.168.2.61:5000/nwclass_justin
#IMAGE=192.168.2.61:5000/nwclass

## rm old services
docker service rm justin_client
docker service rm justin_server
for ((i=1; i<=5; i++))
do 
  docker service rm justin_router${i}
done

## client
docker service create --name justin_client --cap-add NET_ADMIN --constraint node.hostname==compnw-worker10 --network overlay_nw1 --publish published=30020,target=4444  ${IMAGE}

docker service update --network-add overlay_nw2 justin_client
docker service update --network-add overlay_nw3 justin_client

## Router1
docker service create --name justin_router1 --cap-add NET_ADMIN --constraint node.hostname==compnw-worker1 --network overlay_nw1 --publish published=31050,target=4444  ${IMAGE}

docker service update --network-add overlay_nw4 justin_router1
docker service update --network-add overlay_nw7 justin_router1

## Router2
docker service create --name justin_router2 --cap-add NET_ADMIN --constraint node.hostname==compnw-worker2 --network overlay_nw2 --publish published=31051,target=4444  ${IMAGE}

docker service update --network-add overlay_nw6 justin_router2
docker service update --network-add overlay_nw7 justin_router2
docker service update --network-add overlay_nw8 justin_router2

## Router3
docker service create --name justin_router3 --cap-add NET_ADMIN --constraint node.hostname==compnw-worker3 --network overlay_nw3 --publish published=31052,target=4444  ${IMAGE}

docker service update --network-add overlay_nw5 justin_router3
docker service update --network-add overlay_nw8 justin_router3

## Router4
docker service create --name justin_router4 --cap-add NET_ADMIN --constraint node.hostname==compnw-worker4 --network overlay_nw4 --publish published=31053,target=4444  ${IMAGE}

docker service update --network-add overlay_nw9 justin_router4

## Router5
docker service create --name justin_router5 --cap-add NET_ADMIN --constraint node.hostname==compnw-worker5 --network overlay_nw5 --publish published=31054,target=4444  ${IMAGE}

docker service update --network-add overlay_nw10 justin_router5

## Server
docker service create --name justin_server --cap-add NET_ADMIN --constraint node.hostname==compnw-worker9 --network overlay_nw6 --publish published=30021,target=5555  ${IMAGE}
docker service update --network-add overlay_nw9 justin_server
docker service update --network-add overlay_nw10 justin_server
