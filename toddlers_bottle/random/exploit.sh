#!/bin/bash
i=0
COMMAND=$(echo $i | ./random)
OUTPUT_STRING="Wrong, maybe you should try 2^32 cases."
OUTPUT_TEST="Wrong, maybe you should try 2^32 cases."
while [ "$OUTPUT_STRING" == "$OUTPUT_TEST" ];
do
	OUTPUT_STRING=$COMMAND
	echo $OUTPUT_STRING 
	echo "attempting $i:"
	i=$((i+1))
done


