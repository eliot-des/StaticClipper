/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin processor.

  ==============================================================================
*/

#include "PluginProcessor.h"
#include "PluginEditor.h"

//==============================================================================
StaticClipperAudioProcessor::StaticClipperAudioProcessor()
#ifndef JucePlugin_PreferredChannelConfigurations
     : AudioProcessor (BusesProperties()
                     #if ! JucePlugin_IsMidiEffect
                      #if ! JucePlugin_IsSynth
                       .withInput  ("Input",  juce::AudioChannelSet::stereo(), true)
                      #endif
                       .withOutput ("Output", juce::AudioChannelSet::stereo(), true)
                      #endif 
     ), 
#else 
    :

#endif
parameters(*this, nullptr, juce::Identifier("ClipperPlugin"), {
        std::make_unique<juce::AudioParameterFloat>("input gain", "Input Gain", juce::NormalisableRange{ -10.f, 30.f ,0.1f, 1.f,false }, 0.f),
        std::make_unique<juce::AudioParameterFloat>("output gain", "Output Gain", juce::NormalisableRange{ -20.f, 10.f ,0.1f, 1.f,false }, 0.f),
        std::make_unique<juce::AudioParameterInt>("mix", "Mix", 0, 100, 100),
        std::make_unique<juce::AudioParameterInt>("shape", "Shape", 1, 4, 1),
        std::make_unique<juce::AudioParameterInt>("oversampling","Oversampling", 1, 4, 1)
        }) {

    inputGainParameter = parameters.getRawParameterValue("input gain");
    outputGainParameter = parameters.getRawParameterValue("output gain");
    mixPercentageParameter = parameters.getRawParameterValue("mix");
    oversamplingParameter = parameters.getRawParameterValue("oversampling");
    shapeParameter = parameters.getRawParameterValue("shape");

    int numInputChannels = getTotalNumInputChannels();

    //initialize all the "oversamplers"
    for (int i = 0; i < 3; ++i)
        oversampler[i] = std::make_unique<juce::dsp::Oversampling<float>>(numInputChannels, i + 1,
            juce::dsp::Oversampling<float>::filterHalfBandPolyphaseIIR);
};



StaticClipperAudioProcessor::~StaticClipperAudioProcessor()
{
}

//==============================================================================
const juce::String StaticClipperAudioProcessor::getName() const
{
    return JucePlugin_Name;
}

bool StaticClipperAudioProcessor::acceptsMidi() const
{
   #if JucePlugin_WantsMidiInput
    return true;
   #else
    return false;
   #endif
}

bool StaticClipperAudioProcessor::producesMidi() const
{
   #if JucePlugin_ProducesMidiOutput
    return true;
   #else
    return false;
   #endif
}

bool StaticClipperAudioProcessor::isMidiEffect() const
{
   #if JucePlugin_IsMidiEffect
    return true;
   #else
    return false;
   #endif
}

double StaticClipperAudioProcessor::getTailLengthSeconds() const
{
    return 0.0;
}

int StaticClipperAudioProcessor::getNumPrograms()
{
    return 1;   // NB: some hosts don't cope very well if you tell them there are 0 programs,
                // so this should be at least 1, even if you're not really implementing programs.
}

int StaticClipperAudioProcessor::getCurrentProgram()
{
    return 0;
}

void StaticClipperAudioProcessor::setCurrentProgram (int index)
{
}

const juce::String StaticClipperAudioProcessor::getProgramName (int index)
{
    return {};
}

void StaticClipperAudioProcessor::changeProgramName (int index, const juce::String& newName)
{
}

//==============================================================================
void StaticClipperAudioProcessor::prepareToPlay (double sampleRate, int samplesPerBlock)
{
    // Use this method as the place to do any pre-playback
    // initialisation that you need..
    for (auto& os : oversampler)
        os->initProcessing(samplesPerBlock);
}

void StaticClipperAudioProcessor::releaseResources()
{
    // When playback stops, you can use this as an opportunity to free up any
    // spare memory, etc.
    
}

#ifndef JucePlugin_PreferredChannelConfigurations
bool StaticClipperAudioProcessor::isBusesLayoutSupported (const BusesLayout& layouts) const
{
  #if JucePlugin_IsMidiEffect
    juce::ignoreUnused (layouts);
    return true;
  #else
    // This is the place where you check if the layout is supported.
    // In this template code we only support mono or stereo.
    // Some plugin hosts, such as certain GarageBand versions, will only
    // load plugins that support stereo bus layouts.
    if (layouts.getMainOutputChannelSet() != juce::AudioChannelSet::mono()
     && layouts.getMainOutputChannelSet() != juce::AudioChannelSet::stereo())
        return false;

    // This checks if the input layout matches the output layout
   #if ! JucePlugin_IsSynth
    if (layouts.getMainOutputChannelSet() != layouts.getMainInputChannelSet())
        return false;
   #endif

    return true;
  #endif
}
#endif

void StaticClipperAudioProcessor::processBlock (juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages)
{
    juce::ScopedNoDenormals noDenormals;
    
    auto totalNumInputChannels  = getTotalNumInputChannels();
    auto totalNumOutputChannels = getTotalNumOutputChannels();

    for (auto i = totalNumInputChannels; i < totalNumOutputChannels; ++i)
        buffer.clear(i, 0, buffer.getNumSamples());

    const auto inputGain = inputGainParameter->load();
    const auto outputGain = outputGainParameter->load();
    const auto mixPercentage = mixPercentageParameter->load();
    const auto shapeSelected = shapeParameter->load()-1;


    const auto oversamplingIndex = static_cast<int>(oversamplingParameter->load()) - 2;


    clipper.setInputGain(inputGain);
    clipper.setOutputGain(outputGain);
    clipper.setMixPercentage(mixPercentage);
    clipper.setShapeSelected(shapeSelected);

    juce::dsp::AudioBlock<float> inputblock {buffer};

    if (oversamplingIndex > -1) {

        auto oversampledblock = oversampler[oversamplingIndex]->processSamplesUp(inputblock);

        clipper.processBlock(oversampledblock);

        oversampler[oversamplingIndex]->processSamplesDown(inputblock);
    }
    else {
        clipper.processBlock(inputblock);
    }
}

//==============================================================================
bool StaticClipperAudioProcessor::hasEditor() const
{
    return true; // (change this to false if you choose to not supply an editor)
}

juce::AudioProcessorEditor* StaticClipperAudioProcessor::createEditor()
{
    return new StaticClipperAudioProcessorEditor (*this, parameters);
}

//==============================================================================
void StaticClipperAudioProcessor::getStateInformation (juce::MemoryBlock& destData)
{
    // You should use this method to store your parameters in the memory block.
    // You could do that either as raw data, or use the XML or ValueTree classes
    // as intermediaries to make it easy to save and load complex data.
    auto state = parameters.copyState();
    std::unique_ptr<juce::XmlElement> xml(state.createXml());
    copyXmlToBinary(*xml, destData);

}

void StaticClipperAudioProcessor::setStateInformation (const void* data, int sizeInBytes)
{
    // You should use this method to restore your parameters from this memory block,
    // whose contents will have been created by the getStateInformation() call.
    std::unique_ptr<juce::XmlElement> xmlState(getXmlFromBinary(data, sizeInBytes));
    if (xmlState.get() != nullptr)
        if (xmlState->hasTagName(parameters.state.getType()))
            parameters.replaceState(juce::ValueTree::fromXml(*xmlState));
}

//==============================================================================
// This creates new instances of the plugin..
juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new StaticClipperAudioProcessor();
}
