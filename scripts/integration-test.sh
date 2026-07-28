#!/usr/bin/env sh
set -eu

curl --fail --silent http://localhost:8080/actuator/health | grep '"status":"UP"'
curl --fail --silent http://localhost:8000/health | grep '"status":"UP"'

curl --fail --silent -X POST http://localhost:8080/api/orders \
  -H 'Content-Type: application/json' \
  -d '{"customerId":"C-100","product":"Laptop","amount":999.99}' | grep '"status":"ACCEPTED"'

curl --fail --silent -X POST http://localhost:8000/api/risk \
  -H 'Content-Type: application/json' \
  -d '{"customer_id":"C-100","amount":999.99,"international":false,"prior_chargebacks":0}' | grep '"approved":true'

echo "Integration tests passed"
