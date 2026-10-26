# ARP research findings

Primary sources retrieved from RFC Editor pages/text on 2026-10-26. The supported
statements below describe IPv4 address resolution over Ethernet and RFC 5227 address
conflict detection within the stated applicability. RFC 826 describes the ARP packet
format and generic resolution exchange; RFC 1122 supplies the Internet host routing and
cache requirements. RFC 5227 explicitly updates RFC 826 for conflict detection without
changing its packet format or the meaning of its fields (§1.2).

## Claim register

| Claim ID | Claim | Source and exact section | Evidence summary | Applicability / exceptions | State |
|---|---|---|---|---|---|
| ARP-C1 | For an outgoing IP datagram, the IP layer selects a next hop; a connected destination is sent directly, while a remote destination is sent to a gateway. Address resolution is for the routing-selected immediate target on the outgoing Ethernet. | RFC1122 §3.3.1, §3.3.1.1; RFC826 “Packet Generation” | RFC 1122 distinguishes connected destination from gateway-routed destination. RFC 826 says routing determines the next-hop protocol address and resolution converts the immediate target's protocol address to its Ethernet address. | The destination's MAC is used only when that destination itself is the next hop. Proxy ARP may cause an intermediary to answer for an IP address; RFC 1122 §2.3.2.1 notes the exception's impact on cache validity but detailed proxy rules are outside scope. | supported |
| ARP-C2 | RFC 826 defines an ARP packet with hardware/protocol type, address lengths, opcode, sender hardware/protocol addresses, and target hardware/protocol addresses; request is opcode 1 and reply is opcode 2. For Ethernet, hardware type is 1 and hardware address length is 6 bytes. | RFC826 “Definitions”; “Packet format”; “Packet Generation” | The packet format names fields `ar$hrd`, `ar$pro`, `ar$hln`, `ar$pln`, `ar$op`, `ar$sha`, `ar$spa`, `ar$tha`, and `ar$tpa`; request/reply opcodes and Ethernet values are specified in the preceding definitions and generation text. | RFC 826 generalizes hardware/protocol address lengths beyond original 10 Mbit Ethernet. Here scope is IPv4 over Ethernet; do not imply every ARP hardware type uses these Ethernet values. | supported |
| ARP-C3 | With no usable table mapping, an ARP Request is broadcast on the hardware selected by routing; a receiver for the target protocol address learns the sender mapping and replies to the requester. | RFC826 “Packet Generation”; “Packet Reception” | RFC 826 describes table lookup, request generation and broadcast, then processing the sender mapping before opcode handling; a target that receives a request swaps sender/target fields and sends a reply. | RFC 826 uses a generic algorithm; RFC 5227 specifies additional IPv4 conflict-detection cases, which should not be conflated with ordinary resolution. | supported |
| ARP-C4 | Implementations must be able to flush outdated ARP cache entries; if using a timeout, it should be configurable. They must also prevent repeated ARP Requests for the same IP at a high rate. | RFC1122 §2.3.2.1 | RFC 1122 states MUST for an invalidation mechanism, SHOULD for configurable timeout if used, and MUST for a mechanism preventing ARP flooding; its recommended maximum is one request per second per destination. | Requirement applies to Internet host implementations as specified in RFC 1122; this is not an OS-specific cache lifetime. | supported |
| ARP-C5 | RFC 5227 address probing, announcement and ongoing conflict detection are distinct from ordinary address resolution. An ARP Probe is a broadcast Request with sender IP zero and target IP equal to the candidate; an Announcement is a Request with sender and target IP both set to the chosen address. | RFC5227 §1.1, §2.1, §2.1.1, §2.3 | §2.1 requires probing before use for implementations of this specification and says not to probe periodically. §2.1.1 specifies fields; §2.3 specifies the Announcement and its cache-refresh purpose. | RFC 5227 §1.3 applies to IEEE 802 LANs and other ARP links at least 1 Mb/s with round-trip latency at most one second; slower/higher-latency links may have late detections and may need different timing guidance. | supported |
| ARP-C6 | ARP does not authenticate claims: a malicious host can send fraudulent ARP packets and interfere with other hosts, including by answering requests with its own hardware address. | RFC5227 §5 Security Considerations; RFC826 “Packet Reception” | RFC 5227 explicitly says ACD inherits ARP's security vulnerabilities and describes fraudulent replies; RFC 826's receive algorithm updates an existing sender mapping from packet contents before checking opcode, without specifying authentication. | This is a limitation of protocol trust on a shared link, not a complete security analysis or mitigation guide. | supported |

## Normative force and qualifications

RFC 1122's cache requirements above retain MUST/SHOULD strength and context. RFC 5227
§2.1 says an implementation of that specification MUST probe before use and MUST NOT
probe periodically; §2.3 says it MUST announce after probing. These requirements are
scoped to implementations of RFC 5227's address-conflict-detection specification and its
§1.3 link applicability. Do not generalize them to every historical host implementation.

## Source relationship and remaining boundary

RFC Editor metadata identifies RFC 826 and RFC 1122 as Internet Standards, and RFC 5227
as a Proposed Standard / Standards Track document. RFC 826 is updated by RFC 5227 and RFC
5494; RFC 5227 says it updates RFC 826. RFC 1122's metadata lists RFCs 1349, 4379, 5884,
6093, 6298, 6633, 6864, 8029, and 9293 as updates; none of those are treated here as
changing the cited ARP sections. RFC Editor metadata pages list no Obsoletes or
Obsoleted-by relation for these three records. Check current RFC Editor metadata again at
review time.

Proxy ARP is mentioned only as a routing/address-resolution caveat: RFC 1122 §2.3.2.1
notes it increases the likelihood that ARP cache entries become invalid. Its detailed
operation is intentionally not asserted here. Do not teach that ordinary ARP itself
authenticates mappings or guarantees that an answer belongs to the intended endpoint.
