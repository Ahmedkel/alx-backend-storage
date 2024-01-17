-- SQL script that ranks country origins of bands, ordered by the number:
SELECT origin, COUNT(*) as nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;