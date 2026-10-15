"""Computer Networks curriculum seed data for SkillForge — expert-level, gradual difficulty.

Expected sibling schema (tables created by migration m1n2curr001_curriculum):
  curriculum_domains   (slug PK, name, icon, description)
  curriculum_modules   (slug PK, domain_slug FK, name, order_index, description)
  curriculum_lessons   (slug PK, module_id FK, title, content, order_index, ...)
  curriculum_questions (id PK, domain_slug, module_slug, lesson_id FK,
                        difficulty 1-10, prompt, choices JSON, answer_index,
                        explanation, company_tags JSON)

Usage:
  from app.adapters.outbound.cn_curriculum_seed import seed, CURRICULUM
  seed(session)       # idempotent ORM insert (deterministic uuid5 ids)
  python -m app.adapters.outbound.cn_curriculum_seed   # verify counts

Content module -> sibling module mapping (sibling seeded 5 CN modules):
  osi-tcpip      -> network-models
  ip-subnetting  -> ip-addressing
  tcp-udp        -> tcp-udp
  app-layer      -> application-layer
  routing-switching -> routing-switching
  net-security   -> application-layer   (TLS/HTTPS live at the app layer)
  advanced       -> network-models      (SDN/5G are network architectures)

All content is original — classic networking concepts explained in
SkillForge's own words, with hand-verified subnetting math.
"""

from __future__ import annotations

import json
import sys
import uuid as _uuid
from datetime import datetime, timezone as _tz


# ---------------------------------------------------------------------------
# Compact builders
# ---------------------------------------------------------------------------

def Q(prompt, choices, answer_index, difficulty, explanation, companies):
    """One MCQ. choices: exactly 4 strings. answer_index: 0-3."""
    assert len(choices) == 4, f"need 4 choices: {prompt[:40]}"
    assert 0 <= answer_index <= 3
    assert 1 <= difficulty <= 10
    return {
        "qtype": "mcq",
        "prompt": prompt,
        "choices": choices,
        "answer_index": answer_index,
        "difficulty": difficulty,
        "explanation": explanation,
        "company_tags": companies,
    }


def L(slug, title, theory_md, questions):
    assert 5 <= len(questions) <= 8, f"lesson {slug}: need 5-8 questions"
    diffs = [q["difficulty"] for q in questions]
    assert max(diffs) - min(diffs) >= 4, f"lesson {slug}: difficulty span too narrow"
    return {
        "slug": slug,
        "title": title,
        "theory_md": theory_md,
        "difficulty_min": min(diffs),
        "difficulty_max": max(diffs),
        "questions": questions,
    }


def M(slug, name, description, lessons):
    return {"slug": slug, "name": name, "description": description,
            "lessons": lessons}


# ---------------------------------------------------------------------------
# DOMAIN
# ---------------------------------------------------------------------------

DOMAIN = {
    "slug": "cn",
    "name": "Computer Networks",
    "icon": "🌐",
    "description": (
        "Asked in EVERY interview. 7 modules, 41 lessons, 250+ questions — "
        "from 'what is OSI' to subnetting math, TLS handshakes and SDN, "
        "difficulty rising gradually 1 to 10 inside every lesson."
    ),
}

SIBLING_DOMAIN_SLUG = "cn"
MODULE_MAP = {
    "osi-tcpip": "network-models",
    "ip-subnetting": "ip-addressing",
    "tcp-udp": "tcp-udp",
    "app-layer": "application-layer",
    "routing-switching": "routing-switching",
    "net-security": "application-layer",
    "advanced": "network-models",
}


# ---------------------------------------------------------------------------
# MODULE 1 — OSI & TCP/IP (7 lessons)
# ---------------------------------------------------------------------------

_osi_tcpip = M("osi-tcpip", "OSI & TCP/IP Models",
    "The 7-layer OSI model, the 4-layer TCP/IP model, and how data gets wrapped (encapsulation) as it travels.",
[

L("osi-overview", "What is the OSI Model?",
"""## The OSI model in one minute

The **OSI (Open Systems Interconnection)** model splits networking into
**7 layers**. Each layer does one job and talks only to the layers
directly above and below it. This separation lets vendors build
interoperable hardware and software.

## The 7 layers (top to bottom)

| # | Layer | Job |
|---|-------|-----|
| 7 | Application | What the user sees: HTTP, DNS, FTP |
| 6 | Presentation | Data format: encryption, compression, encoding |
| 5 | Session | Manages conversations: start/stop sessions |
| 4 | Transport | End-to-end delivery: TCP/UDP, ports |
| 3 | Network | Addressing & routing: IP |
| 2 | Data Link | Hop-to-hop: MAC addresses, Ethernet, switches |
| 1 | Physical | Bits on wire: cables, hubs, signals |

## Mnemonic (top → bottom)

**A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing
""",
[
Q("How many layers does the OSI model have?",
  ["5", "4", "7", "8"], 2, 1,
  "OSI has exactly 7 layers, from Physical (1) to Application (7).",
  ["TCS", "Infosys", "Wipro"]),
Q("Which OSI layer is responsible for end-to-end delivery using ports?",
  ["Network layer", "Transport layer", "Session layer", "Data Link layer"], 1, 2,
  "Layer 4 (Transport) provides end-to-end delivery; TCP/UDP ports identify the receiving application.",
  ["Accenture", "Cognizant"]),
Q("At which layer do MAC addresses operate?",
  ["Network", "Transport", "Data Link", "Physical"], 2, 3,
  "MAC addresses are Layer 2 (Data Link) — used for hop-to-hop delivery on a LAN.",
  ["TCS", "HCL"]),
Q("Which layer handles encryption and data compression?",
  ["Session", "Presentation", "Application", "Transport"], 1, 4,
  "Layer 6 (Presentation) translates data formats: encryption, compression, character encoding.",
  ["Infosys", "Tech Mahindra"]),
Q("A router operates primarily at which OSI layer?",
  ["Layer 2", "Layer 3", "Layer 4", "Layer 7"], 1, 5,
  "Routers forward by IP address — Layer 3 (Network). Switches are Layer 2.",
  ["Cisco", "Juniper"]),
Q("Why was the OSI model created?",
  ["To make networks faster", "To standardize how different vendors' equipment interoperates",
   "To replace TCP/IP", "To add security to networks"], 1, 7,
  "OSI is a reference model for interoperability — real networks mostly run TCP/IP, but OSI is the common vocabulary.",
  ["Amazon", "Microsoft"]),
Q("Which device works at ALL seven OSI layers?",
  ["Switch", "Router", "Hub", "Gateway"], 3, 9,
  "A gateway translates between different protocols, so it must understand every layer; switches/routers stop at 2/3.",
  ["Cisco", "Google"]),
]),

L("osi-layers-7-5", "Layers 7–5: Application, Presentation, Session",
"""## Layer 7 — Application

Closest to the user. Protocols: **HTTP** (web), **DNS** (names),
**FTP** (files), **SMTP** (mail). Note: this is NOT your web app —
it's the *protocol* your app speaks.

## Layer 6 — Presentation

The translator. Jobs:
- **Encoding**: ASCII, UTF-8, JPEG, MP3
- **Encryption**: TLS/SSL lives here conceptually
- **Compression**: gzip, zip

## Layer 5 — Session

Manages *conversations* between applications:
- Establishes, maintains, terminates sessions
- **Checkpoints**: resume a download from where it stopped
- Example: a video call session, an RPC session
""",
[
Q("DNS operates at which OSI layer?",
  ["Transport", "Network", "Application", "Session"], 2, 1,
  "DNS is an application-layer (L7) protocol — it serves user applications.",
  ["TCS", "Infosys"]),
Q("TLS/SSL encryption is conceptually associated with which layer?",
  ["Network", "Presentation", "Data Link", "Physical"], 1, 3,
  "Encryption/format translation is the Presentation layer's job (L6).",
  ["Wipro", "Accenture"]),
Q("What is the main job of the Session layer?",
  ["Routing packets", "Managing dialogue: setup, maintenance, teardown of sessions",
   "Error detection", "Bit transmission"], 1, 4,
  "L5 manages sessions between applications, including checkpoints for recovery.",
  ["Cognizant", "HCL"]),
Q("Which of these is NOT an application-layer protocol?",
  ["HTTP", "FTP", "SMTP", "TCP"], 3, 5,
  "TCP is Transport (L4). HTTP, FTP, SMTP are all L7.",
  ["Amazon", "TCS"]),
Q("A resumed file download continues from a checkpoint. Which layer concept is this?",
  ["Flow control", "Session recovery via checkpoints", "Congestion control", "Fragmentation"], 1, 7,
  "Checkpoints are a Session-layer (L5) mechanism for resuming interrupted transfers.",
  ["Microsoft", "Google"]),
Q("Why do we say a web browser is NOT the Application layer?",
  ["Browsers are hardware", "The browser is software using HTTP; HTTP is the L7 protocol",
   "Browsers use TCP only", "Browsers bypass OSI"], 1, 9,
  "L7 means the *protocol* (HTTP), not the end-user program that speaks it.",
  ["Atlassian", "Flipkart"]),
]),

L("osi-layer-4", "Layer 4: Transport — TCP & UDP, Ports",
"""## The Transport layer's promise

Layer 4 gives **end-to-end** delivery between *processes* (not just hosts).
The magic ingredient: **port numbers** (0–65535).

- **Well-known ports**: 0–1023 (HTTP 80, HTTPS 443, DNS 53, SSH 22, FTP 21)
- **Registered**: 1024–49151
- **Dynamic/private**: 49152–65535

## TCP vs UDP (preview — full module later)

| | TCP | UDP |
|---|---|---|
| Reliable? | Yes (ACKs, retransmission) | No (fire and forget) |
| Ordered? | Yes | No |
| Speed | Slower | Faster |
| Use | Web, email, files | Video calls, DNS, gaming |

A **socket** = IP address + port. That's how your OS knows which app
gets which packet.
""",
[
Q("What is the port number for HTTPS?",
  ["80", "443", "22", "53"], 1, 1,
  "HTTPS = 443, HTTP = 80, SSH = 22, DNS = 53.",
  ["TCS", "Infosys", "Wipro"]),
Q("Which range contains well-known ports?",
  ["0–1023", "1024–49151", "49152–65535", "0–255"], 0, 2,
  "Well-known ports are 0–1023, assigned by IANA for standard services.",
  ["Accenture"]),
Q("What does a socket uniquely identify?",
  ["A router", "An IP + port combination (one endpoint of a connection)",
   "A cable", "A DNS record"], 1, 4,
  "Socket = IP address + port number — identifies one end of a transport connection.",
  ["Amazon", "Microsoft"]),
Q("Why does UDP have no connection setup?",
  ["It is unreliable by design — no handshake, just sends datagrams",
   "It uses ports differently", "It runs at Layer 3", "It is encrypted"], 0, 5,
  "UDP is connectionless: no handshake, no ACKs — minimal overhead, maximal speed.",
  ["Google", "Cisco"]),
Q("Two browser tabs connect to the same web server. How does the server tell their traffic apart?",
  ["Different IP addresses", "Different source ports on the client side",
   "Different protocols", "It cannot"], 1, 7,
  "Each TCP connection is identified by the 4-tuple (src IP, src port, dst IP, dst port) — source ports differ.",
  ["Microsoft", "Atlassian"]),
Q("How many usable port numbers exist per IP address?",
  ["1024", "65535", "65536", "32768"], 2, 9,
  "Ports are 16-bit: 0–65535 = 65536 total (port 0 is reserved, so 65535 usable).",
  ["Goldman Sachs", "Google"]),
]),

L("osi-layer-3", "Layer 3: Network — IP Addressing & Routing",
"""## The Network layer's job

Get a packet from **any source to any destination** across many networks.
Two key tools:

1. **Logical addressing (IP)**: every host gets a globally meaningful address
2. **Routing**: routers pick the best path hop by hop

## Key insight: hop-by-hop

Unlike Transport (end-to-end), Layer 3 works **hop by hop**. Each router
looks at the destination IP, consults its **routing table**, and forwards
the packet to the next hop. No router knows the full path.

## IP versions

- **IPv4**: 32-bit (4.3 billion addresses — exhausted, hence NAT)
- **IPv6**: 128-bit (340 undecillion — effectively infinite)
""",
[
Q("What is the primary job of the Network layer?",
  ["Reliable delivery", "Routing packets across networks using logical addressing",
   "Framing bits", "Session management"], 1, 1,
  "L3 (Network) routes packets between networks using IP addresses.",
  ["TCS", "Infosys"]),
Q("How does a router decide where to forward a packet?",
  ["It knows the full path", "It consults its routing table for the best next hop",
   "It broadcasts everywhere", "It asks the sender"], 1, 3,
  "Forwarding is hop-by-hop: each router picks only the next hop from its table.",
  ["Cisco", "Juniper"]),
Q("How many bits is an IPv4 address?",
  ["16", "32", "64", "128"], 1, 2,
  "IPv4 = 32 bits (e.g. 192.168.1.1). IPv6 = 128 bits.",
  ["Wipro", "HCL"]),
Q("Why was NAT introduced?",
  ["To make networks faster", "IPv4 addresses ran out — NAT lets many private hosts share one public IP",
   "To encrypt traffic", "To replace DNS"], 1, 5,
  "NAT (Network Address Translation) multiplexes private addresses behind public ones — the main IPv4 life-support.",
  ["Amazon", "Accenture"]),
Q("Which statement about hop-by-hop vs end-to-end is TRUE?",
  ["TCP is hop-by-hop", "IP routing is hop-by-hop; TCP reliability is end-to-end",
   "Both are end-to-end", "Both are hop-by-hop"], 1, 7,
  "Each router only chooses the next hop (hop-by-hop); TCP's ACKs run between the original endpoints (end-to-end).",
  ["Microsoft", "Google"]),
Q("A packet travels through 5 routers. How many routing decisions are made?",
  ["1", "5", "10", "0 — the sender decides"], 1, 9,
  "Each of the 5 routers makes its own independent next-hop decision.",
  ["Cisco", "Arista"]),
]),

L("osi-layers-2-1", "Layers 2 & 1: Data Link and Physical",
"""## Layer 2 — Data Link

Delivers **frames** between two nodes on the *same* link (hop-to-hop).

- **MAC addresses**: 48-bit hardware addresses (e.g. `AA:BB:CC:11:22:33`)
- **Switches** learn MAC → port mappings and forward frames
- **Error detection**: CRC checksums (detect, usually don't correct)
- Sublayers: LLC + MAC

## Layer 1 — Physical

Raw **bits** as signals: voltage, light pulses, radio waves.
Devices: **hubs** (dumb repeaters — one collision domain),
cables (twisted pair, fiber), connectors.

## The classic interview trio

| Device | Layer | Smart? |
|---|---|---|
| Hub | 1 | No — repeats to all ports |
| Switch | 2 | Yes — learns MACs, forwards selectively |
| Router | 3 | Yes — routes by IP between networks |
""",
[
Q("What is the size of a MAC address?",
  ["32 bits", "48 bits", "64 bits", "128 bits"], 1, 1,
  "MAC = 48 bits, written as 6 hex pairs like AA:BB:CC:11:22:33.",
  ["TCS", "Infosys"]),
Q("How does a switch differ from a hub?",
  ["No difference", "A switch learns MAC addresses and forwards only to the right port; a hub repeats to all",
   "A hub is faster", "Switches use IP addresses"], 1, 3,
  "Hubs flood every frame everywhere (one collision domain); switches forward selectively.",
  ["Cisco", "Wipro"]),
Q("What does the CRC in a frame do?",
  ["Encrypts data", "Detects transmission errors", "Routes the frame", "Compresses data"], 1, 4,
  "CRC is an error-DETECTION code at Layer 2; bad frames are dropped.",
  ["Accenture", "HCL"]),
Q("Which device creates separate collision domains per port?",
  ["Hub", "Repeater", "Switch", "Modem"], 2, 5,
  "Each switch port is its own collision domain; a hub shares one across all ports.",
  ["Juniper", "TCS"]),
Q("ARP resolves which mapping?",
  ["Domain name to IP", "IP address to MAC address", "Port to service", "MAC to vendor"], 1, 7,
  "ARP (Address Resolution Protocol) maps a Layer-3 IP to a Layer-2 MAC on the local network.",
  ["Amazon", "Microsoft", "Google"]),
Q("If two hosts have the same MAC on one LAN, what happens?",
  ["Nothing", "Frames may go to the wrong host — switches get confused",
   "The network gets faster", "IP addresses change"], 1, 9,
  "MACs must be unique per LAN; duplicates corrupt the switch's forwarding table.",
  ["Cisco", "Arista"]),
]),

L("tcpip-model", "The TCP/IP Model (4 Layers)",
"""## TCP/IP: the model that actually runs the internet

While OSI is the textbook, **TCP/IP is what routers really speak**.
It collapses OSI's 7 layers into 4:

| TCP/IP layer | ≈ OSI layers |
|---|---|
| Application | 7 + 6 + 5 (App, Presentation, Session) |
| Transport | 4 (TCP/UDP) |
| Internet | 3 (IP) |
| Network Access | 2 + 1 (Data Link + Physical) |

## Why TCP/IP won

- **It was running code first** (ARPANET, 1983) — OSI arrived later as a paper standard
- Simpler, pragmatic, "rough consensus and running code"
- Protocols first (TCP, IP, UDP), model documented afterwards

Interviews love: *"Compare OSI and TCP/IP"* — answer with the table above
plus "OSI is prescriptive (7 strict layers), TCP/IP is descriptive."
""",
[
Q("How many layers does the TCP/IP model have?",
  ["7", "5", "4", "3"], 2, 1,
  "TCP/IP has 4 layers: Application, Transport, Internet, Network Access.",
  ["TCS", "Infosys"]),
Q("Which OSI layers map to TCP/IP's Application layer?",
  ["Only Layer 7", "Layers 5, 6, 7", "Layers 3, 4", "Layer 4 only"], 1, 3,
  "TCP/IP's Application layer absorbs OSI's top three (Session, Presentation, Application).",
  ["Wipro", "Accenture"]),
Q("Why did TCP/IP beat OSI in practice?",
  ["It has more layers", "It was working code deployed first; OSI was a later paper standard",
   "It is more secure", "It uses fewer addresses"], 1, 5,
  "Running code beats perfect specs — TCP/IP ran the ARPANET years before OSI was finalized.",
  ["Google", "Microsoft"]),
Q("The 'Internet' layer of TCP/IP corresponds to which OSI layer?",
  ["Transport", "Network", "Data Link", "Session"], 1, 4,
  "TCP/IP Internet layer ≈ OSI Network layer (L3) — IP addressing and routing.",
  ["Cisco", "HCL"]),
Q("Which statement is TRUE?",
  ["OSI came before TCP/IP", "TCP/IP protocols existed before the TCP/IP model was formally described",
   "OSI has 4 layers", "TCP/IP was designed by ISO"], 1, 7,
  "TCP/IP grew organically from ARPANET protocols; the 4-layer model was documented to describe what already worked.",
  ["Amazon", "Atlassian"]),
Q("A protocol suite is described as 'descriptive not prescriptive'. What does that mean?",
  ["It has no rules", "It describes existing working protocols rather than mandating a strict design",
   "It is slower", "It needs no addresses"], 1, 9,
  "TCP/IP documents reality; OSI prescribes how things *should* be built.",
  ["Flipkart", "Google"]),
]),

L("encapsulation", "Encapsulation — How Data Gets Wrapped",
"""## Wrapping at every layer (sender side)

As data goes DOWN the stack, each layer adds its header (sometimes trailer):

```
Application data
  → [TCP header | data]              = SEGMENT   (L4)
  → [IP header | TCP header | data]  = PACKET    (L3)
  → [Eth header | IP | TCP | data | FCS] = FRAME (L2)
  → bits on the wire                              (L1)
```

## Unwrapping (receiver side)

The receiver strips headers bottom-up: NIC checks the frame,
IP reads the packet, TCP reads the segment, the app gets pure data.

## PDU names (interview favorite!)

| Layer | PDU name |
|---|---|
| Transport (4) | **Segment** (TCP) / Datagram (UDP) |
| Network (3) | **Packet** |
| Data Link (2) | **Frame** |
| Physical (1) | **Bits** |

**MTU** (Maximum Transmission Unit): biggest frame a link allows
(Ethernet = 1500 bytes). Bigger packets get **fragmented** at L3.
""",
[
Q("What is the PDU at the Network layer called?",
  ["Segment", "Packet", "Frame", "Bits"], 1, 1,
  "L3 PDU = packet. Segment = L4, frame = L2, bits = L1.",
  ["TCS", "Infosys"]),
Q("What is the PDU of the Transport layer when using TCP?",
  ["Packet", "Frame", "Segment", "Datagram"], 2, 2,
  "TCP's PDU is a segment; UDP's is a datagram.",
  ["Wipro", "Accenture"]),
Q("What is the MTU of standard Ethernet?",
  ["512 bytes", "1500 bytes", "9000 bytes", "64 bytes"], 1, 3,
  "Ethernet MTU = 1500 bytes (payload). Jumbo frames go to 9000.",
  ["Cisco", "Juniper"]),
Q("What happens when a packet exceeds the link MTU?",
  ["It is dropped silently", "It is fragmented into smaller pieces",
   "It is compressed", "It takes a different route"], 1, 5,
  "IP fragmentation splits oversized packets; the receiver reassembles them.",
  ["Amazon", "Microsoft"]),
Q("Which header is added FIRST during encapsulation?",
  ["Ethernet", "IP", "TCP", "FCS trailer"], 2, 7,
  "Encapsulation goes top-down: the Transport (TCP) header is added before Network (IP) and Data Link (Ethernet).",
  ["Google", "Cisco"]),
Q("The FCS trailer is added at which layer and why?",
  ["L3 for routing", "L2 for error detection",
   "L4 for ordering", "L7 for encryption"], 1, 9,
  "Frame Check Sequence (CRC) trailer at Layer 2 lets the receiver detect corrupted frames.",
  ["Arista", "Juniper"]),
]),
])


