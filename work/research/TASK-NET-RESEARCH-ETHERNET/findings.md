# Findings: Ethernet (draft)

Access date for web sources: 2026-10-26. Claims below distinguish directly checked
RFC text/official metadata from gaps caused by unavailable normative IEEE text.

## Findings summary

The RFC sources establish two different encapsulation conventions relevant to IP:
RFC 894 puts IPv4 directly in the Ethernet data field and requires Type `0x0800`,
while RFC 1042 uses 802.2 LLC/SNAP over IEEE 802 and places an EtherType in SNAP's
protocol identifier. They are useful protocol-specific descriptions, not complete
current Ethernet or bridge specifications. The IEEE SA catalog identifies active
802.3-2022 and 802.1Q-2022 editions, but the actual standard clauses could not be
retrieved. Accordingly, current frame-layout details and bridge forwarding rules are
not marked supported here.

## Claim ledger

| Claim | Formulation | Evidence and concise support | Applicability / limits | State |
|---|---|---|---|---|
| ETH-01 | In RFC 894's Ethernet encapsulation, the frame Type is `0x0800`; its data field contains the IPv4 header followed by IP data. | `RFC894`, “Frame Format”: specifies type `0800` and data field content. | RFC 894 is an Internet Standard from 1984 and explicitly scoped to 10 Mb/s Ethernet with 48-bit addresses (Introduction). It documents IP encapsulation, not the general Ethernet MAC frame. | supported |
| ETH-02 | RFC 1042's IEEE 802 IP method places IP within 802.2 LLC and SNAP; SNAP's organization code plus following 16-bit value conveys the EtherType. | `RFC1042`, “Introduction” and “Header Format”: LLC/SNAP encapsulation and SNAP protocol identifier. | RFC 1042 addresses IP/ARP over historical 802.3, 802.4, and 802.5. Do not treat this as an IEEE 802.3 frame specification for all present-day Ethernet. | supported |
| ETH-03 | RFC 894 alone does not specify switch source learning, filtering, or flooding. | `RFC894`, “Status of this Memo”, “Frame Format”, and remaining scope: the memo describes IP datagram encapsulation and address mapping; no bridge relay algorithm is specified. | Scope statement about this RFC, not a claim that bridge learning is outside Ethernet standards. IEEE 802.1Q is the relevant requested primary source, but clauses were not retrievable. | supported |
| ETH-04 | RFC 1042 describes source/destination address and length fields for its IEEE 802.3 discussion and gives 64-octet minimum and 1518-octet maximum for 10BASE5; with LLC/SNAP it derives 1492-octet IP datagrams. | `RFC1042`, “Frame Format and MAC Level Issues” / “For IEEE 802.3”. | Historical 10BASE5 values and RFC's LLC/SNAP encapsulation. The RFC explicitly distinguishes 1492 from 1500 Ethernet MTU; these values cannot be generalized to the current 802.3 MAC frame. | supported, scoped |
| ETH-05 | RFC 894 says the Ethernet data field is at least 46 octets (pad with zero octets when needed), excludes padding from IP total length, and gives a 1500-octet maximum IP datagram. | `RFC894`, “Frame Format”. | The next sentence in the RFC appears to contain an editorial slip: it again says “minimum length” immediately before deriving a “maximum length” IP datagram. Preserve that ambiguity in teaching notes. RFC 894 does not define complete modern on-wire frame-size boundaries. | supported, scoped |
| ETH-06 | EtherType provides protocol identification/context for interpreting the Ethernet/802.3 data field; IEEE RA points to IEEE 802.3 clauses 3, 3.1.1, and 3.2.6. | `IEEE_RA_ETHERTYPE`, “EtherType description”; `IEEE8023_2022`, official catalog scope/edition only. | IEEE RA web description. Exact Length/Type encoding thresholds and boundary values require IEEE 802.3 text and remain unchecked. | supported, scoped |
| ETH-07 | The exact current MAC frame fields, frame-size counting boundaries (including whether preamble/SFD/IFG are excluded), basic minimum/maximum values, and a precise 1500-byte IP MTU relationship should be taught from IEEE 802.3-2022 clauses/figures. | `IEEE8023_2022`, official page identifies the active 2022 edition and offers a GET download; `IEEE8023_INTERP_4_07_02` is historical interpretation only. | Current standard text was unavailable through the IEEE GET web endpoint and network proxy. RFCs are not substitutes for the requested clause-level proof. | unresolved |
| ETH-08 | IEEE 802.1Q is the primary source for a bridge's source-MAC learning and forwarding/filtering/flooding behavior. | `IEEE8021Q_2022`, official description says it specifies MAC service over bridged networks and MAC/VLAN bridge operation, management, protocols, and algorithms. | Current standard text could not be retrieved, so no specific rule, exact clause, or scenario behavior is verified. VLAN details intentionally outside scope beyond the boundary note. | unresolved |
| ETH-09 | The contrast between historical shared half-duplex CSMA/CD and present-day full-duplex Ethernet should be stated with careful mode and media applicability. | `IEEE8023_2022`, official abstract says the CSMA/CD MAC protocol specifies shared-medium half-duplex and full-duplex operation. | The abstract is not normative clause text and does not establish the operational rule that collision detection is inapplicable in full-duplex mode. The current standard's clauses were unavailable; historical/current contrast remains partly unresolved. | unresolved |

| ETH-10 | RFC 1122 requires a 10Mbps Ethernet Internet host to send/receive RFC 894, recommends reception of RFC 1042, permits RFC 1042 sending; a dual-sending host must offer a selector defaulting to RFC 894. | `RFC1122` §2.3.3, explicit MUST/SHOULD/MAY and selector paragraph. | Historical host requirements on 10Mbps cable; not a current full IEEE 802.3 specification. | supported, scoped |

## Open evidence gaps

1. IEEE 802.3-2022 normative clauses and tables were not retrieved. The IEEE SA page
   lists a free GET download, but the GET URL returned HTTP 418 in web access and the
   direct file request was rejected by the network proxy. Exact frame format and size
   claims need reviewer access to the standard.
2. IEEE 802.1Q-2022 normative bridge relay and filtering database clauses were not
   retrieved. No forwarding, filtering, or flooding example below is asserted as a
   verified standard rule.
3. The current full-duplex / CSMA/CD operating relationship needs clause-level proof.
   The official abstract supports only that the standard covers both shared half-duplex
   and full-duplex modes.
4. IEEE catalog pages show amendments/corrigenda in the 802.3 and 802.1Q families.
   This research did not analyze which amendments affect the narrow fundamentals here.

## Vendor-scoped follow-up (draft)

`CISCO_FRAME`, “Frame Formats”, describes six-octet addresses, two-octet Type, four-octet FCS, a 64-octet minimum, and preamble/SFD before the destination. Together with RFC894 “Frame Format”, this supports the explicitly bounded untagged 64-octet example in proposals; the cited text is historical vendor documentation, not an inspected current IEEE standard. `CISCO_SWITCH`, “Transparent Bridging Algorithm”, and `CISCO_LEARN`, “Key takeaway”, support the vendor-scoped four-case table scenario. IEEE 802.3 and 802.1Q clauses/amendments remain unavailable; exact current normative boundaries and IFG require review. Earlier ETH-07/08 remain unresolved as claims about current IEEE normative text.
