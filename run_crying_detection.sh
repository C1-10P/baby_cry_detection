
function clean_up {
        rm recording/signal_9s_1.wav
        rm recording/signal_9s_2.wav
        rm prediction/prediction1.txt
        rm prediction/prediction2.txt
	# Perform program exit housekeeping
	echo "Good Bye."
	stop_playing
	exit
}

trap clean_up SIGHUP SIGINT SIGTERM

function recording1(){
	echo "Start Recording 1 ..."
	arecord -q -D pulse -d 9 -f S16_LE -c1 -r44100 -t wav recording/signal_9s_1.wav
}

function recording2(){
        echo "Start Recording 2 ..."
        arecord -q -D pulse -d 9 -f S16_LE -c1 -r44100 -t wav recording/signal_9s_2.wav
}


function predict1() {
	python2.7 pc_main/make_prediction.py -q --recording=recording/signal_9s_1.wav --prediction=prediction/prediction1.txt
}

function predict2() {
        python2.7 pc_main/make_prediction.py -q --recording=recording/signal_9s_2.wav --prediction=prediction/prediction2.txt
}


function start_playing() {
	if [[ $PLAYING == 0 ]]; then
		echo "start playing"
                aplay -D plughw:0,0 /opt/baby_cry/lullaby/lullaby_classic.wav
		PLAYING=1
	fi
}

function stop_playing(){
	if [[ $PLAYING == 1 ]]; then
		echo "stop playing"
		PLAYING=0
	fi
}

echo "Welcome to Parenting 2.0"
echo ""
while true; do
        echo "Prediction: $(cat prediction/prediction1.txt)"
	recording1
	predict1 &
        echo "Prediction: $(cat prediction/prediction2.txt)"
        recording2
        predict2 & 

#	if [[ $PREDICTION == 0 ]]; then
#		stop_playing
#	else
#		CPT=$(expr $CPT + 1)
#		start_playing
#	fi
done
clean_up
