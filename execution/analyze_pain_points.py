#!/usr/bin/env python3
"""
Website Pain Point Analyzer for Web Agency

Analyzes business websites to identify opportunities for web design and automation services.
Extracts owner information for personalized outreach.

Usage:
    python analyze_pain_points.py --input .tmp/gmb_leads_enhanced_*.txt
"""

import argparse
import json
import csv
import sys
import re
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed.")
    print("Please run: pip install requests beautifulsoup4 lxml")
    sys.exit(1)


class WebsiteAnalyzer:
    """Analyze websites for pain points and opportunities"""
    
    def __init__(self, timeout: int = 10):
        """
        Initialize the analyzer.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def analyze_website(self, url: str, business_name: str) -> Dict:
        """
        Analyze a website for pain points and extract owner info.
        
        Args:
            url: Website URL
            business_name: Name of the business
            
        Returns:
            Dictionary with analysis results
        """
        result = {
            'pain_point': 'Sin Web',
            'pain_point_details': 'No se pudo acceder al sitio web',
            'proposed_solution': 'Creación de sitio web profesional y optimizado para SEO.',
            'opportunity_score': 0,
            'owner_name': 'N/A',
            'owner_email': 'N/A',
            'owner_title': 'N/A',
            'design_issues': [],
            'automation_gaps': []
        }
        
        if not url or url == 'N/A':
            return result
        
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            print(f"    🔍 Analizando: {url}")
            
            # Fetch website
            start_time = time.time()
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            load_time = time.time() - start_time
            
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            html_lower = response.text.lower()
            
            # Analyze design issues
            design_issues = self._analyze_design(soup, html_lower, load_time, response)
            
            # Analyze automation gaps
            automation_gaps = self._analyze_automation(soup, html_lower)
            
            # Determine pain point
            pain_point, details, solution = self._determine_pain_point(
                design_issues, automation_gaps, load_time
            )
            
            # Calculate opportunity score
            opportunity_score = self._calculate_opportunity_score(
                design_issues, automation_gaps, load_time
            )
            
            # Extract owner information
            owner_info = self._extract_owner_info(soup, url, business_name)
            
            result = {
                'pain_point': pain_point,
                'pain_point_details': details,
                'proposed_solution': solution,
                'opportunity_score': opportunity_score,
                'owner_name': owner_info['name'],
                'owner_email': owner_info['email'],
                'owner_title': owner_info['title'],
                'design_issues': design_issues,
                'automation_gaps': automation_gaps,
                'load_time': round(load_time, 2)
            }
            
            print(f"      ✓ Punto de dolor: {pain_point} (Score: {opportunity_score}/10)")
            if owner_info['name'] != 'N/A':
                print(f"      ✓ Propietario: {owner_info['name']} ({owner_info['title']})")
            
            return result
            
        except requests.Timeout:
            print(f"      ⚠️  Timeout - sitio muy lento")
            result['pain_point'] = 'Rendimiento Crítico'
            result['pain_point_details'] = 'Sitio extremadamente lento (timeout) o inaccesible. Pérdida masiva de conversiones.'
            result['proposed_solution'] = 'Optimización técnica de servidores (WPO) y migración a infraestructura de alta velocidad.'
            result['opportunity_score'] = 7
            return result
            
        except requests.RequestException as e:
            print(f"      ⚠️  Error de acceso: {str(e)[:50]}")
            result['pain_point'] = 'Error de Acceso'
            result['pain_point_details'] = f'Sitio inaccesible ({str(e)[:30]}). Posible dominio caducado o servidor caído.'
            result['proposed_solution'] = 'Auditoría de infraestructura o recuperación de dominio.'
            return result
            
        except Exception as e:
            print(f"      ⚠️  Error inesperado: {str(e)[:50]}")
            result['pain_point'] = 'Error Desconocido'
            result['pain_point_details'] = 'No se pudo analizar el sitio.'
            result['proposed_solution'] = 'Revisión manual requerida.'
            return result
    
    def _analyze_design(self, soup: BeautifulSoup, html_lower: str, 
                       load_time: float, response) -> List[str]:
        """Analyze design issues"""
        issues = []
        
        # Check responsive design
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if not viewport:
            issues.append("No responsive (sin viewport)")
        
        # Check load time
        if load_time > 3:
            issues.append(f"Carga lenta ({load_time:.1f}s)")
        
        # Check HTTPS
        if not response.url.startswith('https://'):
            issues.append("Sin HTTPS (inseguro)")
        
        # Check modern frameworks
        modern_indicators = ['react', 'vue', 'angular', 'next.js', 'nuxt']
        has_modern = any(indicator in html_lower for indicator in modern_indicators)
        
        # Check for outdated tech
        outdated_indicators = ['<frame', '<frameset', 'flash', 'swf']
        has_outdated = any(indicator in html_lower for indicator in outdated_indicators)
        
        if has_outdated:
            issues.append("Tecnología obsoleta (Flash/Frames)")
        elif not has_modern:
            # Check copyright year
            copyright_match = re.search(r'©\s*(\d{4})', html_lower)
            if copyright_match:
                year = int(copyright_match.group(1))
                if year < 2020:
                    issues.append(f"Diseño anticuado (copyright {year})")
        
        # Check meta tags (SEO)
        if not soup.find('meta', attrs={'name': 'description'}):
            issues.append("Sin meta description (mal SEO)")
        
        # Check images optimization
        images = soup.find_all('img')
        if images:
            images_without_alt = [img for img in images if not img.get('alt')]
            if len(images_without_alt) > len(images) * 0.5:
                issues.append("Imágenes sin optimizar (sin alt text)")
        
        return issues
    
    def _analyze_automation(self, soup: BeautifulSoup, html_lower: str) -> List[str]:
        """Analyze automation opportunities"""
        gaps = []
        
        # Check for chatbot
        chatbot_indicators = ['intercom', 'drift', 'tawk', 'crisp', 'zendesk', 
                             'livechat', 'tidio', 'chat']
        has_chatbot = any(indicator in html_lower for indicator in chatbot_indicators)
        if not has_chatbot:
            gaps.append("Sin chatbot")
        
        # Check forms
        forms = soup.find_all('form')
        if forms:
            # Check for basic forms (no automation)
            advanced_form_indicators = ['hubspot', 'typeform', 'jotform', 
                                       'google forms', 'mailchimp']
            has_advanced_forms = any(ind in html_lower for ind in advanced_form_indicators)
            if not has_advanced_forms:
                gaps.append("Formularios básicos (sin automatización)")
        
        # Check for booking/calendar system
        calendar_indicators = ['calendly', 'cal.com', 'acuity', 'booking', 
                              'reserva', 'appointment']
        has_calendar = any(indicator in html_lower for indicator in calendar_indicators)
        if not has_calendar:
            # Only flag if it's a service business
            gaps.append("Sin sistema de reservas online")
        
        # Check for CRM integration
        crm_indicators = ['hubspot', 'salesforce', 'pipedrive', 'zoho']
        has_crm = any(indicator in html_lower for indicator in crm_indicators)
        if not has_crm:
            gaps.append("Sin integración CRM visible")
        
        # Check for email marketing
        email_marketing_indicators = ['mailchimp', 'sendinblue', 'convertkit', 
                                     'newsletter', 'suscr']
        has_email_marketing = any(ind in html_lower for ind in email_marketing_indicators)
        if not has_email_marketing:
            gaps.append("Sin email marketing")
        
        # Check for social media integration
        social_widgets = soup.find_all(['iframe', 'div'], 
                                       class_=re.compile(r'(facebook|instagram|twitter)'))
        if not social_widgets:
            gaps.append("Sin integración de redes sociales")
        
        return gaps
    
    def _determine_pain_point(self, design_issues: List[str], 
                             automation_gaps: List[str], load_time: float) -> tuple:
        """Determine primary pain point, details, and proposed solution"""
        
        pain_point = "Ninguno"
        details = "Sitio moderno y bien optimizado"
        solution = "Mantenimiento preventivo y SEO avanzado."
        
        has_design_issues = len(design_issues) > 0
        has_automation_gaps = len(automation_gaps) > 0
        
        # Priority 1: Critical Design Issues (Non-responsive or Security)
        critical_design = [i for i in design_issues if "responsive" in i.lower() or "inseguro" in i.lower()]
        
        if critical_design:
            pain_point = "Diseño Crítico"
            details = f"Hemos detectado problemas graves: {', '.join(critical_design)}. Esto penaliza drásticamente en Google y genera desconfianza."
            solution = "Rediseño completo con estructura Responsive y certificado SSL para garantizar seguridad y posicionamiento."
            
        elif has_design_issues and has_automation_gaps:
            pain_point = "Transformación Digital (Diseño + Automatización)"
            details = f"El sitio tiene {len(design_issues)} áreas de mejora visual y carece de herramientas de captación ({len(automation_gaps)} oportunidades perdidas)."
            solution = "Modernización de la interfaz y despliegue de un 'Funnel' de captación automatizado (Chatbot + Booking)."
            
        elif has_design_issues:
            pain_point = "Diseño y Experiencia de Usuario"
            issue_text = design_issues[0] if design_issues else "Anticuado"
            details = f"La estética actual no refleja la calidad de vuestros servicios. Detectamos: {', '.join(design_issues[:2])}."
            solution = "Restyling visual enfocado en conversión (CRO) para transmitir autoridad premium."
            
        elif has_automation_gaps:
            pain_point = "Fuga de Clientes (Falta Automatización)"
            gap_text = automation_gaps[0] if automation_gaps else "Sin captación"
            details = f"Tenéis tráfico pero no lo capturáis eficientemente. Faltan herramientas clave como: {', '.join(automation_gaps[:2])}."
            solution = "Integración de Agente IA de Captación y sistema de Agendamiento Automático para no perder clientes fuera de horario."
        
        return pain_point, details, solution
    
    def _calculate_opportunity_score(self, design_issues: List[str], 
                                    automation_gaps: List[str], load_time: float) -> int:
        """Calculate opportunity score (1-10)"""
        score = 0
        
        # Design issues (0-5 points)
        score += min(len(design_issues), 5)
        
        # Automation gaps (0-3 points)
        score += min(len(automation_gaps) // 2, 3)
        
        # Slow load time (0-2 points)
        if load_time > 5:
            score += 2
        elif load_time > 3:
            score += 1
        
        return min(score, 10)
    
    def _extract_owner_info(self, soup: BeautifulSoup, url: str, 
                           business_name: str) -> Dict:
        """Extract owner/decision maker information - Enhanced version"""
        owner_info = {
            'name': 'N/A',
            'email': 'N/A',
            'title': 'N/A'
        }
        
        try:
            base_url = url.rsplit('/', 1)[0] if '/' in url else url
            domain = urlparse(url).netloc.replace('www.', '')
            
            # 1. Search in main page first
            main_text = soup.get_text()
            main_html = str(soup)
            
            # 2. Try to find and scrape special pages
            pages_to_check = []
            
            # Find links to contact, about, legal pages
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                href = link.get('href', '').lower()
                link_text = link.get_text().lower()
                
                # Team/About pages (HIGH PRIORITY for decision makers)
                if any(x in href or x in link_text for x in ['equipo', 'team', 'nosotros', 'about', 'quienes', 'sobre-nosotros', 'nuestro-equipo']):
                    full_url = href if href.startswith('http') else f"{base_url}/{href.lstrip('/')}"
                    pages_to_check.append(('team', full_url))
                
                # Contact pages
                elif any(x in href or x in link_text for x in ['contacto', 'contact']):
                    full_url = href if href.startswith('http') else f"{base_url}/{href.lstrip('/')}"
                    pages_to_check.append(('contact', full_url))
                
                # Legal notice pages (very important for Spanish sites!)
                elif any(x in href or x in link_text for x in ['aviso-legal', 'aviso legal', 'legal', 'privacidad', 'privacy']):
                    full_url = href if href.startswith('http') else f"{base_url}/{href.lstrip('/')}"
                    pages_to_check.append(('legal', full_url))
            
            # Scrape additional pages (prioritize team pages, limit to 3)
            additional_texts = []
            # Sort to prioritize team pages first
            pages_to_check.sort(key=lambda x: 0 if x[0] == 'team' else 1 if x[0] == 'legal' else 2)
            for page_type, page_url in pages_to_check[:3]:
                try:
                    print(f"        📄 Revisando {page_type}: {page_url[:50]}...")
                    page_response = self.session.get(page_url, timeout=5)
                    page_soup = BeautifulSoup(page_response.text, 'html.parser')
                    additional_texts.append((page_type, page_soup.get_text(), str(page_soup)))
                except:
                    pass
            
            # Combine all texts for analysis
            all_texts = [(main_text, main_html)] + [(t, h) for _, t, h in additional_texts]
            
            # 3. Extract decision maker name with enhanced patterns
            name_patterns = [
                # High-level roles (Priority 1)
                r'(?:CEO|Fundador|Fundadora|Socio|Socia|Partner):\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+)',
                r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+),?\s+(?:CEO|Fundador|Fundadora|Socio|Socia|Partner)',
                
                # Directors and managers (Priority 2)
                r'(?:Director|Directora|Gerente|Director General|Directora General):\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+)',
                r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+),?\s+(?:Director|Directora|Gerente|Director General)',
                
                # Mid-level responsibility roles (Priority 3)
                r'(?:Responsable|Coordinador|Coordinadora|Jefe|Jefa):\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+)',
                r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+),?\s+(?:Responsable|Coordinador|Coordinadora)',
                
                # Legal sector specific
                r'(?:Abogado|Abogada|Letrado|Letrada):\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+)',
                r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+),?\s+(?:Abogado|Abogada|Letrado)',
                
                # Medical sector specific
                r'(?:Dr\.|Dra\.|Doctor|Doctora|Médico|Médica)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+)',
                r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+),?\s+(?:Dr\.|Dra\.|Médico|Médica)',
                
                # From legal notice (Aviso Legal) - ENHANCED
                r'(?:Titular|Administrador|Propietario|Propietaria):\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+)',
                r'(?:NIF|CIF|DNI).*?([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+)',
                
                # Email signature patterns
                r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+)\s*<[a-z0-9._%+-]+@',
            ]
            
            for text, html in all_texts:
                for pattern in name_patterns:
                    matches = re.findall(pattern, text)
                    if matches:
                        # Take first match that looks like a real name
                        for match in matches:
                            name = match.strip()
                            # Filter out common false positives and HTML artifacts
                            if len(name.split()) >= 2 and len(name) < 50:
                                # Reject if contains newlines or HTML-like patterns
                                if '\n' in name or '<' in name or '>' in name:
                                    continue
                                
                                # Reject names starting with articles or prepositions (not real names)
                                first_word = name.split()[0].lower()
                                if first_word in ['el', 'la', 'los', 'las', 'en', 'de', 'del', 'al', 'un', 'una', 'su', 'mi', 'tu']:
                                    continue
                                
                                # Reject common business/legal terms
                                if not any(x in name.lower() for x in ['bufete', 'abogados', 'despacho', 'sociedad', 'limitada', 's.l.', 's.a.', 'menú', 'menu', 'cerrar', 'inicio', 'seguridad', 'privacidad', 'legal', 'contacto']):
                                    owner_info['name'] = name
                                    
                                    # Extract title from context (expanded roles)
                                    context_start = max(0, text.find(name) - 100)
                                    context_end = min(len(text), text.find(name) + len(name) + 100)
                                    context = text[context_start:context_end]
                                    
                                    # Priority-based title extraction
                                    if 'ceo' in context.lower():
                                        owner_info['title'] = 'CEO'
                                    elif any(x in context.lower() for x in ['fundador', 'fundadora']):
                                        owner_info['title'] = 'Fundador'
                                    elif any(x in context.lower() for x in ['socio', 'socia', 'partner']):
                                        owner_info['title'] = 'Socio'
                                    elif any(x in context.lower() for x in ['director general', 'directora general']):
                                        owner_info['title'] = 'Director General'
                                    elif any(x in context.lower() for x in ['director', 'directora']):
                                        owner_info['title'] = 'Director'
                                    elif any(x in context.lower() for x in ['gerente']):
                                        owner_info['title'] = 'Gerente'
                                    elif any(x in context.lower() for x in ['responsable']):
                                        owner_info['title'] = 'Responsable'
                                    elif any(x in context.lower() for x in ['coordinador', 'coordinadora']):
                                        owner_info['title'] = 'Coordinador'
                                    elif any(x in context.lower() for x in ['dr.', 'dra.', 'doctor', 'doctora', 'médico', 'médica']):
                                        owner_info['title'] = 'Doctor'
                                    elif any(x in context.lower() for x in ['abogado', 'abogada', 'letrado']):
                                        owner_info['title'] = 'Abogado'
                                    elif any(x in context.lower() for x in ['propietario', 'propietaria', 'titular']):
                                        owner_info['title'] = 'Propietario'
                                    
                                    break
                    
                    if owner_info['name'] != 'N/A':
                        break
                
                if owner_info['name'] != 'N/A':
                    break
            
            # 4. Extract email with enhanced patterns
            email_patterns = [
                # Personal emails (name-based)
                rf'([a-z]+\.[a-z]+@{re.escape(domain)})',  # firstname.lastname@
                rf'([a-z]{{1,2}}[a-z]+@{re.escape(domain)})',  # initials + lastname@
                
                # Decision maker emails
                r'(?:socio|partner|director|gerente|ceo)@[a-z0-9.-]+\.[a-z]{2,}',
                
                # Any professional email
                r'([a-z][a-z0-9._-]+@[a-z0-9.-]+\.[a-z]{2,})',
            ]
            
            found_emails = []
            for text, html in all_texts:
                for pattern in email_patterns:
                    emails = re.findall(pattern, text.lower())
                    found_emails.extend(emails)
            
            # Remove duplicates
            found_emails = list(set(found_emails))
            
            # Prioritize emails
            if found_emails:
                # 1. Try to find email with decision maker keywords
                for email in found_emails:
                    if any(x in email for x in ['socio', 'partner', 'director', 'gerente', 'ceo', 'fundador']):
                        owner_info['email'] = email
                        break
                
                # 2. Try to find personal email (name.surname format)
                if owner_info['email'] == 'N/A':
                    for email in found_emails:
                        if '.' in email.split('@')[0]:  # Has dot in local part
                            if not any(x in email for x in ['info', 'contact', 'hello', 'support', 'admin', 'webmaster']):
                                owner_info['email'] = email
                                break
                
                # 3. Use any non-generic email
                if owner_info['email'] == 'N/A':
                    for email in found_emails:
                        if not any(x in email for x in ['info@', 'contact@', 'hello@', 'support@', 'admin@', 'webmaster@', 'noreply@']):
                            owner_info['email'] = email
                            break
            
            # 5. If we found a name but no email, try to construct one
            if owner_info['name'] != 'N/A' and owner_info['email'] == 'N/A':
                name_parts = owner_info['name'].lower().split()
                if len(name_parts) >= 2:
                    # Try common patterns
                    possible_emails = [
                        f"{name_parts[0]}.{name_parts[-1]}@{domain}",
                        f"{name_parts[0][0]}{name_parts[-1]}@{domain}",
                        f"{name_parts[0]}@{domain}",
                    ]
                    # We can't verify these, so we'll mark as "estimated"
                    owner_info['email'] = f"{possible_emails[0]} (estimado)"
            
        except Exception as e:
            print(f"      ⚠️  Error extrayendo info del decisor: {str(e)[:50]}")
        
        return owner_info


def parse_leads_file(file_path: Path) -> List[Dict]:
    """Parse leads from various file formats"""
    ext = file_path.suffix.lower()
    
    try:
        if ext == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Handle various JSON structures
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    if 'leads' in data and isinstance(data['leads'], list):
                        return data['leads']
                    elif 'results' in data and isinstance(data['results'], list):
                        return data['results']
                    else:
                        # Fallback: try to return the dict itself if it looks like a single lead
                        return [data]
                return []
        elif ext == '.csv':
            leads = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    leads.append(row)
            return leads
        else:
            print(f"⚠️  Formato {ext} no soportado directamente")
            print("   Convierte a JSON o CSV primero")
            return []
    except Exception as e:
        print(f"❌ Error al leer archivo {file_path}: {e}")
        return []


def save_results(leads: List[Dict], output_path: Path, format: str):
    """Save analyzed results"""
    
    if format == 'json':
        output_data = {
            'analyzed_at': datetime.now().isoformat(),
            'total_leads': len(leads),
            'leads': leads
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    elif format == 'csv':
        if not leads:
            return
        
        # Define all possible fields
        fieldnames = list(leads[0].keys())
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(leads)
    
    print(f"\n✓ Resultados guardados en: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze websites for pain points and opportunities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_pain_points.py --input .tmp/gmb_leads_enhanced_*.json
  python analyze_pain_points.py --input .tmp/leads.csv --output-format csv
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        required=True,
        help='Path to leads file (JSON or CSV)'
    )
    
    parser.add_argument(
        '--output-format', '-f',
        type=str,
        choices=['json', 'csv'],
        default='csv',
        help='Output format (default: csv)'
    )
    
    args = parser.parse_args()
    
    # Load leads
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"❌ Error: Archivo no encontrado: {input_path}")
        sys.exit(1)
    
    print(f"\n📄 Cargando leads desde: {input_path.name}")
    leads = parse_leads_file(input_path)
    
    if not leads:
        print("❌ Error: No se encontraron leads en el archivo")
        sys.exit(1)
    
    print(f"✓ Cargados {len(leads)} leads\n")
    
    # Setup output
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    tmp_dir = project_root / ".tmp"
    tmp_dir.mkdir(exist_ok=True)
    
    output_filename = f"leads_analyzed_{timestamp}.{args.output_format}"
    output_path = tmp_dir / output_filename
    
    print("=" * 80)
    print("ANÁLISIS DE PUNTOS DE DOLOR")
    print("=" * 80)
    print(f"Total Leads: {len(leads)}")
    print(f"Formato Salida: {args.output_format}")
    print(f"Archivo Salida: {output_path}")
    print("=" * 80 + "\n")
    
    # Initialize analyzer
    analyzer = WebsiteAnalyzer()
    
    # Analyze each lead
    analyzed_leads = []
    
    for i, lead in enumerate(leads, 1):
        print(f"[{i}/{len(leads)}] {lead.get('name', 'Unknown')}")
        
        # Analyze website
        website = lead.get('website', 'N/A')
        business_name = lead.get('name', '')
        
        analysis = analyzer.analyze_website(website, business_name)
        
        # Merge analysis with lead data
        lead.update({
            'pain_point': analysis['pain_point'],
            'pain_point_details': analysis['pain_point_details'],
            'proposed_solution': analysis['proposed_solution'],
            'opportunity_score': analysis['opportunity_score'],
            'owner_name': analysis['owner_name'],
            'owner_email': analysis['owner_email'],
            'owner_title': analysis['owner_title']
        })
        
        analyzed_leads.append(lead)
        
        # Small delay to avoid overwhelming servers
        time.sleep(1)
    
    # Sort by opportunity score
    analyzed_leads.sort(key=lambda x: x.get('opportunity_score', 0), reverse=True)
    
    # Save results
    save_results(analyzed_leads, output_path, args.output_format)
    
    # Print summary
    print("\n" + "=" * 80)
    print("RESUMEN DEL ANÁLISIS")
    print("=" * 80)
    
    # Count pain points
    pain_point_counts = {}
    for lead in analyzed_leads:
        pp = lead.get('pain_point', 'Unknown')
        pain_point_counts[pp] = pain_point_counts.get(pp, 0) + 1
    
    print(f"\nDistribución de Puntos de Dolor:")
    for pp, count in sorted(pain_point_counts.items(), key=lambda x: x[1], reverse=True):
        pct = (count / len(analyzed_leads)) * 100
        print(f"  {pp}: {count} leads ({pct:.0f}%)")
    
    # Top opportunities
    print(f"\nTop 5 Oportunidades (por score):")
    for i, lead in enumerate(analyzed_leads[:5], 1):
        print(f"  {i}. {lead.get('name')} - Score: {lead.get('opportunity_score')}/10")
        print(f"     Punto de dolor: {lead.get('pain_point')}")
        if lead.get('owner_name') != 'N/A':
            print(f"     Contacto: {lead.get('owner_name')} ({lead.get('owner_email')})")
    
    print(f"\n✓ Análisis completado: {len(analyzed_leads)} leads procesados")
    print(f"✓ Archivo guardado: {output_path}")
    print("=" * 80 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
