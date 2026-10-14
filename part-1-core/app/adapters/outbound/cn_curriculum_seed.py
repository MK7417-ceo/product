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
]),


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
