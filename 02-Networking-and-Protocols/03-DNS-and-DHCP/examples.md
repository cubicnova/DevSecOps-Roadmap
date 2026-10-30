# DNS and DHCP — Examples

Commands and output vary by operating system, resolver, and network configuration. Treat sample names and addresses as examples.

## 1. Query an A record

```bash
dig example.com A
```

Look for the `ANSWER SECTION`, which may contain one or more IPv4 addresses. A response with no answer does not necessarily mean the domain does not exist; the queried record type may simply be absent.

## 2. Query common record types

```bash
dig example.com AAAA
dig example.com MX
dig example.com NS
dig example.com TXT
dig example.com SOA
```

A domain can have multiple records of a type. TXT records may contain SPF policies or verification values, but should not contain secrets.

## 3. Ask a specific resolver

```bash
dig @1.1.1.1 example.com A
```

This asks the named resolver directly. Whether it is reachable or permitted depends on the network. Use approved resolvers in enterprise environments.

## 4. Check DNS delegation and trace resolution

```bash
dig +trace example.com
```

This walks through DNS delegation from the root toward the target zone. It can help distinguish delegation issues from a cached answer, though network policy may block some queries.

## 5. Reverse lookup

```bash
dig -x 192.0.2.10
```

`192.0.2.0/24` is reserved for documentation, so this example may not return a meaningful public PTR record. Substitute an address you are authorized to investigate.

## 6. Compare system name resolution

```bash
getent hosts example.com
dig example.com
cat /etc/resolv.conf
```

`dig` queries DNS directly according to its options. `getent` uses the system's configured name-service path, which may include DNS, local files, or other configured sources. `/etc/resolv.conf` may be generated or managed by NetworkManager, systemd-resolved, or another service.

## 7. Inspect local resolver service

On systems using systemd-resolved:

```bash
resolvectl status
resolvectl query example.com
```

These commands are not available on every Linux distribution. Check the documentation for the resolver installed on your system.

## 8. Check DHCP-related network configuration

```bash
ip address show
ip route show
```

These show the address and route currently installed on the host. They do not, by themselves, prove which DHCP server assigned the configuration.

Depending on the system, useful commands may include:

```bash
nmcli device show
networkctl status
```

Avoid blindly releasing or renewing a lease on a remote host: doing so can disconnect your session.

## 9. Understand DHCP DORA

In a typical DHCPv4 exchange on a local segment:

- Discover: client looks for a server.
- Offer: server proposes an address and options.
- Request: client asks to use that offer.
- Acknowledge: server confirms the lease.

A relay agent may forward client messages across subnets. The exchange may look different with renewals, reservations, DHCPv6, or network-specific options.

## 10. Basic DNS troubleshooting sequence

1. Confirm the network interface has an expected address.
2. Check routing with `ip route`.
3. Compare `getent hosts name` with `dig name`.
4. Query an approved resolver explicitly if permitted.
5. Check record type, TTL, delegation, and authoritative data.
6. Test the application separately, for example with `curl -I https://example.com`.
7. Review resolver/server logs where authorized.

A DNS answer can be correct while the target service is unavailable. Likewise, an application may use a cache or a resolver different from the one you tested.
