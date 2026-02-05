#!/usr/bin/env python3
"""
Demo Lead Generator - Sector Legal Vigo

Generates realistic demo data for law firms in Vigo, Spain.
Used when Google blocks scraping.
"""

import json
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# Spanish law firm name components
PREFIXES = ["Despacho", "Bufete", "Abogados", "Asesoría Legal", "Gabinete Jurídico"]
APELLIDOS = [
    "García", "Rodríguez", "Fernández", "López", "Martínez", 
    "González", "Sánchez", "Pérez", "Gómez", "Ruiz",
    "Díaz", "Hernández", "Álvarez", "Jiménez", "Castro",
    "Domínguez", "Vázquez", "Blanco", "Otero", "Iglesias"
]
NOMBRES = [
    "Alejandro", "Carlos", "María", "José", "Antonio",
    "Manuel", "Francisco", "David", "Juan", "Sara",
    "Laura", "Carmen", "Rosa", "Alberto", "Miguel"
]

CATEGORIES = [
    "Abogado Generalista",
    "Derecho Civil",
    "Derecho Laboral", 
    "Derecho de Familia",
    "Derecho Mercantil",
    "Derecho Penal",
    "Derecho Fiscal"
]

# Vigo addresses
CALLES_VIGO = [
    "Calle Príncipe", "Calle Urzáiz", "Gran Vía", "Avenida García Barbón",
    "Calle Colón", "Calle Venezuela", "Calle Policarpo Sanz", "Rúa do Roupeiro",
    "Avenida de Samil", "Calle Velázquez Moreno", "Calle Carral", "Plaza de Compostela"
]

CP_VIGO = ["36201", "36202", "36203", "36204", "36205", "36206", "36207", "36208", "36209", "36210"]


def generate_law_firm_name(index: int) -> tuple:
    """Generate realistic Spanish law firm name and owner name"""
    apellido1 = random.choice(APELLIDOS)
    apellido2 = random.choice([a for a in APELLIDOS if a != apellido1])
    nombre = random.choice(NOMBRES)
    
    name_styles = [
        f"{apellido1} & {apellido2} Abogados",
        f"Bufete {apellido1}",
        f"Despacho {apellido1} {apellido2}",
        f"{apellido1} Abogados",
        f"Asesoría Legal {apellido1}",
        f"Gabinete Jurídico {apellido1}"
    ]
    
    business_name = random.choice(name_styles)
    owner_name = f"{nombre} {apellido1} {apellido2}"
    
    return business_name, owner_name, apellido1.lower()


def generate_phone() -> str:
    """Generate realistic Vigo phone number"""
    prefixes = ["986", "886"]  # Vigo area codes
    prefix = random.choice(prefixes)
    return f"+34 {prefix} {random.randint(100, 999)} {random.randint(100, 999)}"


def generate_email(base_domain: str, has_email: bool) -> str:
    """Generate email based on domain"""
    if not has_email:
        return "N/A"
    
    prefixes = ["info", "contacto", "abogados", "despacho", "consultas"]
    return f"{random.choice(prefixes)}@{base_domain}.es"


def generate_website(base_domain: str, has_website: bool) -> str:
    """Generate website URL"""
    if not has_website:
        return "N/A"
    
    tlds = [".es", ".com", ".gal"]
    return f"https://www.{base_domain}abogados{random.choice(tlds)}"


def calculate_lead_score(has_email: bool, has_social: bool) -> tuple:
    """Calculate lead score based on contact availability"""
    score = 1  # Base
    if has_email:
        score += 3
    if has_social:
        score += 1
    
    labels = {
        5: "⭐⭐⭐⭐⭐ Excelente",
        4: "⭐⭐⭐⭐ Bueno",
        2: "⭐⭐ Regular",
        1: "⭐ Bajo"
    }
    
    return score, labels.get(score, "Desconocido")


