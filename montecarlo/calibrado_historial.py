"""
Monte Carlo calibrado a la cuenta real de Armani AV (datos dados por el usuario):
  - Ano pico: >85 M de views y 85k seguidores en TikTok.
  - 2025: 6,3 M de views en TikTok.
  - 2026: sin publicar, videos en privado; hoy 71k seguidores.
  - Reactivacion: ~30k views en los ultimos 2 meses.
  - Instagram y Facebook (cuentas distintas) activadas: 3-4k views.
  - YouTube Shorts: aun sin activar (canal desde cero).

Supuestos NO confirmados (cambialos cuando tengas el dato):
  - Videos publicados en cada periodo -> media de views por video en TikTok.
  - 3-4k en IG/FB se interpreta como views tipicas por video.

Plan: 4 videos cinematograficos IA de ~15 s (oficial + 3 variantes con frase
para compartir), en 9 plataformas, views contadas hasta el 12-dic-2026.

Modelo: el "regimen" de la cuenta (como ahora / nivel 2025 / nivel pico) es la
mayor incertidumbre. Se simula cada regimen y una mezcla ponderada.
"""
import numpy as np
from datetime import date

N = 200_000
SEED = 12
CORTE = date(2026, 12, 12)

# --- Calibracion TikTok: media de views por video segun regimen -------------
VIDEOS_REACTIVACION, VIEWS_REACTIVACION = 10, 30_000      # supuesto: ~10 videos
VIDEOS_2025, VIEWS_2025 = 60, 6_300_000                   # supuesto: ~60 videos
VIDEOS_PICO, VIEWS_PICO = 100, 85_000_000                 # supuesto: ~100 videos

REGIMENES = {  # nombre: (media por video en TikTok, peso en la mezcla)
    "1. Como ahora (reactivacion)":  (VIEWS_REACTIVACION / VIDEOS_REACTIVACION, 0.45),
    "2. Vuelve al nivel de 2025":    (VIEWS_2025 / VIDEOS_2025, 0.40),
    "3. Vuelve al nivel pico":       (VIEWS_PICO / VIDEOS_PICO, 0.15),
}
MEDIA_TIKTOK_HOY = VIEWS_REACTIVACION / VIDEOS_REACTIVACION

# --- Plataformas: (media por video HOY, prob. despegue, tau dias, sensibilidad
#     al regimen). Sensibilidad 1 = escala igual que TikTok; 0 = no escala.
CINE = 2.5  # bonus cinematografico solo en cuentas nuevas sin historial propio
PLATAFORMAS = {
    "TikTok":             (MEDIA_TIKTOK_HOY, 0.060, 2.5, 1.0),
    "Instagram Reels":    (3_500,            0.040, 3.0, 0.5),
    "Facebook Reels":     (3_500,            0.040, 3.0, 0.5),
    "YouTube Shorts":     (300 * CINE * 3,   0.040, 6.0, 0.4),
    "Snapchat Spotlight": (150 * CINE * 3,   0.025, 2.0, 0.3),
    "Kwai":               (150 * CINE * 3,   0.030, 2.5, 0.3),
    "Pinterest (video)":  ( 60 * CINE * 3,   0.010, 20.0, 0.2),
    "X / Twitter":        ( 80 * CINE * 3,   0.010, 1.0, 0.3),
    "Threads":            ( 60 * CINE * 3,   0.010, 1.5, 0.3),
}
# (x3 en cuentas nuevas = media/mediana de una lognormal con colas; ver nota)

CALENDARIO = [  # (nombre, fecha, es_variante)
    ("Oficial",    date(2026, 11, 24), False),
    ("Variante 1", date(2026, 11, 27), True),
    ("Variante 2", date(2026, 12, 1),  True),
    ("Variante 3", date(2026, 12, 5),  True),
]
FATIGA, X_SHARE = 0.80, 1.4
SIGMA_RUIDO, SIGMA_CREATIVO, SIGMA_VARIANTE, SIGMA_CUENTA = 0.9, 0.6, 0.3, 0.4
VIRAL_MIN_X, VIRAL_ALPHA, TOPE = 10, 1.4, 50_000_000


