"""
Simulacion Monte Carlo: views de los videos cortos de Armani AV publicados en
varias plataformas de video vertical, contadas hasta el 12-dic-2026.

Formato v2: 4 videos cinematograficos generados con IA (~15 s):
  - 1 video oficial
  - 3 variantes del mismo material con distintas frases pensadas para compartir

IMPORTANTE: todos los parametros son SUPUESTOS editables, no benchmarks medidos.
No hay datos reales de la cuenta (seguidores, views previas). Cuando existan,
reemplaza MEDIANA_BASE y P_VIRAL con las medianas reales de tus ultimos videos.

Modelo por video v y plataforma p:
  views_vida = base_p * x_base * creativo * variante_v * cuenta * ruido_vp
               (* multiplicador viral si despega)
  views_al_corte = views_vida * (1 - exp(-edad_dias / tau_p))
- creativo: comun a los 4 videos (mismo material visual -> muy correlacionados).
- variante_v: efecto propio de cada frase (dispersion menor).
- fatiga: las variantes repiten material; parte del publico ya lo vio.
- cuenta: incertidumbre comun sobre el tamano real de la audiencia.
- despegue: Bernoulli(P_VIRAL * x_viral * calidad) -> Pareto (cola pesada).
"""
import numpy as np
from datetime import date

N = 200_000
SEED = 12
CORTE = date(2026, 12, 12)

# plataforma: (mediana de views de vida por video "estandar", prob. de despegue, tau dias)
# Base: artista emergente, cuenta pequena (<~2k seguidores por red).
PLATAFORMAS = {
    "TikTok":             (400, 0.030, 2.5),
    "Instagram Reels":    (250, 0.020, 3.0),
    "YouTube Shorts":     (300, 0.025, 6.0),
    "Facebook Reels":     (200, 0.020, 3.0),
    "Snapchat Spotlight": (150, 0.015, 2.0),
    "Kwai":               (150, 0.020, 2.5),
    "Pinterest (video)":  ( 60, 0.008, 20.0),
    "X / Twitter":        ( 80, 0.008, 1.0),
    "Threads":            ( 60, 0.008, 1.5),
}

# Calendario v2: oficial primero, luego una variante cada ~3-4 dias
CALENDARIO_V2 = [
    ("Oficial",    date(2026, 11, 24), False),
    ("Variante 1", date(2026, 11, 27), True),
    ("Variante 2", date(2026, 12, 1),  True),
    ("Variante 3", date(2026, 12, 5),  True),
]
CALENDARIO_V1 = [
    ("Video 1", date(2026, 11, 24), False),
    ("Video 2", date(2026, 11, 30), False),
    ("Video 3", date(2026, 12, 6),  False),
]

# Escenarios. x_base: multiplicador de views base por mejor retencion
# (cinematografico, 15 s, rewatch). x_viral: multiplicador de prob. de despegue.
# x_share: extra de despegue en variantes con frase para compartir.
# fatiga: factor de views base de cada variante por repetir material.
ESCENARIOS = {
    "A. Calculo anterior (3 videos estandar)":
        dict(cal=CALENDARIO_V1, x_base=1.0, x_viral=1.0, x_share=1.0, fatiga=1.0),
    "B. Cinematografico conservador":
        dict(cal=CALENDARIO_V2, x_base=1.8, x_viral=1.5, x_share=1.2, fatiga=0.75),
    "C. Cinematografico central":
        dict(cal=CALENDARIO_V2, x_base=2.5, x_viral=2.0, x_share=1.4, fatiga=0.80),
    "D. Cinematografico optimista":
        dict(cal=CALENDARIO_V2, x_base=4.0, x_viral=3.0, x_share=1.6, fatiga=0.85),
}

SIGMA_RUIDO = 0.9     # dispersion lognormal video-plataforma
SIGMA_CREATIVO = 0.6  # que tan bien funciona el material visual (comun a los 4)
SIGMA_VARIANTE = 0.3  # efecto propio de cada frase
SIGMA_CUENTA = 0.5    # incertidumbre del tamano real de la audiencia
VIRAL_MIN_X = 10      # un despegue multiplica al menos x10 la base
VIRAL_ALPHA = 1.4     # cola Pareto (menor = colas mas gordas)
TOPE_POR_POST = 5_000_000


def simular(rng, cal, x_base, x_viral, x_share, fatiga):
    edades = np.array([(CORTE - d).days for _, d, _ in cal], dtype=float)
    es_var = np.array([v for _, _, v in cal])
    nv = len(cal)
    creativo = rng.lognormal(0, SIGMA_CREATIVO, size=(N, 1))
    variante = rng.lognormal(0, SIGMA_VARIANTE, size=(N, nv))
    calidad = creativo * variante
    cuenta = rng.lognormal(0, SIGMA_CUENTA, size=(N, 1))
    f_base = np.where(es_var, fatiga, 1.0)
    f_share = np.where(es_var, x_share, 1.0)
    por_plat = {}
    despegue = np.zeros(N, dtype=bool)
    for nombre, (base, pviral, tau) in PLATAFORMAS.items():
        ruido = rng.lognormal(0, SIGMA_RUIDO, size=(N, nv))
        vida = base * x_base * f_base * calidad * cuenta * ruido
        p = np.clip(pviral * x_viral * f_share * calidad, 0, 0.5)
        hit = rng.random((N, nv)) < p
        mult = VIRAL_MIN_X * (1 + rng.pareto(VIRAL_ALPHA, size=(N, nv)))
        vida = np.minimum(np.where(hit, vida * mult, vida), TOPE_POR_POST)
        por_plat[nombre] = (vida * (1 - np.exp(-edades / tau))).sum(axis=1)
        despegue |= hit.any(axis=1)
    total = sum(por_plat.values())
    return total, por_plat, despegue


def fmt(x):
    return f"{x:,.0f}".replace(",", ".")


UMBRALES = [10_000, 25_000, 50_000, 100_000, 250_000, 1_000_000]


def main():
    rng = np.random.default_rng(SEED)
    res = {k: simular(rng, **v) for k, v in ESCENARIOS.items()}
    print(f"Simulaciones: {fmt(N)} por escenario | corte: {CORTE}\n")

    print(f"{'Escenario':42s} {'P10':>8} {'Mediana':>9} {'P90':>9} {'P99':>10}")
    for k, (tot, _, _) in res.items():
        pc = np.percentile(tot, [10, 50, 90, 99])
        print(f"{k:42s} {fmt(pc[0]):>8} {fmt(pc[1]):>9} {fmt(pc[2]):>9} {fmt(pc[3]):>10}")

    print("\nProbabilidad de superar:")
    print(f"{'Escenario':42s} " + " ".join(f"{'>'+fmt(u):>10}" for u in UMBRALES) + "  despegue")
    for k, (tot, _, hit) in res.items():
        print(f"{k:42s} " + " ".join(f"{np.mean(tot > u)*100:9.1f}%" for u in UMBRALES)
              + f"  {hit.mean()*100:6.1f}%")

    k = "C. Cinematografico central"
    _, por_plat, _ = res[k]
    print(f"\nPor plataforma, escenario {k} (suma de 4 videos)")
    print(f"  {'Plataforma':20s} {'P10':>8} {'Mediana':>9} {'P90':>9}")
    for nombre, v in sorted(por_plat.items(), key=lambda kv: -np.median(kv[1])):
        pc = np.percentile(v, [10, 50, 90])
        print(f"  {nombre:20s} {fmt(pc[0]):>8} {fmt(pc[1]):>9} {fmt(pc[2]):>9}")


if __name__ == "__main__":
    main()
