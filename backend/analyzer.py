def analyze_text(text: str):
    text = text.lower()
    findings = []
    
    # Mapping keywords to NIS2 Article 21 Domains
    domain_map = {
        "Incident Handling": ["log", "monitor", "breach", "incident", "alert", "response"],
        "Risk Assessment": ["vulnerability", "risk", "threat", "assessment", "audit"],
        "Supply Chain Security": ["vendor", "third-party", "supplier", "procurement", "contract"],
        "Network & Info System Security": ["encryption", "mfa", "access", "firewall", "password", "auth"]
    }

    for domain, keywords in domain_map.items():
        # Count how many unique keywords appear in the text
        matches = [kw for kw in keywords if kw in text]
        
        if matches:
            # Logic: 1 match = 0.60, 2 = 0.80, 3+ = 0.95 (Confidence Scoring)
            base_score = 0.5
            confidence = min(0.98, base_score + (len(matches) * 0.15))
            
            findings.append({
                "source_fragment": f"Detected: {', '.join(matches[:3])}",
                "identified_control": f"{domain} Protection",
                "nis2_pillar": domain,
                "confidence": round(confidence, 2),
                "reasoning": f"Found {len(matches)} relevant security keywords."
            })

    return findings