# ---------------------------------------------------------------------------
# MODULE 2 — IP ADDRESSING & SUBNETTING (7 lessons)
# ---------------------------------------------------------------------------

_ip_subnetting = M("ip-subnetting", "IP Addressing & Subnetting",
    "IPv4 classes, CIDR, subnet mask math (all hand-verified), VLSM, NAT and IPv6 basics.",
[

L("ipv4-basics", "IPv4 Addresses & Classes",
"""## IPv4 anatomy

An IPv4 address is **32 bits**, written as 4 decimal octets:
`192.168.1.1` = `11000000.10101000.00000001.00000001`

Part is the **network** portion, part is the **host** portion.
The split point decides how many networks vs hosts you get.

## The old class system (A–E)

| Class | First octet | Default mask | Networks | Hosts/net |
|---|---|---|---|---|
| A | 1–126 | /8 (255.0.0.0) | 126 | ~16.7M |
| B | 128–191 | /16 (255.255.0.0) | 16K | 65K |
| C | 192–223 | /24 (255.255.255.0) | 2M | 254 |
| D | 224–239 | multicast | — | — |
| E | 240–255 | experimental | — | — |

Note: **127.x.x.x is loopback** (127.0.0.1 = yourself), not Class A usable.
Classful addressing is obsolete (replaced by CIDR), but interviews still ask it.
""",
[
Q("How many bits is an IPv4 address?",
  ["16", "32", "48", "128"], 1, 1,
  "IPv4 = 32 bits (4 octets). IPv6 = 128 bits.",
  ["TCS", "Infosys"]),
Q("Which class does 172.16.5.4 belong to?",
  ["Class A", "Class B", "Class C", "Class D"], 1, 2,
  "First octet 172 is in 128–191 → Class B.",
  ["Wipro", "HCL"]),
Q("What is 127.0.0.1?",
  ["A public IP", "Loopback — refers to the local machine",
   "A multicast address", "A Class C address"], 1, 3,
  "127.0.0.0/8 is loopback; 127.0.0.1 means 'this host'.",
  ["Accenture", "TCS"]),
Q("Which range is Class D used for?",
  ["Private networks", "Multicast", "Loopback", "Experimental research"], 1, 4,
  "224.0.0.0–239.255.255.255 is reserved for multicast.",
  ["Cisco", "Juniper"]),
Q("A Class C network has how many usable host addresses by default?",
  ["256", "254", "65534", "510"], 1, 5,
  "2^8 = 256 addresses minus network and broadcast = 254 usable.",
  ["Amazon", "Infosys"]),
Q("Why is classful addressing considered obsolete?",
  ["It was too fast", "It wastes addresses — CIDR allows flexible allocation",
   "It had no classes", "It only worked on LANs"], 1, 7,
  "Fixed class sizes waste IPs (a company needing 300 hosts got a whole Class B of 65K). CIDR fixed this.",
  ["Microsoft", "Google"]),
Q("First octet 191. What class, and how many host bits by default?",
  ["Class B, 16 host bits", "Class C, 8 host bits",
   "Class A, 24 host bits", "Class B, 8 host bits"], 0, 9,
  "191 is in 128–191 → Class B, default /16 → 16 host bits.",
  ["Goldman Sachs", "Cisco"]),
]),

L("private-public-ip", "Private vs Public IPs & Special Addresses",
"""## Private address ranges (RFC 1918) — not routable on the internet

| Class | Range | CIDR |
|---|---|---|
| A | 10.0.0.0 – 10.255.255.255 | 10.0.0.0/8 |
| B | 172.16.0.0 – 172.31.255.255 | 172.16.0.0/12 |
| C | 192.168.0.0 – 192.168.255.255 | 192.168.0.0/16 |

Your home Wi-Fi (192.168.x.x) is private — your router NATs it to one public IP.

## Special addresses to memorize

- **0.0.0.0/0** — default route ("everything")
- **127.0.0.1** — loopback
- **169.254.x.x** — APIPA link-local (DHCP failed)
- **255.255.255.255** — limited broadcast
- **224.0.0.0/4** — multicast
""",
[
Q("Which of these is a private IP?",
  ["8.8.8.8", "172.20.10.5", "11.0.0.1", "200.1.1.1"], 1, 1,
  "172.16.0.0–172.31.255.255 is private (Class B range). 11.0.0.1 is public!",
  ["TCS", "Infosys"]),
Q("What does 0.0.0.0/0 mean in a routing table?",
  ["No route", "Default route — matches everything", "Loopback", "Broadcast"], 1, 3,
  "0.0.0.0/0 is the default route, used when no specific route matches.",
  ["Cisco", "Accenture"]),
Q("Your laptop gets 169.254.10.5. What happened?",
  ["DHCP failed — APIPA self-assigned address", "You got a public IP",
   "VPN connected", "DNS is down"], 0, 4,
  "169.254.0.0/16 (APIPA) means the DHCP request got no answer.",
  ["HCL", "Wipro"]),
Q("How many Class C private networks exist (192.168.0.0/16)?",
  ["1", "16", "256", "65536"], 2, 5,
  "192.168.0.0/16 gives 16 bits for subnets → 2^8 = 256 /24 networks.",
  ["Amazon", "Juniper"]),
Q("Can two different companies both use 10.0.0.5 internally?",
  ["No — IPs must be globally unique", "Yes — private addresses are reusable behind NAT",
   "Only with permission", "Only on weekends"], 1, 7,
  "Private addresses are not internet-routable, so reuse across organizations is fine.",
  ["Microsoft", "Google"]),
Q("Which address would a host use to ping itself?",
  ["192.168.1.1", "127.0.0.1", "0.0.0.0", "255.255.255.255"], 1, 2,
  "127.0.0.1 (loopback) always refers to the local machine.",
  ["TCS", "Cognizant"]),
]),

L("subnet-masks", "Subnet Masks — The Math",
"""## What a mask does

A subnet mask splits the 32 bits into **network bits (1s)** and
**host bits (0s)**. Example /26:

```
IP:   192.168.1.77  = 11000000.10101000.00000001.01001101
Mask: 255.255.255.192 (11111111.11111111.11111111.11000000)
AND → Network: 192.168.1.64
```

## Masks to memorize (last octet)

| CIDR | Mask | Addresses | Usable hosts |
|---|---|---|---|
| /24 | 255.255.255.0 | 256 | 254 |
| /25 | 255.255.255.128 | 128 | 126 |
| /26 | 255.255.255.192 | 64 | 62 |
| /27 | 255.255.255.224 | 32 | 30 |
| /28 | 255.255.255.240 | 16 | 14 |
| /29 | 255.255.255.248 | 8 | 6 |
| /30 | 255.255.255.252 | 4 | 2 |

## Formulas

- **Addresses** = 2^(host bits)
- **Usable hosts** = 2^(host bits) − 2 (minus network & broadcast)
- **Subnets** created = 2^(borrowed bits)
""",
[
Q("What is the subnet mask for /27?",
  ["255.255.255.192", "255.255.255.224", "255.255.255.240", "255.255.255.128"], 1, 2,
  "/27 = 27 ones: 11111111.11111111.11111111.11100000 = 255.255.255.224.",
  ["TCS", "Infosys", "Wipro"]),
Q("How many usable hosts in a /28 subnet?",
  ["16", "14", "30", "12"], 1, 3,
  "32 − 28 = 4 host bits → 2^4 = 16 addresses − 2 = 14 usable.",
  ["Accenture", "HCL"]),
Q("Which mask gives exactly 2 usable host addresses?",
  ["/29", "/30", "/31", "/28"], 1, 4,
  "/30: 2 host bits → 4 addresses − 2 = 2 usable (used for point-to-point links).",
  ["Cisco", "Juniper"]),
Q("192.168.5.0/24 is split into /26 subnets. How many subnets?",
  ["2", "4", "8", "16"], 1, 5,
  "Borrowed bits = 26 − 24 = 2 → 2^2 = 4 subnets.",
  ["Amazon", "TCS"]),
Q("What is the broadcast address of 10.1.1.0/26?",
  ["10.1.1.64", "10.1.1.63", "10.1.1.127", "10.1.1.255"], 1, 7,
  "/26 block size = 64. First block 10.1.1.0–63, broadcast = last address = 10.1.1.63.",
  ["Microsoft", "Google"]),
Q("A /20 network: how many host bits and usable hosts?",
  ["12 host bits, 4094 usable", "20 host bits, 4094 usable",
   "12 host bits, 4096 usable", "8 host bits, 254 usable"], 0, 9,
  "32 − 20 = 12 host bits → 2^12 = 4096 − 2 = 4094 usable hosts.",
  ["Goldman Sachs", "Cisco"]),
]),

L("cidr", "CIDR Notation",
"""## CIDR = Classless Inter-Domain Routing

`/n` means "first n bits are the network portion". It killed the
rigid class system.

```
192.168.1.0/24  → 24 network bits, 8 host bits
10.0.0.0/8      → 8 network bits, 24 host bits
172.16.0.0/12   → 12 network bits, 20 host bits
```

## Reading CIDR quickly

- Bigger n = **smaller** network (fewer hosts)
- /32 = exactly one host (a host route)
- /0 = the whole internet (default route)

## Supernet vs subnet

- **Subnetting**: splitting one big block into smaller ones (/24 → four /26s)
- **Supernetting (aggregation)**: combining small blocks into one route
  (four /24s → one /22) — keeps routing tables small. BGP depends on this.
""",
[
Q("What does the '24' mean in 192.168.1.0/24?",
  ["24 hosts", "First 24 bits are network", "24 subnets", "Port 24"], 1, 1,
  "/n = n network bits. /24 → 24 network bits, 8 host bits.",
  ["TCS", "Infosys"]),
Q("Which is the LARGER network: /16 or /24?",
  ["/24", "/16", "Same size", "Cannot tell"], 1, 2,
  "Smaller prefix = more host bits = bigger network. /16 has 65K addresses; /24 has 256.",
  ["Wipro", "Accenture"]),
Q("What is a /32 route?",
  ["The whole internet", "A route to exactly one host IP",
   "A multicast group", "An invalid route"], 1, 4,
  "/32 = all 32 bits are network → identifies a single host.",
  ["Cisco", "Juniper"]),
Q("What is route aggregation (supernetting)?",
  ["Splitting networks", "Combining multiple small routes into one larger prefix",
   "Encrypting routes", "Deleting old routes"], 1, 5,
  "Aggregation (e.g. four /24s → one /22) shrinks global routing tables — essential for BGP scale.",
  ["Amazon", "Microsoft"]),
Q("How many /26 networks fit inside one /24?",
  ["2", "4", "8", "6"], 1, 7,
  "2^(26−24) = 4. Each /26 has 64 addresses; 4 × 64 = 256 = one /24. ✓",
  ["Google", "TCS"]),
Q("An ISP advertises 203.0.113.0/24 as two /25s instead. What problem does this cause?",
  ["Faster routing", "Routing table bloat — de-aggregation",
   "Better security", "Nothing"], 1, 9,
  "De-aggregation inflates global BGP tables; aggregation is preferred.",
  ["Arista", "Juniper"]),
]),

L("subnetting-practice", "Subnetting Practice — Calculated",
"""## The block-size method (fastest for exams)

**Block size** = 256 − interesting octet of the mask.
For 192.168.10.0/27: mask octet = 224 → block = 256 − 224 = **32**.
Subnets: .0, .32, .64, .96, .128, .160, .192, .224.

## Worked example: 172.16.0.77/21

- Mask: /21 → third octet 248 (256−8), block size = **8**
- Subnets in 3rd octet: 0, 8, 16, ...
- 77 falls in the 72–79 block → **network 172.16.72.0**
- Broadcast: 172.16.79.255, usable: 172.16.72.1 – 172.16.79.254

## Checklist per question

1. Block size = 256 − mask octet
2. List subnet boundaries
3. Find which block the IP sits in → network address
4. Broadcast = next network − 1
5. Usable = network+1 … broadcast−1
""",
[
Q("192.168.1.0/26 — what is the block size?",
  ["128", "64", "32", "16"], 1, 3,
  "Mask octet = 192 → block = 256 − 192 = 64.",
  ["TCS", "Infosys"]),
Q("Which subnet does 192.168.1.100/26 belong to?",
  ["192.168.1.0", "192.168.1.64", "192.168.1.96", "192.168.1.128"], 1, 4,
  "Block size 64 → subnets .0, .64, .128… 100 is in .64–.127 → network 192.168.1.64.",
  ["Wipro", "Accenture"]),
Q("Broadcast address of 192.168.1.64/26?",
  ["192.168.1.63", "192.168.1.127", "192.168.1.128", "192.168.1.255"], 1, 5,
  "Subnet .64–.127 → broadcast is the last address: 192.168.1.127.",
  ["Cisco", "HCL"]),
Q("How many usable hosts in 172.16.0.0/21?",
  ["510", "2046", "1022", "4094"], 1, 6,
  "Host bits = 32 − 21 = 11 → 2^11 = 2048 − 2 = 2046 usable.",
  ["Amazon", "Microsoft"]),
Q("First usable IP in 10.5.128.0/19?",
  ["10.5.128.0", "10.5.128.1", "10.5.0.1", "10.5.159.254"], 1, 7,
  "Network is 10.5.128.0 → first usable is network + 1 = 10.5.128.1.",
  ["Google", "TCS"]),
Q("A host needs 1000 usable IPs with minimal waste. Best CIDR?",
  ["/22", "/21", "/23", "/20"], 1, 9,
  "/22 → 1022 usable (fits 1000, waste 22). /23 → only 510 (too small).",
  ["Goldman Sachs", "Cisco"]),
]),

L("vlsm", "VLSM — Variable Length Subnet Masks",
"""## Why VLSM?

Fixed subnetting wastes addresses: a point-to-point link needs 2 IPs
but a /26 gives 62. **VLSM** lets each subnet use a different mask —
right-size every piece.

## The rule: biggest first

1. Sort requirements **largest → smallest**
2. Allocate each from the remaining space
3. Never overlap

## Worked example: 192.168.1.0/24 needs 100, 50, 25 hosts + 2 WAN links

- 100 hosts → /25 (126 usable): 192.168.1.0/25 (.0–.127)
- 50 hosts → /26 (62 usable): 192.168.1.128/26 (.128–.191)
- 25 hosts → /27 (30 usable): 192.168.1.192/27 (.192–.223)
- WAN 1 → /30: 192.168.1.224/30
- WAN 2 → /30: 192.168.1.228/30
- Leftover: 192.168.1.232–255 free ✓
""",
[
Q("What problem does VLSM solve?",
  ["Slow routing", "Address waste from one-size-fits-all subnetting",
   "DNS failures", "Cable faults"], 1, 3,
  "VLSM allows different mask lengths per subnet so each gets only what it needs.",
  ["Cisco", "Juniper"]),
Q("In VLSM design, which requirement is allocated FIRST?",
  ["Smallest", "Largest", "WAN links", "Alphabetical"], 1, 4,
  "Allocate largest first — small blocks fragment the space and can block big allocations.",
  ["TCS", "Accenture"]),
Q("A WAN link needs 2 usable IPs. Best mask?",
  ["/29", "/30", "/31", "/27"], 1, 5,
  "/30 → 4 addresses, 2 usable — the standard point-to-point choice.",
  ["HCL", "Wipro"]),
Q("Using the worked example, which subnet holds the 25-host LAN?",
  ["192.168.1.128/26", "192.168.1.192/27", "192.168.1.0/25", "192.168.1.224/30"], 1, 6,
  "/27 gives 30 usable (fits 25); allocated at .192 after the /25 and /26 blocks.",
  ["Amazon", "Microsoft"]),
Q("Can VLSM subnets overlap?",
  ["Yes, if different masks", "No — overlapping subnets break routing",
   "Only on WAN links", "Only with NAT"], 1, 8,
  "Overlaps create ambiguous routes. Every allocated block must be disjoint.",
  ["Google", "Arista"]),
Q("An engineer subnets 10.0.0.0/16 with VLSM for 500, 200, 100 hosts. First allocation?",
  ["10.0.0.0/23", "10.0.0.0/24", "10.0.2.0/23", "10.0.0.0/25"], 0, 10,
  "Largest first: 500 hosts → /23 (510 usable) → 10.0.0.0/23.",
  ["Cisco", "Goldman Sachs"]),
]),

L("nat-ipv6", "NAT & IPv6 Basics",
"""## NAT recap (3 flavors)

- **Static NAT**: 1 private ↔ 1 public (fixed mapping)
- **Dynamic NAT**: pool of public IPs assigned on demand
- **PAT (overload)**: many private → 1 public using *ports* — what your home router does

## IPv6 essentials

- **128-bit** addresses, hex groups: `2001:0db8:0000:0000:0000:ff00:0042:8329`
- **Compression**: `2001:db8::ff00:42:8329` (:: = one run of zeros, once only)
- **No NAT needed** — enough addresses for everything
- **No broadcast** — uses multicast instead
- Types: global unicast, **link-local** (`fe80::/10`), loopback `::1`

## NAT drawbacks (interview gold)

Breaks end-to-end connectivity, complicates P2P/VoIP, hides hosts
(troubleshooting pain), and was only ever a *workaround* for IPv4 exhaustion.
""",
[
Q("What does PAT (NAT overload) use to multiplex many hosts onto one public IP?",
  ["Different MACs", "Port numbers", "VLAN tags", "Hostnames"], 1, 2,
  "PAT tracks (private IP, private port) ↔ (public IP, public port) mappings.",
  ["TCS", "Infosys"]),
Q("How many bits is an IPv6 address?",
  ["32", "64", "128", "256"], 2, 1,
  "IPv6 = 128 bits vs IPv4's 32.",
  ["Wipro", "HCL"]),
Q("What is the IPv6 loopback address?",
  ["127.0.0.1", "::1", "fe80::1", "::ffff"], 1, 3,
  "::1 is IPv6 loopback (like 127.0.0.1 in v4).",
  ["Accenture", "Cisco"]),
Q("Which is a valid IPv6 compression?",
  ["2001:db8::1::2", "2001:db8::1", "2001:db8:1", "2001::db8::1"], 1, 5,
  ":: can replace ONE run of zero groups only — '2001:db8::1' is valid.",
  ["Juniper", "Amazon"]),
Q("What is the IPv6 link-local prefix?",
  ["fc00::/7", "fe80::/10", "2001::/16", "::/0"], 1, 6,
  "fe80::/10 = link-local (auto-configured, non-routable).",
  ["Microsoft", "Google"]),
Q("Why is NAT considered a workaround, not a solution?",
  ["It is too fast", "It breaks end-to-end connectivity and complicates P2P/VoIP/troubleshooting",
   "It needs IPv6", "It encrypts traffic"], 1, 8,
  "NAT hides hosts and breaks protocols assuming end-to-end addressing; IPv6 is the real fix.",
  ["Cisco", "Atlassian"]),
]),
])


