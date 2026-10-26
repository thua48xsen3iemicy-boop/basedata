# Static route findings (draft)

A static route is a manually supplied route candidate to a destination prefix. The cited RFCs define IPv4 host and router forwarding behavior, not a universal configuration syntax, interface-only route behavior, recursive next-hop resolution, or administrative distance. Those implementation questions remain open until a named platform and version are selected.

| Claim | Formulation | Evidence | Scope / limit | State |
|---|---|---|---|---|
| STA-01 | A router first retains routes matching destination bits, then retains those with the longest matching prefix. | RFC1812 §5.2.4.3, Basic Match and Longest Match, including 10.144.2.5 example. | IPv4 router FIB selection; route must actually be installed and usable. | supported |
| STA-02 | A less specific static prefix does not override a more specific connected prefix merely because it was configured manually. | RFC1812 §5.2.4.3 applies longest match before metric/vendor policy; source of candidate is absent from Basic/Longest Match. | Inference for two installed candidate routes; policy and route eligibility must be held constant. | supported, scoped |
| STA-03 | A gateway next hop must ultimately be reachable on an outgoing link before Ethernet resolution can transmit a frame. | RFC1812 §5.2.4.3; RFC826 “Packet Generation”. | Conceptual Ethernet example; recursion/validation at installation is platform-specific. | supported, scoped |
| STA-04 | A forward path alone is insufficient for a reply; the receiving side needs an outbound route toward the original source and IPv4 forwarding on the transit router. | RFC1812 §5.2.1.2 and §5.2.4; RFC1122 §3.3.1. | Example assumes no filtering, NAT, source-route, policy routing, or address conflicts. | supported, scoped |
| STA-05 | Syntax for prefix + next hop vs interface, recursive resolution, metric and administrative preference is identical across systems. | No versioned platform document selected. | A generalization would be unsound. | unresolved |

## Blocked evidence

Select a concrete OS/router release and read its official route configuration/reference documentation before teaching commands, interface-only routes, recursion, or route preference. The RFCs do not establish these implementation rules.

## Linux/iproute2 follow-up (draft)

`IPROUTE2_MAN`, SYNOPSIS and DESCRIPTION (`dev`, `via`, `onlink`, `metric`, `default`): `ip route add 198.51.100.0/24 via 192.0.2.1 dev eth0` sets a gateway; `ip route add 198.51.100.0/24 dev eth0` sets an interface route; `ip route add default via 192.0.2.1 dev eth0` installs a default. On Ethernet an interface route treats destinations as directly reachable, so neighbor resolution and link topology matter. `onlink` tells Linux to treat a gateway as directly attached even without a matching interface prefix; it is not recursive lookup and does not establish actual reachability. The manual describes lower metric as preferred; in this simple main-table example, longest prefix is considered before same-prefix metric comparison (RFC1812 §5.2.4.3). Policies, route types and equal-cost ties are excluded.

Experiment in isolated `unshare -Urn`, kernel `6.18.55`, iproute2 `6.15.0`: dummy and veth creation failed; loopback was brought up and assigned `192.0.2.10/24`. A route `198.51.100.0/24 via 192.0.2.1 dev lo` and default via `192.0.2.2` were accepted. Adding `203.0.113.0/24 via 198.51.100.1 dev lo` failed with `Nexthop has invalid gateway`, although a route to that gateway via `192.0.2.1` existed. The same command with `onlink` was accepted and shown in the route table. This demonstrates this specific recursive gateway chain is rejected in this runtime; it does not prove that every Linux configuration rejects all forms of recursion. Loopback does not establish actual Ethernet neighbor delivery. No host network was modified.

**Remaining evidence gap:** the manual does not specify full recursive gateway resolution semantics. A version-pinned kernel source review and Ethernet namespace test are needed to generalize beyond the observed rejected chain; do not teach `onlink` as recursion. The accessible manual is not tagged as 6.15.0.
