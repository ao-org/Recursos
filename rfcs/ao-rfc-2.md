# Título del RFC: Implementación de Penalizaciones Basadas en Actividad para Experiencia y Oro en el Juego

- Autor: Lucas Recoaro (@recox)
- Fecha: 04/12/2023
- Estado: Borrador

## Resumen
Este RFC propone implementar un sistema en nuestro juego donde los personajes inactivos pierdan un porcentaje de su experiencia y oro después de períodos específicos de inactividad. El objetivo es fomentar la participación frecuente de los jugadores y crear cambios dinámicos en las clasificaciones y la economía del juego.

## Motivación
El juego actualmente enfrenta desafíos con tablas de clasificación estancadas y una economía inflada debido a jugadores inactivos. Esta propuesta busca abordar estos problemas incentivando el juego regular y manteniendo una economía equilibrada.

## Especificación
- Después de 60 días de inactividad, los personajes perderán el 5% de su oro (inventario o banco), semanalmente.
- Después de 30 días de inactividad, los personajes comenzarán a perder el 5% de su experiencia por día.
- Los personajes listados en MAO (MercadoAO) estarán exentos de estas penalizaciones.

## Implementación
Los cambios se implementarán mediante una actualización del lado del servidor. Se integrarán mecanismos para rastrear la actividad del jugador y ajustar los niveles de experiencia y oro.

## Referencias
- Análisis comparativo de mecánicas similares
