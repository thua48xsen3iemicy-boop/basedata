# TASK-NET-SECOND-PASS — researcher report (draft)

Base `58ed09a`; branch `research/network-foundations-second-pass`; next role `machine_reviewer`. No canonical knowledge, original handoff, order, schema, validator, or dynamic-routing material changed. Changed paths are the eight scoped research directories and this report; the new handoff is listed separately below.

## Review findings, independently checked

| REVIEW item | Decision and evidence | Resolution path |
|---|---|---|
| 1 MAC YAML | confirmed/fixed. `yaml.safe_load` raised `ScannerError` at colon in unquoted IEEE tutorial title; all eight files now parse. | `TASK-NET-RESEARCH-MAC/sources.yaml` |
| 2 ARP root | confirmed/fixed. Parsed root was a mapping with `sources`; now it is a list of three sources, with metadata retained. | `TASK-NET-RESEARCH-ARP/sources.yaml` |
| 3 RFC directions | confirmed/fixed in ARP, DIRECT and further themes. `updates` now means documents changed by the record; `updated_by` denotes changers. RFC 5227 updates RFC 826; RFC 2644 updates RFC 1812. A previous RFC 793 item under BROADCAST/RFC1122 was erroneous and removed. RFC 8190 is an IANA registry reference, not an RFC-style update to the registry, so that relation is unknown. | all eight `sources.yaml` |
| 4 Ethernet alignment | confirmed/partly blocked. Encapsulation outcome now tests RFC 1122 default choice. The frame-size outcome gets a 40-octet example with the supported six-octet pad deduction; a complete destination-through-FCS numerical key remains blocked pending IEEE text. Bridge outcome remains explicitly unscorable. RFC 1042's 1492-octet example remains a scoped explanatory check. | Ethernet `findings.md`, `proposals.md` |
| 5 RFC1122 §2.3.3 | confirmed/fixed. Directly inspected section: 10Mbps Ethernet hosts MUST send/receive RFC 894, SHOULD receive RFC 1042, MAY send RFC 1042; a host sending both MUST provide selector defaulting to RFC 894. It is historical host scope, not a current IEEE 802.3 field specification. | Ethernet three files |
| 6 static/default and IEEE | confirmed/partly blocked. Six files for STATIC/DEFAULT added. IEEE 802.3 and 802.1Q normative text remains inaccessible; official IEEE metadata and limited RFC/IEEE RA material cannot establish full frame layout or bridge relay behavior. | STATIC/DEFAULT three files each; Ethernet/BROADCAST limitations |
| 7 MAC broadcast | confirmed/fixed. RFC 894 “Broadcast Address” explicitly gives all-ones Ethernet destination `FF-FF-FF-FF-FF-FF`; earlier proposals contradicted supported MAC-04. Scope remains RFC 894's 10Mbps/48-bit Ethernet IP method. | MAC `proposals.md` |

## Topic status and evidence limits

| Topic | Checked and preserved | Changed / outstanding |
|---|---|---|
| MAC | RFC 894 “Broadcast Address” re-read; 48-bit/bits and RFC 9542 successor evidence retained. | YAML fixed; broadcast evidence aligned; current IEEE clauses still unavailable. |
| Ethernet | RFC 894 Frame Format, RFC 1042 historical LLC/SNAP, RFC 1122 §2.3.3 re-read or compared. | Requirement and keys aligned; current frame-size and bridge rule blocked on IEEE normative text. |
| ARP | RFC 826 and RFC 5227 relationships and first-pass packet/next-hop scenarios retained. | Root list and update direction fixed; no claim of full update-chain audit. |
| Broadcast | RFC 2644 §3 directed-broadcast default distinguished from layer-2 domain. | Metadata corrected; 802.1Q bridge flooding/domain details blocked. |
| IPv4 | Existing /31 exception and address roles preserved; metadata direction corrected. | IANA registry relation no longer misrepresented as RFC update; full current registry audit outstanding. |
| DIRECT | Next hop vs destination and Linux-specific connected/local behavior preserved. | RFC relation direction corrected; exact OS release for Linux pages remains unspecified. |
| STATIC | RFC 1812 §§5.2.4.2–3 and RFC 1122 §3.3.1 establish installed-route selection and two-subnet example. | New files; platform installation, interface-only and recursion blocked. |
| DEFAULT | RFC 4632 §3.1 explicitly labels `0.0.0.0/0`; RFC 1812 §5.2.4.3 ranks it after matching specific prefixes. | New files; platform command/preference behavior blocked. |

## Outcome → scenario → answer → evidence