def generate_lead(index: int) -> Dict:
    """Generate a single realistic law firm lead in Vigo"""
    
    # Realistic probability distribution
    has_email = random.random() < 0.70  # 70% have email
    has_social = random.random() < 0.50  # 50% have social (law firms less digital)
    has_website = random.random() < 0.80  # 80% have website
    
    business_name, owner_name, base_domain = generate_law_firm_name(index)
    
    street_num = random.randint(1, 150)
    street = random.choice(CALLES_VIGO)
    floor = random.choice(["", f", {random.randint(1,8)}º", f", Bajo", f", Entresuelo"])
    cp = random.choice(CP_VIGO)
    
    rating = round(random.uniform(3.8, 5.0), 1)
    reviews = random.randint(5, 120)
    
    score, score_label = calculate_lead_score(has_email, has_social)
    
    website = generate_website(base_domain, has_website)
    
    lead = {
        'lead_number': index,
        'lead_score': score,
        'score_label': score_label,
        'name': business_name,
        'category': random.choice(CATEGORIES),
        'address': f"{street} {street_num}{floor}, {cp} Vigo, Pontevedra",
        'phone': generate_phone(),
        'email': generate_email(base_domain, has_email),
        'website': website,
        'rating': str(rating),
        'reviews': str(reviews),
        'hours': "Lun-Vie 9:00-14:00, 16:00-20:00" if random.random() > 0.2 else "N/A",
        'price_level': random.choice(["€€", "€€€", "N/A"]),
        'google_maps_url': f"https://maps.google.com/?cid={random.randint(10000000, 99999999)}",
        'owner_name': owner_name,
        'owner_title': random.choice(["Socio Director", "Abogado Principal", "Director", "Fundador"]),
    }
    
    # Generate social media (law firms typically less active)
    if has_social:
        handle = base_domain + "abogados"
        lead['facebook'] = f"https://facebook.com/{handle}" if random.random() > 0.4 else "N/A"
        lead['instagram'] = "N/A"  # Law firms rarely on Instagram
        lead['tiktok'] = "N/A"
        lead['linkedin'] = f"https://linkedin.com/company/{handle}" if random.random() > 0.3 else "N/A"
        lead['twitter'] = f"https://twitter.com/{handle}" if random.random() > 0.7 else "N/A"
    else:
        lead['facebook'] = "N/A"
        lead['instagram'] = "N/A"
        lead['tiktok'] = "N/A"
        lead['linkedin'] = "N/A"
        lead['twitter'] = "N/A"
    
    return lead


def main():
    """Generate demo leads for Vigo law firms"""
    
    # Setup output
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    tmp_dir = project_root / ".tmp"
    tmp_dir.mkdir(exist_ok=True)
    
    output_path = tmp_dir / f"vigo_legal_leads_{timestamp}.json"
    
    print("\n" + "=" * 80)
    print("DEMO LEAD GENERATOR - SECTOR LEGAL VIGO")
    print("(Genera datos realistas de prueba)")
    print("=" * 80)
    print(f"Sector: Abogados / Despachos Legales")
    print(f"Ubicación: Vigo, Pontevedra")
    print(f"Número de Leads: 15")
    print(f"Output: {output_path}")
    print("=" * 80 + "\n")
    
    # Generate leads
    print("📊 Generando leads de despachos legales en Vigo...")
    results = []
    
    for i in range(1, 16):
        lead = generate_lead(i)
        results.append(lead)
        print(f"  [{i}/15] {lead['name']} - Puntuación: {lead['lead_score']}/5")
    
    # Sort by lead score
    results.sort(key=lambda x: x['lead_score'], reverse=True)
    
    # Renumber after sorting
    for i, lead in enumerate(results, 1):
        lead['lead_number'] = i
    
    print(f"\n✓ Generados {len(results)} leads")
    
    # Save as JSON
    output_data = {
        'generated_at': datetime.now().isoformat(),
        'total_leads': len(results),
        'sector': 'Legal / Abogados',
        'location': 'Vigo, Pontevedra, España',
        'note': 'Demo data para testing - no son negocios reales',
        'leads': results
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Guardado en: {output_path}")
    
    # Summary
    high_value = [l for l in results if l['lead_score'] >= 4]
    print(f"\n📈 Leads de alto valor (Score 4-5): {len(high_value)}")
    
    for lead in high_value:
        print(f"   • {lead['name']} ({lead['category']}) - Score: {lead['lead_score']}")
    
    print("\n" + "=" * 80)
    print("⚠️  NOTA: Estos son DATOS DE DEMO para testing.")
    print("    No son negocios reales. Usar solo para demostración.")
    print("=" * 80 + "\n")
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
