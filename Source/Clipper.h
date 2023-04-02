#pragma once
#include "JuceHeader.h"

class Clipper
{
public:
	Clipper();

	void setInputGain(float inputGain);
	void setOutputGain(float outputGain);
	void setMixPercentage(float mixPercentage);
	void setShapeSelected(float shapeSelected);


	void processBlock(juce::dsp::AudioBlock<float> &audioBlock);

private:

	float inputGain;
	float outputGain;
	float mixPercentage;
	float shapeSelected;

	std::vector<std::function<float(float)>> sigmoidFunctions;
};