# ---------------------------------------------------------------------------
# MODULE 3 — TCP & UDP (6 lessons)
# ---------------------------------------------------------------------------

_tcp_udp = M("tcp-udp", "TCP & UDP",
    "The 3-way handshake, sequence numbers, flow control, congestion control (slow start), and when to use UDP.",
[

L("tcp-vs-udp", "TCP vs UDP — The Eternal Debate",
"""## Head-to-head

| Feature | TCP | UDP |
|---|---|---|
| Connection | Connection-oriented (handshake) | Connectionless |
| Reliability | Guaranteed (ACK + retransmit) | Best-effort |
| Ordering | Yes | No |
| Speed/overhead | Slower, 20-byte header | Faster, 8-byte header |
| Flow control | Yes (sliding window) | No |
| Congestion control | Yes | No |

## Choosing

- **TCP**: web, email, file transfer, databases — correctness matters
- **UDP**: DNS, live video/voice, online gaming, DHCP — speed matters,
  app handles loss itself

## The interview one-liner

"TCP trades speed for reliability; UDP trades reliability for speed."
""",
[
Q("Which protocol is connection-oriented?",
  ["UDP", "TCP", "IP", "ICMP"], 1, 1,
  "TCP establishes a connection via handshake; UDP just sends.",
  ["TCS", "Infosys"]),
Q("What is the UDP header size?",
  ["20 bytes", "8 bytes", "40 bytes", "16 bytes"], 1, 2,
  "UDP header = 8 bytes (vs TCP's 20 minimum).",
  ["Wipro", "HCL"]),
Q("Why is DNS primarily UDP?",
  ["UDP is reliable", "DNS queries are tiny and fast — one request, one reply",
   "UDP encrypts data", "TCP cannot carry DNS"], 1, 4,
  "Small request/response fits one datagram; TCP's handshake would triple the packets. (Zone transfers use TCP.)",
  ["Amazon", "Google"]),
Q("Which application should use TCP?",
  ["Live video call", "Online FPS game", "File download", "DNS lookup"], 2, 5,
  "File downloads need every byte correct and ordered → TCP.",
  ["Microsoft", "Accenture"]),
Q("What does 'connection-oriented' actually guarantee?",
  ["Encryption", "Both sides agree on state (seq numbers, windows) before data flows",
   "Faster delivery", "No headers"], 1, 7,
  "The handshake synchronizes sequence numbers and parameters — both ends know a connection exists.",
  ["Cisco", "Atlassian"]),
Q("A protocol needs reliability AND low latency for real-time audio. What do engineers actually do?",
  ["Use TCP anyway", "Use UDP and add app-level reliability (like QUIC/WebRTC do)",
   "Use IP directly", "Impossible"], 1, 9,
  "Real-time apps use UDP + custom reliability (retransmit only what matters) — the QUIC/WebRTC approach.",
  ["Google", "Microsoft"]),
]),

L("three-way-handshake", "The TCP 3-Way Handshake",
"""## SYN → SYN-ACK → ACK

```
Client                          Server
  | ---- SYN (seq=x) ------------> |
  | <--- SYN-ACK (seq=y, ack=x+1) - |
  | ---- ACK (ack=y+1) -----------> |
```

1. **SYN**: "Can we talk? My sequence starts at x."
2. **SYN-ACK**: "Yes! My sequence starts at y. Got your x."
3. **ACK**: "Got your y. Let's talk."

## Why 3 steps and not 2?

The third ACK confirms the *server's* SYN arrived. With only 2 steps,
the server couldn't know the client is really there — opening the door
to **SYN flood attacks** (spoofed SYNs exhaust server resources).

## Teardown: 4-way (FIN)

Each side closes independently: FIN → ACK, FIN → ACK.
The side closing first enters **TIME_WAIT** (2×MSL) to catch stray packets.
""",
[
Q("What are the 3 steps of the TCP handshake?",
  ["SYN, ACK, FIN", "SYN, SYN-ACK, ACK", "HELLO, ACK, BYE", "REQ, ACK, DONE"], 1, 1,
  "SYN → SYN-ACK → ACK synchronizes both sides' sequence numbers.",
  ["TCS", "Infosys", "Wipro"]),
Q("Why does TCP need the third ACK?",
  ["For speed", "So the server knows its SYN-ACK arrived — prevents half-open connections",
   "For encryption", "It doesn't — 2 would suffice"], 1, 5,
  "Without the final ACK, the server can't confirm the client received its sequence number.",
  ["Amazon", "Microsoft"]),
Q("What is a SYN flood attack?",
  ["Flooding with data", "Spoofed SYNs exhaust server's half-open connection queue",
   "Stealing passwords", "DNS poisoning"], 1, 6,
  "Attackers send SYNs with fake sources; the server holds half-open connections until timeout.",
  ["Cisco", "Palo Alto"]),
Q("How many packets to TEAR DOWN a TCP connection (normal case)?",
  ["2", "3", "4", "6"], 2, 4,
  "FIN/ACK in each direction = 4 packets (each side closes independently).",
  ["Google", "Juniper"]),
Q("What is TIME_WAIT and why does it exist?",
  ["Waiting for DNS", "Post-close state (2×MSL) to catch delayed/stray packets",
   "Handshake retry", "Congestion pause"], 1, 8,
  "TIME_WAIT ensures late duplicates don't corrupt a *new* connection reusing the same ports.",
  ["Atlassian", "Netflix"]),
Q("During the handshake, what does ack=x+1 mean?",
  ["Packet x was lost", "'I received everything up to x, send x+1 next'",
   "Connection refused", "Window is x+1"], 1, 7,
  "ACK numbers are cumulative: ack=N means 'next expected byte is N'.",
  ["Goldman Sachs", "Cisco"]),
]),

L("tcp-headers", "TCP Segment Structure & Sequence Numbers",
"""## TCP header (20 bytes minimum)

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                      Sequence Number                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                   Acknowledgment Number                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Data|       |C|E|U|A|P|R|S|F|                               |
|Offset|Reservd|W|C|R|C|S|S|Y|I|            Window             |
|     |       |R|E|G|K|H|T|N|N|                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

## Flags that matter

- **SYN** — synchronize sequence numbers (connection start)
- **ACK** — acknowledgment field is valid
- **FIN** — no more data (close)
- **RST** — reset connection immediately
- **PSH** — push data to app now

## Sequence numbers

Every **byte** gets a number. If you send 1000 bytes starting at seq=5000,
the next segment starts at 6000. ACKs confirm bytes, enabling
retransmission of exactly what's missing.
""",
[
Q("What is the minimum TCP header size?",
  ["8 bytes", "20 bytes", "40 bytes", "60 bytes"], 1, 2,
  "TCP header = 20 bytes minimum (up to 60 with options).",
  ["TCS", "Infosys"]),
Q("Which flag starts a TCP connection?",
  ["ACK", "FIN", "SYN", "RST"], 2, 1,
  "SYN synchronizes sequence numbers to open a connection.",
  ["Wipro", "HCL"]),
Q("What does the RST flag do?",
  ["Restarts the handshake", "Abruptly resets/terminates the connection",
   "Requests retransmission", "Opens a new stream"], 1, 4,
  "RST kills the connection immediately — no graceful FIN exchange.",
  ["Cisco", "Palo Alto"]),
Q("You send 500 bytes with seq=1000. What seq does the next segment use?",
  ["1001", "1500", "500", "1000"], 1, 5,
  "Sequence numbers count BYTES: 1000 + 500 = 1500.",
  ["Amazon", "Google"]),
Q("Why does TCP number bytes instead of packets?",
  ["To save space", "So any subset can be retransmitted precisely and reordered correctly",
   "For encryption", "Historical accident"], 1, 7,
  "Byte numbering allows retransmitting exactly the missing range, whatever the segment boundaries.",
  ["Microsoft", "Netflix"]),
Q("A receiver gets segments with seq 1000 (100B), then seq 1300 (100B). What happened?",
  ["Normal", "Bytes 1100–1299 are missing — a gap needing retransmission",
   "Duplicate data", "Connection closed"], 1, 9,
  "1000+100=1100 expected next, but 1300 arrived → 200 bytes lost in transit.",
  ["Cisco", "Arista"]),
]),

L("flow-control", "Flow Control — Sliding Window",
"""## Don't overwhelm the receiver

The receiver advertises a **window** = "I can take N more bytes."
The sender never sends more than the window allows.

```
Sender:  can send bytes 5000–6000 (window=1000)
  → sends 5000–5500, waits
Receiver: processes, ACKs with window=1000 again
  → sender continues
```

## Sliding window mechanics

- Window **slides forward** as ACKs arrive
- **Zero window** = "stop, my buffer is full" (sender probes with 1-byte segments)
- **Cumulative ACKs**: ack=6000 confirms everything before 6000

## Flow control vs congestion control

- **Flow control**: protect the *receiver* (window from receiver)
- **Congestion control**: protect the *network* (window from sender's estimate)
""",
[
Q("What is the purpose of flow control?",
  ["Avoid network congestion", "Prevent overwhelming the receiver's buffer",
   "Encrypt data", "Choose routes"], 1, 2,
  "Flow control matches sender speed to what the receiver can handle.",
  ["TCS", "Infosys"]),
Q("Who advertises the receive window?",
  ["The sender", "The receiver", "The router", "DNS"], 1, 3,
  "The receiver tells the sender how much buffer space remains.",
  ["Wipro", "Accenture"]),
Q("What does a zero-window advertisement mean?",
  ["Connection closed", "'Stop sending — my buffer is full'",
   "No congestion", "Handshake failed"], 1, 5,
  "Zero window pauses the sender; it sends tiny probes until the window reopens.",
  ["Cisco", "Juniper"]),
Q("ACK=7000 arrives. What does the sender know?",
  ["Byte 7000 was lost", "All bytes before 7000 are received",
   "Send byte 7000 next", "Window is 7000"], 1, 6,
  "Cumulative ACK: everything up to (not including) 7000 is confirmed.",
  ["Amazon", "Microsoft"]),
Q("Flow control vs congestion control — what's the difference?",
  ["Same thing", "Flow control protects the receiver; congestion control protects the network",
   "Congestion is faster", "Flow control uses UDP"], 1, 8,
  "Receiver-advertised window (flow) vs sender-estimated network capacity (congestion).",
  ["Google", "Netflix"]),
Q("Why do senders use 1-byte probes during zero window?",
  ["To test speed", "To detect when the receiver's window reopens (ACKs can be lost)",
   "To keep the connection alive", "For security"], 1, 10,
  "If the window-update ACK is lost, the sender would wait forever — probes prevent deadlock.",
  ["Cisco", "Arista"]),
]),

L("congestion-control", "Congestion Control — Slow Start & AIMD",
"""## The problem

Too many senders → router queues overflow → packets drop → retransmissions
→ *more* traffic → **congestion collapse**. TCP must sense and back off.

## Slow start

- Start with small **cwnd** (congestion window, e.g. 1–10 segments)
- **Double** cwnd every RTT while no loss (exponential!)
- 1, 2, 4, 8, 16… until loss or **ssthresh**

## Congestion avoidance (AIMD)

After slow start: **Additive Increase** (+1/cwnd per RTT),
**Multiplicative Decrease** (halve on loss). This AIMD sawtooth is
provably fair — competing flows converge to equal shares.

## Fast retransmit & recovery

- **3 duplicate ACKs** → retransmit immediately (don't wait for timeout)
- Halve cwnd, continue (fast recovery) instead of restarting slow start
""",
[
Q("What is slow start?",
  ["Slow typing", "Exponentially growing the congestion window from small until loss",
   "A routing protocol", "DNS caching"], 1, 3,
  "Slow start doubles cwnd each RTT — 'slow' only compared to dumping everything at once.",
  ["TCS", "Infosys"]),
Q("What does AIMD stand for and do?",
  ["Automatic IP Management Device",
   "Additive Increase Multiplicative Decrease — fair bandwidth sharing",
   "Advanced Internet Mail Daemon", "Asynchronous Input Method Driver"], 1, 5,
  "AIMD: +1 per RTT, halve on loss. Competing flows converge to fairness.",
  ["Google", "Amazon"]),
Q("What triggers fast retransmit?",
  ["Timeout", "3 duplicate ACKs", "Zero window", "SYN flood"], 1, 6,
  "3 dup ACKs strongly suggest one segment lost while later ones arrived — retransmit now.",
  ["Cisco", "Juniper"]),
Q("Why is it called 'slow' start if it doubles every RTT?",
  ["It is actually slow", "It's slow relative to sending the full window immediately",
   "Marketing", "It halves each time"], 1, 7,
  "Doubling from 1 is cautious vs blasting; the name contrasts with instant full-rate sending.",
  ["Microsoft", "Netflix"]),
Q("Two TCP flows share a bottleneck. What does AIMD guarantee long-term?",
  ["First flow wins", "They converge to roughly equal shares (fairness)",
   "Both collapse", "Random shares"], 1, 9,
  "AIMD's decrease hits the bigger flow harder — a classic fairness result (Chiu/Jain).",
  ["Google", "Stanford"]),
Q("A timeout (not 3 dup ACKs) occurs. What does classic TCP do?",
  ["Nothing", "Drops cwnd to 1 and restarts slow start",
   "Doubles cwnd", "Closes connection"], 1, 8,
  "Timeout = severe congestion signal → reset to 1 segment, slow-start again (modern TCP is gentler).",
  ["Arista", "Cisco"]),
]),

L("udp-use-cases", "UDP Deep Dive & Connection Teardown",
"""## UDP header (8 bytes — tiny!)

Source port, dest port, length, checksum. That's it.

## Where UDP wins

- **DNS**: single query/response
- **DHCP**: bootstrapping (no connection possible yet!)
- **VoIP/Video** (RTP): late data is useless — skip retransmits
- **Gaming**: position updates 60×/sec — old ones are stale anyway
- **QUIC**: Google's UDP-based transport (HTTP/3) — reliability rebuilt on top

## TCP teardown (4-way)

```
A: FIN → B        "I'm done sending"
B: ACK → A        "Got it"
B: FIN → A        "I'm done too"
A: ACK → B        "Got it"  → A enters TIME_WAIT
```

Each direction closes independently — full-duplex needs two FINs.
""",
[
Q("Why can't DHCP use TCP?",
  ["It can", "The host has no IP yet — can't complete a handshake",
   "DHCP is encrypted", "TCP is too fast"], 1, 4,
  "DORA happens before the client has an address; connectionless UDP broadcast is the only option.",
  ["Cisco", "Juniper"]),
Q("In VoIP, why is a lost packet NOT retransmitted?",
  ["It is retransmitted", "By the time it'd arrive, the conversation moved on — late audio is useless",
   "UDP can't retransmit", "Packets never get lost"], 1, 5,
  "Real-time media prefers timely loss over late perfection.",
  ["Google", "Microsoft"]),
Q("How many FIN exchanges to fully close a TCP connection?",
  ["1", "2 (one per direction)", "3", "4"], 1, 3,
  "TCP is full-duplex: each side sends FIN and gets ACK — 4 packets total.",
  ["TCS", "Infosys"]),
Q("What is QUIC?",
  ["A DNS server", "Google's UDP-based reliable transport (basis of HTTP/3)",
   "A firewall", "An email protocol"], 1, 6,
  "QUIC rebuilds TCP-like reliability + TLS on top of UDP for faster handshakes.",
  ["Cloudflare", "Google"]),
Q("A game sends player positions via TCP. What's the problem?",
  ["None", "Head-of-line blocking: one lost packet delays ALL newer updates",
   "Too fast", "No encryption"], 1, 8,
  "TCP's ordering guarantee means a single loss stalls everything behind it — terrible for real-time.",
  ["Riot", "Valve"]),
Q("After active close, why does the closer wait in TIME_WAIT?",
  ["To save power", "To catch stray duplicates and ensure the final ACK arrived (2×MSL)",
   "To renegotiate", "It doesn't"], 1, 7,
  "TIME_WAIT (2×MSL ≈ 2–4 min) prevents old packets corrupting future connections on the same ports.",
  ["Netflix", "Amazon"]),
]),
])


