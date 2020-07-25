NetAddr.localAddr    // retrieve the current IP and port

//n = NetAddr.new("127.0.0.1", 57120);


SynthDef.new(\happyImage,
{
	arg scaleIndex = 0, inputAmp = 200;
    var scale = Scale.harmonicMajor;

	var output = SinOsc.ar(
        (
            DegreeToKey.kr(
                scale.as(LocalBuf),
                scaleIndex/10, // Scale index
                scale.stepsPerOctave,
                1, // mul = 1
                60 // offset by 72 notes
            )
            + LFNoise1.kr([3,3], 0.04) // add some low freq stereo detuning
        ).midicps, // convert midi notes to hertz
        0,
        0.25
    );


	output = Pan2.ar(output,0);
	Out.ar(0, output*MouseX.kr(0.5,0))
}).add;

SynthDef.new(\sadImage,
{
	arg scaleIndex = 0, inputAmp = 200;
    var scale = Scale.harmonicMinor;

	var output = LFSaw.ar(
        (
            DegreeToKey.kr(
                scale.as(LocalBuf),
                scaleIndex/10, //Scale index
                scale.stepsPerOctave,
                1, // mul = 1
                60 // offset by 72 notes
            )
            + LFNoise1.kr([3,3], 0.04) // add some low freq stereo detuning
        ).midicps, // convert midi notes to hertz
        0,
        0.25
    );


	output = Pan2.ar(output,0);
	Out.ar(0, output*MouseX.kr(0,0.5))
}).add;


(
SynthDef(\sine,{arg freq=440, amp=0.5;
Out.ar(0,SinOsc.ar(freq,0,amp))
}
).load(s);
)

~sinImg = Synth("sine"); // create the synth
~happyImg = Synth("happyImage"); // create the synth
~sadImg = Synth("sadImage"); // create the synth
~happyImg.free;
~sadImg.free;

(
o = OSCFunc({ |msg|
	msg[2].postln;
	//~sinImg.set(\freq, msg[2]);
	~happyImg.set(\scaleIndex, msg[2]);
}, '/happyMsg') // no add needed here
)

(
o = OSCFunc({ |msg|
	msg[2].postln;
	~sadImg.set(\scaleIndex, msg[2]);
}, '/sadMsg') // no add needed here
)

o.free;    // remove the OSCFunc when you are done.
~sinImg.free;

//~myRunningSynth.set(\freq, 880);

Scale.directory;

(
r = {
    var scale = Scale.harmonicMajor;

}.play;
)




x = Synth(\imagePiano);



r.free;

// change scale
a = Scale.phrygian;

// change tuning
a.tuning_(\just);

// can also set tuning at creation time
a = Scale.ionian(\pythagorean);