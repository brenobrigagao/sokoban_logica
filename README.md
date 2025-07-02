# Solucionador de Sokoban

Programa que soluciona mapas do Sokoban usando a satisfatibilidade da lógica proposicional.
Gera soluções passo a passo mostrando cada turno até atingir o objetivo.

## Como usar

```bash

git clone https://github.com/brenobrigagao/sokoban_logica.git
cd sokoban_logica
python examples.py

```

## Exemplo 1

### Input

```python

map_1 = [
    list("######"),
    list("#   m#"),
    list("#SB  #"),
    list("#    #"),
    list("######")
]

```

### Output

```bash

Tentando resolver com 0 turnos...
Tempo para processar as restrições até turno 0: 0.0234
Tempo para fazer o check() no turno 0: 0.0031

Tentando resolver com 1 turnos...
Tempo para processar as restrições até turno 1: 0.0225
Tempo para fazer o check() no turno 1: 0.0040

Tentando resolver com 2 turnos...
Tempo para processar as restrições até turno 2: 0.0225
Tempo para fazer o check() no turno 2: 0.0090

Tentando resolver com 3 turnos...
Tempo para processar as restrições até turno 3: 0.0294
Tempo para fazer o check() no turno 3: 0.0144

Tentando resolver com 4 turnos...
Tempo para processar as restrições até turno 4: 0.0227
Tempo para fazer o check() no turno 4: 0.0152

Tentando resolver com 5 turnos...
Tempo para processar as restrições até turno 5: 0.0225

✅ Solução encontrada com 5 turnos!

========== Turno 0 ==========
######
#...m#
#SB..#
#....#
######

========== Turno 1 ==========
######
#...m#
#.SB.#
#....#
######

========== Turno 2 ==========
######
#...m#
#..SB#
#....#
######

========== Turno 3 ==========
######
#...m#
#...B#
#..S.#
######

========== Turno 4 ==========
######
#...m#
#...B#
#...S#
######

========== Turno 5 ==========
######
#...b#
#...S#
#....#
######

==============================

```

## Exemplo 2

### Input

```python

map_2 = [
    list("######"),
    list("#x   #"),
    list("#BBBm#"),
    list("#m   #"),
    list("######")
]

```

### Output

```bash

Tentando resolver com 0 turnos...
Tempo para processar as restrições até turno 0: 0.0332
Tempo para fazer o check() no turno 0: 0.0015

Tentando resolver com 1 turnos...
Tempo para processar as restrições até turno 1: 0.0328
Tempo para fazer o check() no turno 1: 0.0062

Tentando resolver com 2 turnos...
Tempo para processar as restrições até turno 2: 0.0326
Tempo para fazer o check() no turno 2: 0.0096

Tentando resolver com 3 turnos...
Tempo para processar as restrições até turno 3: 0.0327

✅ Solução encontrada com 3 turnos!

========== Turno 0 ==========
#####
#SBm#
#B..#
#m..#
#####

========== Turno 1 ==========
#####
#.Bm#
#S..#
#b..#
#####

========== Turno 2 ==========
#####
#SBm#
#...#
#b..#
#####

========== Turno 3 ==========
#####
#.Sb#
#...#
#b..#
#####

==============================

```

## Exemplo 3

### Input 

```python

map_3 = [
    list("#####"),
    list("#SBm#"),
    list("#B  #"),
    list("#m  #"),
    list("#####")
]

```

### Output

