"""Registry de vozes americanas.

Usa quantas vozes o roteiro precisar (sem limite artificial de 4).
Prioridade: accent americano. Lily/Alice entram só como extras
quando faltam timbres femininos distintos no mesmo áudio.
"""

from __future__ import annotations

from .models import VoiceProfile

# --- Pool americano (free tier) ---
V_SARAH = "EXAVITQu4vr4xnSDxMaL"
V_JESSICA = "cgSgspJ2msm6clMCkdW9"
V_LAURA = "FGY2WhTYpPnrIDTdsKH5"
V_ADAM = "pNInz6obpgDQGcFmaJgB"
V_ANTONI = "ErXwobaYiN019PkySvjV"
V_BRIAN = "nPczCjzI2devNBz1zQrb"
V_BILL = "pqHfZKP75CvOlQylNhV4"
V_RIVER = "SAz9YHcvj6GT2YYXdXww"
# Extras (mesmo áudio com 5+ falantes femininos)
V_LILY = "pFZP5JQG7iQjIQuC4Bku"
V_ALICE = "Xb7hH8MSUJpSbSDYk0k2"

NARRATOR = VoiceProfile(
    voice_id=V_ADAM,
    name="Adam",
    description="Narrador americano de magazine / documentário",
    stability=0.55,
    similarity_boost=0.75,
    style=0.15,
    speed=0.95,
)

# Americans abroad — 7 speakers, 7 voice_ids distintos
SARAH = VoiceProfile(V_SARAH, "Sarah", "NY→UK, profissional", 0.52, 0.82, 0.25, 0.98)
AMY = VoiceProfile(V_JESSICA, "Jessica", "TN→Thailand, entusiasta", 0.30, 0.85, 0.65, 1.05)
JAYNE = VoiceProfile(V_LAURA, "Laura", "CT→Argentina, calorosa", 0.40, 0.80, 0.45, 1.0)
GABY = VoiceProfile(V_RIVER, "River", "MN→Mexico, foodie", 0.35, 0.78, 0.55, 1.03)
ERIC = VoiceProfile(V_BRIAN, "Brian", "NY→Iceland, seco", 0.48, 0.80, 0.30, 0.97)
CHRISTINA = VoiceProfile(V_LILY, "Lily", "CA→Morocco, curiosa", 0.32, 0.85, 0.50, 1.02)

DOUG = VoiceProfile(
    V_ANTONI, "Antoni", "Doug Pitt: humilde, simpático, pé no chão",
    stability=0.42, similarity_boost=0.80, style=0.40, speed=1.0,
)

INTERVIEWER = VoiceProfile(
    V_JESSICA, "Jessica", "Entrevistadora curiosa e clara",
    stability=0.45, similarity_boost=0.78, style=0.35, speed=1.02,
)
MARJAN = VoiceProfile(
    V_SARAH, "Sarah", "Cirurgiã: confiante, calorosa, profissional",
    stability=0.50, similarity_boost=0.82, style=0.30, speed=0.98,
)

STATS = VoiceProfile(
    V_BILL, "Bill", "Reportagem / estatística",
    stability=0.55, similarity_boost=0.75, style=0.20, speed=0.96,
)
TEEN_A = VoiceProfile(V_JESSICA, "Jessica", "Teen voz A", 0.35, 0.80, 0.45, 1.02)
TEEN_B = VoiceProfile(V_LAURA, "Laura", "Teen voz B", 0.35, 0.80, 0.40, 1.0)
TEEN_C = VoiceProfile(V_SARAH, "Sarah", "Teen voz C", 0.38, 0.78, 0.42, 1.01)

ALEXIS = VoiceProfile(
    V_BILL, "Bill", "Alexis (Ikaria): idoso, trabalhador, sábio",
    stability=0.60, similarity_boost=0.78, style=0.25, speed=0.90,
)
MARIA = VoiceProfile(
    V_LAURA, "Laura", "María (Nicoya): idosa, calorosa, ativa",
    stability=0.55, similarity_boost=0.80, style=0.35, speed=0.92,
)

DAVID = VoiceProfile(
    V_BRIAN, "Brian", "David Guetta: energético, descontraído",
    stability=0.35, similarity_boost=0.80, style=0.55, speed=1.02,
)
MANAGER = VoiceProfile(
    V_BILL, "Bill", "Manager: direto, autoritário",
    stability=0.55, similarity_boost=0.75, style=0.25, speed=1.0,
)

