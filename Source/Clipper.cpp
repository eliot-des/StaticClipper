#include "Clipper.h"

Clipper::Clipper() {
	sigmoidFunctions.push_back([](float x) -> float {
			// Sigmoid 1
			constexpr auto a = 1.054540849128137;
			constexpr auto b = 0.913306378788536;
			constexpr auto c = 2.1855552498905344;
			constexpr auto n = 3.15420507919188;

			return x * a / std::pow(1 + std::pow(std::abs(c * x), n), b / n);
		});


	sigmoidFunctions.push_back([](float x) -> float {
			// Sigmoid 2
			return std::tanh(x);
		});


	sigmoidFunctions.push_back([](float x) -> float {
			// Sigmoid 3
			constexpr auto s = 5.f;

			return x / std::pow(1+std::pow(std::abs(x),s), 1 / s);
		});


	sigmoidFunctions.push_back([](float x) -> float {
			// Sigmoid 4 -> scale arc tangent
			constexpr auto pi = 3.14159265358979323846;

			return 2 / pi * std::atan(pi / 2 *x);
		});
}


void Clipper::setInputGain(float inputGain) {
	this->inputGain = inputGain;
}


void Clipper::setOutputGain(float outputGain) {
	this->outputGain = outputGain;
}


void Clipper::setMixPercentage(float mixPercentage) {
	this->mixPercentage = mixPercentage;
}


void Clipper::setShapeSelected(float shapeSelected) {
	this->shapeSelected = shapeSelected;
}


void Clipper::processBlock(juce::dsp::AudioBlock<float> &audioBlock) {
	
	const auto mix = mixPercentage / 100.0f;

	for (auto channel = 0; channel < audioBlock.getNumChannels(); ++channel) {

		auto *channelSamples = audioBlock.getChannelPointer(channel);

		
		for (auto i = 0; i < audioBlock.getNumSamples(); i++) {

			const auto inputSample = channelSamples[i];
			
			const auto amplifiedSample = inputSample * std::pow(10, inputGain / 20);

			//sigmoid function
			const auto clippedSample = sigmoidFunctions[shapeSelected](amplifiedSample) * std::pow(10, outputGain / 20);

			channelSamples[i] = clippedSample * mix + (1 - mix) * inputSample;
		}
	}

}

