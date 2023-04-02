/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin editor.

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include "PluginProcessor.h"

//==============================================================================
/**
*/
class StaticClipperAudioProcessorEditor  : public juce::AudioProcessorEditor
{
public:
    StaticClipperAudioProcessorEditor 
    (StaticClipperAudioProcessor&, juce::AudioProcessorValueTreeState& vts);
    ~StaticClipperAudioProcessorEditor() override;

    //==============================================================================
    void paint (juce::Graphics&) override;
    void resized() override;

private:
    // This reference is provided as a quick way for your editor to
    // access the processor object that created it.
    StaticClipperAudioProcessor& audioProcessor;

    juce::Slider inputgainSlider;
    juce::Slider outputgainSlider;
    juce::Slider mixSlider;
    juce::ComboBox osComboBox;
    juce::ComboBox shapeComboBox;

    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment>   inputgainAttachement;
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment>   outputgainAttachement;
    std::unique_ptr<juce::AudioProcessorValueTreeState::SliderAttachment>   mixAttachement;
    std::unique_ptr<juce::AudioProcessorValueTreeState::ComboBoxAttachment> osComboBoxAttachment;
    std::unique_ptr<juce::AudioProcessorValueTreeState::ComboBoxAttachment> shapeComboBoxAttachment;


    juce::Label inputgainLabel;
    juce::Label outputgainLabel;
    juce::Label mixLabel;
    juce::Label osLabel;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (StaticClipperAudioProcessorEditor)
};