# ---------------------------------------------------------------------------
# MODULE 4 — APPLICATION LAYER (6 lessons)
# ---------------------------------------------------------------------------

_app_layer = M("app-layer", "Application Layer",
    "DNS (recursive vs iterative), HTTP/1.1 vs 2 vs 3, DHCP, email and FTP, cookies and sessions.",
[

L("dns", "DNS — How Names Become IPs",
"""## DNS: the internet's phone book

`example.com` → `93.184.216.34`. Without DNS, you'd memorize IPs.

## Recursive vs iterative queries

**Recursive** (your laptop → resolver): "Get me the answer, do the work."
The resolver does all the legwork and returns the final IP.

**Iterative** (resolver → root → TLD → authoritative): each server says
"I don't know, but ask *them*." The resolver follows referrals itself.

## Record types

| Type | Meaning |
|---|---|
| A | IPv4 address |
| AAAA | IPv6 address |
| CNAME | Alias (www → example.com) |
| MX | Mail server |
| TXT | Arbitrary text (SPF, verification) |
| NS | Name servers for a zone |

## Caching & TTL

Every answer carries a **TTL** (time-to-live). Resolvers cache answers
until TTL expires — that's why DNS changes take time to propagate.
""",
[
Q("What does DNS do?",
  ["Assigns IP addresses", "Translates domain names to IP addresses",
   "Routes packets", "Encrypts traffic"], 1, 1,
  "DNS = Domain Name System: names → IPs.",
  ["TCS", "Infosys"]),
Q("In a recursive query, who does the legwork?",
  ["The client", "The resolver — it returns the final answer",
   "The root server", "Nobody"], 1, 3,
  "Recursive = 'do it all for me'. Iterative = 'give me referrals, I'll chase them'.",
  ["Google", "Cloudflare"]),
Q("Which record type maps a name to an IPv6 address?",
  ["A", "AAAA", "CNAME", "MX"], 1, 2,
  "A = IPv4, AAAA = IPv6 (four times the 'A').",
  ["Wipro", "HCL"]),
Q("What does a CNAME record do?",
  ["Maps to IPv4", "Creates an alias from one name to another",
   "Handles email", "Lists name servers"], 1, 4,
  "CNAME: www.example.com → example.com.",
  ["Accenture", "Amazon"]),
Q("Why does a DNS change take hours to fully propagate?",
  ["Slow servers", "Resolvers cache old answers until TTL expires",
   "DNS is down", "Root servers are slow"], 1, 5,
  "TTL-based caching means stale answers persist until they expire everywhere.",
  ["Cloudflare", "Microsoft"]),
Q("Which servers does an iterative resolver contact, in order?",
  ["Authoritative, TLD, root", "Root → TLD → authoritative",
   "TLD → root → authoritative", "Any order"], 1, 7,
  "The hierarchy is walked top-down: root, then TLD (.com), then authoritative.",
  ["Google", "Cisco"]),
Q("What is DNS hijacking/poisoning?",
  ["Deleting domains", "Corrupting DNS responses so victims go to attacker IPs",
   "Slow DNS", "Blocking ports"], 1, 9,
  "Cache poisoning injects fake records — victims trust the forged answer. DNSSEC counters it.",
  ["Palo Alto", "Cloudflare"]),
]),

L("http-basics", "HTTP Basics — Methods & Status Codes",
"""## HTTP: the web's language

**Stateless** request/response protocol. Every request stands alone —
the server remembers nothing between requests (that's what cookies are for).

## Methods

| Method | Meaning | Safe? | Idempotent? |
|---|---|---|---|
| GET | Read | ✅ | ✅ |
| POST | Create/submit | ❌ | ❌ |
| PUT | Replace | ❌ | ✅ |
| PATCH | Partial update | ❌ | ✅ |
| DELETE | Remove | ❌ | ✅ |
| HEAD | Headers only | ✅ | ✅ |

**Idempotent** = repeating it has the same effect as doing it once.
(DELETE twice: still deleted. POST twice: two resources!)

## Status code families

- **2xx** success (200 OK, 201 Created)
- **3xx** redirection (301 Moved Permanently, 304 Not Modified)
- **4xx** client error (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found)
- **5xx** server error (500 Internal Error, 503 Unavailable)
""",
[
Q("Is HTTP stateful or stateless?",
  ["Stateful", "Stateless", "Both", "Neither"], 1, 1,
  "HTTP is stateless — each request is independent; state lives in cookies/sessions.",
  ["TCS", "Infosys"]),
Q("Which method is idempotent but NOT safe?",
  ["GET", "POST", "PUT", "HEAD"], 2, 3,
  "PUT changes state (not safe) but repeating it gives the same result (idempotent).",
  ["Amazon", "Flipkart"]),
Q("What does 404 mean?",
  ["Server error", "Not Found — resource doesn't exist", "Redirect", "OK"], 1, 2,
  "4xx = client error; 404 = the requested resource wasn't found.",
  ["Wipro", "HCL"]),
Q("Difference between 401 and 403?",
  ["Same thing", "401 = unauthenticated (who are you?); 403 = unauthorized (you can't)",
   "401 is server error", "403 means OK"], 1, 5,
  "401: missing/invalid credentials. 403: authenticated but forbidden.",
  ["Microsoft", "Google"]),
Q("Why is POST not idempotent?",
  ["It is", "Repeating POST typically creates duplicate resources",
   "POST is encrypted", "POST has no body"], 1, 6,
  "Two identical POSTs → two orders created. That's why browsers warn on resubmit.",
  ["Atlassian", "Razorpay"]),
Q("What does a 301 response tell the client?",
  ["Error", "Resource moved permanently — update your bookmarks/use the new URL",
   "Try again later", "Access denied"], 1, 4,
  "301 = permanent redirect; clients/crawlers should use the new location henceforth.",
  ["Cloudflare", "Amazon"]),
]),

L("http2-http3", "HTTP/1.1 vs HTTP/2 vs HTTP/3",
"""## HTTP/1.1 (1997) — the classic

- Text-based, one request per connection (keep-alive helps)
- **Head-of-line blocking**: one slow response stalls everything behind it
- 6 parallel connections per browser — a hack around the limitation

## HTTP/2 (2015) — multiplexing

- **Binary** framing (not text)
- **Multiplexing**: many streams over ONE TCP connection
- Header compression (HPACK), server push
- Still TCP underneath → TCP-level head-of-line blocking remains!

## HTTP/3 (2022) — QUIC

- Runs over **QUIC (UDP-based)** — each stream independent
- **No TCP head-of-line blocking** at all
- Faster handshakes (0-RTT), built-in TLS 1.3
- Perfect for lossy mobile networks

## Interview summary

"1.1: text, sequential. 2: binary multiplexed over TCP. 3: QUIC over UDP, per-stream independence."
""",
[
Q("What is head-of-line blocking in HTTP/1.1?",
  ["Slow DNS", "One slow response blocks subsequent responses on the same connection",
   "Too many headers", "Encryption overhead"], 1, 3,
  "1.1 serves responses in order — a slow first response stalls the rest.",
  ["Google", "Cloudflare"]),
Q("What is HTTP/2's biggest improvement?",
  ["Encryption", "Multiplexing many streams over one TCP connection",
   "Bigger headers", "UDP transport"], 1, 4,
  "Multiplexing kills application-level head-of-line blocking.",
  ["Amazon", "Netflix"]),
Q("Does HTTP/2 eliminate ALL head-of-line blocking?",
  ["Yes completely", "No — TCP-level blocking remains (one lost packet stalls all streams)",
   "It adds more", "It removes TCP"], 1, 7,
  "H/2 multiplexes over a single TCP connection, so TCP's ordered delivery still blocks on loss.",
  ["Google", "Fastly"]),
Q("What transport does HTTP/3 use?",
  ["TCP", "QUIC over UDP", "SCTP", "Raw IP"], 1, 5,
  "HTTP/3 = QUIC (UDP-based) with per-stream independence + built-in TLS 1.3.",
  ["Cloudflare", "Microsoft"]),
Q("Why is HTTP/3 better on mobile networks?",
  ["Bigger packets", "Independent streams survive packet loss without stalling others",
   "No encryption", "Fewer servers"], 1, 8,
  "Lossy networks hurt TCP-based H/2; QUIC isolates loss per stream.",
  ["Google", "Meta"]),
Q("What is HPACK?",
  ["A video codec", "HTTP/2's header compression",
   "A handshake", "A port number"], 1, 9,
  "HPACK compresses repetitive headers across requests on a connection.",
  ["Fastly", "Cloudflare"]),
]),

L("dhcp", "DHCP — Getting an IP Automatically",
"""## DORA — the 4-step dance (all broadcast at first!)

```
Client                          Server
  | ------ DISCOVER (broadcast) ----> |  "Anyone out there?"
  | <------ OFFER ------------------ |  "Take 192.168.1.50"
  | ------ REQUEST (broadcast) ----> |  "I'll take it!"
  | <------ ACK -------------------- |  "It's yours for 24h"
```

**D**iscover, **O**ffer, **R**equest, **A**ck.

## The lease

IPs are **leased**, not owned. Client renews at 50% of lease time (T1).
Lease expires → client must DORA again. That's why your IP sometimes changes.

## Key facts

- DHCP uses **UDP ports 67 (server) / 68 (client)**
- Initial messages are **broadcast** (client has no IP yet — same reason as before!)
- Also delivers: subnet mask, gateway, DNS servers
""",
[
Q("What does DORA stand for?",
  ["Data Over Radio Access", "Discover, Offer, Request, Acknowledge",
   "Domain Object Request API", "Dynamic Online Resource Allocation"], 1, 2,
  "DORA = the 4 DHCP steps.",
  ["TCS", "Infosys"]),
Q("Why does DHCP use broadcast for DISCOVER?",
  ["It's faster", "The client has no IP yet and doesn't know any server address",
   "Broadcast is secure", "Routers require it"], 1, 4,
  "No unicast possible without an address — broadcast reaches any DHCP server on the LAN.",
  ["Cisco", "Juniper"]),
Q("DHCP server and client ports?",
  ["80/443", "67/68", "53/54", "21/22"], 1, 3,
  "UDP 67 = server, 68 = client.",
  ["Wipro", "HCL"]),
Q("Besides an IP, what else does DHCP provide?",
  ["Nothing", "Subnet mask, default gateway, DNS servers",
   "Passwords", "Wi-Fi keys"], 1, 5,
  "A full network config: IP + mask + gateway + DNS.",
  ["Accenture", "TCS"]),
Q("A client renews its lease at what point?",
  ["At expiry", "At 50% of lease time (T1)", "Every hour", "Never"], 1, 6,
  "T1 (50%) tries renewal with the original server; T2 (87.5%) broadcasts to any server.",
  ["Microsoft", "Cisco"]),
Q("Two DHCP servers on one LAN both answer a DISCOVER. What happens?",
  ["Crash", "Client typically takes the first OFFER",
   "Both assign", "Network dies"], 1, 8,
  "First OFFER usually wins — rogue DHCP servers exploit exactly this.",
  ["Palo Alto", "Juniper"]),
]),

L("email-ftp", "Email (SMTP) & File Transfer (FTP)",
"""## Email: three protocols, three jobs

- **SMTP** (port 25/587): *sending* mail — client → server, server → server
- **POP3** (110): *downloading* mail — usually deletes from server
- **IMAP** (143/993): *accessing* mail — stays on server, syncs everywhere

Your phone uses IMAP (that's why mail syncs across devices).

## FTP: two connections!

- **Control** (port 21): commands ("give me file X")
- **Data** (port 20): the actual file bytes

**Active vs passive**: in active mode the *server* connects back to the
client (firewalls hate this); passive mode has the client open both —
passive is the modern default.

## SFTP ≠ FTP

SFTP runs over **SSH** (port 22) — encrypted. Plain FTP sends
passwords in cleartext. Never use plain FTP for anything sensitive.
""",
[
Q("Which protocol SENDS email?",
  ["POP3", "IMAP", "SMTP", "HTTP"], 2, 1,
  "SMTP sends; POP3/IMAP retrieve.",
  ["TCS", "Infosys"]),
Q("Why does your phone use IMAP instead of POP3?",
  ["It's faster", "Mail stays on server and syncs across all devices",
   "It's free", "POP3 is dead"], 1, 3,
  "IMAP = server-side mailbox, multi-device sync. POP3 downloads (and often deletes).",
  ["Google", "Microsoft"]),
Q("FTP uses how many connections?",
  ["1", "2 — control (21) and data (20)", "3", "0"], 1, 4,
  "Separate control and data connections is FTP's famous quirk.",
  ["Wipro", "Accenture"]),
Q("In FTP active mode, who initiates the data connection?",
  ["The client", "The server connects back to the client",
   "The router", "Nobody"], 1, 5,
  "Active: server → client data connection (firewall-unfriendly). Passive reverses this.",
  ["Cisco", "HCL"]),
Q("What's the difference between FTP and SFTP?",
  ["Same thing", "SFTP runs over SSH — encrypted; FTP is cleartext",
   "SFTP is faster", "FTP is newer"], 1, 6,
  "SFTP = SSH File Transfer Protocol (port 22), fully encrypted.",
  ["Amazon", "Palo Alto"]),
Q("SMTP default port for submission (with auth)?",
  ["25", "587", "465", "110"], 1, 7,
  "587 = message submission (STARTTLS); 25 = server-to-server relay; 465 = implicit TLS.",
  ["Microsoft", "Google"]),
]),

L("cookies-sessions", "Cookies, Sessions & Statelessness",
"""## HTTP forgot everything — cookies remember

HTTP is stateless, but apps need login state. Solution: the server
gives the browser a **cookie** (small key-value), and the browser
sends it back with every request.

## Cookies vs sessions

| | Cookie | Session |
|---|---|---|
| Stored | Browser | Server |
| Size | ~4KB | Unlimited |
| Security | Visible to user (don't store secrets!) | Only an ID travels |
| Survives | Browser-controlled expiry | Server timeout |

Typical flow: login → server creates session, sends `session_id` cookie →
browser sends cookie each request → server looks up session.

## Cookie flags (security!)

- **HttpOnly**: JS can't read it (XSS protection)
- **Secure**: only sent over HTTPS
- **SameSite**: controls cross-site sending (CSRF protection)
""",
[
Q("Why do we need cookies if HTTP works fine?",
  ["We don't", "HTTP is stateless — cookies preserve state like logins across requests",
   "Cookies speed up DNS", "Cookies replace TCP"], 1, 2,
  "Without cookies, the server couldn't tell request #2 is from the same logged-in user.",
  ["TCS", "Infosys"]),
Q("Where is session data actually stored?",
  ["In the browser", "On the server; only the session ID travels in a cookie",
   "In DNS", "In the URL"], 1, 3,
  "Sessions = server-side storage keyed by the cookie's session ID.",
  ["Amazon", "Flipkart"]),
Q("What does the HttpOnly flag do?",
  ["Encrypts the cookie", "Blocks JavaScript from reading the cookie (XSS defense)",
   "Makes it permanent", "Hides it from the server"], 1, 5,
  "HttpOnly cookies are invisible to document.cookie — stolen-XSS scripts can't grab them.",
  ["Microsoft", "Google"]),
Q("What attack does SameSite=Strict mitigate?",
  ["DDoS", "CSRF — the browser won't send the cookie on cross-site requests",
   "SQL injection", "Phishing"], 1, 6,
  "SameSite stops the browser attaching cookies to cross-origin requests — CSRF's lifeblood.",
  ["Palo Alto", "Atlassian"]),
Q("A user clears cookies. What happens to their session?",
  ["Nothing", "They're logged out — the session ID is gone",
   "Server crashes", "Password changes"], 1, 4,
  "No session cookie → server can't match requests to the session → logged out.",
  ["Wipro", "Razorpay"]),
Q("Why shouldn't secrets live in cookies directly?",
  ["They can", "Cookies are stored client-side and visible/editable by the user",
   "Cookies are too small always", "Servers can't read cookies"], 1, 7,
  "Never trust client storage — keep secrets server-side in the session.",
  ["CRED", "PhonePe"]),
]),
])


