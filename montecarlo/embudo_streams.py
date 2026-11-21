"""
Embudo Monte Carlo: views de los 4 videos (calibrado_historial.py) ->
personas unicas alcanzadas -> oyentes el dia del debut -> streams dia 1.

Debut: 3 EPs, 28 canciones en total, el 12-dic-2026 (sabado).

TODAS las tasas de conversion son SUPUESTOS con rango amplio, no benchmarks
medidos. Reemplazalas con datos reales (clics del Linktree, pre-saves, oyentes
mensuales de Spotify for Artists) en cuanto existan.
"""
import numpy as np
import calibrado_historial as ch

N = ch.N
rng = np.random.default_rng(2026)


def lognorm_rango(lo, hi, size):
    """Lognormal cuyo P10-P90 aproximado es [lo, hi]."""
    mu = (np.log(lo) + np.log(hi)) / 2
    sigma = (np.log(hi) - np.log(lo)) / (2 * 1.2816)
    return rng.lognormal(mu, sigma, size)


# ---- 1. Views de los videos (mezcla de regimenes de la cuenta) -------------
escalas = {p: ch.media_unitaria(rng, v[1]) for p, v in ch.PLATAFORMAS.items()}
regs = list(ch.REGIMENES.values())
sims = [ch.simular(rng, media, escalas)[0] for media, _ in regs]
pesos = np.array([w for _, w in regs]); pesos /= pesos.sum()
eleccion = rng.choice(len(regs), size=N, p=pesos)
views = np.stack(sims)[eleccion, np.arange(N)]

# ---- 2. Personas unicas ------------------------------------------------------
# Views por persona (rewatch del loop de 15 s + ver varias variantes): 1,3-2,5
views_por_persona = lognorm_rango(1.3, 2.5, N)
solape_entre_redes = 0.10
personas = views / views_por_persona * (1 - solape_entre_redes)

# ---- 3. De persona alcanzada a oyente el dia del debut -----------------------
# % de alcanzados que van a escuchar en algun momento: 0,2%-2% (P10-P90).
# Dilucion: cuando un video se vuelve muy viral llega a publico menos afin.
conv_interes = lognorm_rango(0.002, 0.02, N)
dilucion = np.clip((views / np.median(views)) ** -0.15, 0.4, 1.5)
interesados_videos = personas * conv_interes * dilucion
# De esos, % que escucha justo el dia 1 (pre-save, aviso, video del dia): 25-55%
pct_dia1 = np.clip(lognorm_rango(0.25, 0.55, N), 0, 1)
oyentes_videos = interesados_videos * pct_dia1

# Base de seguidores existente que escucha el dia 1 aunque no vea estos videos
SEGUIDORES = 71_000 + 3_500 + 3_500       # TikTok + IG + FB (aprox.)
oyentes_base = SEGUIDORES * lognorm_rango(0.002, 0.012, N)

oyentes_total = oyentes_videos + oyentes_base

# ---- 4. Reparto por plataforma de streaming ----------------------------------
cuota_spotify = np.clip(rng.normal(0.55, 0.07, N), 0.35, 0.75)
oyentes_spotify = oyentes_total * cuota_spotify

# ---- 5. Streams por oyente el dia 1 (catalogo de 28 canciones) ---------------
# Mezcla: casual (1-3 canciones), interesado (4-10), fan que escucha todo (28-45)
def streams_por_oyente(size):
    tipo = rng.choice(3, size=size, p=[0.62, 0.28, 0.10])
    casual = rng.integers(1, 4, size)
    medio = rng.integers(4, 11, size)
    fan = rng.integers(28, 46, size)
    return np.choose(tipo, [casual, medio, fan])

# media exacta de la mezcla (para escalar sin simular cada oyente)
m = streams_por_oyente(2_000_000).mean()
# incertidumbre del promedio real de esta audiencia (x0,7 - x1,4)
spl = m * lognorm_rango(0.7, 1.4, N)
streams_spotify = oyentes_spotify * spl
streams_global = oyentes_total * spl


def fmt(x):
    if x >= 1e6:
        return f"{x/1e6:.1f} M"
    if x >= 1e4:
        return f"{x/1e3:.0f} mil"
    return f"{x:,.0f}".replace(",", ".")


def fila(nombre, a):
    q = np.percentile(a, [10, 25, 50, 75, 90, 99])
    print(f"{nombre:34s} " + " ".join(f"{fmt(x):>9}" for x in q))


print(f"Embudo al 12-dic-2026 | {N:,} simulaciones | streams/oyente medio = {m:.1f}\n")
print(f"{'Metrica':34s} {'P10':>9} {'P25':>9} {'Mediana':>9} {'P75':>9} {'P90':>9} {'P99':>9}")
fila("Views de los 4 videos", views)
fila("Personas unicas alcanzadas", personas)
fila("Oyentes dia 1 desde los videos", oyentes_videos)
fila("Oyentes dia 1 desde seguidores", oyentes_base)
fila("OYENTES DIA 1 (todas las DSP)", oyentes_total)
fila("Oyentes dia 1 en Spotify", oyentes_spotify)
fila("STREAMS DIA 1 - SPOTIFY", streams_spotify)
fila("STREAMS DIA 1 - GLOBAL (todas)", streams_global)

print("\nProbabilidad de superar (streams dia 1):")
for u in [1_000, 5_000, 10_000, 25_000, 50_000, 100_000, 500_000]:
    print(f"  > {fmt(u):>8}:  Spotify {np.mean(streams_spotify > u)*100:5.1f}%"
          f"   Global {np.mean(streams_global > u)*100:5.1f}%")
