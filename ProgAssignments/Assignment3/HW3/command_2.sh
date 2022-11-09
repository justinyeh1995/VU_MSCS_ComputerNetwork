h2 python3 router.py &> r2.log &
h3 python3 router.py &> r3.log &
h4 python3 router.py &> r4.log &
h5 python3 grocery_server.py &> grocery.log &
h6 python3 health_server.py &> health.log &
h1 python3 refrigerator.py -g 10.0.0.5 -s 10.0.0.6 -i 10 #0 | grep "Total" | awk '{print $NF}' > client1_single.csv 
