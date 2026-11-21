"""
Simulacion Monte Carlo: views de 3 videos cortos "dopaminicos" de Armani AV
publicados en varias plataformas de video vertical, contadas hasta el 12-dic-2026.

IMPORTANTE: todos los parametros son SUPUESTOS editables, no benchmarks medidos.
No hay datos reales de la cuenta (seguidores, views previas). Cuando existan,
reemplaza MEDIANA_BASE y P_VIRAL con las medianas reales de tus ultimos videos.

Modelo por video v y plataforma p:
  views_vida = base_p * calidad_v * cuenta * ruido_vp * (multiplicador viral si toca)
  views_al_corte = views_vida * (1 - exp(-edad_dias / tau_p))
- calidad_v: comun a todas las plataformas (un buen video rinde mejor en todas).
- cuenta: factor comun a todo (incertidumbre sobre el tamano real de la audiencia).
- viral: Bernoulli(P_VIRAL[p] * calidad relativa) -> Pareto (cola pesada).
"""
import numpy as np
from datetime import date

N = 200_000
SEED = 12
CORTE = date(2026, 12, 12)

# Calendario propuesto (editable): 1 video por semana
PUBLICACIONES = [date(2026, 11, 24), date(2026, 11, 30), date(2026, 12, 6)]

# Escenario: artista emergente, cuenta pequena (<~2k seguidores por red).
# plataforma: (mediana views de vida por video, prob. viral, tau dias de vida util)
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

SIGMA_RUIDO = 0.9     # dispersion lognormal video-plataforma
SIGMA_CALIDAD = 0.6   # dispersion de calidad entre los 3 videos
SIGMA_CUENTA = 0.5    # incertidumbre del tamano real de la audiencia
VIRAL_MIN_X = 10      # un viral multiplica al menos x10 la base
VIRAL_ALPHA = 1.4     # cola Pareto (menor = colas mas gordas)
TOPE_POR_POST = 5_000_000


def simular(rng):
    edades = np.array([(CORTE - d).days for d in PUBLICACIONES], dtype=float)
    nv = len(PUBLICACIONES)
    calidad = rng.lognormal(0, SIGMA_CALIDAD, size=(N, nv))
    cuenta = rng.lognormal(0, SIGMA_CUENTA, size=(N, 1))
    por_plat = {}
    hubo_viral = np.zeros(N, dtype=bool)
    for nombre, (base, pviral, tau) in PLATAFORMAS.items():
        ruido = rng.lognormal(0, SIGMA_RUIDO, size=(N, nv))
        vida = base * calidad * cuenta * ruido
        p = np.clip(pviral * calidad, 0, 0.5)  # mejores videos, mas prob. de viral
        viral = rng.random((N, nv)) < p
        mult = VIRAL_MIN_X * (1 + rng.pareto(VIRAL_ALPHA, size=(N, nv)))
        vida = np.where(viral, vida * mult, vida)
        vida = np.minimum(vida, TOPE_POR_POST)
        acum = vida * (1 - np.exp(-edades / tau))
        por_plat[nombre] = acum.sum(axis=1)
        hubo_viral |= viral.any(axis=1)
    total = sum(por_plat.values())
    return total, por_plat, hubo_viral


def fmt(x):
    return f"{x:,.0f}".replace(",", ".")


def main():
    rng = np.random.default_rng(SEED)
    total, por_plat, hubo_viral = simular(rng)
    q = lambda a, k: np.percentile(a, k)

    print(f"Simulaciones: {fmt(N)} | corte: {CORTE} | publicaciones: "
          + ", ".join(str(d) for d in PUBLICACIONES))
    print("\nTOTAL (3 videos x todas las plataformas)")
    print(f"  P10 {fmt(q(total,10))} | P25 {fmt(q(total,25))} | Mediana {fmt(q(total,50))}"
          f" | P75 {fmt(q(total,75))} | P90 {fmt(q(total,90))} | P99 {fmt(q(total,99))}")
    print(f"  Media {fmt(total.mean())} (inflada por los virales)")
    print("\nProbabilidad de superar:")
    for u in [5_000, 10_000, 25_000, 50_000, 100_000, 250_000, 1_000_000]:
        print(f"  > {fmt(u):>9}: {np.mean(total > u)*100:5.1f}%")
    print(f"  Al menos un post viral (>=x10): {hubo_viral.mean()*100:.1f}%")

    print("\nPor plataforma (suma de 3 videos)")
    print(f"  {'Plataforma':20s} {'P10':>8} {'Mediana':>9} {'P90':>9} {'%total med.':>11}")
    med_tot = sum(np.median(v) for v in por_plat.values())
    for nombre, v in sorted(por_plat.items(), key=lambda kv: -np.median(kv[1])):
        print(f"  {nombre:20s} {fmt(q(v,10)):>8} {fmt(q(v,50)):>9} {fmt(q(v,90)):>9}"
              f" {np.median(v)/med_tot*100:10.0f}%")


if __name__ == "__main__":
    main()
