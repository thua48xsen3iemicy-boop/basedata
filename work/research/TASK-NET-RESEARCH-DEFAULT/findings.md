# Default route findings (draft)

| Claim | Formulation | Evidence | Applicability / limit | State |
|---|---|---|---|---|
| DEF-01 | `0.0.0.0/0` matches any IPv4 destination and is the least specific prefix. | RFC4632 §3.1 prefix-size table; RFC1812 §5.2.4.3 Basic Match/Longest Match. | FIB route prefix; distinct from a host's `0.0.0.0` address and from next-hop gateway IP. | supported |
| DEF-02 | A matching connected or specific static prefix beats a default prefix in the conceptual router lookup. | RFC1812 §5.2.4.3 prunes by longest prefix after basic match. | Routes already installed/eligible; TOS/policy/metric ties not modeled. | supported, scoped |
| DEF-03 | Default route, default gateway, and static configuration refer to different things: prefix match, selected next-hop address, and route origin. | RFC4632 §3.1 for prefix; RFC1812 §§5.2.4.2–3 for next hop; RFC1122 §3.3.1 for gateway selection. | Synthesis for teaching; no claim of universal command syntax or automatic configuration mechanism. | supported, scoped |
| DEF-04 | On an Ethernet routed path ARP targets the immediate next-hop IP, not automatically the final destination. | RFC826 “Packet Generation”; RFC1122 §3.3.1. | Assumes a selected reachable gateway and ordinary IPv4/Ethernet; proxy ARP and non-Ethernet excluded. | supported, scoped |
| DEF-05 | If no route matches, forwarding cannot choose a next hop; a default provides a match but does not guarantee delivery or a return route. | RFC1812 §5.2.4.3 empty-candidate discussion; RFC1122 §3.3.1. | Error handling details differ for host/router and failure point. | supported, scoped |

## Open evidence

A named platform/version is needed to document a static default-route command, installation constraints, route preference for same-prefix candidates, and diagnostic output. No universal command or administrative-distance value is proposed. The RFC Editor update chains were recorded; only the narrow cited sections were substantively inspected here.