# ---------------------------------------------------------------------------
# MODULE 5 — ROUTING & SWITCHING (6 lessons)
# ---------------------------------------------------------------------------

_routing_switching = M("routing-switching", "Routing & Switching",
    "Hubs vs switches vs routers, VLANs, routing tables, distance-vector vs link-state, OSPF/BGP concepts, STP.",
[

L("switches-hubs", "Hubs vs Switches vs Routers",
"""## The trio, precisely

| | Hub | Switch | Router |
|---|---|---|---|
| Layer | 1 | 2 | 3 |
| Forwards by | Nothing (repeats) | MAC table | Routing table (IP) |
| Collision domains | 1 (all ports) | 1 per port | 1 per port |
| Broadcast domains | 1 | 1 | 1 per interface |

## How a switch learns

1. Frame arrives on port 3 from MAC AA
2. Switch records: AA → port 3 (MAC table)
3. Destination MAC known? Forward to that port only. Unknown? **Flood** (like a hub, once)
4. Table entries **age out** (default ~300s)

## Routers separate broadcast domains

A broadcast (255.255.255.255) never crosses a router — each router
interface is its own broadcast domain. That's why big LANs are
subnetted across router interfaces.
""",
[
Q("A switch forwards frames based on what?",
  ["IP addresses", "MAC addresses", "Port numbers", "Nothing"], 1, 1,
  "Switches are Layer 2 — they learn and forward by MAC.",
  ["TCS", "Infosys"]),
Q("How many collision domains does an 8-port switch create?",
  ["1", "8", "0", "4"], 1, 2,
  "Each switch port is its own collision domain → 8.",
  ["Wipro", "HCL"]),
Q("What does a switch do with a frame for an unknown destination MAC?",
  ["Drops it", "Floods it out all ports (except incoming)",
   "Sends to router", "Buffers forever"], 1, 3,
  "Unknown unicast is flooded — the reply teaches the switch the location.",
  ["Cisco", "Juniper"]),
Q("Why don't broadcasts cross routers?",
  ["They do", "Routers terminate broadcast domains by design — broadcasts stay local",
   "Broadcasts are too big", "Firewalls block them"], 1, 5,
  "Each router interface = separate broadcast domain; this contains broadcast storms.",
  ["Accenture", "TCS"]),
Q("How long do MAC table entries typically live?",
  ["Forever", "~300 seconds (aging time), refreshed by traffic",
   "1 second", "Until reboot"], 1, 6,
  "Aging prevents stale entries when hosts move; traffic refreshes the timer.",
  ["Arista", "Cisco"]),
Q("A hub receives a frame on port 1. What does it do?",
  ["Forwards to the right port", "Repeats it out ALL other ports",
   "Drops it", "Asks the router"], 1, 4,
  "Hubs are dumb Layer-1 repeaters — every port sees every frame (and collisions).",
  ["Juniper", "HCL"]),
]),

L("vlans", "VLANs — Virtual LANs",
"""## One switch, many LANs

A **VLAN** partitions a switch into multiple logical LANs. Ports in
VLAN 10 can't talk to VLAN 20 without a router — even on the same hardware.

**Why**: security (HR vs guests), broadcast control, organization.

## Trunking (802.1Q)

A **trunk** link carries *multiple* VLANs between switches. Each frame
gets a 4-byte **802.1Q tag** with the VLAN ID (12 bits → 4096 VLANs,
0 and 4095 reserved).

## Inter-VLAN routing

VLANs need a Layer-3 device to talk: **router-on-a-stick** (one router
interface, subinterfaces per VLAN) or a Layer-3 switch.
""",
[
Q("What is a VLAN?",
  ["A faster cable", "A logical partition of a switch into separate broadcast domains",
   "A router brand", "A VPN"], 1, 2,
  "VLANs split one physical switch into multiple isolated Layer-2 networks.",
  ["TCS", "Infosys"]),
Q("How many VLANs does the 12-bit ID support?",
  ["256", "4096", "65536", "1024"], 1, 3,
  "2^12 = 4096 (VLAN 1 default, 0/4095 reserved).",
  ["Cisco", "Wipro"]),
Q("What is a trunk port?",
  ["A slow port", "A port carrying multiple VLANs using 802.1Q tags",
   "A router port", "A broken port"], 1, 4,
  "Trunks tag frames so switches know which VLAN each belongs to.",
  ["Juniper", "Accenture"]),
Q("Can two hosts in different VLANs communicate directly?",
  ["Yes always", "No — needs inter-VLAN routing via a Layer-3 device",
   "Yes with a hub", "Only on Wi-Fi"], 1, 5,
  "VLANs are separate broadcast domains; a router/L3 switch must route between them.",
  ["HCL", "TCS"]),
Q("What is router-on-a-stick?",
  ["A broken router", "One router interface with subinterfaces routing between VLANs",
   "A wireless router", "A firewall"], 1, 7,
  "Subinterfaces (e.g. g0/0.10, g0/0.20) each handle one VLAN's traffic.",
  ["Cisco", "Amazon"]),
Q("Which VLAN is the default on Cisco switches?",
  ["VLAN 0", "VLAN 1", "VLAN 100", "VLAN 4095"], 1, 6,
  "VLAN 1 is default/native — best practice is to move user traffic off it.",
  ["Arista", "Juniper"]),
]),

L("routing-tables", "Routing Tables & Longest Prefix Match",
"""## What's in a routing table?

| Destination | Next hop | Interface | Metric |
|---|---|---|---|
| 10.1.0.0/16 | 192.168.1.1 | eth0 | 10 |
| 0.0.0.0/0 | 192.168.1.254 | eth0 | 1 |

Plus: **directly connected** networks and **local** addresses.

## Longest prefix match (THE rule)

When multiple routes match, the **most specific (longest prefix) wins**:

```
Packet to 10.1.5.9:
  10.0.0.0/8    matches
  10.1.0.0/16   matches  ← longer
  10.1.5.0/24   matches  ← LONGEST → winner
```

## Static vs dynamic

- **Static**: hand-configured (small networks, default routes)
- **Dynamic**: protocols (RIP, OSPF, BGP) learn and adapt automatically
""",
[
Q("What does a routing table contain?",
  ["Passwords", "Destination networks, next hops, interfaces, metrics",
   "User accounts", "DNS records"], 1, 1,
  "Each entry says: to reach network X, send via next-hop Y on interface Z.",
  ["TCS", "Infosys"]),
Q("Routes 10.0.0.0/8 and 10.1.0.0/16 both match. Which wins for 10.1.5.9?",
  ["10.0.0.0/8", "10.1.0.0/16", "Neither", "Random"], 1, 3,
  "Longest prefix match: /16 is more specific than /8.",
  ["Cisco", "Juniper"]),
Q("What is 0.0.0.0/0 in a routing table?",
  ["An error", "Default route — the gateway of last resort",
   "Loopback", "Broadcast"], 1, 2,
  "When nothing else matches, packets go to the default gateway.",
  ["Wipro", "HCL"]),
Q("Static vs dynamic routing — when is static better?",
  ["Never", "Tiny networks / stub default routes — simple, no overhead",
   "Always", "Only on Wi-Fi"], 1, 5,
  "Static is fine for simple topologies; dynamic wins when links change.",
  ["Accenture", "TCS"]),
Q("What is 'metric' in a routing entry?",
  ["Speed of light", "Cost of the route — lower is preferred",
   "Packet size", "Encryption level"], 1, 4,
  "Metric (hops, bandwidth, delay...) lets routers compare alternate paths.",
  ["Amazon", "Juniper"]),
Q("A packet matches 192.168.0.0/16, 192.168.1.0/24, and 0.0.0.0/0. Winner?",
  ["192.168.0.0/16", "192.168.1.0/24", "0.0.0.0/0", "Dropped"], 1, 6,
  "/24 is the longest match — specificity always wins.",
  ["Google", "Arista"]),
]),

L("distance-vector", "Distance Vector Routing (RIP)",
"""## The idea: rumors

Each router tells neighbors its *entire* table: "I can reach X in N hops."
Neighbors believe, add 1, and repeat. **Bellman-Ford** underneath.

## RIP specifics

- Metric = **hop count**, max **15** (16 = unreachable!)
- Updates every **30 seconds** (periodic, chatty)
- **Split horizon**: don't advertise a route back where you learned it
- **Poison reverse**: advertise it back with metric 16 (explicitly dead)

## Count to infinity (the classic flaw)

A–B–C line, A dies. B still thinks "C reaches A in 2" → B says "3" →
C says "4"… they count up to 16 before agreeing A is gone.
Slow convergence — why link-state won.
""",
[
Q("What algorithm does distance-vector routing use?",
  ["Dijkstra", "Bellman-Ford", "A*", "BFS"], 1, 3,
  "Distance vector = distributed Bellman-Ford: relax via neighbors' claims.",
  ["TCS", "Infosys"]),
Q("In RIP, what does hop count 16 mean?",
  ["16 routers away", "Unreachable (infinity)",
   "Fastest path", "Default route"], 1, 4,
  "RIP caps at 15 hops; 16 = infinity = dead.",
  ["Cisco", "Juniper"]),
Q("What is 'count to infinity'?",
  ["A fast algorithm", "Slow convergence where routers increment metrics after a failure",
   "A security feature", "Packet fragmentation"], 1, 5,
  "Bad news propagates slowly as routers keep believing stale rumors, counting up to 16.",
  ["Amazon", "Wipro"]),
Q("What does split horizon prevent?",
  ["Slow links", "Advertising a route back to the neighbor you learned it from (loops)",
   "Encryption", "Broadcasts"], 1, 6,
  "Don't tell B about a route you learned FROM B — kills simple 2-node loops.",
  ["Accenture", "HCL"]),
Q("How often does RIP broadcast its full table?",
  ["Never", "Every 30 seconds", "Every hour", "Only on change"], 1, 7,
  "Periodic full updates — simple but chatty (a reason OSPF replaced it).",
  ["Juniper", "TCS"]),
Q("RIP's max useful network diameter is 15 hops. Why is this a limitation?",
  ["It's not", "Large enterprise/ISP networks exceed 15 hops — RIP can't serve them",
   "It wastes ports", "It needs IPv6"], 1, 8,
  "The 15-hop cap makes RIP suitable only for small networks.",
  ["Cisco", "Arista"]),
]),

L("link-state", "Link State Routing (OSPF)",
"""## The idea: everyone gets the full map

Each router **floods** its local link states; every router builds an
identical **link-state database** (the whole topology), then runs
**Dijkstra** locally to compute shortest paths.

## OSPF specifics

- Metric = **cost** (based on bandwidth; faster link = lower cost)
- **Areas**: hierarchy to scale (backbone Area 0 connects all)
- Only sends **changes** (plus periodic refresh) — efficient
- Fast convergence vs RIP

## Dijkstra in one line

"Repeatedly pick the unvisited node with the smallest known distance,
relax its neighbors." — O(E log V) with a heap.

## Link-state vs distance-vector

| | DV (RIP) | LS (OSPF) |
|---|---|---|
| Knowledge | Neighbors' rumors | Full topology |
| Algorithm | Bellman-Ford | Dijkstra |
| Convergence | Slow | Fast |
| Chatter | Periodic full tables | Event-driven updates |
""",
[
Q("What does each OSPF router compute with?",
  ["Bellman-Ford", "Dijkstra's shortest path on the full topology",
   "BFS", "Random"], 1, 3,
  "Link-state = everyone knows the map; Dijkstra finds best paths locally.",
  ["Cisco", "Juniper"]),
Q("In OSPF, lower cost means…?",
  ["Slower link", "Preferred path — cost is inverse to bandwidth",
   "More hops", "Encrypted"], 1, 4,
  "Cost ~ 10^8/bandwidth: fast links get low cost and win.",
  ["TCS", "Infosys"]),
Q("What is OSPF Area 0?",
  ["A VLAN", "The backbone area — all other areas connect through it",
   "A firewall zone", "The DMZ"], 1, 5,
  "Hierarchical design: Area 0 (backbone) interconnects all areas, limiting flooding scope.",
  ["Amazon", "Wipro"]),
Q("Why does OSPF converge faster than RIP?",
  ["It has fewer routers", "Changes flood immediately; routers recompute from the full map",
   "It uses UDP", "It doesn't"], 1, 6,
  "Event-driven updates + complete topology = fast, correct reconvergence.",
  ["Google", "Accenture"]),
Q("A link fails in OSPF. What happens first?",
  ["Count to infinity", "The routers adjacent flood updated LSAs; all recompute",
   "Nothing for 30s", "Manual fix"], 1, 7,
  "Link-state advertisements propagate the change; Dijkstra reruns everywhere.",
  ["Juniper", "Arista"]),
Q("Dijkstra with a binary heap runs in…?",
  ["O(V^2)", "O(E log V)", "O(V+E)", "O(1)"], 1, 9,
  "Classic result: O((V+E) log V), usually written O(E log V).",
  ["Goldman Sachs", "Google"]),
]),

L("bgp-stp", "BGP & Spanning Tree (STP)",
"""## BGP: routing between organizations

- **EGP** (Exterior Gateway Protocol) — the Internet's routing protocol
- Works on **Autonomous Systems** (ASes, e.g. ISPs) with **AS numbers**
- **Path vector**: advertises the full AS path (loop prevention!)
- Policy-driven: business relationships (customer/provider/peer) matter more than hops
- Runs over **TCP 179** — needs reliability for the global table (~1M routes)

## STP: no loops in switched LANs

Redundant switch links create **broadcast storms** (loops!). STP:
1. Elects a **root bridge** (lowest bridge ID)
2. Each switch picks a **root port** (shortest path to root)
3. Blocks redundant ports → a **loop-free tree**
4. On failure, unblocks backup (convergence ~30-50s; RSTP is faster)

## Interview contrast

"BGP routes between ASes using policy + AS-path; STP prevents Layer-2 loops by blocking redundant ports."
""",
[
Q("What does BGP route between?",
  ["Hosts", "Autonomous Systems (ISPs/organizations)",
   "VLANs", "Processes"], 1, 2,
  "BGP is the inter-domain protocol gluing ASes into the Internet.",
  ["Cisco", "Juniper"]),
Q("How does BGP prevent loops?",
  ["Hop count", "AS-path: if your own AS number is in the path, reject it",
   "TTL", "Encryption"], 1, 5,
  "Path-vector: the full AS sequence travels with the route — seeing yourself = loop.",
  ["Amazon", "Cloudflare"]),
Q("Why does BGP run over TCP?",
  ["It's faster", "The global routing table needs reliable delivery (TCP 179)",
   "UDP is banned", "For encryption"], 1, 6,
  "~1M prefixes must arrive intact — TCP's reliability fits.",
  ["Arista", "Juniper"]),
Q("What problem does STP solve?",
  ["Slow internet", "Layer-2 loops causing broadcast storms on redundant links",
   "IP conflicts", "DNS failures"], 1, 4,
  "Parallel switch links loop broadcasts forever; STP blocks redundancies into a tree.",
  ["TCS", "Wipro"]),
Q("How is the STP root bridge chosen?",
  ["Random", "Lowest bridge ID (priority + MAC)",
   "Fastest switch", "Oldest switch"], 1, 7,
  "Lowest bridge ID wins; ties break on MAC.",
  ["Cisco", "HCL"]),
Q("RSTP vs STP — the main improvement?",
  ["More VLANs", "Much faster convergence (seconds vs ~30-50s)",
   "Wireless support", "IPv6"], 1, 8,
  "RSTP (802.1w) adds rapid port roles/handshakes for fast failover.",
  ["Juniper", "Accenture"]),
]),
])


