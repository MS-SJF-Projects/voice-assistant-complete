import azure.cognitiveservices.speech as speechsdk
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

# Replace the None values in the following variables according to README.md
speech_key = None
language_key = None
language_region = 'westeurope'
language_endpoint = None
language_project = 'sjf22-clu'
deployment_name = 'Testing'

# global services
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=language_region)
speech_config.speech_recognition_language="en-US"

client = ConversationAnalysisClient(language_endpoint, AzureKeyCredential(language_key))

def recognize_from_microphone():
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

    return None

def speak(text):
    # TODO: combine audio_config's?
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name='en-US-JennyNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

def extract_intent(text):
    with client:
        query = text
        result = client.analyze_conversation(
            task={
                "kind": "Conversation",
                "analysisInput": {
                    "conversationItem": {
                        "participantId": "1",
                        "id": "1",
                        "modality": "text",
                        "language": "en",
                        "text": query
                    },
                    "isLoggingEnabled": False
                },
                "parameters": {
                    "projectName": language_project,
                    "deploymentName": deployment_name,
                    "verbose": True
                }
            }
        )
    print("query: {}".format(result["result"]["query"]))
    print("project kind: {}\n".format(result["result"]["prediction"]["projectKind"]))

    print("top intent: {}".format(result["result"]["prediction"]["topIntent"]))
    print("category: {}".format(result["result"]["prediction"]["intents"][0]["category"]))
    print("confidence score: {}\n".format(result["result"]["prediction"]["intents"][0]["confidenceScore"]))

    print("entities:")
    for entity in result["result"]["prediction"]["entities"]:
        print("\ncategory: {}".format(entity["category"]))
        print("text: {}".format(entity["text"]))
        print("confidence score: {}".format(entity["confidenceScore"]))
        if "resolutions" in entity:
            print("resolutions")
            for resolution in entity["resolutions"]:
                print("kind: {}".format(resolution["resolutionKind"]))
                print("value: {}".format(resolution["value"]))
        if "extraInformation" in entity:
            print("extra info")
            for data in entity["extraInformation"]:
                print("kind: {}".format(data["extraInformationKind"]))
                if data["extraInformationKind"] == "ListKey":
                    print("key: {}".format(data["key"]))
                if data["extraInformationKind"] == "EntitySubtype":
                    print("value: {}".format(data["value"]))

    return result["result"]["prediction"]["topIntent"]

text = recognize_from_microphone()
if text is not None:
    intent = extract_intent(text)

    if intent == "BookFlight":
        speak("Got it, you want to book a flight.")
    elif intent == "GetWeather":
        speak("You wanna know the weather?")
    elif intent == "Cancel":
        speak("Ok, bye.")
