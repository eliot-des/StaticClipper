/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin editor.

  ==============================================================================
*/

#include "PluginProcessor.h"
#include "PluginEditor.h"

//==============================================================================
StaticClipperAudioProcessorEditor::StaticClipperAudioProcessorEditor 
(StaticClipperAudioProcessor& p, juce::AudioProcessorValueTreeState& vts):
AudioProcessorEditor (&p), audioProcessor (p)
{
    //=======================Input Gain Dial==================================

    addAndMakeVisible(inputgainSlider);
    inputgainSlider.setSliderStyle(juce::Slider::SliderStyle::RotaryHorizontalVerticalDrag);
    inputgainSlider.setColour(juce::Slider::ColourIds::rotarySliderFillColourId, juce::Colours::whitesmoke.darker(0.2f));
    inputgainSlider.setColour(juce::Slider::ColourIds::thumbColourId, juce::Colours::white);
    inputgainSlider.setColour(juce::Slider::ColourIds::rotarySliderOutlineColourId, juce::Colours::black.brighter(0.1f));
    inputgainSlider.setColour(juce::Slider::ColourIds::textBoxOutlineColourId, juce::Colours::transparentBlack);
    inputgainSlider.setTextBoxStyle(juce::Slider::TextBoxBelow, false, 60, 20);
    inputgainSlider.setTextValueSuffix(" dB");

    inputgainAttachement.reset(new juce::AudioProcessorValueTreeState::SliderAttachment(vts, "input gain", inputgainSlider));


    addAndMakeVisible(inputgainLabel);
    inputgainLabel.attachToComponent(&inputgainSlider, false);
    inputgainLabel.setText("Input Gain", juce::dontSendNotification);
    inputgainLabel.setJustificationType(juce::Justification::centredBottom);
    inputgainLabel.setFont(juce::Font("Futura", 20.0f, juce::Font::bold));



    //======================Output Gain Dial==================================

    addAndMakeVisible(outputgainSlider);
    outputgainSlider.setSliderStyle(juce::Slider::SliderStyle::RotaryHorizontalVerticalDrag);
    outputgainSlider.setColour(juce::Slider::ColourIds::rotarySliderFillColourId, juce::Colours::whitesmoke.darker(0.2f));
    outputgainSlider.setColour(juce::Slider::ColourIds::thumbColourId, juce::Colours::white);
    outputgainSlider.setColour(juce::Slider::ColourIds::rotarySliderOutlineColourId, juce::Colours::black.brighter(0.1f));
    outputgainSlider.setColour(juce::Slider::ColourIds::textBoxOutlineColourId, juce::Colours::transparentBlack);
    outputgainSlider.setTextBoxStyle(juce::Slider::TextBoxBelow, false, 60, 20);
    outputgainSlider.setTextValueSuffix(" dB");

    outputgainAttachement.reset(new juce::AudioProcessorValueTreeState::SliderAttachment(vts, "output gain", outputgainSlider));


    addAndMakeVisible(outputgainLabel);
    outputgainLabel.attachToComponent(&outputgainSlider, false);
    outputgainLabel.setText("Output Gain", juce::dontSendNotification);
    outputgainLabel.setJustificationType(juce::Justification::centredBottom);
    outputgainLabel.setFont(juce::Font("Futura", 20.0f, juce::Font::bold));



    //======================Mix Slider==================================

    addAndMakeVisible(mixSlider);
    mixSlider.setSliderStyle(juce::Slider::SliderStyle::LinearHorizontal);
    mixSlider.setColour(juce::Slider::ColourIds::backgroundColourId, juce::Colours::black.brighter(0.1f));
    mixSlider.setColour(juce::Slider::ColourIds::trackColourId, juce::Colours::whitesmoke.darker(0.2f));
    mixSlider.setColour(juce::Slider::ColourIds::thumbColourId, juce::Colours::white);
    mixSlider.setColour(juce::Slider::ColourIds::textBoxOutlineColourId, juce::Colours::transparentBlack);
    mixSlider.setTextBoxStyle(juce::Slider::TextBoxBelow, false, 60, 20);
    mixSlider.setTextValueSuffix(" %");

    mixAttachement.reset(new juce::AudioProcessorValueTreeState::SliderAttachment(vts, "mix", mixSlider));

    addAndMakeVisible(mixLabel);
    mixLabel.attachToComponent(&mixSlider, false);
    mixLabel.setText("Mix", juce::dontSendNotification);
    mixLabel.setJustificationType(juce::Justification::centred);
    mixLabel.setFont(juce::Font("Futura", 20.0f, juce::Font::bold));


    //======================Oversampling  Toggle==================================

    addAndMakeVisible(osComboBox);
    osComboBoxAttachment.reset(new juce::AudioProcessorValueTreeState::ComboBoxAttachment(vts, "oversampling", osComboBox));

    osComboBox.addItem("Off", 1);
    osComboBox.addItem("2x", 2);
    osComboBox.addItem("4x", 3);
    osComboBox.addItem("8x", 4);
    osComboBox.setSelectedId(1);

    osComboBox.setColour(juce::ComboBox::ColourIds::backgroundColourId, juce::Colours::black.brighter(0.09f));
    osComboBox.setColour(juce::ComboBox::ColourIds::outlineColourId, juce::Colours::black.brighter(0.09f));
    osComboBox.getLookAndFeel().setColour(juce::PopupMenu::ColourIds::backgroundColourId, juce::Colours::black.brighter(0.09f));
    osComboBox.getLookAndFeel().setColour(juce::PopupMenu::ColourIds::highlightedBackgroundColourId, juce::Colours::black.brighter(0.15f));

    addAndMakeVisible(osLabel);
    osLabel.attachToComponent(&osComboBox, false);
    osLabel.setText("Oversampling", juce::dontSendNotification);
    osLabel.setJustificationType(juce::Justification::centredTop);
    osLabel.setFont(juce::Font("Futura", 20.0f, juce::Font::bold));


    //======================Shape ComboBox==================================

    addAndMakeVisible(shapeComboBox);

    shapeComboBoxAttachment.reset(new juce::AudioProcessorValueTreeState::ComboBoxAttachment(vts, "shape", shapeComboBox));

    shapeComboBox.addItem("Boss DS-1", 1);
    shapeComboBox.addItem("Tanh", 2);
    shapeComboBox.addItem("Sigmoid 1", 3);
    shapeComboBox.addItem("Scale Atan", 4);
    shapeComboBox.setSelectedId(1);

    shapeComboBox.setColour(juce::ComboBox::ColourIds::backgroundColourId, juce::Colours::black.brighter(0.09f));
    shapeComboBox.setColour(juce::ComboBox::ColourIds::outlineColourId, juce::Colours::black.brighter(0.09f));
    shapeComboBox.getLookAndFeel().setColour(juce::PopupMenu::ColourIds::backgroundColourId, juce::Colours::black.brighter(0.09f));
    shapeComboBox.getLookAndFeel().setColour(juce::PopupMenu::ColourIds::highlightedBackgroundColourId, juce::Colours::black.brighter(0.15f));


    setSize(500, 250);
}

