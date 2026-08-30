# tests/matrix

**Директория:** `tests/matrix/`

## Назначение

Fixture-копия `adjacency_matrix.csv` для тестов `Destination`.

Она нужна, чтобы тесты не зависели от того, какая матрица сейчас лежит в production `matrix/`.

При изменении схемы CSV обновлять необходимо обе стороны осознанно: production matrix и test fixture.