# Chicago — 4 estações + narrador = 5 vozes distintas
SPRING = VoiceProfile(V_LAURA, "Laura", "Chicago spring", 0.40, 0.80, 0.40, 1.0)
SUMMER = VoiceProfile(V_JESSICA, "Jessica", "Chicago summer", 0.32, 0.80, 0.55, 1.03)
FALL = VoiceProfile(V_BRIAN, "Brian", "Chicago fall", 0.35, 0.80, 0.50, 1.05)
WINTER = VoiceProfile(V_ANTONI, "Antoni", "Chicago winter", 0.50, 0.78, 0.25, 0.96)

# Glass Bottle — narrador + mother + walid + prince (4 distintas)
MOTHER = VoiceProfile(V_SARAH, "Sarah", "Mãe idosa: cansada, emotiva", 0.55, 0.82, 0.35, 0.92)
WALID = VoiceProfile(V_ANTONI, "Antoni", "Walid: preguiçoso / ambicioso", 0.40, 0.78, 0.45, 1.0)
PRINCE = VoiceProfile(V_BRIAN, "Brian", "Príncipe: admirado, generoso", 0.35, 0.80, 0.55, 1.02)

HOST = VoiceProfile(V_LAURA, "Laura", "Host engajada / perguntas", 0.35, 0.80, 0.45, 1.02)
GREENBERG = VoiceProfile(V_BRIAN, "Brian", "Psicólogo: calmo, científico", 0.50, 0.80, 0.30, 0.97)
KURT = VoiceProfile(V_BILL, "Bill", "Bio Vonnegut: seco, intelectual", 0.55, 0.78, 0.25, 0.94)
BILLY = VoiceProfile(V_BRIAN, "Brian", "Bio Billy Dee: carismático", 0.40, 0.80, 0.40, 0.98)
ADELE = VoiceProfile(V_JESSICA, "Jessica", "Bio Adele: jovem, clara", 0.38, 0.82, 0.40, 1.0)

# New Year's — intro Adam + 3 personagens distintos
MINA = VoiceProfile(V_LAURA, "Laura", "Mina: frustrada", 0.40, 0.80, 0.45, 1.0)
JENNY = VoiceProfile(V_JESSICA, "Jessica", "Jenny: animada", 0.30, 0.85, 0.60, 1.04)
ANDY = VoiceProfile(V_ANTONI, "Antoni", "Andy DJ: bem-humorado", 0.38, 0.80, 0.45, 1.0)

# Haunted — 3 vozes distintas (+ intro narrator = Adam)
HAUNT_DOC = VoiceProfile(V_BILL, "Bill", "História do hotel", 0.55, 0.75, 0.15, 0.95)
HAUNT_SPOOKY = VoiceProfile(V_RIVER, "River", "Fantasmas: misterioso", 0.45, 0.78, 0.40, 0.94)
GUEST = VoiceProfile(V_BRIAN, "Brian", "Convidado Twitter: casual", 0.35, 0.78, 0.50, 1.02)

# Travers murder
GRANGER = VoiceProfile(V_BILL, "Bill", "Detetive Granger: grave, lento, firme", 0.58, 0.78, 0.22, 0.92)
AMANDA = VoiceProfile(V_LAURA, "Laura", "Amanda: tensa, controlada, depois fria", 0.42, 0.82, 0.35, 0.96)

