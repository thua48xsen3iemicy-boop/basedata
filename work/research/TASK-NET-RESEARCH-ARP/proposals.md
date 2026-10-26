# ARP proposals

These are draft research proposals for the author and machine reviewer. Candidate IDs
are not registered entities; compare them against adjacent Ethernet, IPv4, and route
outcomes before registration.

## Proposed unit and dependencies

- Candidate unit: `NET.ARP.RESOLUTION` (candidate ID only), covering ARP request/reply,
  mapping fields, and cache behavior on IPv4 over Ethernet.
- Candidate unit: `NET.IPV4.ADDRESS.CONFLICT.DETECTION` (candidate ID only), covering
  RFC 5227 probes, announcements, and conflict detection.
- Prerequisite: existing `NET.IPV4.ADDRESS`; adjacent Ethernet framing and next-hop
  selection outcomes should be linked after their IDs are confirmed.

## Measurable candidate outcomes and scenarios

1. **Candidate LO.NET.ARP.01 — Decode an ARP request.** Given an IPv4-over-Ethernet ARP
   Request trace with field names and values, identify the opcode, sender and target
   protocol/hardware addresses, and which target protocol address is being queried.

   **Scenario:** A capture has `ar$op=1`, sender IP `192.0.2.10`, sender MAC
   `02:00:00:00:00:10`, target IP `192.0.2.20`, and unknown target MAC. Classify it.

   **Answer:** It is an ARP Request asking for the hardware mapping of `192.0.2.20`;
   the sender asserts the pair `192.0.2.10` / `02:00:00:00:00:10`.

   **Rationale:** RFC 826 “Definitions” assigns opcode 1 to REQUEST; “Packet format”
   defines sender/target fields; “Packet Generation” describes request population.

2. **Candidate LO.NET.ARP.02 — Select the address to resolve for a routed datagram.**
   Given source/destination reachability and a selected next hop, identify which protocol
   address's Ethernet mapping is needed and explain when the ARP cache is consulted.

   **Scenario:** A host sends to remote IP `198.51.100.40` through connected gateway
   `192.0.2.1`. Which IPv4 address does it resolve to an Ethernet destination?

   **Answer:** It resolves `192.0.2.1`, the selected immediate next hop, rather than
   `198.51.100.40`.

   **Rationale:** RFC 1122 §3.3.1 and §3.3.1.1 require next-hop selection and sending
   remote traffic to a gateway; RFC 826 “Packet Generation” says resolution converts
   the routing-selected immediate target protocol address into an Ethernet address.
   Proxy ARP can make an intermediary answer for an IP mapping and should be taught only
   as a caveat (RFC 1122 §2.3.2.1).

3. **Candidate LO.NET.ARP.03 — Distinguish conflict-detection packets.** Given an ARP
   Request trace, classify ordinary resolution, Probe, or Announcement from sender and
   target IP fields, and state what conflict question is being tested.

   **Scenario:** An ARP Request is broadcast with sender IP `0.0.0.0` and target IP
   `192.0.2.30`. Is it ordinary resolution or an RFC 5227 Probe?

   **Answer:** It is an ARP Probe for `192.0.2.30`, not an ordinary resolution query
   from an already configured sender.

   **Rationale:** RFC 5227 §2.1.1 defines a Probe as a broadcast Request with all-zero
   sender IP and target IP set to the candidate address. Section 2.3 defines an
   Announcement separately: sender and target IP are both the chosen address.

## Editorial notes

- Keep RFC 826 packet generation/reception separate from RFC 5227's address
  conflict-detection lifecycle.
- Teach cache invalidation as an implementation requirement, without inventing a
  universal cache lifetime; RFC 1122 §2.3.2.1 requires invalidation and says a timeout,
  if used, should be configurable.
- Teach the trust limitation narrowly: RFC 5227 §5 says ARP inherits vulnerabilities
  that let malicious hosts interfere by sending fraudulent packets. Do not present ARP as
  authenticated or turn the unit into a security-hardening guide.
- Proxy ARP is a brief exception only; detailed behavior should be assigned separately
  if needed.