# ---------------------------------------------------------------------------
# MODULE 6 — NETWORK SECURITY (5 lessons)
# ---------------------------------------------------------------------------

_net_security = M("net-security", "Network Security",
    "Firewalls, VPNs and tunneling, the TLS handshake step-by-step, DDoS, IDS/IPS.",
[

L("firewalls", "Firewalls",
"""## Three generations

1. **Packet filter** (stateless): allow/deny by IP, port, protocol.
   Fast, dumb — can't tell legit from spoofed easily.
2. **Stateful**: tracks connection state. "Allow return traffic for
   connections *we* started." The workhorse of the 2000s.
3. **NGFW** (Next-Gen): adds application awareness, IPS, URL filtering,
   user identity. (Palo Alto, Fortinet.)

## Default policies

- **Default-deny** (whitelist): block everything, allow exceptions — secure
- **Default-allow** (blacklist): allow everything, block known-bad — convenient, leaky

## DMZ

A **demilitarized zone**: public servers (web, mail) sit between the
outer and inner firewalls — reachable from the internet, isolated
from the internal LAN.
""",
[
Q("What does a stateful firewall track?",
  ["Passwords", "Connection state — to allow return traffic of initiated connections",
   "DNS names", "User behavior"], 1, 3,
  "Stateful inspection remembers outbound connections and permits their replies.",
  ["Palo Alto", "Cisco"]),
Q("Which default policy is more secure?",
  ["Default-allow", "Default-deny (whitelist)",
   "No policy", "Allow all"], 1, 2,
  "Default-deny blocks everything except explicit allows — smaller attack surface.",
  ["TCS", "Infosys"]),
Q("What is a DMZ?",
  ["A VPN", "A buffer network for public servers between two firewalls",
   "A type of malware", "A DNS zone"], 1, 4,
  "DMZ hosts internet-facing servers isolated from the internal LAN.",
  ["Wipro", "Accenture"]),
Q("What can a packet filter NOT do well?",
  ["Block ports", "Distinguish legitimate vs spoofed packets in a stateless way",
   "Read IPs", "Run fast"], 1, 5,
  "Stateless filters see packets in isolation — no connection context.",
  ["HCL", "Fortinet"]),
Q("What does NGFW add over stateful firewalls?",
  ["More ports", "App awareness, IPS, URL filtering, user identity",
   "Faster cables", "Bigger racks"], 1, 6,
  "Next-gen = Layer-7 intelligence on top of stateful filtering.",
  ["Palo Alto", "Amazon"]),
Q("Where should the firewall rule 'allow established' typically sit?",
  ["Last", "Near the top — fast-path return traffic before expensive checks",
   "Nowhere", "In the DMZ"], 1, 8,
  "Early established-match avoids re-evaluating every return packet against the full ruleset.",
  ["Juniper", "Palo Alto"]),
]),

L("vpn", "VPNs & Tunneling",
"""## What a VPN does

Creates an **encrypted tunnel** through an untrusted network. Your traffic
is encapsulated + encrypted — the coffee-shop Wi-Fi sees only gibberish.

## Main protocols

- **IPsec**: network-layer suite (AH = integrity, ESP = encryption).
  Site-to-site VPNs. Two modes: **transport** (host-to-host) vs **tunnel** (gateway-to-gateway).
- **SSL/TLS VPN**: browser or client-based, easier through firewalls (port 443).
- **WireGuard**: modern, tiny codebase, fast (UDP-based).

## Tunneling concept

Take a packet, wrap it *inside* another packet. The inner packet's
addresses can even be private — the outer header does the delivery.
(GRE, IPsec tunnel mode, and VPNs all use this trick.)

## Split tunnel vs full tunnel

- **Full**: all traffic via VPN (secure, slower, company sees everything)
- **Split**: only corporate traffic via VPN (faster, less private)
""",
[
Q("What does a VPN primarily provide?",
  ["Faster internet", "Encrypted tunnel protecting traffic on untrusted networks",
   "Free Wi-Fi", "More bandwidth"], 1, 1,
  "Encryption + tunneling = confidentiality and integrity over hostile networks.",
  ["TCS", "Infosys"]),
Q("In IPsec, what does ESP provide that AH doesn't?",
  ["Integrity", "Encryption (confidentiality)",
   "Authentication", "Nothing"], 1, 4,
  "AH = integrity/auth only. ESP adds encryption.",
  ["Cisco", "Palo Alto"]),
Q("What is split tunneling?",
  ["Splitting cables", "Only corporate traffic goes through VPN; rest goes direct",
   "Two VPNs at once", "Broken VPN"], 1, 5,
  "Split = faster + less company visibility; full = maximum control.",
  ["Accenture", "Wipro"]),
Q("Why is WireGuard notable?",
  ["It's old", "Tiny auditable codebase, very fast, UDP-based",
   "It needs no keys", "It's unencrypted"], 1, 6,
  "~4k lines vs IPsec's hundreds of thousands — simpler = fewer bugs, plus speed.",
  ["Cloudflare", "Mullvad"]),
Q("In IPsec tunnel mode, what gets encrypted?",
  ["Nothing", "The entire original IP packet (header + payload)",
   "Only the payload", "Only the header"], 1, 7,
  "Tunnel mode wraps the whole inner packet; transport mode protects only the payload.",
  ["Juniper", "Palo Alto"]),
Q("Your VPN is on but DNS leaks. What does that mean?",
  ["VPN is fast", "DNS queries bypass the tunnel — exposing browsing to the local network/ISP",
   "VPN is broken fully", "Nothing"], 1, 8,
  "DNS leaks defeat VPN privacy; clients must route DNS through the tunnel.",
  ["Proton", "Mullvad"]),
]),

L("tls-handshake", "The TLS Handshake — Step by Step",
"""## TLS 1.2 handshake (the classic)

```
Client                                              Server
  | ---- ClientHello (ciphers, random Rc) ---------> |
  | <---- ServerHello (chosen cipher, random Rs) --- |
  | <---- Certificate (public key) ---------------- |
  | ---- ClientKeyExchange (premaster, encrypted) -> |
  | ---- ChangeCipherSpec, Finished --------------> |
  | <---- ChangeCipherSpec, Finished -------------- |
```

1. **Hello**: agree on cipher suite + exchange randoms
2. **Certificate**: server proves identity (CA-signed)
3. **Key exchange**: client sends premaster secret encrypted with server's public key
4. **Finished**: both derive session keys, switch to encrypted chat

## TLS 1.3 (faster)

- **1-RTT** (vs 2-RTT in 1.2), **0-RTT** resumption
- Removed weak ciphers (RSA key exchange, CBC modes)
- Encrypted handshake after ServerHello (less metadata leakage)

## Key insight

**Asymmetric crypto** (slow) only bootstraps trust; then both sides
use fast **symmetric** session keys. Certificates + CA chain = identity.
""",
[
Q("What is the purpose of the server Certificate in TLS?",
  ["Encryption", "Proving the server's identity via CA signature",
   "Speed", "Compression"], 1, 2,
  "The client validates the CA-signed cert to know it's talking to the real server.",
  ["TCS", "Infosys"]),
Q("Why does TLS switch to symmetric keys after the handshake?",
  ["Symmetric is weaker", "Asymmetric crypto is slow — symmetric is ~1000x faster for bulk data",
   "Regulations", "Tradition"], 1, 5,
  "Public-key crypto bootstraps trust; symmetric keys do the heavy lifting.",
  ["Google", "Cloudflare"]),
Q("How many round trips does TLS 1.3 need?",
  ["2", "1 (and 0-RTT for resumption)",
   "3", "0"], 1, 6,
  "TLS 1.3 cut the handshake to 1-RTT; resumption can hit 0-RTT.",
  ["Microsoft", "Amazon"]),
Q("What does 'premaster secret' become?",
  ["A password", "Input to derive the symmetric session keys (with client+server randoms)",
   "The certificate", "A cookie"], 1, 7,
  "master_secret = PRF(premaster, Rc + Rs); session keys derive from it.",
  ["Palo Alto", "Cisco"]),
Q("In TLS 1.2, how does the client securely send the premaster secret?",
  ["Plaintext", "Encrypted with the server's public key from its certificate",
   "Via DNS", "It doesn't"], 1, 4,
  "Only the server's private key can decrypt it — that's the point of the certificate.",
  ["Wipro", "Accenture"]),
Q("What did TLS 1.3 remove and why?",
  ["Nothing", "Weak primitives (RSA key exchange, CBC, SHA-1) — smaller, safer protocol",
   "Certificates", "Encryption"], 1, 9,
  "1.3 deleted legacy options, killing whole classes of downgrade attacks.",
  ["Google", "Mozilla"]),
]),

L("ddos", "DDoS Attacks & Mitigation",
"""## The idea

Overwhelm the target with traffic from **many** sources (a botnet).
Not about breaking in — about making the service **unavailable**.

## Main flavors

- **Volumetric** (L3/L4): UDP floods, ICMP floods, amplification (DNS/NTP reflection — small request, huge reply)
- **Protocol**: SYN floods, Ping of Death — exhaust state/resources
- **Application** (L7): slowloris (slow headers), HTTP floods — hard to distinguish from legit users

## Defenses (defense in depth)

1. **Overprovision + anycast**: absorb and spread (Cloudflare/Akamai model)
2. **Scrubbing centers**: dirty traffic cleaned upstream
3. **Rate limiting / WAF**: per-IP throttles, challenge pages
4. **SYN cookies**: stateless SYN handling defeats SYN floods
""",
[
Q("What is the goal of a DDoS attack?",
  ["Steal data", "Make a service unavailable by overwhelming it",
   "Install malware", "Phish users"], 1, 1,
  "DDoS = Distributed Denial of Service: availability attack, not intrusion.",
  ["TCS", "Infosys"]),
Q("What is DNS amplification?",
  ["Fast DNS", "Spoofed small queries trigger huge responses to the victim",
   "DNS caching", "Encrypted DNS"], 1, 5,
  "Attackers abuse open resolvers: 60-byte query → 4000-byte reply at the victim. Amplification factor ~60x.",
  ["Cloudflare", "Akamai"]),
Q("What is slowloris?",
  ["A firewall", "L7 attack holding connections open with slow partial headers",
   "A VPN", "A worm"], 1, 6,
  "Slowloris drips header bytes to exhaust server connection slots — little bandwidth needed.",
  ["Palo Alto", "Imperva"]),
Q("How do SYN cookies defeat SYN floods?",
  ["They encrypt SYNs", "Server stays stateless — encodes state in the SYN-ACK sequence number",
   "They block all SYNs", "They add RAM"], 1, 7,
  "No half-open queue to exhaust: state is reconstructed from the client's final ACK.",
  ["Linux", "Cloudflare"]),
Q("Why is anycast effective against volumetric DDoS?",
  ["It's encrypted", "Attack traffic spreads across many global PoPs instead of one target",
   "It's faster", "It hides IPs"], 1, 8,
  "Anycast routes each bot to the nearest scrubbing PoP — the flood is diluted globally.",
  ["Cloudflare", "Google"]),
Q("L7 DDoS vs volumetric — which is harder to filter and why?",
  ["Volumetric", "L7 — attack requests look like legitimate user traffic",
   "Same", "Neither"], 1, 9,
  "You can't just drop packets; you need behavioral analysis/WAF to spot L7 abuse.",
  ["Akamai", "Imperva"]),
]),

L("ids-ips", "IDS vs IPS & Security Monitoring",
"""## IDS vs IPS

| | IDS (Detection) | IPS (Prevention) |
|---|---|---|
| Placement | Out-of-band (span port) | Inline (traffic flows through) |
| Action | **Alerts** | **Blocks/drops** |
| Risk | Missed attacks | False positives break legit traffic |

## Detection methods

- **Signature-based**: known attack patterns (Snort rules) — fast, blind to zero-days
- **Anomaly-based**: baseline normal, flag deviations — catches novel attacks, noisier
- **Hybrid**: both (modern NGFW/EDR)

## Supporting cast

- **SIEM**: collects/correlates logs (Splunk, ELK) — the security dashboard
- **Honeypot**: fake vulnerable system to study attackers safely
- **Zero Trust**: "never trust, always verify" — no implicit LAN trust
""",
[
Q("What is the key difference between IDS and IPS?",
  ["Price", "IDS only alerts; IPS sits inline and blocks",
   "Speed", "Vendor"], 1, 2,
  "Detection = passive monitoring; Prevention = active inline blocking.",
  ["Palo Alto", "Cisco"]),
Q("Why is an IPS riskier to deploy than IDS?",
  ["Cost", "False positives can block legitimate traffic (inline)",
   "It's slower", "Needs more power"], 1, 5,
  "Inline blocking means a bad signature = outage. Tune carefully.",
  ["Fortinet", "TCS"]),
Q("Signature vs anomaly detection?",
  ["Same", "Signatures match known attacks (fast, blind to zero-days); anomaly flags deviations (catches novel, noisier)",
   "Anomaly is older", "Signatures need AI"], 1, 6,
  "Complementary: signatures for known, anomaly for unknown.",
  ["CrowdStrike", "Wipro"]),
Q("What is a honeypot?",
  ["A firewall", "A decoy system designed to attract and study attackers",
   "A VPN", "Antivirus"], 1, 3,
  "Honeypots waste attacker time and reveal their tools/techniques safely.",
  ["Accenture", "HCL"]),
Q("What does a SIEM do?",
  ["Encrypts", "Centralizes and correlates security logs for detection/response",
   "Routes packets", "Filters spam"], 1, 4,
  "SIEM (Splunk/ELK) = the security team's single pane of glass.",
  ["Splunk", "IBM"]),
Q("What is Zero Trust in one line?",
  ["No passwords", "'Never trust, always verify' — no implicit trust for LAN/insiders",
   "Zero firewalls", "Trust everyone"], 1, 7,
  "Every request is authenticated/authorized regardless of network location.",
  ["Google", "Microsoft"]),
]),
])


