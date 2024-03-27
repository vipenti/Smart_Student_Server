# Simulating Students in a Metaverse

This is project was made for my Internship at [SesaLab](https://github.com/SeSaLabUnisa) ([UniSa](https://unisa.it))

AI is everywhere, let's bring it in the MetaVerse!

## What even is this?

I'm simulating active listening and **curious** students in [SENEM](https://github.com/vipenti/SENEM_Metaverse) by [vipenti](https://github.com/vipenti)

Let's look at it step by step:
1. A professor teaches his lesson on SENEM
2. A random student is created with random attributes (such as intelligence, voice and personality)
3. The program transcribes the speech thanks to Whisper
4. Evaluates if it's needed to make a question based on what the teacher said
(also based on randomised students personality and intelligence)
5. Eventually Makes an API call to the Text Completion API and thus creates a question
6. *Asks* the question by voice using OpenAI's TTS API

Basically a simulated classroom of students that are listening, participating and active

# How does it work?

## Main files

Let's look at the main files:

### main.py

The functioning part of the project, basically does what is listed [above](#How-does-it-work?)

More specifically:
- Instantiates the 'small' model ([Whisper](https://github.com/openai/whisper))
- Creates a Student (my own class, more on it later) with it's own API management classes (again more on them later)
- The **true** body of the file a loop that does the following:
- Records audio with an instance of AudioManager (once again my own class that manages audio)
- Saves recording to a temporary file
- Transcribes the audio with the **Whisper** model
- Generates a question through the **Student** class
- Generates audio once again with the **Student** class

### speaking_interface.py

Contains the **Speaker** class, how does it work?s

**Initialisation**

```API_key```
> OpenAI API key to initialise models

```voice```
> Specific voice to instatiate OpenAI_TTS_Manager class

```voice_model```
> Model voice chosen to instatiate OpenAI_TTS_Manager class (i.e. "tts-1")

```completions_model```
> Completion model chosen to instatiate ChatGPT_Manager class (i.e. "gpt-3.5-turbo", "gpt-4")

```starting_prompt```
> Starting system prompt to feed to the Completion model

**Methods**

```generate_response```
> Delegates method call to Completion Manager

```generate_audio```
> Delegates method call to Audio Manager

```voice```
> Changes voice of its own Audio Manager


### student.py 

Inherits from **Speaker** class, what does it add?

### *Enums*

**Personality** enum, used for dictating questions frequency along with the

**Intelligence** enum

### *Student class*

**Costants**

```STARTING_PROMPT```
> starting prompt to format with initialisation attributes, dictates Completion model behaviour

```NOT_UNDERSTOOD```
> starting prompt when the student "doesn't understand" the question

```UNRELATED_QUESTION```
> starting prompt to be formatted and to check lesson/teacher explanation pertinence later on

**Initialisation**

```personality```
> Student's own personality (Personality enum)

```intelligence```
> Intelligence's own personality (Intelligence enum), also used to format *STARTING_PROMPT*

```subject```
> Lesson subject that the student is following, used to format *STARTING_PROMPT*

**Methods**

```generate_response```
*Is quite a bit different from parent's class method

Attributes: *```message```*, *```check_correlation```*

This is a long one, brace yourself
> Checks if we need to check for correlation between lesson and intended subject formatting  ```UNRELATED_QUESTION```

> if yes, then makes an API call to Text Completion thanks to the ChatGPT_Manager class, and check for correlation

> if the speaker is lecturing about the 'correct' subject then the following happens:

> with a probability based on personality it decides whether to ask the question or not (this probability increases the more the user is silent)

> if the student decides to speak, with a probability based on intelligence it's decided if the student understood the lesson (it increases the more the student doesn't get lesson)
> [Case 1] The student didn't understand
> - ```NOT_UNDERSTOOD``` constant is given to as a prompt
> - The Completions model will output something on the line of "Could you repeat the last concept? I didn't quite get that"
> [Case 2] The student understood
> - the brief part of speech is given as prompt and the model will output a proper question

## Utility files

### audioManager.py
Contain the AudioManager class

**Costants**

```SILENT_FRAME_SIZE```
> Duration in millisecond for each frame of the audio file

```VAD_ALLOWED_SAMPLERATES```
> List of valid sample rates for Voice Aactivation Detection or VAD

```DEFAULT_SAVING_FOLDER```
> Duh

**Initialisation**

```chunk``` 
> number of frames per buffer

```sample_format```
> Format in terms of bit per sample

```channels```
> Number of channels of audio recording

```sample_rate```
> Number of samples per second

```max_silent_seconds```
> Number of seconds after which the recording stops

```max_recording_length```
> Maximum amount of seconds per recording


**Methods**

* Not yet completed, also need to add running requirements
