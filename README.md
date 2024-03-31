# Simulating Students in a Metaverse

This is project was made for my Internship at [SesaLab](https://github.com/SeSaLabUnisa) ([UniSa](https://unisa.it))

AI is everywhere, let's bring it into the MetaVerse!

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

As simple as running the python script!

You'll just need to create a folder named configs in under the project folder

Then you'll need to create a **.json** file named ```API_key.json``` 

Where your OpenAI API key will be inserted, it should look like this:

```
{
    "API_KEY": "sk-didYouExpectToStealMyAPIkey?"
}
```