# ---------------------------------------------------------------------------
# MODULE 7 — ADVANCED (4 lessons)
# ---------------------------------------------------------------------------

_advanced = M("advanced", "Advanced Topics",
    "SDN, WebSockets, QUIC deep dive, and 5G network concepts.",
[

L("sdn", "SDN — Software Defined Networking",
"""## The big idea: separate brains from brawn

Traditional: every router/switch runs its own control plane (distributed smarts).
**SDN**: centralize the control plane in a **controller**; switches become
dumb fast **forwarding** boxes.

## The three planes

- **Data plane**: forwards packets (the switches)
- **Control plane**: decides routes (the controller — centralized!)
- **Management plane**: config/monitoring (NETCONF, dashboards)

## OpenFlow

The classic southbound protocol: controller installs **flow table**
entries ("if dst=10.0.0.5 → output port 3") into switches via OpenFlow.
Switches just match + act.

## Why it matters

Programmable networks: spin up policies in software, global view for
traffic engineering, the foundation of modern data-center fabrics
(and a hot interview topic).
""",
[
Q("What does SDN separate?",
  ["Hardware from software", "Control plane (decisions) from data plane (forwarding)",
   "TCP from UDP", "IPv4 from IPv6"], 1, 3,
  "Centralized controller decides; switches just forward per installed rules.",
  ["Cisco", "Google"]),
Q("What is OpenFlow?",
  ["A firewall", "Southbound protocol: controller programs switch flow tables",
   "A VPN", "A routing algorithm"], 1, 5,
  "OpenFlow = the API between controller and dumb switches.",
  ["ONF", "Arista"]),
Q("What sits in a switch flow table?",
  ["Passwords", "Match fields + actions (e.g. 'dst=X → output port 3')",
   "User data", "DNS records"], 1, 6,
  "Flow entries are match-action rules installed by the controller.",
  ["Juniper", "VMware"]),
Q("SDN's biggest operational win?",
  ["Cheaper cables", "Network-wide programmability + global view for traffic engineering",
   "Faster CPUs", "More ports"], 1, 7,
  "One program changes the whole fabric consistently — no box-by-box CLI.",
  ["Google", "Microsoft"]),
Q("Which plane does the SDN controller belong to?",
  ["Data", "Control", "Management", "Physical"], 1, 4,
  "Controller = centralized control plane.",
  ["TCS", "Infosys"]),
Q("Traditional vs SDN control: what's the core difference?",
  ["Speed", "Distributed per-device smarts vs centralized controller",
   "Cables", "Protocols"], 1, 8,
  "Traditional routers each run OSPF/BGP locally; SDN moves decisions to the controller.",
  ["Cisco", "Arista"]),
Q("What is the 'southbound' vs 'northbound' API in SDN?",
  ["Cable directions", "Southbound: controller→switch (OpenFlow); Northbound: controller→apps",
   "Compass routing", "Two VPNs"], 1, 9,
  "Southbound programs the data plane; northbound exposes network services to applications.",
  ["ONF", "VMware"]),
]),

L("websockets", "WebSockets — Beyond Request/Response",
"""## The problem with HTTP

HTTP is **client-initiated**: the server can't push. Workarounds:
- **Polling**: client asks every N seconds (wasteful)
- **Long polling**: server holds the request until data arrives (hacky)
- **SSE**: server→client stream (one-way)

## WebSocket: full-duplex over one TCP connection

1. Client sends HTTP **Upgrade** request (`Upgrade: websocket`)
2. Server replies **101 Switching Protocols**
3. Now: **both sides send frames anytime** — chat, games, live dashboards

Runs over **ws://** (80) or **wss://** (443, encrypted).

## WebSocket vs SSE vs polling

| | Direction | Overhead |
|---|---|---|
| Polling | Client→server asks | High |
| SSE | Server→client only | Medium |
| WebSocket | **Both ways** | Low (after handshake) |

Use WebSocket for chat, multiplayer, trading tickers, collaborative editing.
""",
[
Q("Why can't plain HTTP push data to clients?",
  ["It can", "HTTP is client-initiated — servers only respond",
   "It's too slow", "Firewalls"], 1, 2,
  "No server-initiated messages in HTTP/1.1 semantics — hence polling/SSE/WebSocket.",
  ["TCS", "Infosys"]),
Q("What status code completes a WebSocket upgrade?",
  ["200", "101 Switching Protocols", "404", "301"], 1, 4,
  "101 = protocol switch accepted; then raw frames flow both ways.",
  ["Google", "Microsoft"]),
Q("WebSocket vs SSE — key difference?",
  ["Same", "WebSocket is full-duplex; SSE is server→client only",
   "SSE is faster", "WebSocket is older"], 1, 5,
  "Need client→server pushes (chat, games)? WebSocket. One-way feed? SSE suffices.",
  ["Slack", "Discord"]),
Q("What does wss:// mean?",
  ["Broken socket", "WebSocket over TLS (encrypted, port 443)",
   "Faster socket", "UDP socket"], 1, 6,
  "wss = secure WebSocket, like https is to http.",
  ["Cloudflare", "Wipro"]),
Q("Why is polling wasteful for live data?",
  ["It's not", "Most polls return 'nothing new' — empty requests burn bandwidth/battery",
   "It's insecure", "Servers crash"], 1, 7,
  "Polling trades latency vs waste; WebSocket eliminates the tradeoff.",
  ["Meta", "Robinhood"]),
Q("After the handshake, what does WebSocket run over?",
  ["A new HTTP connection per message", "The same single TCP connection, full-duplex frames",
   "UDP", "Two connections"], 1, 8,
  "One upgraded TCP connection carries bidirectional frames — minimal overhead.",
  ["Socket.io", "Pusher"]),
]),

L("quic", "QUIC — The Future Transport",
"""## QUIC in one paragraph

Google's **UDP-based** transport (now RFC 9000, basis of **HTTP/3**):
rebuilds TCP-like reliability + TLS 1.3 on top of UDP, but with
**independent streams** — one lost packet stalls only its own stream.

## Killer features

- **0-RTT / 1-RTT handshakes** (TCP+TLS needed 2-3)
- **No head-of-line blocking** across streams
- **Connection migration**: switch Wi-Fi→cellular, connection survives
  (identified by connection ID, not IP+port!)
- Built-in encryption (everything except a few header bits)

## Why UDP?

Middleboxes ossified TCP — new TCP options get blocked. UDP is a
dumb envelope middleboxes pass through, so innovation lives in
user space (no kernel upgrades needed!).

## Interview line

"QUIC = reliable, encrypted, multiplexed transport over UDP —
faster handshakes, per-stream independence, connection migration."
""",
[
Q("What problem does QUIC solve that TCP couldn't?",
  ["Speed of light", "Head-of-line blocking + slow handshakes + no connection migration",
   "DNS", "IPv6"], 1, 5,
  "QUIC's streams are independent and handshakes are 0/1-RTT.",
  ["Google", "Cloudflare"]),
Q("Why is QUIC built on UDP?",
  ["UDP is reliable", "Middleboxes pass UDP through; TCP is ossified — innovation happens in user space",
   "UDP is encrypted", "Faster DNS"], 1, 7,
  "New TCP features die in middleboxes; UDP is a neutral envelope.",
  ["Fastly", "Mozilla"]),
Q("How does QUIC survive a Wi-Fi → cellular switch?",
  ["It doesn't", "Connection IDs (not IP+port) identify connections",
   "It restarts", "Magic"], 1, 6,
  "QUIC connections are bound to IDs, so IP changes don't kill them.",
  ["Google", "Meta"]),
Q("Which HTTP version runs on QUIC?",
  ["HTTP/1.1", "HTTP/2", "HTTP/3", "HTTP/0.9"], 2, 4,
  "HTTP/3 = HTTP over QUIC.",
  ["Cloudflare", "Apple"]),
Q("QUIC handshake vs TCP+TLS 1.2 handshake?",
  ["Same", "QUIC: 0-1 RTT; TCP+TLS 1.2: 3-4 RTTs",
   "QUIC is slower", "No handshake in QUIC"], 1, 8,
  "Fewer round trips = huge win on high-latency mobile networks.",
  ["Google", "Akamai"]),
Q("Is QUIC traffic visible to middleboxes?",
  ["Fully", "Mostly encrypted — only a few header bits are visible (a privacy win)",
   "Not at all", "Yes, all of it"], 1, 9,
  "QUIC encrypts almost everything, limiting middlebox interference/snooping.",
  ["Mozilla", "Cloudflare"]),
]),

L("5g-networks", "5G Network Concepts",
"""## 5G's three promises (ITU)

- **eMBB**: Enhanced Mobile Broadband — 10-20 Gbps peak (4K/8K, AR)
- **URLLC**: Ultra-Reliable Low Latency — ~1ms (remote surgery, V2X)
- **mMTC**: Massive Machine-Type — 1M devices/km² (IoT sensors)

## Network slicing (the big idea)

**One physical network → many virtual networks**, each tuned:
a slice for emergency services (URLLC), one for streaming (eMBB),
one for sensors (mMTC). SDN/NFV make this possible.

## 5G architecture notes

- **Small cells**: dense low-power base stations (mmWave needs them)
- **Edge computing (MEC)**: process at the tower, not the cloud — kills latency
- **Standalone (SA)** vs **Non-standalone (NSA)**: SA = pure 5G core; NSA = 5G radio on 4G core (early deployments)

## Frequency reality

mmWave (24-40 GHz) = huge speed, tiny range, blocked by walls.
Sub-6 GHz = the practical workhorse coverage layer.
""",
[
Q("What are 5G's three ITU service classes?",
  ["Fast, faster, fastest", "eMBB, URLLC, mMTC",
   "2G, 3G, 4G", "TCP, UDP, QUIC"], 1, 3,
  "Enhanced broadband, ultra-reliable low-latency, massive IoT.",
  ["Ericsson", "Nokia"]),
Q("What is network slicing?",
  ["Cutting cables", "Multiple virtual networks with different SLAs on one physical infrastructure",
   "Phone screens", "SIM cards"], 1, 5,
  "Slicing = e.g. a URLLC slice for ambulances + eMBB slice for video, same towers.",
  ["Huawei", "Samsung"]),
Q("Why does mmWave need small cells?",
  ["It's cheap", "High frequencies have short range and poor obstacle penetration",
   "Regulations", "Battery life"], 1, 6,
  "mmWave = gigabits but meters of range; dense small cells compensate.",
  ["Qualcomm", "Verizon"]),
Q("What is MEC and why does 5G need it?",
  ["A phone brand", "Multi-access Edge Computing — process at the tower to hit ~1ms latency",
   "A cable", "A satellite"], 1, 7,
  "URLLC's 1ms budget can't survive a round trip to a distant cloud.",
  ["AWS", "Ericsson"]),
Q("NSA vs SA 5G?",
  ["Same", "NSA = 5G radio over 4G core (transitional); SA = full 5G core",
   "NSA is faster", "SA is older"], 1, 8,
  "Early 5G was NSA; true slicing/URLLC needs Standalone.",
  ["Nokia", "T-Mobile"]),
Q("Roughly how many devices per km² does mMTC target?",
  ["100", "10,000", "1,000,000", "1 billion"], 2, 4,
  "mMTC = massive IoT: ~1M devices/km².",
  ["Ericsson", "IoT Analytics"]),
]),
])


