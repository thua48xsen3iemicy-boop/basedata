# Ethernet

Заказ: `TASK-NET-RESEARCH-ETHERNET`. Результаты: `work/research/TASK-NET-RESEARCH-ETHERNET/`.

## Вопросы исследования

- Назначение Ethernet, основные поля кадра, EtherType и отличие Ethernet II от IEEE 802 LLC/SNAP
- Размер кадра, полезная нагрузка и IP MTU: явно указать, какие поля входят в размер; VLAN только как оговорка
- Обучение коммутатора по source MAC, forwarding/filtering/flooding: искать IEEE 802.1Q; не приписывать эти правила RFC 894; современный full-duplex и исторический CSMA/CD

## Отправные источники (не проверены в рамках постановки)

- IEEE 802.3 (найти официальную доступную редакцию IEEE; зафиксировать версию и доступность).
- RFC 894: https://www.rfc-editor.org/info/rfc894
- RFC 1042: https://www.rfc-editor.org/info/rfc1042

Для существующих read_ids читать соответствующие unit.yaml и связанные тексты по ID, не всё дерево. По соседним темам описывать только необходимые границы и фиксировать зависимости для рецензента.
