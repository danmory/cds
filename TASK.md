# Поиск наименьшего связного доминирующего множества

## Определение

Доминирующим множеством в графе G = (V, E) называется множество M ⊂ V ,
такое что любая вершина v либо лежит в M, либо соединена ребром с одной из
вершин, лежащих в M.

## Задание

1. Докажите, что задача поиска наименьшего связного доминирующего множества NP-трудная;
2. Имплементируйте какой-нибудь алгоритм поиска наименьшего связного доминирующего множества, работающий за O(c^n) для c < 1.95.