```bash

Tentando resolver com 0 turnos...
Tempo para processar as restrições até turno 0: 0.0610
Tempo para fazer o check() no turno 0: 0.0053

Tentando resolver com 1 turnos...
Tempo para processar as restrições até turno 1: 0.0595
Tempo para fazer o check() no turno 1: 0.0133

Tentando resolver com 2 turnos...
Tempo para processar as restrições até turno 2: 0.0603
Tempo para fazer o check() no turno 2: 0.0197

Tentando resolver com 3 turnos...
Tempo para processar as restrições até turno 3: 0.0598
Tempo para fazer o check() no turno 3: 0.0351

Tentando resolver com 4 turnos...
Tempo para processar as restrições até turno 4: 0.0595
Tempo para fazer o check() no turno 4: 0.0520

Tentando resolver com 5 turnos...
Tempo para processar as restrições até turno 5: 0.0720
Tempo para fazer o check() no turno 5: 0.0752

Tentando resolver com 6 turnos...
Tempo para processar as restrições até turno 6: 0.0600
Tempo para fazer o check() no turno 6: 0.0909

Tentando resolver com 7 turnos...
Tempo para processar as restrições até turno 7: 0.0600
Tempo para fazer o check() no turno 7: 0.1043

Tentando resolver com 8 turnos...
Tempo para processar as restrições até turno 8: 0.0601
Tempo para fazer o check() no turno 8: 0.1389

Tentando resolver com 9 turnos...
Tempo para processar as restrições até turno 9: 0.0602
Tempo para fazer o check() no turno 9: 0.1712

Tentando resolver com 10 turnos...
Tempo para processar as restrições até turno 10: 0.0603
Tempo para fazer o check() no turno 10: 0.2512

Tentando resolver com 11 turnos...
Tempo para processar as restrições até turno 11: 0.0599
Tempo para fazer o check() no turno 11: 0.2813

Tentando resolver com 12 turnos...
Tempo para processar as restrições até turno 12: 0.0598
Tempo para fazer o check() no turno 12: 0.4226

Tentando resolver com 13 turnos...
Tempo para processar as restrições até turno 13: 0.0604

✅ Solução encontrada com 13 turnos!

========== Turno 0 ==========
######
#x...#
#BBBm#
#m...#
######

========== Turno 1 ==========
######
#m...#
#SBBm#
#b...#
######

========== Turno 2 ==========
######
#x...#
#.BBm#
#b...#
######

========== Turno 3 ==========
######
#mS..#
#.BBm#
#b...#
######

========== Turno 4 ==========
######
#m.S.#
#.BBm#
#b...#
######

========== Turno 5 ==========
######
#m..S#
#.BBm#
#b...#
######

========== Turno 6 ==========
######
#m...#
#.BBx#
#b...#
######

========== Turno 7 ==========
######
#m...#
#.BBm#
#b..S#
######

========== Turno 8 ==========
######
#m...#
#.BBm#
#b.S.#
######

========== Turno 9 ==========
######
#m...#
#.BBm#
#bS..#
######

========== Turno 10 ==========
######
#mB..#
#.SBm#
#b...#
######

========== Turno 11 ==========
######
#mB..#
#..Sb#
#b...#
######

========== Turno 12 ==========
######
#mBS.#
#...b#
#b...#
######

========== Turno 13 ==========
######
#bS..#
#...b#
#b...#
######

==============================

```

## Exemplo 4

### Input

```python

map_4 = [
    list("####### "),
    list("##S##mm#"),
    list("# BB Bm#"),
    list("#   B  #"),
    list("####  m#"),
    list("   #####")
]

```

### Output

