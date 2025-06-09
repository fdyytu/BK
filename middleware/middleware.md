# Middleware Layer – Modular Architecture

This directory defines a **modular and scalable middleware layer** designed to support complex applications such as digital product platforms, e-wallet systems, and integrated PPOB (Payment Point Online Bank) services.

## 🎯 Purpose

This layer acts as a bridge between FastAPI's routing and the core application logic. It provides:

- Cross-cutting concerns (e.g., security, caching, validation)
- Pluggable strategies (e.g., JWT, rate limiting, anti-fraud)
- Support for third-party integrations
- Transaction and product flow validation
- Multi-level user authorization & access control
- High-performance tools (Redis, RabbitMQ, Circuit Breakers)

---

## 🧩 Folder Structure

### `core/`
Foundational contracts and middleware registry.

- `abstract/`: Base classes for validators, middleware, handlers.
- `interfaces/`: Interface definitions for plug-and-play components.
- `registry/`: Dependency container and middleware registration system.

---

### `authentication/`
Pluggable auth strategies and providers.

- `strategies/`: JWT, OAuth2, API Key handling.
- `providers/`: Google, Facebook, Apple auth.
- `services/`: Token issuance, refresh, session logic.

---

### `authorization/`
Role & permission management.

- `rbac/`: Role-based access control components.
- `policies/`: Access policy rules & rate limiting policies.
- `services/`: Policy enforcement and evaluation engines.

---

### `transaction/`
Validation and execution of financial transactions.

- `processors/`: Payment, refund, wallet processors.
- `validators/`: Check balance, limits, and fraud.
- `handlers/`: Handle success, failure, and retry flows.

---

### `product/`
Manage digital product inventory and pricing.

- `inventory/`: Stock control and availability checks.
- `pricing/`: Dynamic pricing and commission rules.
- `validators/`: Validation rules per product or category.

---

### `security/`
Application-wide security components.

- `encryption/`: AES and RSA handlers.
- `firewall/`: IP and request-level filtering.
- `anti_fraud/`: Pattern, ML-based detection, rule engines.
- `audit/`: Logging and compliance checkers.

---

### `integration/`
Third-party APIs and provider integrations.

- `payment_gateway/`: Midtrans, Xendit, DOKU connectors.
- `provider/`: PPOB & telco/game utility providers.
- `partner/`: Partner-level APIs and webhook handling.

---

### `performance/`
System performance, caching, and queuing.

- `cache/`: Redis manager and cache strategies.
- `queue/`: RabbitMQ manager, strategy, DLQ handler.
- `optimization/`: Response and query performance enhancers.

---

### `monitoring/`
Track and observe system metrics.

- `metrics/`: Prometheus and Grafana clients.
- `tracing/`: OpenTelemetry, Jaeger tracers.
- `alerting/`: Alert manager and notification systems.

---

### `resilience/`
Resilient architecture patterns.

- `circuit_breaker/`: Breaker logic and state management.
- `rate_limiter/`: Token bucket and sliding window strategies.
- `fallback/`: Fallback handler and retry mechanism.

---

### `utils/`
Common utilities and decorators.

- `decorators/`: Decorators for caching, validation, monitoring.
- `helpers/`: Crypto, datetime, and validation helpers.
- `constants/`: Shared constants (error/status/config).

---

## 🛠 Tech Stack & Integration

- **Framework**: FastAPI
- **Messaging Queue**: RabbitMQ
- **Cache Layer**: Redis
- **Monitoring**: Prometheus, Grafana, OpenTelemetry
- **Authentication**: JWT, OAuth2
- **Use Case**: Digital Product API, PPOB Platform, Financial Transaction System

---

## 🧠 Design Principles

- **SOLID**: Interface-based separation of concerns.
- **DRY**: Shared helpers & base classes.
- **Composable**: Swap strategies/policies without code rewrites.
- **Observable**: Full support for tracing, logging, and alerting.

---

## 🔌 Getting Started

To implement or test:

```bash
cd middleware/
# Add your logic or extend components
# e.g., implement your jwt_strategy.py