# ---------------------------------------------------------------------------
# ASSEMBLY
# ---------------------------------------------------------------------------

CURRICULUM = {
    "domain": DOMAIN,
    "modules": [
        _osi_tcpip,
        _ip_subnetting,
        _tcp_udp,
        _app_layer,
        _routing_switching,
        _net_security,
        _advanced,
    ],
}


# ---------------------------------------------------------------------------
# Integration helpers (mirror dsa_curriculum_seed.py)
# ---------------------------------------------------------------------------

def _lesson_id(slug):
    return str(_uuid.uuid5(_uuid.NAMESPACE_URL, "skillforge:cn:lesson:" + slug))


def _question_id(lesson_slug, idx):
    return str(_uuid.uuid5(
        _uuid.NAMESPACE_URL, f"skillforge:cn:question:{lesson_slug}:{idx}"))


def _now_iso():
    return datetime.now(_tz.utc).isoformat()


def _as_sql_value(v):
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, (list, dict)):
        v = json.dumps(v, ensure_ascii=False)
    return "'" + str(v).replace("'", "''") + "'"


def _iter_rows():
    """Yield (kind, dict) for every lesson and question, mapped to the
    sibling's already-seeded CN modules."""
    order_per_module = {}
    for m in CURRICULUM["modules"]:
        sib = MODULE_MAP[m["slug"]]
        order_per_module.setdefault(sib, 100)
        for les in m["lessons"]:
            lid = _lesson_id(les["slug"])
            order_per_module[sib] += 1
            yield ("lesson", {
                "id": lid,
                "module_slug": sib,
                "slug": les["slug"],
                "title": les["title"],
                "content": les["theory_md"],
                "order_index": order_per_module[sib],
            })
            for qi, q in enumerate(les["questions"]):
                yield ("question", {
                    "id": _question_id(les["slug"], qi),
                    "lesson_id": lid,
                    "module_slug": sib,
                    "qtype": "mcq",
                    "difficulty": q["difficulty"],
                    "prompt": q["prompt"],
                    "choices": q["choices"],
                    "answer_index": q["answer_index"],
                    "explanation": q["explanation"],
                    "company_tags": q["company_tags"],
                })


def emit_sql(out=None):
    """Emit INSERTs against the real curriculum_* tables.

    Lessons attach to the sibling's already-seeded CN modules via a
    module_id subselect; questions carry domain/module slugs + lesson_id.
    Safe to run after migration m1n2curr001_curriculum.
    """
    out = out or sys.stdout
    ts = _now_iso()
    for kind, r in _iter_rows():
        if kind == "lesson":
            out.write(
                "INSERT INTO curriculum_lessons "
                "(id, module_id, slug, title, content, order_index, "
                "estimated_minutes, has_visual) "
                "SELECT %s, m.id, %s, 30, 0 FROM curriculum_modules m "
                "WHERE m.slug = %s AND m.domain_slug = %s;\n"
                % (_as_sql_value(r["id"]),
                   ", ".join(_as_sql_value(r[k]) for k in
                             ("slug", "title", "content", "order_index")),
                   _as_sql_value(r["module_slug"]),
                   _as_sql_value(SIBLING_DOMAIN_SLUG)))
        else:
            out.write(
                "INSERT INTO curriculum_questions "
                "(id, domain_slug, module_slug, lesson_id, difficulty, qtype, "
                "prompt, choices, answer_index, explanation, company_tags, "
                "created_at) VALUES (%s);\n"
                % ", ".join([
                    _as_sql_value(r["id"]),
                    _as_sql_value(SIBLING_DOMAIN_SLUG),
                    _as_sql_value(r["module_slug"]),
                    _as_sql_value(r["lesson_id"]),
                    str(r["difficulty"]),
                    _as_sql_value(r["qtype"]),
                    _as_sql_value(r["prompt"]),
                    _as_sql_value(r["choices"]),
                    _as_sql_value(r["answer_index"]),
                    _as_sql_value(r["explanation"]),
                    _as_sql_value(r["company_tags"]),
                    _as_sql_value(ts),
                ]))
    out.flush()


def seed(session=None):
    """Idempotent ORM insert using the real models.

    Idempotent on lesson/question ids (deterministic uuid5) — skips existing.
    Returns counts dict.
    """
    from app.adapters.outbound.models import (
        CurriculumLessonModel, CurriculumQuestionModel, CurriculumModuleModel,
    )
    counts = {"lessons": 0, "questions": 0, "skipped": 0}
    mod_ids = {}
    for m in CURRICULUM["modules"]:
        sib = MODULE_MAP[m["slug"]]
        if sib not in mod_ids:
            mod = session.query(CurriculumModuleModel).filter_by(
                slug=sib, domain_slug=SIBLING_DOMAIN_SLUG).one()
            mod_ids[sib] = mod.id
    for kind, r in _iter_rows():
        if kind == "lesson":
            exists = session.query(CurriculumLessonModel).filter_by(
                id=r["id"]).first()
            if exists:
                counts["skipped"] += 1
                continue
            session.add(CurriculumLessonModel(
                id=r["id"], module_id=mod_ids[r["module_slug"]],
                slug=r["slug"], title=r["title"], content=r["content"],
                order_index=r["order_index"], estimated_minutes=30,
                has_visual=False))
            counts["lessons"] += 1
        else:
            exists = session.query(CurriculumQuestionModel).filter_by(
                id=r["id"]).first()
            if exists:
                counts["skipped"] += 1
                continue
            session.add(CurriculumQuestionModel(
                id=r["id"], domain_slug=SIBLING_DOMAIN_SLUG,
                module_slug=r["module_slug"], lesson_id=r["lesson_id"],
                difficulty=r["difficulty"], qtype=r["qtype"],
                prompt=r["prompt"],
                choices=json.dumps(r["choices"]) if r["choices"] else None,
                answer_index=r["answer_index"], explanation=r["explanation"],
                company_tags=json.dumps(r["company_tags"]),
                created_at=datetime.now(_tz.utc)))
            counts["questions"] += 1
    session.commit()
    return counts


def verify_counts():
    modules = CURRICULUM["modules"]
    lessons = sum(len(m["lessons"]) for m in modules)
    mcqs = sum(len(les["questions"]) for m in modules for les in m["lessons"])
    per_module = {m["slug"]: (len(m["lessons"]),
                              sum(len(les["questions"]) for les in m["lessons"]))
                  for m in modules}
    narrow = [les["slug"] for m in modules for les in m["lessons"]
              if les["difficulty_max"] - les["difficulty_min"] < 4]
    unmapped = [m["slug"] for m in modules if m["slug"] not in MODULE_MAP]
    bad_sib = [m["slug"] for m in modules
               if MODULE_MAP.get(m["slug"]) not in
               {"network-models", "ip-addressing", "tcp-udp",
                "routing-switching", "application-layer"}]
    return {"modules": len(modules), "lessons": lessons, "mcqs": mcqs,
            "per_module": per_module, "narrow_lessons": narrow,
            "unmapped_modules": unmapped, "bad_sibling": bad_sib}


if __name__ == "__main__":
    c = verify_counts()
    print("modules:", c["modules"])
    print("lessons:", c["lessons"])
    print("mcq questions:", c["mcqs"])
    print("\nper module (lessons, mcqs) -> sibling module:")
    for m in CURRICULUM["modules"]:
        nl, nq = c["per_module"][m["slug"]]
        print(f"  {m['slug']:20s} lessons={nl:2d} mcqs={nq:3d} -> {MODULE_MAP[m['slug']]}")
    assert not c["narrow_lessons"], c["narrow_lessons"]
    assert not c["unmapped_modules"], c["unmapped_modules"]
    assert not c["bad_sibling"], c["bad_sibling"]
    assert c["modules"] == 7 and c["lessons"] == 41
    assert c["mcqs"] >= 250
    print("\nAll assertions passed.")
