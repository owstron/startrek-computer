import speech_recognition as sr


def recognize_speech_from_audio(recognizer, 
                                file_path, 
                                offset=0, 
                                duration=0,
                                verbose=False):
    '''
        Recognizes speech from an audio file

        Parameters:

            recognizer -> an instance of speech_recognition.Recognizer class

            file_path -> location of the file

            offset -> The starting position of the file to transcribe
                Default: 0. Starts from the beginning of the file

            duration -> The length of audio to transcribe.
                Default: 0. Reads the whole file
            
            verbose -> (bool) Option to show all the transcripts.
    '''

    # load files
    audio_file = sr.AudioFile(file_path)
    with audio_file as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.1)
        audio = recognizer.record(source, offset=offset, duration=duration)

    # response object
    response = {
        'success': True,
        'error': None,
        'transcript': None
    }

    # Cathching request error or Unknown Value Errors
    try:
        respone['trascript'] = recognizer.recognize_google(audio, show_all=verbose)
    except sr.RequestError:
        # Unreachable API error
        response['success'] = False
        response['error'] = 'API Unavailable'
    except sr.UnknownValueError:
        # unrecognizable speech
        response['error'] = 'Unable to recognize speech'

    return response


def recognize_audio_from_microphone(recognizer, microphone, verbose=False):
    '''
        Transcribe speech directly from microphone

        Parameter:
            
            recognizer -> an instance of speech_recognition.Recognizer class

            microphone -> an instance of speech_recognition.Microphone class

    '''

    # Read from microphone and reduce ambient noise
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print('Recording Started')
        audio = recognizer.listen(source) 
        # waits for 0.5 seconds before stopping recording
    print('Recording Ended')
    print('-' * 20)
    
    # set up response object
    response = {
        'success': True,
        'error': None,
        'transcript': None
    }

    # Cathching request error or Unknown Value Errors
    try:
        respone['trascript'] = recognizer.recognize_google(audio, show_all=verbose)
    except sr.RequestError:
        # Unreachable API error
        response['success'] = False
        response['error'] = 'API Unavailable'
    except sr.UnknownValueError:
        # unrecognizable speech
        response['error'] = 'Unable to recognize speech'

    return response

if __name__ == '__main__':
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # # testing 1st function
    # file_path = 'harvard.wav'
    # print(recognize_speech_from_audio(r, file_path))

    # testing 2nd function
    print(recognize_audio_from_microphone(recognizer, microphone))