| Outcome (candidate unless noted) | Scenario and answer | Evidence / status |
|---|---|---|
| MAC FORMAT.01 | AC first octet; AC least-significant bit transmitted first. | IEEE-MAC-TUTORIAL Fig. 1; RFC9542 §1.1; scoped. |
| MAC BITS.01 | `03` gives M=1, X=1. | RFC9542 §2.1.1; scoped. |
| MAC UNIQUENESS.01 | `02:…` does not prove OUI owner/device identity. | RFC9542 §§2.1.2, 6. |
| MAC NEXT_HOP.01 | Resolve gateway `192.0.2.1`, not destination `198.51.100.20`. | RFC826 “Packet Generation”. |
| Ethernet ENCAPSULATION.01 | IPv4 type `0x0800`; LLC/SNAP alternative; RFC 894 sending default for specified dual host. | RFC894 Frame Format; RFC1042 Header Format; RFC1122 §2.3.3. |
| Ethernet LENGTHS.01 | 40-octet IP datagram needs 6-octet pad to reach RFC894 data minimum; complete frame total blocked. | RFC894 Frame Format; IEEE 802.3 clause unavailable. |
| Ethernet BRIDGE.01 | Unknown-destination egress ports blocked. | IEEE 802.1Q normative clauses unavailable. |
| ARP .01/.02/.03 | Request queries `192.0.2.20`; remote gateway target is `192.0.2.1`; sender `0.0.0.0` Probe for `192.0.2.30`. | RFC826 Packet format/Generation; RFC1122 §3.3.1; RFC5227 §2.1.1. |
| Broadcast DOMAIN.01 / IPv4 BROADCAST.01/.02 | H1 broadcast through bridge to H2: blocked pending IEEE 802.1Q; limited `255.255.255.255` stays on connected network; default router blocks network-prefix-directed broadcast. | RFC919 §§4,6; RFC1122 §3.3.6; RFC2644 §3; IEEE 802.1Q blocked. |
| IPv4 existing A/B and candidate C/D | 32-bit dotted IPv4 value; `/26` means 26 prefix bits; `192.0.2.70` belongs to `192.0.2.64/26`; both `198.51.100.10/31` endpoint addresses usable on p2p, neither directed broadcast. | RFC791 §3.1; RFC4632 §3.1; RFC3021 §§2–3. |
| DIRECT .01/.02/.03/.04 | On-link destination `192.0.2.77` uses eth0 and self `192.0.2.10` is local; ARP resolves immediate target; Linux `noprefixroute` is platform-scoped. | RFC1122 §3.3.1; RFC1812 §5.2.4; RFC826 Packet Generation; iproute2 manuals. |
| STATIC .01 | Connected `/24` beats static `/16` for `192.0.2.77`. | RFC1812 §5.2.4.3. |
| STATIC .02 | A→R→B needs B's route back to A and router forwarding. | RFC1122 §3.3.1; RFC1812 §§5.2.1.2,5.2.4. |
| STATIC .03 | Off-link gateway recursion/installation result blocked. | Named OS release and official manual needed. |
| DEFAULT .01 | `0.0.0.0/0` prefix, `192.0.2.1` next hop, neither is local host address. | RFC4632 §3.1; RFC1812 §5.2.4. |
| DEFAULT .02 | Connected `/24`, static `/24`, then `/0`; ARP targets final on-link IP or chosen gateway. | RFC1812 §5.2.4.3; RFC826 Packet Generation. |
| DEFAULT .03 | No match means no next hop; default alone does not establish reply route. | RFC1812 §5.2.4.3; RFC1122 §3.3.1. |

Existing first-pass keyed scenarios remain in their proposals. Their historical source-access statements are not silently updated. The matrix summarizes their answers; an independent reviewer must inspect each complete prompt and scope before use.

## Cross-topic resolution and next author orders

- Owner `NET.L2.MAC48.FORMAT/BITS/SCOPE`: MAC. Ethernet consumes MAC addressing without making ARP a prerequisite of MAC. ARP owns IPv4-to-Ethernet mapping; MAC's next-hop example is a boundary explanation, not a second ARP unit.
- Owner `NET.ETHERNET.FRAME/ENCAPSULATION/MTU`: Ethernet. `NET.ETHERNET.BRIDGE-RELAY` and `NET.L2.BROADCAST-DOMAIN` require the same missing 802.1Q clause review; bridge relay should own forwarding logic, broadcast-domain unit should consume it and describe scope, not duplicate the algorithm.
- Owner `NET.IPV4.ROUTE.LOOKUP` and `NET.IPV4.ROUTE.STATIC`: STATIC; owner `NET.IPV4.ROUTE.DEFAULT`: DEFAULT. DIRECT's candidate `LO.NET.ROUTING.DIRECT.*` owns on-link/local distinction, not generic lookup. Author should normalize `NET.ROUTING.*` vs `NET.IPV4.ROUTE.*` spelling before registering IDs. Route lookup selects next hop; ARP resolves that target on Ethernet. These are not reciprocal prerequisites.
- Owner IPv4 subnet address roles and /31 exception: IPv4. Broadcast owns limited/directed broadcast behavior, not subnet address calculation. No candidate registered in knowledge.
- Suggested author orders: (1) MAC + ARP boundary with RFC 9542 review; (2) IPv4 address/CIDR /31; (3) connected/static/default lookup using only source-supported outcomes; (4) Ethernet framing and bridge/broadcast domain after authorized access to current IEEE clauses. Keep platform-specific route-recursion as a separate named-OS order.

## Checks and residual limits

Commands run in this branch: `python tools/validate.py` → `PASS: 3 units, 4 outcomes, 1 questions, 10 work orders; structural references and hours valid`; `git diff --check` → exit 0; Python `yaml.safe_load` over all eight `sources.yaml` → eight root lists, mandatory fields present, unique IDs. Text scan of findings IDs found references to RFC1812 in BROADCAST only as context through RFC2644's update, not as independent evidence. Source URL, section and claim reasoning was selectively checked via RFC Editor web access; this is not a full factual audit. Direct `curl` requests to RFC Editor returned `CONNECT tunnel failed, response 403`; web retrieval worked. Full IEEE 802.3/802.1Q normative texts were not retrieved. Exact amended IEEE clauses, Linux release-specific behavior, and exhaustive RFC update effects remain for reviewer/expert. All output is draft.

## Follow-up: precise RFC references

Basic Match, Longest Match and the empty candidate rule are in RFC 1812 §5.2.4.3, Next Hop Address; these references have been corrected in STATIC, DEFAULT and this report. §5.2.4.2 remains listed for Local/Remote Decision. The earlier checks did not catch this error. Platform-specific documentation and IEEE evidence require further work; the remaining blocked statements above are unchanged.
