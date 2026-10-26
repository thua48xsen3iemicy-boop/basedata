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
