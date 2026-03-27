# Quantum Cryptography & Post-Quantum Cryptography

A concise guide to quantum cryptographic protocols and the modern algorithms designed to withstand quantum attacks.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Quantum Key Distribution (QKD)](#quantum-key-distribution-qkd)
   - [BB84 Protocol](#bb84-protocol)
3. [Quantum Threats to Classical Cryptography](#quantum-threats-to-classical-cryptography)
   - [Grover's Algorithm](#grovers-algorithm)
   - [Shor's Algorithm](#shors-algorithm)
4. [Post-Quantum Cryptography (PQC)](#post-quantum-cryptography-pqc)
   - [CRYSTALS-Kyber (ML-KEM)](#crystals-kyber-ml-kem)
   - [CRYSTALS-Dilithium (ML-DSA)](#crystals-dilithium-ml-dsa)
   - [SPHINCS+ (SLH-DSA)](#sphincs-slh-dsa)
   - [FALCON (FN-DSA)](#falcon-fn-dsa)
   - [BIKE & HQC (Code-Based)](#bike--hqc-code-based)
5. [NIST Standardization](#nist-standardization)
6. [Choosing the Right Algorithm](#choosing-the-right-algorithm)
7. [Further Reading](#further-reading)

---

## Introduction

Quantum computing poses a fundamental threat to most of today's public-key cryptography. Algorithms like RSA, ECDSA, and Diffie-Hellman derive their security from the computational hardness of problems — integer factorization and discrete logarithms — that a sufficiently powerful quantum computer can solve efficiently.

This document covers:
- **Quantum cryptography**: protocols that *use* quantum mechanics to secure communications (e.g., QKD).
- **Post-quantum cryptography (PQC)**: classical algorithms designed to be *resistant* to quantum attacks.

These are distinct fields. QKD requires quantum hardware; PQC runs on conventional computers.

---

## Quantum Key Distribution (QKD)

QKD uses the laws of quantum mechanics to distribute cryptographic keys with information-theoretic security. Any eavesdropping attempt disturbs the quantum states being transmitted, making interception detectable.

### BB84 Protocol

**Proposed by:** Charles Bennett & Gilles Brassard, 1984  
**Security basis:** Heisenberg Uncertainty Principle, quantum no-cloning theorem

BB84 was the first quantum key distribution protocol and remains the most widely studied.

#### How It Works

1. **Alice** generates a random bit string and encodes each bit as a photon polarization, choosing randomly between two *bases*:
   - **Rectilinear basis (+):** `0` → horizontal `—`, `1` → vertical `|`
   - **Diagonal basis (×):** `0` → `\`, `1` → `/`

2. **Bob** measures each incoming photon, also choosing a basis randomly and independently for each bit.

3. **Sifting:** Alice and Bob publicly compare *which bases* they used (not the bit values). They discard bits where their bases differed. Statistically, ~50% of bits are kept.

4. **Error estimation:** They sacrifice a small random subset of the remaining bits to estimate the error rate (QBER — Quantum Bit Error Rate). A high QBER indicates eavesdropping or channel noise.

5. **Classical post-processing:** They apply information reconciliation (error correction) and privacy amplification to distill a shared secret key that an eavesdropper has negligible information about.

#### Why Eavesdropping Is Detectable

An eavesdropper (Eve) must measure photons to intercept information, but she doesn't know Alice's basis for each photon. When she guesses wrong, she collapses the quantum state — Bob then receives a disturbed photon, introducing detectable errors.

#### Limitations

- Requires quantum channels (typically fiber optic or free-space optical links).
- Distance-limited; quantum repeaters are an active research area.
- Vulnerable to *implementation* attacks (side-channel, detector blinding) even if theoretically secure.
- Key rates are low compared to classical communication.

---

## Quantum Threats to Classical Cryptography

### Grover's Algorithm

**Proposed by:** Lov Grover, 1996  
**Impact:** Quadratic speedup for unstructured search

Grover's algorithm searches an unsorted database of `N` items in `O(√N)` operations, compared to `O(N)` classically.

**Cryptographic impact:**
- Effectively **halves the security level** of symmetric keys and hash functions.
- AES-128 → ~64-bit quantum security. **Mitigation:** use AES-256.
- SHA-256 → ~128-bit quantum security. Generally still acceptable.

Grover's is a polynomial speedup — significant, but manageable by doubling key sizes. It does **not** break symmetric cryptography outright.

### Shor's Algorithm

**Proposed by:** Peter Shor, 1994  
**Impact:** Exponential speedup for factoring and discrete logarithm problems

Shor's algorithm solves integer factorization and discrete logarithms in **polynomial time**, breaking:

| Algorithm | Classical Security | Quantum Security (Shor) |
|-----------|-------------------|------------------------|
| RSA-2048  | ~112 bits         | **Broken**             |
| ECC-256   | ~128 bits         | **Broken**             |
| DH-2048   | ~112 bits         | **Broken**             |

This is the primary driver behind the development of post-quantum cryptography. No key size increase can salvage RSA or ECC against a cryptographically relevant quantum computer.

---

## Post-Quantum Cryptography (PQC)

PQC algorithms run on classical hardware and are designed to be secure against both classical and quantum adversaries. They rely on mathematical problems believed to be hard even for quantum computers.

**Main hard problem families:**
- **Lattice-based:** Learning With Errors (LWE), Module-LWE, NTRU
- **Hash-based:** One-way functions; quantum-safe by design
- **Code-based:** Decoding random linear codes (McEliece, 1978)
- **Isogeny-based:** Elliptic curve isogenies *(SIKE was broken classically in 2022 — largely abandoned)*

---

### CRYSTALS-Kyber (ML-KEM)

**Type:** Key Encapsulation Mechanism (KEM)  
**Standard:** FIPS 203 (ML-KEM) — finalized August 2024  
**Hard problem:** Module Learning With Errors (MLWE)

Kyber is the primary PQC algorithm for key exchange and encryption. It generates a shared secret through encapsulation/decapsulation, replacing RSA/ECDH in TLS, SSH, and similar protocols.

**Security levels:**

| Variant      | NIST Level | Classical Security | Public Key | Ciphertext |
|--------------|------------|-------------------|------------|------------|
| Kyber-512    | 1 (AES-128 equivalent) | ~102 bits | 800 B | 768 B |
| Kyber-768    | 3 (AES-192 equivalent) | ~161 bits | 1184 B | 1088 B |
| Kyber-1024   | 5 (AES-256 equivalent) | ~218 bits | 1568 B | 1568 B |

**Why it matters:** Kyber-768 is already being deployed by Google, Apple, Signal, and Cloudflare in hybrid TLS configurations alongside ECDH.

---

### CRYSTALS-Dilithium (ML-DSA)

**Type:** Digital Signature Algorithm  
**Standard:** FIPS 204 (ML-DSA) — finalized August 2024  
**Hard problem:** Module Learning With Errors + Short Integer Solution (MLWE/MSIS)

Dilithium replaces ECDSA and RSA signatures. It uses a "Fiat-Shamir with aborts" construction over module lattices.

**Security levels:**

| Variant       | NIST Level | Public Key | Signature |
|---------------|------------|------------|-----------|
| Dilithium2    | 2          | 1312 B     | 2420 B    |
| Dilithium3    | 3          | 1952 B     | 3293 B    |
| Dilithium5    | 5          | 2592 B     | 4595 B    |

**Trade-off:** Signatures are significantly larger than ECDSA (64 bytes for P-256). For most applications this is acceptable; for constrained protocols (e.g., blockchain, IoT), careful profiling is needed.

---

### SPHINCS+ (SLH-DSA)

**Type:** Digital Signature Algorithm  
**Standard:** FIPS 205 (SLH-DSA) — finalized August 2024  
**Hard problem:** Security of hash functions (SHA-256, SHAKE)

SPHINCS+ is a **stateless hash-based signature** scheme. Its security reduces entirely to the one-wayness of the underlying hash function — no algebraic structure to attack.

**Key properties:**
- **Conservative:** Minimal assumptions; quantum-safe hash functions are well-understood.
- **Stateless:** Unlike XMSS/LMS (stateful schemes), no state management is required.
- **Trade-off:** Significantly larger signatures (8–50 KB depending on parameters) and slower signing than lattice-based alternatives.

**When to use:** When long-term security assurance matters more than performance, or as a conservative fallback alongside Dilithium.

---

### FALCON (FN-DSA)

**Type:** Digital Signature Algorithm  
**Standard:** FIPS 206 (FN-DSA) — finalized August 2024  
**Hard problem:** NTRU lattice / Short Integer Solution (SIS)

FALCON produces much **smaller signatures** than Dilithium, making it attractive for bandwidth-constrained environments.

| Variant   | NIST Level | Public Key | Signature |
|-----------|------------|------------|-----------|
| FALCON-512  | 1        | 897 B      | ~666 B    |
| FALCON-1024 | 5        | 1793 B     | ~1280 B   |

**Trade-off:** FALCON's signing requires discrete Gaussian sampling, which is complex to implement in constant time. Side-channel resistance demands careful implementation.

---

### BIKE & HQC (Code-Based)

**Type:** Key Encapsulation Mechanisms  
**NIST status:** Round 4 candidates (alternate KEMs under evaluation)  
**Hard problem:** Decoding random quasi-cyclic codes

**BIKE** (Bit Flipping Key Encapsulation) and **HQC** (Hamming Quasi-Cyclic) are code-based alternatives to Kyber. They offer different security/size trade-offs and provide algorithm diversity — important if a lattice vulnerability is ever discovered.

- Smaller public keys than classic McEliece (which has ~1 MB keys)
- Decryption failure probability requires careful parameter selection
- Likely to be standardized as backup KEMs

---

## NIST Standardization

NIST ran a multi-year PQC standardization process (2016–2024):

| Algorithm      | Role        | Standard    | Status           |
|----------------|-------------|-------------|------------------|
| ML-KEM (Kyber) | KEM         | FIPS 203    | ✅ Final (Aug 2024) |
| ML-DSA (Dilithium) | Signature | FIPS 204  | ✅ Final (Aug 2024) |
| SLH-DSA (SPHINCS+) | Signature | FIPS 205  | ✅ Final (Aug 2024) |
| FN-DSA (FALCON) | Signature  | FIPS 206    | ✅ Final (Aug 2024) |
| BIKE           | KEM         | Under review | 🔄 Round 4       |
| HQC            | KEM         | Under review | 🔄 Round 4       |
| Classic McEliece | KEM       | Under review | 🔄 Round 4       |

---

## Choosing the Right Algorithm

| Use Case | Recommendation |
|----------|---------------|
| TLS / key exchange | **ML-KEM (Kyber-768)** |
| Code signing, certificates | **ML-DSA (Dilithium3)** or **FN-DSA (FALCON-512)** |
| Long-term archival / PKI | **SLH-DSA (SPHINCS+)** as conservative backup |
| Constrained bandwidth (IoT, blockchain) | **FALCON** for small signatures |
| Defense in depth | **Hybrid** classical + PQC (e.g., X25519 + Kyber) |

**Hybrid mode** is currently recommended by NIST, NSA, and ANSSI: combine a classical algorithm (ECDH/ECDSA) with a PQC algorithm. This protects against both implementation flaws in new PQC code and future quantum attacks on classical crypto.

---

## Further Reading

- [NIST PQC Project](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [FIPS 203 — ML-KEM](https://doi.org/10.6028/NIST.FIPS.203)
- [FIPS 204 — ML-DSA](https://doi.org/10.6028/NIST.FIPS.204)
- [FIPS 205 — SLH-DSA](https://doi.org/10.6028/NIST.FIPS.205)
- [Original BB84 Paper (Bennett & Brassard, 1984)](https://doi.org/10.1016/j.tcs.2014.05.025)
- [Open Quantum Safe (liboqs)](https://openquantumsafe.org/) — open-source PQC implementations
- [PQCRYPTO Project](https://pqcrypto.eu.org/)
- [NSA CNSA 2.0 Suite](https://www.nsa.gov/Cybersecurity/Post-Quantum-Cybersecurity-Resources/)
