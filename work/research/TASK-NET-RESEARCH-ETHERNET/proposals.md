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
   locate the protocol identifier in each, and state one scope limit for each with no
   confusion between LLC length and EtherType.
2. **Candidate `LO.NET.ETHERNET.LENGTHS.01`:** Given stated byte-count boundaries,
   calculate a complete untagged Ethernet II MAC frame size from destination address
   through FCS for an IP datagram no larger than the stated 1500-byte limit, and explain
   whether padding is part of the IP datagram. This outcome is not ready to publish
   until current IEEE 802.3 frame boundaries are verified.
3. **Candidate `LO.NET.ETHERNET.BRIDGE.01`:** Given a small bridge table and an ingress
   frame's source/destination addresses, determine the learned source entry and the
   resulting forward/filter/flood action for known unicast, same-port destination, and
   unknown destination cases. Blocked until applicable IEEE 802.1Q clauses are checked.

## Check scenarios with key and rationale

### Scenario 1 — Ethernet II and LLC/SNAP

**Prompt:** An IPv4 payload is sent using RFC 894. What value appears in the Ethernet
Type field, and where does the IP header begin? In an RFC 1042 IEEE 802 encapsulation,
which sublayer/header sequence carries the protocol identifier?

**Answer:** RFC 894 specifies Type `0x0800`; the IP header begins in the Ethernet data
field. RFC 1042 uses 802.2 LLC followed by SNAP; SNAP's organization code and next
16-bit field identify the EtherType.

**Rationale:** RFC 894 “Frame Format”; RFC 1042 “Introduction” and “Header Format”.
The answer distinguishes two encapsulations and does not infer the general Ethernet
MAC frame layout from the IP encapsulation RFC.

### Scenario 2 — MTU versus LLC/SNAP payload

**Prompt:** Under RFC 1042's IEEE 802.3 example, why is the derived maximum IP datagram
1492 octets rather than 1500?

**Answer:** That RFC's 10BASE5 maximum is 1518 octets from destination address through
FCS. Subtracting its 18 octets of MAC header/trailer and 8 octets of LLC/SNAP gives
1492 octets available for the IP datagram. RFC 1042 explicitly distinguishes this
from the 1500 Ethernet MTU value.

**Rationale:** RFC 1042 “Frame Format and MAC Level Issues” / “For IEEE 802.3”. This is
the historical LLC/SNAP example, not a general present-day Ethernet II frame formula.

### Scenario 3 — Bridge decision

**Prompt:** A bridge receives a frame whose destination is absent from its forwarding
database. What ports must receive it?

**Answer:** **Unresolved in this evidence package.** Consult the applicable 802.1Q
bridged-network forwarding/filtering clauses before assigning ports; neither RFC 894
nor RFC 1042 specifies this bridge decision.

**Rationale:** The checked RFC scopes are IP encapsulation, and only IEEE 802.1Q is
identified by IEEE as the bridge standard. The normative clause text was unavailable.
This scenario deliberately cannot serve as an assessment key until reviewed.

## Proposed editorial boundaries

- State explicitly that RFC 894 describes IP directly in the Ethernet data field with
  Type `0x0800`; its rules do not describe switch learning.
- State explicitly that RFC 1042 is LLC/SNAP over IEEE 802 and its 1492 calculation
  applies to its 10BASE5/802.3 example; do not teach 1492 as the Ethernet II IP MTU.
- Define every future frame-size number with endpoints named (for example,
  destination-address octet through FCS); treat preamble/SFD and interframe gap
  separately only after confirming the current standard's frame terminology.
- Do not present bridge source-learning or flooding rules or assert CSMA/CD is disabled
  in full duplex until exact current IEEE clauses have been checked.
- Keep VLAN tagging to one boundary note: it can add a tag to the MAC frame and affect
  frame-length accounting; exact tag field size and revised maximum are not verified in
  this package.
