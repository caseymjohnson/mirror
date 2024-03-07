from pocketsphinx import LiveSpeech


'''
Casey Johnson 3.1.24

This script is used to parse microphone date (of speech) into text.
The pocketsphinx (CMU) framework is used for this as it operates offline with no required credentials.

For pocketsphinx keyphrase search to work:
    keyphrase.dic is the phonetic data for words of interest
    keyphrase.list is the confidence thresholds for words of interest
    allVocab.dic is included in this repository should future users want to expand the keyphrase lists

MIRROR must be spoken (then brief pause) before giving command
This ensures that ambiant noise is not undesirably interpreted as command

'''

# where to dump parsed commands (a separate script handles action)
outputFile = 'parsedText.txt'

# initialize pocketsphinx instance
speech = LiveSpeech(kws='keyphrase.list', dic='keyphrase.dic', remove_noise=True)

# continuously capture speech
for phrase in speech:

    text = phrase.hypothesis()

    # if the hypothesis has multiple parts, take the first
    if ' ' in text:
        text = text.split(' ')[0]
    
    print(text)

    # append to file
    with open(outputFile, 'a') as f:
        f.write(text + '\n')
    f.close()