# Proposals: Ethernet (draft)

This is a proposal for a later author/reviewer step, not approved canonical knowledge.
Create candidates only after comparing with other network-foundations research.

## Candidate atomic units and dependencies

- `NET.ETHERNET.FRAME` (candidate): distinguish MAC frame, frame fields, and MAC client
  payload; depends on an accepted MAC-address unit. Hold detailed field sizes and exact
  frame-length convention until IEEE 802.3 clauses are available.
- `NET.ETHERNET.ENCAPSULATION` (candidate): compare Ethernet II Type-based IP
  encapsulation (RFC 894) with IEEE 802 LLC/SNAP IP encapsulation (RFC 1042). Depends
  on frame unit and candidate `NET.ETHERNET.ETHERTYPE`.
- `NET.ETHERNET.MTU` (candidate): explain IP MTU versus MAC frame size and padding,
  with limits of source/version made explicit. Depends on frame and encapsulation units.
- `NET.ETHERNET.BRIDGE-RELAY` (candidate, blocked): source learning and forwarding,
  filtering, and flooding. Depends on MAC-address unit and verified IEEE 802.1Q clauses.
- `NET.ETHERNET.DUPLEX` (candidate, blocked for normative detail): contrast shared
  half-duplex CSMA/CD with full duplex, bounded to supported IEEE 802.3 modes.

## Measurable outcome candidates

1. **Candidate `LO.NET.ETHERNET.ENCAPSULATION.01`:** Given an RFC 894 IPv4 frame
   description and an RFC 1042 LLC/SNAP description, identify the encapsulation method,
   locate the protocol identifier in each, and state RFC 1122 §2.3.3 default sending choice for a dual-format 10Mbps host with no confusion between LLC length and EtherType.
2. **Candidate `LO.NET.ETHERNET.LENGTHS.01`:** Given stated byte-count boundaries,
   calculate a complete untagged Ethernet II MAC frame size from destination address
   through FCS for an IP datagram no larger than the stated 1500-byte limit, and explain
   whether padding is part of the IP datagram. This outcome is limited to the historical RFC 894 and Cisco-described model; current IEEE clause verification remains open.
3. **Candidate `LO.NET.ETHERNET.BRIDGE.01`:** Given a small bridge table and an ingress
   frame's source/destination addresses, determine the learned source entry and the
   resulting forward/filter/flood action for known unicast, same-port destination, and
   unknown destination cases. Limited to the cited Cisco model; current IEEE 802.1Q clause verification remains open.

## Check scenarios with key and rationale

### Scenario 1 — Ethernet II and LLC/SNAP

**Prompt:** An IPv4 payload is sent using RFC 894. What value appears in the Ethernet
Type field, and where does the IP header begin? In an RFC 1042 IEEE 802 encapsulation,
which sublayer/header sequence carries the protocol identifier? For a dual-sending host on RFC 1122’s 10Mbps Ethernet, which format is the sending default?

**Answer:** RFC 894 specifies Type `0x0800`; the IP header begins in the Ethernet data
field. RFC 1042 uses 802.2 LLC followed by SNAP; SNAP's organization code and next
16-bit field identify the EtherType. RFC 894 is the sending default under RFC 1122 §2.3.3 for the stated host context.

**Rationale:** RFC 894 “Frame Format”; RFC 1042 “Introduction” and “Header Format”; RFC 1122 §2.3.3 requires an Internet host on 10Mbps Ethernet to send/receive RFC 894 and, if it sends both, to default its sending selector to RFC 894.
The answer distinguishes two encapsulations and does not infer the general Ethernet
MAC frame layout from the IP encapsulation RFC.

### Scenario 2 — RFC 894 untagged Ethernet II example

**Prompt:** A 40-octet IPv4 datagram is sent in the ordinary untagged RFC 894 Ethernet II model. Count from destination address through FCS, and distinguish padding from IP length.

**Answer:** 6 octets of padding; 6 destination + 6 source + 2 Type + 40 IP + 6 padding + 4 FCS = **64 octets**. Preamble/SFD precede the counted frame; IFG is a separate interval. A 1500-octet IP datagram yields 1518 octets in this model. The IP total length excludes padding.

**Rationale:** RFC894 “Frame Format” specifies minimum 46-octet data and maximum 1500-octet IP datagram; CISCO_FRAME “Frame Formats” gives addresses, Type, FCS and placement of preamble/SFD. This is a historical vendor-described Ethernet II model, not a claim that current IEEE text or all tagged/jumbo variants were examined. IFG terminology remains a current IEEE verification gap.

### Scenario 2a — MTU versus LLC/SNAP payload

**Prompt:** Under RFC 1042's IEEE 802.3 example, why is the derived maximum IP datagram
1492 octets rather than 1500?

**Answer:** That RFC's 10BASE5 maximum is 1518 octets from destination address through
FCS. Subtracting its 18 octets of MAC header/trailer and 8 octets of LLC/SNAP gives
1492 octets available for the IP datagram. RFC 1042 explicitly distinguishes this
from the 1500 Ethernet MTU value.

**Rationale:** RFC 1042 “Frame Format and MAC Level Issues” / “For IEEE 802.3”. This is
the historical LLC/SNAP example, not a general present-day Ethernet II frame formula.

### Scenario 3 — Cisco simple switch model

**Prompt:** Ports 1–3 are forwarding in one VLAN, without special filters. CAM has B→2 and C→1. A frame with source A arrives on port 1. Determine source learning and egress for destination B, C, unknown D, and broadcast, as independent cases.

**Answer:** Learn A→1. B: forward to port 2. C: filter (same ingress port). D: flood to ports 2 and 3. Broadcast: flood to ports 2 and 3. These rules assume ordinary learning enabled and all three ports forwarding.

**Rationale:** CISCO_LEARN “Key takeaway” documents ingress source learning; CISCO_SWITCH “Transparent Bridging Algorithm” documents destination lookup, same-port filtering and flooding within VLAN excluding ingress. This is a vendor-scoped example; normative IEEE 802.1Q clause verification remains open.

## Proposed editorial boundaries

- State explicitly that RFC 894 describes IP directly in the Ethernet data field with
  Type `0x0800`; its rules do not describe switch learning.
- State explicitly that RFC 1042 is LLC/SNAP over IEEE 802 and its 1492 calculation
  applies to its 10BASE5/802.3 example; do not teach 1492 as the Ethernet II IP MTU.
- Define every future frame-size number with endpoints named (for example,
  destination-address octet through FCS); treat preamble/SFD and interframe gap
  separately only after confirming the current standard's frame terminology.
- Bridge scenarios above are limited to the cited Cisco model. Do not claim current IEEE clause verification; full-duplex CSMA/CD behavior remains unverified.
- Keep VLAN tagging to one boundary note: it can add a tag to the MAC frame and affect
  frame-length accounting; exact tag field size and revised maximum are not verified in
  this package.
