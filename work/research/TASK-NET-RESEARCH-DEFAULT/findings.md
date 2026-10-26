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

## Linux/iproute2 follow-up (draft)

`IPROUTE2_MAN`, SYNOPSIS and DESCRIPTION (`dev`, `via`, `onlink`, `metric`, `default`): `ip route add 198.51.100.0/24 via 192.0.2.1 dev eth0` sets a gateway; `ip route add 198.51.100.0/24 dev eth0` sets an interface route; `ip route add default via 192.0.2.1 dev eth0` installs a default. On Ethernet an interface route treats destinations as directly reachable, so neighbor resolution and link topology matter. `onlink` tells Linux to treat a gateway as directly attached even without a matching interface prefix; it is not recursive lookup and does not establish actual reachability. The manual describes lower metric as preferred; in this simple main-table example, longest prefix is considered before same-prefix metric comparison (RFC1812 §5.2.4.3). Policies, route types and equal-cost ties are excluded.

Experiment in isolated `unshare -Urn`, kernel `6.18.55`, iproute2 `6.15.0`: dummy and veth creation failed; loopback was brought up and assigned `192.0.2.10/24`. A route `198.51.100.0/24 via 192.0.2.1 dev lo` and default via `192.0.2.2` were accepted. Adding `203.0.113.0/24 via 198.51.100.1 dev lo` failed with `Nexthop has invalid gateway`, although a route to that gateway via `192.0.2.1` existed. The same command with `onlink` was accepted and shown in the route table. This demonstrates this specific recursive gateway chain is rejected in this runtime; it does not prove that every Linux configuration rejects all forms of recursion. Loopback does not establish actual Ethernet neighbor delivery. No host network was modified.

**Remaining evidence gap:** the manual does not specify full recursive gateway resolution semantics. A version-pinned kernel source review and Ethernet namespace test are needed to generalize beyond the observed rejected chain; do not teach `onlink` as recursion. The accessible manual is not tagged as 6.15.0.
