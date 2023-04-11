import subprocess
from pydub import AudioSegment
import openai

openai.api_key = "$API_KEY"

def video_to_audio(video_file, file_name_prefix):
    audio_file = f"{file_name_prefix}_audio.wav"
    print("Converting video to audio file...\n")
    subprocess.call(["ffmpeg", "-y", "-i", video_file, "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", audio_file], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    print("Audio file has been converted...finishing\n")
    return audio_file

# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

def audio_to_transcript(audio_file, file_name_prefix):
    print("Starting to audio transcribe...\n")
    audio = AudioSegment.from_file(audio_file)
    
    chunk_size_ms = 6 * 60 * 1000  # 6 minutes in milliseconds
    chunks = list(audio[::chunk_size_ms])

    transcript = ""
    for i, chunk in enumerate(chunks):
        # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
        silence_chunk = AudioSegment.silent(duration=500)
        # Add the padding chunk to beginning and end of the entire chunk.
        audio_chunk = silence_chunk + chunk + silence_chunk

        # Normalize the entire chunk.
        normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

        chunk_file = f"{file_name_prefix}_normalized_chunk_{i}.wav"
        normalized_chunk.export(chunk_file, format="wav")
        
        with open(chunk_file, "rb") as f:
            response = openai.Audio.transcribe("whisper-1", f)
        
        # Append the response to the existing list
        transcript += response["text"] + "\n"
        print("transcript chunck processed: %d \n" % i)

    print("Audio transcripts finished\n")

    with open(f"{file_name_prefix}_transcripts.txt", "w", encoding="utf-8") as f:
        f.write(transcript)

def MoM_generation(file_name_prefix):
    
    print("MoM Generation started...\n")

    # Prompt text
    prompt = """
    generate meeting minutes from the input text. Include Key discussion topics, any decisions, Action items, questions asked and their answers, summary of topic discussed.
    Input Text:
    """

    # Read transcripts from file
    with open(f"{file_name_prefix}_transcripts.txt", "r", encoding="utf-8") as f:
        transcript_string = f.read()

    # Split the input text into chunks based on line endings
    input_chunks = transcript_string.split('\n')

    # Generate meeting minutes from each input chunk
    meeting_minutes = ""

    for chunk in input_chunks:
        chunk = prompt + chunk 
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chunk,
            max_tokens=256,
            n=1,
            stop=None,
            temperature=0.5,
        )
        generated_text = response.choices[0].text.strip()
        meeting_minutes += generated_text
        print("Generated text:", generated_text)

    # Write the meeting minutes to file
    with open(f"{file_name_prefix}_meeting_minutes.txt", "a") as f:
        f.write(meeting_minutes)
    print(f"{file_name_prefix} MoM Generation finished :)\n ")


if __name__ == "__main__":
    video_file_path_1 = "Risk-Workshop-Meeting-Recording.mp4"
    audio_file_1 = video_to_audio(video_file_path_1,"workshop_1")
    audio_to_transcript(audio_file_1, "workshop_1")
    MoM_generation("workshop_1")

    video_file_path_2 = "Risk-Workshop-2-Meeting-Recording.mp4"
    audio_file_2 = video_to_audio(video_file_path_2, "workshop_2")
    audio_to_transcript(audio_file_2, "workshop_2")    
    MoM_generation("workshop_2")
