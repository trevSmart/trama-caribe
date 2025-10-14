# Agents de Trama Caribe

Aquest document descriu els diferents agents utilitzats en el projecte Trama Caribe, les seves funcionalitats i com interactuen entre ells.

## Estructura d'Agents

El projecte utilitza una arquitectura basada en agents per gestionar diferents aspectes de la plataforma. Cada agent té una responsabilitat específica i es comunica amb altres agents segons sigui necessari.

### Agent Principal (Bot)

L'agent principal és responsable de:
- Rebre i processar missatges de Slack
- Coordinar la comunicació entre els diferents agents especialitzats
- Gestionar el flux de treball principal

## Configuració dels Agents

Per configurar els agents, cal definir les variables d'entorn necessàries al fitxer `.env`. Aquestes inclouen:

```
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_APP_TOKEN=xapp-your-token
```

## Desenvolupament de Nous Agents

Per desenvolupar nous agents per al sistema:

1. Crear una nova classe que hereti de la classe base `Agent`
2. Implementar els mètodes necessaris segons la funcionalitat requerida
3. Registrar l'agent al sistema principal

## Integració amb Slack

Els agents es comuniquen amb Slack utilitzant la llibreria `slack-bolt`, que permet:
- Respondre a esdeveniments de Slack
- Enviar missatges als canals
- Processar interaccions amb elements interactius

## Desplegament

Els agents es despleguen com a part del sistema complet. Consulteu la documentació principal per obtenir instruccions detallades sobre el desplegament.
