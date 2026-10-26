# Замечания первого ревью, 2026-10-27

Это проверяемые замечания, а не эталонный ответ. Повторно проверь их, допускается обоснованное несогласие.

## Зафиксированные входы

База постановки: a2976eb. В эту ветку перенесены изменения следующих коммитов
(перенос не означает содержательной приёмки):

| Тема | Исходный head | PR |
|---|---|---|
| Ethernet | 7a01f7a | https://github.com/thua48xsen3iemicy-boop/basedata/pull/2 |
| Broadcast | cc94a0a | https://github.com/thua48xsen3iemicy-boop/basedata/pull/3 |
| Direct | 82dc36e | https://github.com/thua48xsen3iemicy-boop/basedata/pull/4 |
| MAC | 6d1d351 | https://github.com/thua48xsen3iemicy-boop/basedata/pull/5 |
| IPv4 | 7ef70f1 | https://github.com/thua48xsen3iemicy-boop/basedata/pull/6 |
| ARP | 7bddcad (включает bd0905a) | https://github.com/thua48xsen3iemicy-boop/basedata/pull/7 |

На момент первого ревью static/default ветки указывали на a2976eb и не содержали результатов.
Не делай выводов о дальнейшей работе других исполнителей по этому снимку.

## Замечания для повторной проверки

1. **P1 MAC: невалидный YAML.** `work/research/TASK-NET-RESEARCH-MAC/sources.yaml:41`:
   `title: Standard Group MAC Addresses: A Tutorial Guide` требует кавычек вокруг значения.
   yaml.safe_load выдаёт ScannerError. Проверить весь файл после исправления, а не только эту строку.
2. **P2 ARP: форма данных.** В `sources.yaml:1` корневой объект `sources:`, хотя пакет требует список.
   Унифицировать восемь файлов без потери метаданных.
3. **P2 связи RFC:** в ARP sources.yaml:10 и :34 поле updates имеет противоположные направления.
   Аналогичное использование встречается в DIRECT. Проверить все темы.
   Исходная постановка недостаточно точно определяла это поле; не приписывать всю проблему исполнителю.
4. **P2 Ethernet: outcome и проверка не совпадают.** `proposals.md:27–35` обещает вычисление
   Ethernet II frame size и bridge decision; сценарий 2 (:53–64) проверяет LLC/SNAP,
   сценарий 3 (:66–77) не имеет ответа. Нужно соответствие outcome → scenario → answer → evidence.
5. **P2 Ethernet: пропущен RFC1122 §2.3.3.** Добавить к сравнению RFC894/1042 требования
   поддержки и default выбора отправляемой инкапсуляции, сохранив историческую область
   применения раздела (10Mbps Ethernet). Не выдавать её за полную современную IEEE спецификацию.
   Источник: https://www.rfc-editor.org/rfc/rfc1122.html#section-2.3.3
6. **Неполнота:** static/default ещё не представлены; Ethernet/broadcast оставляют основные
   вопросы bridging unresolved из-за недоступного IEEE текста. Закрыть доступные пробелы;
   остаток явно обозначить blocked, не выдумывая проверку источников.
7. **MAC: согласованность evidence.** findings.md помечает MAC-04 supported,
   а proposals.md:58 описывает доказательство broadcast MAC как фрагментарное.
   Сверить с RFC894 “Broadcast Address” и согласовать статус.
   Источник: https://www.rfc-editor.org/rfc/rfc894.html

## Что уже проверялось и чего это не доказывает

На всех шести исходных ветках python tools/validate.py и git diff --check проходили.
Отдельный разбор sources.yaml выявил ошибку MAC; ARP разбирался как dict, остальные — list.
Выборочно сверены RFC894, RFC1122 и RFC5227. Полный аудит всех источников IEEE/RFC не выполнен.
Не превращать эту выборку в отметку о полной фактической верификации.

Полезные результаты, которые стоит сохранить при подтверждении: переход с RFC7042 на RFC9542;
различение next hop/IP destination и connected/local; исключение /31; честная фиксация доступа к IEEE.
