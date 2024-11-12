from pygame import mixer

voiceLines={
    "Intro": [
        mixer.Sound("Assets/BossVoicelines/Intro/That was my fucken house.ogg"),
        mixer.Sound("Assets/BossVoicelines/Intro/Fuck off - Suzanne.ogg")
    ],
    "t1": {
        "start": mixer.Sound("Assets/BossVoicelines/T1/Parents solo missions.ogg"),
        "hit": [
            mixer.Sound("Assets/BossVoicelines/T1/Ow.ogg"),
            mixer.Sound("Assets/BossVoicelines/T1/Owie.ogg"),
            mixer.Sound("Assets/BossVoicelines/T1/That hurts.ogg"),
        ],
        "death": mixer.Sound("Assets/BossVoicelines/T1/Older brother will handle you.ogg"),
        "kill": [mixer.Sound("Assets/BossVoicelines/T1/My parents underestimate me.ogg"),
                 mixer.Sound("Assets/BossVoicelines/T1/How did u die to this.ogg")]
    },
    "t2": {
        "start": mixer.Sound("Assets/BossVoicelines/T2/Younger brother weak.ogg"),
        "hit": [
            mixer.Sound("Assets/BossVoicelines/T2/Fuck off James.ogg"),
            mixer.Sound("Assets/BossVoicelines/T2/Go fuck yourself James.ogg"),
            mixer.Sound("Assets/BossVoicelines/T2/Eh its just a scratch James.ogg"),
        ],
        "death": mixer.Sound("Assets/BossVoicelines/T2/You are stronger than I thought James.ogg"),
        "kill": mixer.Sound("Assets/BossVoicelines/T2/I knew you were weak James.ogg")
    },
    "t3": {
        "start": mixer.Sound("Assets/BossVoicelines/T3/You dare mess with my home.ogg"),
        "hit": [
            mixer.Sound("Assets/BossVoicelines/T3/Oi fuck off mate.ogg"),
            mixer.Sound("Assets/BossVoicelines/T3/UwU fuck off.ogg"),
            mixer.Sound("Assets/BossVoicelines/T3/Harder daddy.ogg"),
        ],
        "death": mixer.Sound("Assets/BossVoicelines/T3/Call in Ettei.ogg"),
        "kill": mixer.Sound("Assets/BossVoicelines/T3/Lets have a barbie.ogg")
    },
    "t4": {
        "start": mixer.Sound("Assets/BossVoicelines/T4/You expect to live.ogg"),
        "hit": [
            mixer.Sound("Assets/BossVoicelines/T4/Small lasers.ogg"),
            mixer.Sound("Assets/BossVoicelines/T4/Go die in a hole.ogg"),
            mixer.Sound("Assets/BossVoicelines/T4/Useless as a Russian election.ogg"),
        ],
        "death": mixer.Sound("Assets/BossVoicelines/T4/Mother we need you.ogg"),
        "kill": mixer.Sound("Assets/BossVoicelines/T4/Lucky keeping your head.ogg")
    },
    "t5": {
        "start": mixer.Sound("Assets/BossVoicelines/T5/New age youngens.ogg"),
        "start2": mixer.Sound("Assets/BossVoicelines/T5/Shit batteries.ogg"),
        "hit": [
            mixer.Sound("Assets/BossVoicelines/T5/Dare attack old woman.ogg"),
            mixer.Sound("Assets/BossVoicelines/T5/Worthless.ogg"),
            mixer.Sound("Assets/BossVoicelines/T5/Thats bullshit.ogg"),
        ],
        "death": mixer.Sound("Assets/BossVoicelines/T5/Go die in a hole Suzanne.ogg"),
        "kill": mixer.Sound("Assets/BossVoicelines/T5/Sky news.ogg")
    }
}