# Public Data Portal integration map

This directory stores metadata and integration definitions, not bulk government datasets or credentials.

## Current scope
- Railway/public transport: TAGO train and subway
- Mobility: transport links, traffic flow, CCTV, frequent routes, traffic-impact assessments
- Land/GIS: land-use planning, cadastral attributes, POI
- Real estate/buildings: official land prices, land transactions, building register, apartment basics
- Regulation/policy: MOLIT regulation guide and policy-analysis data
- Tourism: tourism information, regional visitor indicators, wellness tourism
- Business support: SME program notices

## Security
Set DATA_GO_KR_KEY only in the local environment. Never commit service keys, downloaded internal documents, generated reports, or local RAG databases.

## Activation
Each catalog entry remains disabled until its current Data Portal endpoint and required parameters are verified after the user's API application is approved.
