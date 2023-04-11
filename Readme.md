# Transcipting Script for OpenAI

I will complete this later on how this code is working. But essentially you feed the Teams video into it:
1. It exports it into *.wav format of audio
2. Cuts it into pieces of 6 minute audio and feeds it into Whisper-1 OpenAI model for trasncription
3. Then it records it into a text file with new lines
4. Then reads it from the text file and separate it into an array to feed it into Davinci model with a prompt to get some results.
5. Then you have the MOM.


## Missing and Downsides

- The code is missing a few bits and pieces and does not work competely because it needs some dynamic calculation of input text to assign valid number of tokens to davinci.
- Text that is transcibe is not diarised and it is important to know who said what...Whisper-1 can't do that.
- When you chop audio in 6 minutes, the text written into text file is mid sentence and when you read it back for davinci to minute it, it is sometimes looses its  context.


**This is good code if you have looooong workshops and want to minute and can't be bothered with transcibing from sratch. But the output needs tinkering and changes to suit to get to copy/paste into meeting minutes situation.**

**Use it with API and nothing else if you are worried about privacy and data stuff. Because T&C of OpenAI has changed, and you need to read that to understand if sending voice to API for transciption suits your organisation secrets. Not my issue if you don't pay attention to those stuff.**