# Street / cards / people
RECEPTIONIST = VoiceProfile(V_SARAH, "Sarah", "Recepcionista: prática, clara", 0.48, 0.80, 0.28, 1.0)
STUDENT = VoiceProfile(V_ANTONI, "Antoni", "Estudante: animado, depois assustado", 0.36, 0.80, 0.48, 1.02)
JANE = VoiceProfile(V_JESSICA, "Jessica", "Jane Ross: curiosa, nervosa", 0.38, 0.82, 0.42, 1.0)
FORTUNE = VoiceProfile(V_BILL, "Bill", "Cartomante: baixa, misteriosa", 0.62, 0.78, 0.30, 0.90)
DOOR_MAN = VoiceProfile(V_BRIAN, "Brian", "Homem da porta: seco, calmo", 0.50, 0.78, 0.20, 0.98)
LENA = VoiceProfile(V_LAURA, "Laura", "Lena, Ucrânia", 0.40, 0.80, 0.35, 1.0)
RAHIM = VoiceProfile(V_BRIAN, "Brian", "Rahim, Paquistão", 0.45, 0.78, 0.25, 0.98)
NATASHA = VoiceProfile(V_SARAH, "Sarah", "Natasha, Belarus", 0.42, 0.80, 0.32, 1.0)
TARA = VoiceProfile(V_JESSICA, "Jessica", "Tara, Índia", 0.34, 0.82, 0.45, 1.02)
JULIE = VoiceProfile(V_LILY, "Lily", "Julie, Canadá", 0.40, 0.80, 0.35, 1.0)
STEF = VoiceProfile(V_JESSICA, "Jessica", "Stef: jovem, entusiasmada com viagens", 0.32, 0.82, 0.50, 1.03)
FRANCESCA = VoiceProfile(V_LAURA, "Laura", "Francesca: estagiária, confusa", 0.35, 0.80, 0.40, 1.02)
TIPS = VoiceProfile(V_SARAH, "Sarah", "Dicas de trivia: direta", 0.45, 0.78, 0.25, 1.0)
EATER = VoiceProfile(V_ANTONI, "Antoni", "Narrador em primeira pessoa, casual", 0.40, 0.80, 0.35, 1.0)

DEFAULT_CAST: dict[str, VoiceProfile] = {
    "narrator": NARRATOR,
    "sarah": SARAH,
    "amy": AMY,
    "jayne": JAYNE,
    "gaby": GABY,
    "eric": ERIC,
    "christina": CHRISTINA,
    "doug": DOUG,
    "interviewer": INTERVIEWER,
    "marjan": MARJAN,
    "stats": STATS,
    "teen_a": TEEN_A,
    "teen_b": TEEN_B,
    "teen_c": TEEN_C,
    "alexis": ALEXIS,
    "maria": MARIA,
    "david": DAVID,
    "manager": MANAGER,
    "spring": SPRING,
    "summer": SUMMER,
    "fall": FALL,
    "winter": WINTER,
    "mother": MOTHER,
    "walid": WALID,
    "prince": PRINCE,
    "host": HOST,
    "greenberg": GREENBERG,
    "kurt": KURT,
    "billy": BILLY,
    "adele": ADELE,
    "mina": MINA,
    "jenny": JENNY,
    "andy": ANDY,
    "haunt_doc": HAUNT_DOC,
    "haunt_spooky": HAUNT_SPOOKY,
    "guest": GUEST,
    "granger": GRANGER,
    "amanda": AMANDA,
    "receptionist": RECEPTIONIST,
    "student": STUDENT,
    "jane": JANE,
    "fortune": FORTUNE,
    "door_man": DOOR_MAN,
    "lena": LENA,
    "rahim": RAHIM,
    "natasha": NATASHA,
    "tara": TARA,
    "julie": JULIE,
    "stef": STEF,
    "francesca": FRANCESCA,
    "tips": TIPS,
    "eater": EATER,
}


def resolve_voice(
    speaker: str,
    cast: dict[str, VoiceProfile] | None = None,
    overrides: dict | None = None,
) -> VoiceProfile:
    voices = cast or DEFAULT_CAST
    key = speaker.strip().lower()
    if key not in voices:
        raise KeyError(
            f"Speaker '{speaker}' sem voz. Cadastre em voices.DEFAULT_CAST "
            f"ou no JSON do roteiro. Disponíveis: {sorted(voices)}"
        )
    base = voices[key]
    if not overrides:
        return base
    return VoiceProfile(
        voice_id=overrides.get("voice_id", base.voice_id),
        name=overrides.get("name", base.name),
        description=overrides.get("description", base.description),
        stability=float(overrides.get("stability", base.stability)),
        similarity_boost=float(
            overrides.get("similarity_boost", base.similarity_boost)
        ),
        style=float(overrides.get("style", base.style)),
        speed=float(overrides.get("speed", base.speed)),
        use_speaker_boost=bool(
            overrides.get("use_speaker_boost", base.use_speaker_boost)
        ),
    )
