
SEARCH_STRING="301 - Crying baby"

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

PLAYING=0
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

function analyse_prediction1()
{

if [ -f prediction/prediction1.txt ]; then
 echo "Prediction: $(cat prediction/prediction1.txt)"
 if [[ $(cat prediction/prediction1.txt) == *"$SEARCH_STRING"* ]]; 
then
   start_playing
   return
 fi
fi

stop_playing

}

function analyse_prediction2()
{

if [ -f prediction/prediction2.txt ]; then
 echo "Prediction: $(cat prediction/prediction2.txt)"
 if [[ $(cat prediction/prediction2.txt) == *"$SEARCH_STRING"* ]]; 
then
   start_playing
   return
 fi
fi

stop_playing


}



echo "Welcome to Parenting 2.0"
echo ""
while true; do
        analyse_prediction1
	recording1
	predict1 &
        analyse_prediction2
        recording2
        predict2 & 

done
clean_up
