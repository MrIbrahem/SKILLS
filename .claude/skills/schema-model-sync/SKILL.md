---
name: schema-model-sync
description: Compare raw MySQL/MariaDB schema exports (Adminer CREATE TABLE dumps) against SQLAlchemy 2.0 models in a Flask-SQLAlchemy project, report every difference, and fix the models. Use when the user asks to audit, sync, or verify models against the real database schema.
---

# Schema ↔ Model Sync

## Goal
The database schema (raw SQL exported from Adminer) is the **source of truth**.
Audit every SQLAlchemy model against it, report differences, and update the
**models** so they match. Never change the database or generate destructive migrations.

## Inputs
- Raw schema files (e.g. `schema/*.sql`, `CREATE TABLE ...` statements). If the location is not given, search for `*.sql` files containing `CREATE TABLE`.
- Model files (find classes inheriting from `db.Model` / `Model`, plus mixins used by them).
- Project base: `db = SQLAlchemy(model_class=BaseModel)` where `BaseModel(DeclarativeBase)` and a constraint `naming_convention` are defined.

## Workflow

### 1. Inventory
- Parse every `CREATE TABLE` into: table name, columns (type, length, unsigned, nullable, default, auto_increment), primary key, unique keys, indexes, foreign keys (with ON DELETE / ON UPDATE), check constraints.
- Collect every model: class, `__tablename__`, columns, `__table_args__`, relationships, and which mixins contribute columns (resolve mixin columns per final table).
- Build a table-to-model mapping. Flag tables with no model, and models with no table.

### 2. Compare (per table, per column)
Check each of the following and record a finding for every mismatch:
- **Existence**: missing column in the model, extra column in the model.
- **Type**: `int`→`Integer`, `tinyint`→`SmallInteger`/`Boolean` (note which), `varchar(N)`→`String(N)` (length must match), `text`, `datetime`/`timestamp`, `date`, `blob`→`LargeBinary(N)`, `enum`.
- **Unsigned**: `int unsigned` needs `Integer().with_variant(mysql.INTEGER(unsigned=True), "mysql")` (or equivalent).
- **Nullability**: `NOT NULL` ↔ `Mapped[X]`, `NULL` ↔ `Mapped[X | None]`; `nullable=` must agree.
- **Defaults**: SQL `DEFAULT` ↔ `server_default=text(...)`; `CURRENT_TIMESTAMP` ↔ `func.current_timestamp()`. Python-side `default=` is allowed in addition but never replaces `server_default`.
- **Primary key / autoincrement**.
- **Indexes and unique keys**: compare column sets and **names**. The DB name wins; if it differs from what `naming_convention` would generate, set the name explicitly (`Index("idx_title", "title")`, `UniqueConstraint(..., name="...")`).
- **Foreign keys**: referenced table/column, `ondelete`, `onupdate`. Flag FKs present in the DB but missing in the model and vice versa. Respect comments stating "no FK" intentionally.
- **Collation/charset/engine**: report only; do not model them unless the project already does.

### 3. Report first
Before editing, print a table grouped by severity:
- **Missing** (in DB, not in model)
- **Mismatch** (type, length, nullability, default, index name, FK action)
- **Extra** (in model, not in DB)
- **Informational** (collation, engine, naming differences with no runtime effect)

Each row: `table | column/object | DB says | model says | proposed fix`.

### 4. Apply fixes (models only)
Follow these project rules:
- SQLAlchemy 2.0 style: `Mapped[...]` + `mapped_column(...)`. Omit `mapped_column()` when the annotation alone is enough (no length, default, index, etc.).
- MySQL needs explicit string lengths: always `String(N)` for `varchar(N)`.
- Use `import datetime as dt` and `dt.date` / `dt.datetime` to avoid shadowing columns named `date`.
- **Mixins**: columns with `ForeignKey`, `relationship`, `Index`, `UniqueConstraint`, or `__table_args__` must NOT be shared directly in a mixin. Either define them in each concrete model or wrap them in `declared_attr` / `declared_attr.directive`. Plain columns can stay in mixins.
- Do not add `BaseModel` as an extra base class next to `db.Model`.
- Do not override `__init__` to silently ignore unknown keys.
- Do not duplicate `to_json`; the base one is used. Sensitive columns (tokens, secrets, passwords) must never be serialized: keep or add an exclusion/whitelist, and never expose them.
- Keep existing docstrings/`CREATE TABLE` comments up to date with the new schema.
- All code comments and docstrings in English.
- Preserve existing behavior: do not rename attributes or tables, and do not remove columns from models without listing them under "Extra" and asking for confirmation.

### 5. Verify
- Run the existing test suite and a type check if configured.
- Write or update a small test that imports all models and compares `Model.__table__` columns against the parsed schema (column names, nullability, PK) so future drift is caught.
- Optionally run `alembic revision --autogenerate` in a scratch way (do not commit) to confirm the diff is empty.

### 6. Final output
- Short summary: tables checked, fixes applied, items needing a human decision.
- List of intentionally unchanged differences and why.
- Never leave edits half-applied: if blocked, report exactly what remains.

## Do not
- Do not modify the SQL dump files or the live database.
- Do not generate `DROP` / `ALTER ... DROP` migrations.
- Do not guess: if the dump is ambiguous (e.g. `tinyint(1)` could be bool or int), ask or list the assumption in the report.