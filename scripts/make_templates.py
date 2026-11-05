"""Generate docs/network_template.html and docs/pipelines_template.html from the skill's hybrid template.

The skill template provides the stage, styles and presenter/auto-play script; this file only defines the
header tabs, the scenes and the captions of each page. Rebuild the pages afterwards with scripts/build.sh.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = pathlib.Path.home() / ".claude/skills/architecture-animated/assets/hybrid_template.html"

EXTRA_CSS = """
  /* added for this repo */
  .node.v { flex-direction:column; align-items:flex-start; gap:8px; padding:14px 16px; }
  .node.v .ico { flex:0 0 auto; }
  .zone.sub { background:#FFFFFF; border-color:#B9C7CD; }
  .zone.sub .zl { color:var(--muted); border-color:#B9C7CD; }
  .zone .zl { color:var(--muted); }
  .chip.note { border-color:var(--navy); color:var(--navy); font-weight:600; }
  .li { display:flex; justify-content:space-between; align-items:center; gap:14px; font-size:14px; padding:9px 12px;
    border-radius:8px; border:1px solid var(--line); background:var(--wash); margin-top:8px; }
  .li span { font-weight:700; }
  .li em { font-style:normal; color:var(--muted); font-size:13px; text-align:right; }
  .zc.big .zh { font-size:17px; }
  .zc.big .zh svg { width:30px; height:30px; }
"""


def node(cls, x, y, w, h, icon, name, desc, t, badge="", badge_on=False):
    b = f'<span class="badge{" on" if badge_on else ""}">{badge}</span>' if badge else ""
    return (f'<div class="node {cls} rev" data-t="{t}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">{b}'
            f'<div class="ico">{{{{{icon}}}}}</div><div><div class="name">{name}</div><div class="desc">{desc}</div></div></div>')


def wire(pid, d, t, hot=False):
    return f'<path id="{pid}" class="wire{" hot" if hot else ""}" pathLength="1" d="{d}" data-t="{t}"/>'


def pulse(pid, t, dur="1.2s"):
    return (f'<circle class="pulse" r="5" data-t="{t}"><animateMotion dur="{dur}" repeatCount="indefinite" begin="indefinite">'
            f'<mpath href="#{pid}"/></animateMotion></circle>')


def zone(cls, x, y, w, h, label, t=0):
    return f'<div class="zone {cls} rev" data-t="{t}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px"><span class="zl">{label}</span></div>'


def title(k, h):
    return f'<div class="stitle rev" data-t="0"><div class="k">{k}</div><div class="h">{h}</div></div>'


def svg(*items):
    return '<svg class="wires" viewBox="0 0 1280 720">' + "".join(items) + "</svg>"


def scene(i, dur, *parts):
    return f'<section class="scene" data-scene="{i}" data-dur="{dur}">\n' + "\n".join(parts) + "\n</section>"


def blk(i, go, x, w, title_, body, icons, tag_cls, tag, rows, t):
    r = "".join(f'<div><span>{a}</span><b{" class=\"always\"" if hot else ""}>{b}</b></div>' for a, b, hot in rows)
    ic = "".join("{{" + n + "}}" for n in icons)
    return (f'<div class="blk rev" data-t="{t}" data-go="{go}" style="left:{x}px;width:{w}px">'
            f'<div class="num">{i}</div><div class="bt">{title_}</div><div class="bd">{body}</div>'
            f'<div class="icons">{ic}</div><span class="wtag {tag_cls}">{tag}</span>'
            f'<div class="run"><div class="lbl">What runs</div>{r}</div></div>')


CHECK = ('<svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="#00A06B" stroke-width="2"/>'
         '<path d="M7 12.5l3.2 3.2L17 9" stroke="#00A06B" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def ok(x, y, text, t):
    return f'<div class="nocall rev" data-t="{t}" style="left:{x}px;top:{y}px">{CHECK}{text}</div>'


# ---------------------------------------------------------------- page 1: networking and storage
NET_PILLS = ["Overview", "Classic", "Serverless", "Storage", "Checklist"]

net = []
net.append(scene(0, 8000,
    title("Azure Databricks PoC", "Where compute runs, and how it reaches your data"),
    blk(1, 1, 40, 360, "Classic compute", "Runs in your VNet. Pulls on-prem data over your site-to-site VPN",
        ["I_JOBS", "I_VPN", "I_ONPREM"], "aws", "In your Azure subscription",
        [("On-prem sources", "VPN gateway", False), ("Internet", "firewall or NAT gateway", False)], 300),
    blk(2, 2, 460, 360, "Serverless compute", "Runs in the Databricks serverless plane: transformations and the SQL warehouse for Power BI",
        ["I_SERVERLESS", "I_DBSQL", "I_REPORT"], "dbx", "Managed by Databricks",
        [("Power BI, transformations", "no network setup", True), ("On-prem", "only via Private Link", False)], 1200),
    blk(3, 3, 880, 360, "Storage accounts", "Your ADLS Gen2. Unity Catalog governs access with a managed identity",
        ["I_UC", "I_KEY", "I_S3"], "aws", "In your Azure subscription",
        [("Access", "Access Connector", False), ("With a storage firewall", "subnets or NSP", False)], 2100),
))

net.append(scene(1, 9000,
    title("1 &middot; Classic compute", "Classic compute: your VNet, your VPN"),
    zone("", 24, 176, 216, 432, "Your premises"),
    zone("aws", 256, 176, 772, 432, "Your Azure subscription"),
    zone("sub", 272, 204, 280, 388, "Hub VNet"),
    zone("sub", 572, 204, 440, 388, "Databricks VNet &middot; VNet injection"),
    zone("", 1044, 176, 212, 432, "Internet"),
    svg(wire("c1", "M 588 366 L 536 366", 2100, True),
        wire("c2", "M 288 366 L 228 366", 2400, True),
        wire("c3", "M 588 344 C 562 344, 562 270, 536 270", 3800),
        wire("c4", "M 588 390 C 562 390, 562 496, 536 496", 5100),
        wire("c5", "M 412 546 L 412 574 L 1150 574 L 1150 452", 5600),
        '<text class="wlabel" x="790" y="566" text-anchor="middle" data-t="5800">internet-bound traffic</text>',
        pulse("c1", 2300, "1.0s"), pulse("c2", 2600, "1.0s"), pulse("c5", 5900, "3.0s")),
    node("db", 588, 320, 408, 92, "I_JOBS", "Classic compute",
         "Lakeflow Connect gateway and classic jobs, in two subnets", 400, "no public IPs", True),
    node("ext", 288, 320, 248, 92, "I_VPN", "VPN gateway", "Site-to-site VPN to your premises", 1600, "new or existing"),
    node("ext", 36, 311, 192, 110, "I_ONPREM", "SQL Server", "Office Presence and Yield Management sources", 1900),
    node("ext", 288, 226, 248, 82, "I_DNS", "DNS servers", "Resolve the on-prem hostnames", 3500),
    node("ext", 288, 446, 248, 100, "I_FIREWALL", "Firewall", "Internet egress, or a NAT gateway on the Databricks subnets", 4900),
    node("ext", 1058, 300, 184, 152, "I_GLOBE", "Internet", "Databricks control plane, package repositories, ClickUp API", 5300),
    node("ext", 588, 446, 408, 100, "I_ROUTE", "Route table on both subnets",
         "On-prem ranges via the VPN gateway, internet via the firewall or NAT gateway", 7100),
))

net.append(scene(2, 9000,
    title("2 &middot; Serverless compute", "Serverless: no setup, unless it must reach on-prem"),
    zone("dbx", 24, 176, 240, 432, "Databricks serverless"),
    zone("aws", 284, 176, 712, 300, "Your Azure subscription"),
    zone("", 1016, 176, 240, 300, "Your premises"),
    svg(wire("s6", "M 300 545 L 248 545", 2000),
        wire("s1", "M 144 306 L 144 352", 3900, True),
        wire("s2", "M 248 402 L 300 402", 4400, True),
        wire("s3", "M 510 402 L 536 402", 5900, True),
        wire("s4", "M 746 402 L 772 402", 6400, True),
        wire("s5", "M 980 402 L 1032 402", 6900, True),
        pulse("s2", 4600, "0.8s"), pulse("s5", 7100, "0.8s")),
    node("db", 40, 210, 208, 96, "I_SERVERLESS", "Serverless compute", "Jobs, pipelines, notebooks", 300),
    node("db", 40, 494, 208, 96, "I_DBSQL", "Serverless SQL warehouse", "Queried by Power BI", 1300),
    node("ext", 300, 500, 250, 90, "I_REPORT", "Power BI service", "DirectQuery or Import", 1700),
    ok(580, 527, "No network setup for Power BI and transformations", 2400),
    f'<div class="chip note rev" data-t="3500" style="left:300px;top:216px">Only needed if serverless must reach on-prem</div>',
    node("db", 40, 352, 208, 100, "I_PLINK", "NCC private endpoint", "Rule with your on-prem hostnames", 3700),
    node("ext", 300, 352, 210, 100, "I_PLINK", "Private Link Service", "On an internal Standard Load Balancer", 4200),
    node("ext", 536, 352, 210, 100, "I_VM", "Forwarder VM", "Relays the traffic to on-prem", 5700),
    node("ext", 772, 352, 208, 100, "I_VPN", "VPN gateway", "The same site-to-site VPN", 6200),
    node("ext", 1032, 352, 208, 100, "I_ONPREM", "SQL Server", "On-prem sources", 6700),
))

net.append(scene(3, 8500,
    title("3 &middot; Storage accounts", "Storage: your ADLS, governed by Unity Catalog"),
    zone("dbx", 24, 176, 420, 432, "Databricks"),
    zone("aws", 464, 176, 792, 432, "Your Azure subscription"),
    svg(wire("t1", "M 428 260 L 484 260", 2000, True),
        wire("t2", "M 804 260 C 842 260, 842 360, 880 360", 2300, True),
        wire("t3", "M 428 396 L 484 396", 3900),
        wire("t4", "M 804 396 L 880 396", 4100),
        wire("t5", "M 428 532 L 484 532", 5900),
        wire("t6", "M 804 532 C 842 532, 842 440, 880 440", 6100),
        pulse("t2", 2500, "1.2s")),
    node("hero", 880, 300, 360, 192, "I_S3", "Your ADLS Gen2 storage accounts",
         "Managed tables, external locations and the workspace storage. Firewall setting: enabled from selected networks", 300),
    node("db", 40, 210, 388, 100, "I_UC", "Unity Catalog", "Storage credential and external locations: who can read which path", 1300),
    node("ext", 484, 210, 320, 100, "I_KEY", "Access Connector", "Managed identity with a storage role: no keys", 1700),
    node("db", 40, 346, 388, 100, "I_JOBS", "Classic compute", "Runs in your VNet", 3300),
    node("ext", 484, 346, 320, 100, "I_ROUTE", "Allow your VNet subnets", "Service endpoint or private endpoint on the storage account", 3600, "only with a firewall"),
    node("db", 40, 482, 388, 100, "I_SERVERLESS", "Serverless compute", "SQL warehouse, jobs, pipelines", 5300),
    node("ext", 484, 482, 320, 100, "I_SHIELD", "Network security perimeter",
         "Allow the AzureDatabricksServerless service tag, or use an NCC private endpoint", 5600, "only with a firewall"),
))


def li(name, detail, t):
    return f'<div class="li rev" data-t="{t}"><span>{name}</span><em>{detail}</em></div>'


net.append(scene(4, 8000,
    title("4 &middot; Setup checklist", "What to set up, and when"),
    f'<div class="zc big rev" data-t="300" style="left:40px;top:196px;width:590px;border-top-color:var(--navy)">'
    f'<div class="zh">{{{{I_CHECK}}}}For the PoC</div>'
    + li("Premium workspace, VNet injection", "two subnets in your VNet", 900)
    + li("Secure cluster connectivity", "no public IPs on the clusters", 1200)
    + li("Peering to your hub", "use remote gateways / gateway transit", 1500)
    + li("Route table on both subnets", "on-prem via VPN, internet via firewall or NAT", 1800)
    + li("DNS", "resolve on-prem names, forward Azure names to Azure DNS", 2100)
    + li("Access Connector + storage credential", "Unity Catalog access to your ADLS", 2400)
    + "</div>",
    f'<div class="zc big rev" data-t="3500" style="left:650px;top:196px;width:590px;border-top-color:var(--lava)">'
    f'<div class="zh">{{{{I_SHIELD}}}}Only if you need it</div>'
    + li("Serverless must reach on-prem", "NCC + Private Link Service + forwarder VM", 3900)
    + li("Storage firewall enabled", "network security perimeter for serverless", 4200)
    + li("Workspace behind inbound Private Link", "Power BI VNet data gateway", 4500)
    + li("Fabric workspace blocks public access", "resource instance rule for the Access Connector", 4800)
    + "</div>",
))

NET_CAPS = """
  0: [[0, 'Two kinds of compute: <b>classic in your VNet</b>, serverless managed by Databricks']],
  1: [[0, 'Classic compute runs <b>in your VNet</b>, peered to your hub'],
      [1500, 'Traffic to on-prem stays private: <b>through the VPN gateway</b>'],
      [3400, 'Your <b>DNS</b> resolves the on-prem hostnames'],
      [4800, 'Internet traffic goes <b>through your firewall</b>, or a NAT gateway if there is none'],
      [7000, 'One <b>route table</b> on the Databricks subnets decides which path']],
  2: [[0, 'Serverless runs <b>outside your VNet</b>, in the Databricks serverless plane'],
      [1200, 'Power BI and transformations need <b>no network setup</b>'],
      [3400, 'To reach on-prem: an <b>NCC private endpoint</b> to a Private Link Service in your VNet'],
      [5600, 'A small <b>forwarder VM</b> relays it over your VPN. Not needed for the PoC']],
  3: [[0, 'Your data stays in <b>your own storage accounts</b>'],
      [1200, 'Unity Catalog reads through an <b>Access Connector</b>: a managed identity, no keys'],
      [3200, 'Storage firewall on? Classic compute is allowed <b>from your VNet subnets</b>'],
      [5200, 'Serverless needs a <b>network security perimeter</b> with the Databricks service tag, or a private endpoint']],
  4: [[0, 'What to set up for the PoC, and what <b>only when needed</b>'],
      [800, 'For the PoC: <b>one VNet-injected workspace</b>, peered to your hub'],
      [3400, 'Only if needed: <b>serverless to on-prem, firewalls, Private Link</b>']]
"""

# ---------------------------------------------------------------- page 2: PoC pipelines
# column x positions and widths (vertical cards)
C1, C2, C3, C4, C5 = 40, 280, 520, 762, 1032
W1, W2, W3, W4, W5 = 186, 196, 196, 210, 208
TOP, MID, BOT, H = 208, 316, 432, 150


def v(cls, x, y, w, icon, name, desc, t, badge="", on=False):
    return node(cls + " v", x, y, w, H, icon, name, desc, t, badge, on)


def zones3(src="Source"):
    return [zone("", 24, 176, 218, 432, src), zone("dbx", 262, 176, 730, 432, "Azure Databricks"), zone("", 1012, 176, 244, 432, "Power BI")]


# shared wire shapes
W_C1_C2TOP = "M 226 391 C 253 391, 253 283, 280 283"
W_C2TOP_C2BOT = "M 378 358 L 378 432"
W_C2BOT_C3 = "M 476 507 C 498 507, 498 391, 520 391"
W_C3_C4TOP = "M 716 391 C 739 391, 739 283, 762 283"
W_C4 = "M 867 358 L 867 432"
W_C4_C5 = "M 972 507 C 1002 507, 1002 391, 1032 391"

pip = []
pip.append(scene(0, 8000,
    title("PoC pipelines", "Four Fabric workloads, rebuilt on Azure Databricks"),
    blk(1, 1, 40, 290, "Office Presence", "One SQL Server database, pulled", ["I_LFC", "I_PIPELINES", "I_REPORT"], "aws", "Classic + serverless",
        [("Ingestion", "Lakeflow Connect", False), ("Serves", "SQL warehouse", False)], 300),
    blk(2, 2, 340, 290, "ClickUp Workload", "ClickUp API, pulled by your Python notebook", ["I_API", "I_JOBS", "I_REPORT"], "dbx", "Serverless",
        [("Ingestion", "serverless job", False), ("VPN", "not needed", True)], 900),
    blk(3, 3, 640, 290, "Yield Management", "On-prem databases plus data in Fabric", ["I_ONPREM", "I_UC", "I_REPORT"], "aws", "Classic + serverless",
        [("On-prem", "classic, over VPN", False), ("Fabric", "OneLake federation", False)], 1500),
    blk(4, 4, 940, 290, "Startlap Box CT", "Daily history plus today, pushed every 10 minutes", ["I_STREAMING", "I_DELTA", "I_DBSQL"], "dbx", "Serverless",
        [("Push", "Zerobus Ingest", False), ("Queries", "SQL warehouse", False)], 2100),
))

pip.append(scene(1, 9500,
    title("1 &middot; Office Presence", "Office Presence: SQL Server to Power BI"),
    *zones3(),
    svg(wire("p1", W_C1_C2TOP, 1600, True), wire("p2", W_C2TOP_C2BOT, 3300), wire("p3", W_C2BOT_C3, 4900),
        wire("p4", W_C3_C4TOP, 5500), wire("p5", W_C4, 7100), wire("p6", W_C4_C5, 7600, True),
        pulse("p1", 1800), pulse("p6", 7800)),
    v("ext", C1, MID, W1, "I_DB", "SQL Server", "Office Presence database, pulled", 300, "on-prem: to confirm"),
    v("db", C2, TOP, W2, "I_LFC", "Ingestion gateway", "Lakeflow Connect: reads changes with change tracking or CDC", 1300, "classic, your VNet", True),
    v("db", C2, BOT, W2, "I_LFC", "Ingestion pipeline", "Applies the changes to streaming tables", 3100, "serverless"),
    v("db", C3, MID, W3, "I_PIPELINES", "Lakeflow pipeline", "Silver and gold tables, with data quality checks", 4700, "serverless"),
    v("db", C4, TOP, W4, "I_METRIC", "Metric view", "Office Presence KPIs, defined once", 5300),
    v("db", C4, BOT, W4, "I_DBSQL", "SQL warehouse", "Serverless, serves Power BI", 6900, "serverless"),
    v("ext", C5, MID, W5, "I_REPORT", "Office Presence report", "DirectQuery or Import", 7400),
))

pip.append(scene(2, 8500,
    title("2 &middot; ClickUp Workload", "ClickUp Workload: API to Power BI, all serverless"),
    *zones3(),
    svg(wire("q1", "M 226 391 L 280 391", 1600, True), wire("q2", "M 476 391 L 520 391", 3500),
        wire("q3", W_C3_C4TOP, 4900), wire("q4", W_C4, 5300), wire("q5", W_C4_C5, 5800, True),
        pulse("q1", 1800), pulse("q5", 6000)),
    v("ext", C1, MID, W1, "I_API", "ClickUp API", "Tasks and workload, over REST", 300),
    v("db", C2, MID, W2, "I_JOBS", "Lakeflow Job", "Your Python notebook, on a schedule. Token in a secret scope", 1300, "serverless", True),
    ok(280, 500, "No VPN needed: ClickUp is a public API", 2300),
    v("db", C3, MID, W3, "I_PIPELINES", "Lakeflow pipeline", "Raw API responses to silver and gold", 3300, "serverless"),
    v("db", C4, TOP, W4, "I_METRIC", "Metric view", "Workload KPIs, defined once", 4700),
    v("db", C4, BOT, W4, "I_DBSQL", "SQL warehouse", "Serverless, serves Power BI", 5100, "serverless"),
    v("ext", C5, MID, W5, "I_REPORT", "ClickUp Workload report", "DirectQuery or Import", 5600),
))

pip.append(scene(3, 9500,
    title("3 &middot; Yield Management", "Yield Management: on-prem and Fabric, one model"),
    *zones3("Sources"),
    svg(wire("y1", "M 226 283 L 280 283", 1700, True), wire("y2", "M 226 507 L 280 507", 3300, True),
        wire("y3", "M 476 283 C 498 283, 498 391, 520 391", 4900), wire("y4", W_C2BOT_C3, 5000),
        wire("y5", W_C3_C4TOP, 6500), wire("y6", W_C4, 6900), wire("y7", W_C4_C5, 7400, True),
        pulse("y1", 1900), pulse("y2", 3500), pulse("y7", 7600)),
    v("ext", C1, TOP, W1, "I_ONPREM", "On-prem databases", "Several sources, pulled over the VPN", 300),
    v("ext", C1, BOT, W1, "I_TILES", "Fabric data", "Lakehouse or Warehouse in OneLake", 400, "to confirm"),
    v("db", C2, TOP, W2, "I_LFC", "Lakeflow Connect", "Or JDBC, on classic compute in your VNet", 1500, "classic, your VNet", True),
    v("db", C2, BOT, W2, "I_UC", "OneLake federation", "Foreign catalog in Unity Catalog: read-only, no copy", 3100),
    v("db", C3, MID, W3, "I_PIPELINES", "Lakeflow pipeline", "Joins all sources into one yield model", 4700, "serverless"),
    v("db", C4, TOP, W4, "I_METRIC", "Metric views", "Yield KPIs, one definition for every report", 6300),
    v("db", C4, BOT, W4, "I_DBSQL", "SQL warehouse", "Serverless, serves Power BI", 6700, "serverless"),
    v("ext", C5, MID, W5, "I_REPORT", "Yield Management report", "DirectQuery or Import", 7200),
))

pip.append(scene(4, 9500,
    title("4 &middot; Startlap Box CT", "Startlap Box CT: history plus today, always current"),
    *zones3(),
    svg(wire("z1", W_C1_C2TOP, 1500, True), wire("z2", "M 476 283 L 520 283", 2200, True),
        wire("z3", "M 560 358 C 560 400, 420 390, 420 432", 3400), wire("z4", "M 476 507 L 520 507", 3900),
        wire("z5", "M 716 283 L 762 283", 5300, True), wire("z6", "M 716 507 C 739 507, 739 305, 762 305", 5500),
        wire("z7", W_C4, 6900), wire("z8", W_C4_C5, 7400, True),
        pulse("z1", 1700, "1.0s"), pulse("z2", 2400, "0.8s"), pulse("z5", 5600, "0.8s"), pulse("z8", 7600)),
    v("ext", C1, MID, W1, "I_DB", "Your producer", "Pushes today's records every 10 minutes", 300, "to confirm"),
    v("db", C2, TOP, W2, "I_STREAMING", "Zerobus Ingest", "Push API (SDK or REST): records land in Delta within seconds", 1300, "serverless", True),
    v("db", C3, TOP, W3, "I_DELTA", "today", "Today's records, updated every 10 minutes", 2000),
    v("db", C2, BOT, W2, "I_JOBS", "Nightly job", "Moves the closed day into history", 3600, "on schedule"),
    v("db", C3, BOT, W3, "I_DELTA", "history", "All days up to yesterday", 4100),
    v("db", C4, TOP, W4, "I_SYNC", "Lambda view", "history UNION ALL today: one source for the report", 5100),
    v("db", C4, BOT, W4, "I_DBSQL", "SQL warehouse", "Serverless. Lakehouse//RT (Beta) if many users", 6700, "serverless"),
    v("ext", C5, MID, W5, "I_REPORT", "Startlap Box CT report", "DirectQuery: always current", 7200),
))

PIP_PILLS = ["Overview", "Office Presence", "ClickUp", "Yield Mgmt", "Startlap Box CT"]
PIP_CAPS = """
  0: [[0, 'Four Fabric workloads, rebuilt <b>end to end</b> on Azure Databricks']],
  1: [[0, 'Office Presence: one <b>SQL Server</b> database, pulled'],
      [1200, 'Lakeflow Connect: the <b>gateway runs on classic compute</b> in your VNet, over the VPN'],
      [3000, 'A <b>serverless</b> ingestion pipeline applies the changes to Delta tables'],
      [4600, 'A Lakeflow pipeline builds <b>silver and gold</b>; a metric view defines the KPIs'],
      [6800, 'Power BI queries a <b>serverless SQL warehouse</b>']],
  2: [[0, 'ClickUp Workload: data pulled from the <b>ClickUp API</b>'],
      [1200, 'Your Python notebook runs as a <b>serverless Lakeflow Job</b>, on a schedule'],
      [3200, 'A Lakeflow pipeline turns the raw responses into <b>silver and gold</b>'],
      [4600, 'A metric view defines the KPIs; Power BI queries the <b>SQL warehouse</b>']],
  3: [[0, 'Yield Management: <b>several sources</b>, on-prem and in Fabric'],
      [1400, 'On-prem databases come in over the VPN, on <b>classic compute</b>'],
      [3000, 'Fabric data is read in place with <b>OneLake catalog federation</b>: no copy'],
      [4600, 'One Lakeflow pipeline joins them into a <b>single yield model</b>'],
      [6200, 'Metric views keep <b>one definition</b> per KPI for Power BI']],
  4: [[0, 'Startlap Box CT: today\\'s records are <b>pushed every 10 minutes</b>'],
      [1200, '<b>Zerobus Ingest</b> writes them straight into a Delta table, within seconds'],
      [3200, 'A nightly job moves the closed day into <b>history</b>'],
      [5000, 'The <b>lambda view</b> unions history and today: one source for the report'],
      [6600, 'Frequent DirectQuery hits a <b>serverless SQL warehouse</b>']]
"""


def page(base, page_title, brand, pills, scenes, caps):
    html = base
    html = html.replace("<title>Serving from your own infrastructure</title>", f"<title>{page_title}</title>")
    html = html.replace('<div class="t">Serving from your own infrastructure</div>', f'<div class="t">{brand}</div>')
    pill_html = "\n".join(
        f'      <div class="pill" data-p="{i}"><b>{"&#8635;" if i == 0 else i}</b>{p}</div>' for i, p in enumerate(pills))
    html = re.sub(r'<div class="pills">.*?</div>\n  </div>', f'<div class="pills">\n{pill_html}\n    </div>\n  </div>', html, count=1, flags=re.S)
    a = html.index("  <!-- ============ OVERVIEW")
    b = html.index('  <div class="cap">')
    html = html[:a] + "\n\n".join(scenes) + "\n\n" + html[b:]
    html = re.sub(r"const CAPS = \{.*?\n\};", "const CAPS = {" + caps + "};", html, count=1, flags=re.S)
    html = html.replace("</style>", EXTRA_CSS + "</style>", 1)
    assert "Serving from your own" not in html
    return html


def main():
    base = BASE.read_text()
    out = ROOT / "docs"
    (out / "network_template.html").write_text(
        page(base, "Azure Databricks PoC: networking and storage", "Networking and storage", NET_PILLS, net, NET_CAPS))
    (out / "pipelines_template.html").write_text(
        page(base, "Azure Databricks PoC: pipelines", "PoC pipelines", PIP_PILLS, pip, PIP_CAPS))
    idx = (pathlib.Path.home() / ".claude/skills/architecture-animated/assets/index_template.html").read_text()
    vals = {
        "PAGE_TITLE": "Azure Databricks PoC architecture",
        "HEADLINE": "Azure Databricks PoC architecture",
        "WHAT": "the networking setup and the four PoC pipelines",
        "PAGE_1": "network", "LABEL_1": "Networking and storage", "KICKER_1": "Setup",
        "TITLE_1": "Classic, serverless and storage",
        "DESC_1": "How classic and serverless compute reach on-prem sources, the internet and your storage accounts, plus a setup checklist.",
        "PAGE_2": "pipelines", "LABEL_2": "4 pipelines", "KICKER_2": "PoC",
        "TITLE_2": "PoC pipelines",
        "DESC_2": "High-level design for Office Presence, ClickUp Workload, Yield Management and Startlap Box CT, each ending in Power BI.",
        "REPO_URL": "https://github.com/koritadenada/azure-databricks-poc-architecture",
        "REPO_LABEL": "github.com/koritadenada/azure-databricks-poc-architecture",
    }
    idx = idx.replace("Code, notebooks and deployment instructions:", "Source:")
    for k, val in vals.items():
        idx = idx.replace("{{" + k + "}}", val)
    left = re.findall(r"\{\{[A-Z_0-9]+\}\}", idx)
    assert not left, left
    (out / "index.html").write_text(idx)
    print("templates and index written")


if __name__ == "__main__":
    main()
