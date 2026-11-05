# grocerymate-stats

Ein serverloser Statistik-Endpunkt für GroceryMate auf AWS, komplett mit Terraform bereitgestellt. `GET /stats` liefert Kennzahlen als JSON. Die Datenbank-Konfiguration kommt aus dem SSM Parameter Store.

Die Kennzahlen sind derzeit simuliert (`"db_status": "simuliert"`): Die Lambda-Funktion liest zwar die Konfiguration, baut aber keine Datenbankverbindung auf.

## Architektur

```
API Gateway -> Lambda -> SSM Parameter Store
```

- **API Gateway (HTTP API):** stellt die Route `GET /stats` auf der Stage `prod` bereit.
- **Lambda (`grocerymate-stats`, Python 3.11):** verarbeitet die Anfrage und gibt die Statistik als JSON zurück.
- **SSM Parameter Store:** enthält die Konfiguration unter `/grocerymate/*`. Die IAM-Rolle der Lambda-Funktion darf nur diese Parameter lesen.

## Voraussetzungen

- Terraform
- AWS CLI mit konfiguriertem Profil `default` (Region `eu-central-1`)
- Die folgenden SSM-Parameter vom Typ `String`. Terraform legt sie nicht selbst an, ohne sie antwortet der Endpunkt mit HTTP 500:
  - `/grocerymate/db_host`
  - `/grocerymate/db_name`
  - `/grocerymate/db_user`

Beispiel für einen Parameter:

```bash
aws ssm put-parameter --name /grocerymate/db_name --type String --value grocerymate --region eu-central-1
```

## Starten

```bash
terraform init
terraform apply
```

Nach `terraform apply` steht die URL des Endpunkts in der Ausgabe `stats_url`.

## Abbauen

```bash
terraform destroy
```

Die SSM-Parameter bleiben dabei erhalten, weil sie nicht von Terraform verwaltet werden.
