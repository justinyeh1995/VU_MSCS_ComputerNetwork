for num in 1 2 3
do
	for loss in noloss loss
		do
			for switch in single linear tree
				do	
				  echo client${num}_${switch}_$loss
				done
		done
done
