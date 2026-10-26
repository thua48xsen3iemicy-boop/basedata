# Default route proposals (draft)

Candidate unit `NET.IPV4.ROUTE.DEFAULT` owns meaning of `0.0.0.0/0`; common lookup belongs to `NET.IPV4.ROUTE.LOOKUP` proposed under STATIC. Prerequisites: `NET.IPV4.CIDR`, connected-route concept, lookup, then default. Next-hop ARP belongs to ARP; do not duplicate its packet format here.

## Outcomes and keyed scenarios

1. `LO.NET.IPV4.ROUTE.DEFAULT.01` (candidate): Identify default prefix, selected gateway, and static configuration as separate roles. **Scenario:** a route line says `0.0.0.0/0 via 192.0.2.1`. Which value is the destination prefix, which is the next hop, and is `0.0.0.0` this host's IP? **Answer:** `0.0.0.0/0` is the all-destination prefix; `192.0.2.1` is the gateway/next-hop IP; `0.0.0.0` in this line is not a local interface IP. The line is stipulated as statically installed, not evidence of a dynamic protocol. **Evidence:** RFC4632 §3.1 table; RFC1812 §§5.2.4.2–3.

2. `LO.NET.IPV4.ROUTE.DEFAULT.02` (candidate): Select connected, specific static, or default and identify Ethernet ARP target. **Scenario:** host/router has connected `192.0.2.0/24`, static `198.51.100.0/24 via 192.0.2.2`, static default `0.0.0.0/0 via 192.0.2.1`, all eligible. Destinations `192.0.2.40`, `198.51.100.40`, `203.0.113.40`. **Answer:** `/24` connected and ARP for `192.0.2.40`; `/24` static and ARP for `192.0.2.2`; `/0` and ARP for `192.0.2.1`, respectively. **Rationale:** longest match in RFC1812 §5.2.4.3; immediate Ethernet target in RFC826 “Packet Generation”. The gateway addresses are within the connected prefix; IP destination in the packet stays unchanged. No proxy ARP, filtering, or failed neighbor resolution assumed.

3. `LO.NET.IPV4.ROUTE.DEFAULT.03` (candidate): Explain an absent match and missing reverse path. **Scenario:** remove default and static `/24`; send to `203.0.113.40`. Then restore default but give the remote side no route to source `192.0.2.10`. **Answer:** first lookup has no match, so it cannot select a next hop. With default restored, an outbound next hop is selected, but a reply cannot be inferred; a reverse route is required. **Evidence:** RFC1812 §5.2.4.3 empty-set rule; RFC1122 §3.3.1 host outbound routing. No guarantee of end-to-end delivery follows from a local default.

Common errors: treating `/0` as a usable host IP, ARPing for every remote IP, assuming default always wins, and assuming a route implies reverse connectivity. A separate author order should choose a named OS release before adding syntax or route preference values.

## Linux static installation

For iproute2, `ip route add default via 192.0.2.1 dev eth0` specifies a default via a gateway; `IPROUTE2_MAN` DESCRIPTION (`default`, `via`, `dev`). For a route through a link without a gateway, use a `dev` route. The gateway must be usable in the selected setup; `onlink` asserts direct adjacency and is not evidence of reachability or recursive resolution. See STATIC findings for the isolated loopback experiment and its limitations.
