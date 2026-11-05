# Azure Databricks PoC architecture

Interactive architecture pages for an Azure Databricks proof of concept that rebuilds four existing Fabric
workloads, end to end, with Power BI on top.

- **Networking and storage** (`docs/network.html`): classic compute in a VNet-injected workspace with a site-to-site
  VPN, serverless compute (and the Private Link path it needs only to reach on-prem), storage account access,
  and a setup checklist.
- **PoC pipelines** (`docs/pipelines.html`): high-level design for Office Presence, ClickUp Workload,
  Yield Management and Startlap Box CT.

Live: https://koritadenada.github.io/azure-databricks-poc-architecture/

## Controls

Right arrow, Space or click: next step. Left arrow: back. Tabs or 0-9: open a part. `?mode=auto` loops all parts.

## Rebuild

```bash
./scripts/build.sh           # regenerate templates and pages
./scripts/build.sh --shots   # also screenshot every scene and refresh the landing-page thumbnails
```

`scripts/make_templates.py` defines the scenes and captions; the stage, styles and presenter script come from the
`architecture-animated` skill template.

## References

- [VNet injection](https://learn.microsoft.com/en-us/azure/databricks/security/network/classic/vnet-inject)
- [Connect a workspace to an on-premises network](https://learn.microsoft.com/en-us/azure/databricks/security/network/classic/on-prem-network)
- [Serverless private connectivity to resources in your VNet](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/pl-to-internal-network)
- [Serverless firewall for storage (network security perimeter)](https://learn.microsoft.com/en-us/azure/databricks/security/network/serverless-network-security/serverless-firewall)
- [Unity Catalog managed identities](https://learn.microsoft.com/en-us/azure/databricks/connect/unity-catalog/cloud-storage/azure-managed-identities)
- [Lakeflow Connect SQL Server](https://learn.microsoft.com/en-us/azure/databricks/ingestion/lakeflow-connect/sql-server-pipeline)
- [OneLake catalog federation](https://learn.microsoft.com/en-us/azure/databricks/query-federation/onelake)
- [Zerobus Ingest](https://learn.microsoft.com/en-us/azure/databricks/ingestion/zerobus-overview)
- [SQL warehouse types](https://learn.microsoft.com/en-us/azure/databricks/compute/sql-warehouse/warehouse-types)