StaticClipperAudioProcessorEditor::~StaticClipperAudioProcessorEditor()
{
}

//==============================================================================
void StaticClipperAudioProcessorEditor::paint (juce::Graphics& g)
{
    // (Our component is opaque, so we must completely fill the background with a solid colour)


    const juce::Colour myBlack = juce::Colours::black.brighter(0.13f);
    const juce::Colour myDarkgrey = juce::Colours::darkgrey.darker(0.94f);

    const auto area = getLocalBounds();

    const juce::Point<float> startPoint = { (float)area.getWidth() / 2.0f, 0.f };
    const juce::Point<float> endPoint = { (float)area.getWidth() / 2.0f, (float)area.getHeight() };




    g.fillAll(myDarkgrey);
    g.setColour(myBlack);
    g.fillRect(0, 0, area.getWidth(), area.getHeight() / 5);

    //======================Plugin Name==================================
    g.setColour(juce::Colours::whitesmoke);
    g.setFont(juce::Font("Futura", 35.0f, juce::Font::bold));
    g.drawFittedText("StaticClipper", 15, 0, 300, getHeight() / 5, juce::Justification::centredLeft, 1);

    //const auto roundRectangleWidth = getWidth()*1/5;
    //const auto roundRectangleHeight = getHeight()*2/3;
    //g.drawRoundedRectangle(getWidth() *5/6 - roundRectangleWidth/2, getHeight()* 7 / 12 - roundRectangleHeight/2, roundRectangleWidth, roundRectangleHeight, 4.f,3.f);

    //creator name and plugin version
    g.setFont(juce::Font("Futura", 15.0f, juce::Font::bold));
    g.drawFittedText("Eliot.D \n Beta Version", 0, 0, area.getWidth() - 15, area.getHeight() / 5, juce::Justification::centredRight, 1);

    //black lines
    g.setColour(juce::Colours::black.brighter(0.07f));
    g.fillRect(0, area.getHeight() / 5, area.getWidth(), 3);
    g.fillRect(area.getWidth() * 2.f/3.f, area.getHeight() / 5.f, 3.f, area.getHeight() * 4.f/5.f);
}

void StaticClipperAudioProcessorEditor::resized()
{
    constexpr auto knobWidth = 150.f;
    constexpr auto knobHeight = 150.f;

    constexpr auto sliderWidth = 130.f;
    constexpr auto sliderHeight = 40.f;

    constexpr auto toggleWidth = 120.f;
    constexpr auto toggleheight = 50.f;

    constexpr auto osBoxWidth = 120;
    constexpr auto osBoxHeight = 27;

    constexpr auto shapeBoxWidth = 120;
    constexpr auto shapeBoxHeight = 27;

    inputgainSlider.setBounds(getWidth() / 6.f - knobWidth / 2.f + 10,
        getHeight() * 2.f / 3.f - knobHeight / 2.f , knobWidth, knobHeight);

    outputgainSlider.setBounds(getWidth() / 2.f - knobWidth / 2.f - 10,
        getHeight() * 2.f / 3.f - knobHeight / 2.f , knobWidth, knobHeight);

    mixSlider.setBounds(getWidth() * 5.f / 6.f - sliderWidth / 2.f,
        getHeight() * 5.f / 6.f - sliderHeight / 2.f , sliderWidth, sliderHeight);


    osComboBox.setBounds(getWidth() * 5.f / 6.f - osBoxWidth / 2.f,
        getHeight() * 3.f / 7.f - osBoxHeight / 2.f + 10, osBoxWidth, osBoxHeight);

    shapeComboBox.setBounds(getWidth() *1/2 - shapeBoxWidth / 2 + 22, getHeight() / 10 - shapeBoxHeight / 2,
        shapeBoxWidth, shapeBoxHeight);


}
