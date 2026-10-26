# Static route proposals (draft)

Candidate units: `NET.IPV4.ROUTE.STATIC` owns manual prefix/next-hop configuration as a concept; `NET.IPV4.ROUTE.LOOKUP` owns common prefix matching, shared with direct/default. Prerequisites: `NET.IPV4.CIDR`, the connected-route unit, then lookup; ARP is needed only for the Ethernet egress example. No dependency from MAC back to ARP.

## Outcomes and keyed scenarios

1. `LO.NET.IPV4.ROUTE.STATIC.01` (candidate): Given two installed routes with different prefix lengths, select the route for an address and explain why its origin does not beat specificity. **Scenario:** connected `192.0.2.0/24` and static `192.0.0.0/16 via 192.0.2.1`, destination `192.0.2.77`. **Answer:** connected `/24`; both match and `/24` is longer. **Evidence:** RFC1812 §5.2.4.2 Basic/Longest Match. This presumes both candidates are eligible, and makes no cross-platform administrative-distance claim.

2. `LO.NET.IPV4.ROUTE.STATIC.02` (candidate): Trace an explicit next hop and required reverse route for two subnets. **Scenario:** A=`192.0.2.10/24`, R=`192.0.2.1/24` and `198.51.100.1/24`, B=`198.51.100.20/24`; A's static `198.51.100.0/24 via 192.0.2.1`, B has no route to `192.0.2.0/24`. Can a reply return? **Answer:** A sends toward R and R can forward to B if forwarding is enabled; B lacks the return route, so successful two-way exchange is not established. Add B's route toward R (`192.0.2.0/24 via 198.51.100.1`) and enable router forwarding, assuming no filtering or other impediment. **Evidence:** RFC1122 §3.3.1; RFC1812 §§5.2.1.2, 5.2.4.2–3. The addresses are documentation examples, not a tested host configuration.

3. `LO.NET.IPV4.ROUTE.STATIC.03` (candidate, blocked): Given a named OS release, decide whether a next hop outside a directly connected prefix is accepted and whether recursion resolves it. **Scenario:** `203.0.113.0/24 via 198.51.100.1`, with only `192.0.2.0/24` connected. **Answer:** unresolved across platforms; there is no defensible universal installation result. **Evidence needed:** official routing configuration and lookup documentation for an agreed platform/version, then an observed route-table example. Do not score this scenario yet.

Common errors to address: treating the configured next-hop as the IP packet destination, treating administrative preference as prefix specificity, and assuming a one-way route implies two-way reachability. An author order should first settle the platform-specific blocked outcome or omit it.
