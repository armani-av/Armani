"""
Embudo Monte Carlo: views de los 4 videos (calibrado_historial.py) ->
personas unicas alcanzadas -> oyentes el dia del debut -> streams dia 1.

Debut: 3 EPs, 28 canciones en total, el 12-dic-2026 (sabado).

Compara dos versiones de los videos:
  - Sin cierre: los videos no dicen fecha ni nombre.
  - Con cierre: los 4 videos terminan con "12 - 12 - 2026 / Armani AV".
    Efecto modelado: mas gente sabe que buscar (nombre) y cuando (fecha), y el
    interes se concentra en el dia 1. Las views no cambian.

TODAS las tasas de conversion son SUPUESTOS con rango amplio, no benchmarks
medidos. Reemplazalas con datos reales (clics del Linktree, pre-saves, oyentes
mensuales de Spotify for Artists) en cuanto existan.
"""
import numpy as np
import calibrado_historial as ch

N = ch.N
rng = np.random.default_rng(2026)


def lognorm_rango(lo, hi, size=N):
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

# ---- 2. Personas unicas (igual en ambas versiones) ---------------------------
views_por_persona = lognorm_rango(1.3, 2.5)   # rewatch del loop + ver variantes
personas = views / views_por_persona * (1 - 0.10)  # 10% solape entre redes
dilucion = np.clip((views / np.median(views)) ** -0.15, 0.4, 1.5)

SEGUIDORES = 71_000 + 3_500 + 3_500       # TikTok + IG + FB (aprox.)
cuota_spotify = np.clip(rng.normal(0.55, 0.07, N), 0.35, 0.75)

# ---- Streams por oyente el dia 1 (catalogo de 28 canciones) ------------------
tipo = rng.choice(3, size=2_000_000, p=[0.62, 0.28, 0.10])
mezcla = np.choose(tipo, [rng.integers(1, 4, 2_000_000),     # casual 1-3
                          rng.integers(4, 11, 2_000_000),    # interesado 4-10
                          rng.integers(28, 46, 2_000_000)])  # fan: todo + repite
SPL_MEDIO = mezcla.mean()
spl = SPL_MEDIO * lognorm_rango(0.7, 1.4)

VERSIONES = {
    # conv_interes: % de alcanzados que van a escuchar en algun momento
    # pct_dia1: de esos, % que escucha justo el 12-dic
    # base: % de seguidores existentes que escucha el dia 1
    "Sin cierre": dict(conv=(0.002, 0.020), dia1=(0.25, 0.55), base=(0.002, 0.012)),
    "Con cierre 12-12-2026 Armani AV":
                  dict(conv=(0.003, 0.030), dia1=(0.35, 0.70), base=(0.003, 0.016)),
}


def embudo(conv, dia1, base):
    interesados = personas * lognorm_rango(*conv) * dilucion
    oy_videos = interesados * np.clip(lognorm_rango(*dia1), 0, 0.9)
    oy_base = SEGUIDORES * lognorm_rango(*base)
    oy_total = oy_videos + oy_base
    oy_spotify = oy_total * cuota_spotify
    return {
        "Oyentes dia 1 desde los videos": oy_videos,
        "Oyentes dia 1 desde seguidores": oy_base,
        "OYENTES DIA 1 (todas las DSP)": oy_total,
        "Oyentes dia 1 en Spotify": oy_spotify,
        "STREAMS DIA 1 - SPOTIFY": oy_spotify * spl,
        "STREAMS DIA 1 - GLOBAL (todas)": oy_total * spl,
    }


def fmt(x):
    if x >= 1e6:
        return f"{x/1e6:.1f} M"
    if x >= 1e4:
        return f"{x/1e3:.0f} mil"
    return f"{x:,.0f}".replace(",", ".")


def fila(nombre, a):
    q = np.percentile(a, [10, 25, 50, 75, 90, 99])
    print(f"{nombre:34s} " + " ".join(f"{fmt(x):>9}" for x in q))


cab = f"{'Metrica':34s} {'P10':>9} {'P25':>9} {'Mediana':>9} {'P75':>9} {'P90':>9} {'P99':>9}"
print(f"Embudo al 12-dic-2026 | {N:,} simulaciones | streams/oyente medio = {SPL_MEDIO:.1f}\n")
print(cab)
fila("Views de los 4 videos", views)
fila("Personas unicas alcanzadas", personas)

res = {}
for nombre, params in VERSIONES.items():
    res[nombre] = embudo(**params)
    print(f"\n--- {nombre} ---")
    print(cab)
    for k, v in res[nombre].items():
        fila(k, v)

print("\nProbabilidad de superar (streams dia 1):")
print(f"  {'':>10} " + " ".join(f"{n[:14]+' Spot.':>21} {n[:14]+' Glob.':>21}" for n in VERSIONES))
for u in [1_000, 5_000, 10_000, 25_000, 50_000, 100_000, 500_000]:
    celdas = []
    for n in VERSIONES:
        r = res[n]
        celdas += [f"{np.mean(r['STREAMS DIA 1 - SPOTIFY'] > u)*100:20.1f}%",
                   f"{np.mean(r['STREAMS DIA 1 - GLOBAL (todas)'] > u)*100:20.1f}%"]
    print(f"  > {fmt(u):>8} " + " ".join(celdas))
