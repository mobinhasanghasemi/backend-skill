# Python Typing & Data Models

## Identity
- ID: python.typing-models
- Type: discipline
- Status: active
- Importance: high

## Purpose
Typed, validated boundaries and clean data models: type hints as documentation + tests, pydantic/dataclasses as runtime guards, and honest unions — so "the bug is on line X" is findable.

## The practice
- **Type every signature** (mypy/pyright in CI) — cheap insurance against 25% class of bugs
- **Boundary validation**: pydantic (fast, JSON-friendly) at API; dataclasses within process; dataclasses+pydantic are complementary:
  - `pydantic.BaseModel` — parse/validate/serialize (API contracts), JSON schema export
  - `@dataclass` — in-memory structured state
- **Option types**: `Optional[T]` is the one that smuggles the bug — prefer `T | None` and exhaustiveness checks (`assert_never`)
- **Generics & protocols**: Protocol for adapters (deco intrusion), TypedDict for dict payloads
- **`Annotated`** field metadata limit — single source of defaults/validation

## Code tiers
### ❌ Bad
```python
def create_user(email, age):
    # no types → "age" arrives as "twenty", or None crashes 30 calls deep later
    if not email or '@' not in email: return "error"
```
### ✅ Good
```python
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    age: int = Field(ge=0, le=130)

def create_user(data: UserCreate) -> UserOut:   # valid before the ORM sees it
```
### ⚡ Better — strict + typed result
```python
class UserIn(BaseModel):
    model_config = ConfigDict(extra="forbid")   # no surprise fields
    ...
class Result: pass
def create_user(data) -> Result[UserOut]:       # errors as data, not exceptions
```
### 🏆 Excellent
```text
# OpenAPI from models (drf-spectacular/fastapi) — one definition, contracts incl
# mypy strict in CI, strict parameters (asym), no Any leaks in boundaries
# domain layer: dataclasses in, pydantic at edges; reproduction of "wrong" states
# model versioning (schema drift checks) for long-lived stores
```

## Failure modes
- typing only at function edges, ground truth none
- Optional everywhere (semantic ambiguity)
- pydantic re-parse of hot paths (cache validated feeds)
- unions & Any defeat the guarantee

## Evidence
- typing/pydantic/mypy official docs (VERIFIED)