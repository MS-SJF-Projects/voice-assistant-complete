# Speech to text

## Goal

In this exercise, you will create an application to recognize and transcribe human speech (often called speech-to-text).

In the first stage we're going to create the necessary speech resources in Azure.

## Tutorial

### Setup speech resources

1. Setup a [speech resource](https://ms.portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices)

   * Select `sjf22` as *Resource group* (use *Create new*)
   * Select *West Europe* as *Region*
   * Select `sjf22-speech` as *Name*
   * Select *Free F0* as *Pricing tier*

2. Setup a [language service](https://aka.ms/languageStudio)

   * Login with your Azure account
   * Create a new language resource

     * Select `sjf22` as *Resource group*
     * Select `sjf22-language` as *Name*
     * Select *westeurope* as *Location*
     * Select *F0* as *Pricing Tier*

3. Create a Conversational Language Understanding project

   * Open the [Language Studio](https://language.cognitive.azure.com/home)
   * Click on [Conversational language understanding](https://language.cognitive.azure.com/clu/projects)
   * Click on *Import* and load the `FlightBooking.json` file from this repository
   * Leave the field *Name* empty
   * Follow this [quickstart](https://docs.microsoft.com/en-us/azure/cognitive-services/language-service/conversational-language-understanding/quickstart?pivots=language-studio) to train, deploy, and test your model

### Setup Python

1. Install the following packages into your Python development environment:

   ```
   pip install azure-cognitiveservices-speech
   pip install azure-ai-language-conversations --pre
   ```

### Setup development environment

1. Open the `sjf22-speech` resource in the [Microsoft Azure portal](https://portal.azure.com/#home)

   * In *Resource Management / Keys and Endpoint*, copy *KEY 1*, save it in the Python variable `speech_key` in `start.py`

1. Open the `sjf22-language` resource in the [Microsoft Azure portal](https://portal.azure.com/#home)

   * In *Resource Management / Keys and Endpoint*

     * copy *KEY 1*, save it in the Python variable `language_key` in `start.py`
     * copy *Endpoint*, save it in the Python variable `language_endpoint` in `start.py`.

2. Get the resource key and region. After your Speech resource is deployed, select **Go to resource** to view and manage keys. For more information about Cognitive Services resources, see [Get the keys for your resource](~/articles/cognitive-services/cognitive-services-apis-create-account.md#get-the-keys-for-your-resource).

## Recognize speech from a microphone

Follow these steps to create a new console application.

1. Open a command prompt where you want the new project, and create a new file named `speech-recognition.py`.
1. Run this command to install the Speech SDK:  

    ```console
    pip install azure-cognitiveservices-speech
    ```

1. Copy the following code into `speech_recognition.py`:

    ```Python
    import azure.cognitiveservices.speech as speechsdk

    def recognize_from_microphone():
        speech_config = speechsdk.SpeechConfig(subscription="YourSubscriptionKey", region="YourServiceRegion")
        speech_config.speech_recognition_language="en-US"

        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        print("Speak into your microphone.")
        speech_recognition_result = speech_recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(speech_recognition_result.text))
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("Speech Recognition canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

    recognize_from_microphone()
    ```

1. In `speech_recognition.py`, replace `YourSubscriptionKey` with your Speech resource key, and replace `YourServiceRegion` with your Speech resource region.

    > [!IMPORTANT]
    > Remember to remove the key from your code when you're done, and never post it publicly. For production, use a secure way of storing and accessing your credentials like [Azure Key Vault](../../../../../key-vault/general/overview.md). See the Cognitive Services [security](../../../../cognitive-services-security.md) article for more information.

1. To change the speech recognition language, replace `en-US` with another [supported language](~/articles/cognitive-services/speech-service/supported-languages.md). For example, `es-ES` for Spanish (Spain). The default language is `en-US` if you don't specify a language. For details about how to identify one of multiple languages that might be spoken, see [language identification](~/articles/cognitive-services/speech-service/language-identification.md). 

Run your new console application to start speech recognition from a microphone:

```console
python speech_recognition.py
```

Speak into your microphone when prompted. What you speak should be output as text: 

```console
Speak into your microphone.
RECOGNIZED: Text=I'm excited to try speech to text.
```

## Remarks
Now that you've completed the quickstart, here are some additional considerations:

- This example uses the `recognize_once_async` operation to transcribe utterances of up to 30 seconds, or until silence is detected. For information about continuous recognition for longer audio, including multi-lingual conversations, see [How to recognize speech](~/articles/cognitive-services/speech-service/how-to-recognize-speech.md).
- To recognize speech from an audio file, use `filename` instead of `use_default_microphone`:

    ```python
    audio_config = speechsdk.audio.AudioConfig(filename="YourAudioFile.wav")
    ```

- For compressed audio files such as MP4, install GStreamer and use `PullAudioInputStream` or `PushAudioInputStream`. For more information, see [How to use compressed input audio](~/articles/cognitive-services/speech-service/how-to-use-codec-compressed-audio-input-streams.md).

### [Return to Main Index](../../README.md)