def media_unitaria(rng, pv, n=400_000):
    """Media de views de vida de un video oficial con escala base = 1."""
    calidad = rng.lognormal(0, SIGMA_CREATIVO, n) * rng.lognormal(0, SIGMA_VARIANTE, n)
    v = calidad * rng.lognormal(0, SIGMA_CUENTA, n) * rng.lognormal(0, SIGMA_RUIDO, n)
    hit = rng.random(n) < np.clip(pv * calidad, 0, 0.6)
    v = np.where(hit, v * VIRAL_MIN_X * (1 + rng.pareto(VIRAL_ALPHA, n)), v)
    return v.mean()


def simular(rng, media_tiktok, escalas_unit):
    factor = media_tiktok / MEDIA_TIKTOK_HOY
    edades = np.array([(CORTE - d).days for _, d, _ in CALENDARIO], float)
    es_var = np.array([v for _, _, v in CALENDARIO])
    nv = len(CALENDARIO)
    calidad = rng.lognormal(0, SIGMA_CREATIVO, (N, 1)) * rng.lognormal(0, SIGMA_VARIANTE, (N, nv))
    cuenta = rng.lognormal(0, SIGMA_CUENTA, (N, 1))
    f_base = np.where(es_var, FATIGA, 1.0)
    f_share = np.where(es_var, X_SHARE, 1.0)
    por = {}
    for p, (media, pv, tau, sens) in PLATAFORMAS.items():
        escala = media * factor ** sens / escalas_unit[p]
        vida = escala * f_base * calidad * cuenta * rng.lognormal(0, SIGMA_RUIDO, (N, nv))
        hit = rng.random((N, nv)) < np.clip(pv * f_share * calidad, 0, 0.6)
        vida = np.where(hit, vida * VIRAL_MIN_X * (1 + rng.pareto(VIRAL_ALPHA, (N, nv))), vida)
        por[p] = (np.minimum(vida, TOPE) * (1 - np.exp(-edades / tau))).sum(1)
    return sum(por.values()), por


def fmt(x):
    if x >= 1e6:
        return f"{x/1e6:.1f} M"
    return f"{x/1e3:.0f} mil" if x >= 1e3 else f"{x:.0f}"


def main():
    rng = np.random.default_rng(SEED)
    escalas = {p: media_unitaria(rng, v[1]) for p, v in PLATAFORMAS.items()}
    umbrales = [100_000, 250_000, 500_000, 1_000_000, 3_000_000, 10_000_000]

    res = {}
    for nombre, (media, peso) in REGIMENES.items():
        res[nombre] = simular(rng, media, escalas)

    # Mezcla: cada simulacion cae en un regimen segun su peso
    pesos = np.array([w for _, w in REGIMENES.values()])
    eleccion = rng.choice(len(pesos), size=N, p=pesos / pesos.sum())
    tots = np.stack([r[0] for r in res.values()])
    mezcla = tots[eleccion, np.arange(N)]
    res["MEZCLA (45% / 40% / 15%)"] = (mezcla, None)

    print(f"4 videos x 9 plataformas | corte {CORTE} | {N:,} simulaciones\n")
    print(f"{'Escenario':32s} {'P10':>8} {'Mediana':>8} {'P90':>8} {'P99':>8} | "
          + " ".join(f"{'>'+fmt(u):>8}" for u in umbrales))
    for k, (tot, _) in res.items():
        q = np.percentile(tot, [10, 50, 90, 99])
        print(f"{k:32s} " + " ".join(f"{fmt(x):>8}" for x in q) + " | "
              + " ".join(f"{np.mean(tot > u)*100:7.0f}%" for u in umbrales))

    for k in REGIMENES:
        print(f"\nPor plataforma — {k} (P10 / mediana / P90)")
        for p, v in sorted(res[k][1].items(), key=lambda kv: -np.median(kv[1])):
            q = np.percentile(v, [10, 50, 90])
            print(f"  {p:20s} {fmt(q[0]):>8} {fmt(q[1]):>8} {fmt(q[2]):>8}")


if __name__ == "__main__":
    main()