```bash

Tentando resolver com 0 turnos...
Tempo para processar as restrições até turno 0: 0.1381
Tempo para fazer o check() no turno 0: 0.0208

Tentando resolver com 1 turnos...
Tempo para processar as restrições até turno 1: 0.1370
Tempo para fazer o check() no turno 1: 0.0325

Tentando resolver com 2 turnos...
Tempo para processar as restrições até turno 2: 0.1376
Tempo para fazer o check() no turno 2: 0.0526

Tentando resolver com 3 turnos...
Tempo para processar as restrições até turno 3: 0.1374
Tempo para fazer o check() no turno 3: 0.1098

Tentando resolver com 4 turnos...
Tempo para processar as restrições até turno 4: 0.1375
Tempo para fazer o check() no turno 4: 0.1569

Tentando resolver com 5 turnos...
Tempo para processar as restrições até turno 5: 0.1379
Tempo para fazer o check() no turno 5: 0.2482

Tentando resolver com 6 turnos...
Tempo para processar as restrições até turno 6: 0.1383
Tempo para fazer o check() no turno 6: 0.3770

Tentando resolver com 7 turnos...
Tempo para processar as restrições até turno 7: 0.1387
Tempo para fazer o check() no turno 7: 0.3421

Tentando resolver com 8 turnos...
Tempo para processar as restrições até turno 8: 0.1378
Tempo para fazer o check() no turno 8: 0.4443

Tentando resolver com 9 turnos...
Tempo para processar as restrições até turno 9: 0.1387
Tempo para fazer o check() no turno 9: 0.5757

Tentando resolver com 10 turnos...
Tempo para processar as restrições até turno 10: 0.1383
Tempo para fazer o check() no turno 10: 0.6981

Tentando resolver com 11 turnos...
Tempo para processar as restrições até turno 11: 0.1371
Tempo para fazer o check() no turno 11: 0.9137

Tentando resolver com 12 turnos...
Tempo para processar as restrições até turno 12: 0.1378
Tempo para fazer o check() no turno 12: 1.1855

Tentando resolver com 13 turnos...
Tempo para processar as restrições até turno 13: 0.1375
Tempo para fazer o check() no turno 13: 1.1401

Tentando resolver com 14 turnos...
Tempo para processar as restrições até turno 14: 0.1379
Tempo para fazer o check() no turno 14: 1.9160

Tentando resolver com 15 turnos...
Tempo para processar as restrições até turno 15: 0.1382
Tempo para fazer o check() no turno 15: 2.3664

Tentando resolver com 16 turnos...
Tempo para processar as restrições até turno 16: 0.1384
Tempo para fazer o check() no turno 16: 2.6425

Tentando resolver com 17 turnos...
Tempo para processar as restrições até turno 17: 0.1382
Tempo para fazer o check() no turno 17: 2.3363

Tentando resolver com 18 turnos...
Tempo para processar as restrições até turno 18: 0.1376
Tempo para fazer o check() no turno 18: 2.9488

Tentando resolver com 19 turnos...
Tempo para processar as restrições até turno 19: 0.1381
Tempo para fazer o check() no turno 19: 3.3590

Tentando resolver com 20 turnos...
Tempo para processar as restrições até turno 20: 0.1379
Tempo para fazer o check() no turno 20: 5.0043

Tentando resolver com 21 turnos...
Tempo para processar as restrições até turno 21: 0.1376
Tempo para fazer o check() no turno 21: 4.4599

Tentando resolver com 22 turnos...
Tempo para processar as restrições até turno 22: 0.1381
Tempo para fazer o check() no turno 22: 4.4899

Tentando resolver com 23 turnos...
Tempo para processar as restrições até turno 23: 0.1379
Tempo para fazer o check() no turno 23: 6.0303

Tentando resolver com 24 turnos...
Tempo para processar as restrições até turno 24: 0.1387
Tempo para fazer o check() no turno 24: 7.5629

Tentando resolver com 25 turnos...
Tempo para processar as restrições até turno 25: 0.1383
Tempo para fazer o check() no turno 25: 10.4057

Tentando resolver com 26 turnos...
Tempo para processar as restrições até turno 26: 0.1384
Tempo para fazer o check() no turno 26: 12.5977

Tentando resolver com 27 turnos...
Tempo para processar as restrições até turno 27: 0.1384
Tempo para fazer o check() no turno 27: 13.5976

Tentando resolver com 28 turnos...
Tempo para processar as restrições até turno 28: 0.1398
Tempo para fazer o check() no turno 28: 22.9161

Tentando resolver com 29 turnos...
Tempo para processar as restrições até turno 29: 0.1374
Tempo para fazer o check() no turno 29: 25.2862

Tentando resolver com 30 turnos...
Tempo para processar as restrições até turno 30: 0.1406

✅ Solução encontrada com 30 turnos!

========== Turno 0 ==========
#######.
##S##mm#
#.BB.Bm#
#...B..#
####..m#
...#####

========== Turno 1 ==========
#######.
##.##mm#
#.SB.Bm#
#.B.B..#
####..m#
...#####

========== Turno 2 ==========
#######.
##.##mm#
#..SBBm#
#.B.B..#
####..m#
...#####

========== Turno 3 ==========
#######.
##.##mm#
#...BBm#
#.BSB..#
####..m#
...#####

========== Turno 4 ==========
#######.
##.##mm#
#...BBm#
#.B.SB.#
####..m#
...#####

========== Turno 5 ==========
#######.
##.##mm#
#...BBm#
#.B..SB#
####..m#
...#####

========== Turno 6 ==========
#######.
##.##bm#
#...BSm#
#.B...B#
####..m#
...#####

========== Turno 7 ==========
#######.
##.##bm#
#...B.m#
#.B..SB#
####..m#
...#####

========== Turno 8 ==========
#######.
##.##bm#
#...B.m#
#.B...B#
####.Sm#
...#####

========== Turno 9 ==========
#######.
##.##bm#
#...B.m#
#.B...B#
####..x#
...#####

========== Turno 10 ==========
#######.
##.##bm#
#...B.b#
#.B...S#
####..m#
...#####

========== Turno 11 ==========
#######.
##.##bb#
#...B.x#
#.B....#
####..m#
...#####

========== Turno 12 ==========
#######.
##.##bb#
#...B.m#
#.B...S#
####..m#
...#####

========== Turno 13 ==========
#######.
##.##bb#
#...B.m#
#.B..S.#
####..m#
...#####

========== Turno 14 ==========
#######.
##.##bb#
#...B.m#
#.B.S..#
####..m#
...#####

========== Turno 15 ==========
#######.
##.##bb#
#...B.m#
#.BS...#
####..m#
...#####

========== Turno 16 ==========
#######.
##.##bb#
#..SB.m#
#.B....#
####..m#
...#####

========== Turno 17 ==========
#######.
##.##bb#
#...SBm#
#.B....#
####..m#
...#####

========== Turno 18 ==========
#######.
##.##bb#
#..S.Bm#
#.B....#
####..m#
...#####

========== Turno 19 ==========
#######.
##.##bb#
#.S..Bm#
#.B....#
####..m#
...#####

========== Turno 20 ==========
#######.
##.##bb#
#S...Bm#
#.B....#
####..m#
...#####

========== Turno 21 ==========
#######.
##.##bb#
#....Bm#
#SB....#
####..m#
...#####

========== Turno 22 ==========
#######.
##.##bb#
#....Bm#
#.SB...#
####..m#
...#####

========== Turno 23 ==========
#######.
##.##bb#
#....Bm#
#..SB..#
####..m#
...#####

========== Turno 24 ==========
#######.
##.##bb#
#....Bm#
#...SB.#
####..m#
...#####

========== Turno 25 ==========
#######.
##.##bb#
#...SBm#
#....B.#
####..m#
...#####

========== Turno 26 ==========
#######.
##.##bb#
#....Sb#
#....B.#
####..m#
...#####

========== Turno 27 ==========
#######.
##.##bb#
#.....b#
#....S.#
####.Bm#
...#####

========== Turno 28 ==========
#######.
##.##bb#
#.....b#
#...S..#
####.Bm#
...#####

========== Turno 29 ==========
#######.
##.##bb#
#.....b#
#......#
####SBm#
...#####

========== Turno 30 ==========
#######.
##.##bb#
#.....b#
#......#
####.Sb#
...#####

==============================

```


