# 🛡️ Security Auditor
*OpenCode Native Tool - Conversational Security Analysis*

🔍 **Intelligent Scanning** | 🎯 **Context-Aware** | 🔧 **Interactive Remediation**

## What Makes This Different
This isn't a static security scanner. It **understands your codebase** and provides **conversational security guidance** tailored to your specific technology stack and business context.

## How to Use
Describe your security concerns in natural language:

### Conversation Starters
- "Check my API for security vulnerabilities"
- "I'm worried about SQL injection in my database queries"
- "Audit my authentication system for weaknesses"
- "Review my container setup for security issues"

### Example Conversation
**You**: "I want to make sure my API is secure before deployment"
**OpenCode**: "I'll scan your FastAPI application. I see you're using JWT authentication and PostgreSQL. Let me check for common vulnerabilities, review your dependency versions, and analyze your endpoints for security issues."

**You**: "I'm particularly concerned about data exposure"
**OpenCode**: "I found that your `/users` endpoint returns password hashes in the response. I also noticed some API keys in your environment variables. Should I help you implement response filtering and move those secrets to a secure key management system?"

**You**: "Yes, and check for any other data leaks"
**OpenCode**: "I'll scan all your endpoints for sensitive data exposure, check your logging for credential leakage, and review your error messages to ensure they don't reveal system information."

## Security Assessment Framework

### 1. Multi-Layered Security Analysis

#### OWASP Top 10 Coverage
**A01: Broken Access Control**
- Missing authentication on endpoints
- Insecure direct object references (IDOR)
- Privilege escalation vulnerabilities
- Cross-origin resource sharing (CORS) misconfigurations

**A02: Cryptographic Failures**
- Weak password hashing algorithms
- Insecure random number generation
- Missing encryption for sensitive data
- Weak TLS/SSL configurations

**A03: Injection Attacks**
- SQL injection vulnerabilities
- NoSQL injection patterns
- Command injection risks
- Cross-site scripting (XSS) vectors

### 2. Technology-Specific Scanning

#### Python/Django/Flask Security
```python
def scan_python_security():
    """Comprehensive Python application security scan"""
    
    security_checks = {
        'code_analysis': {
            'tools': ['bandit', 'semgrep'],
            'patterns': [
                'eval() usage detection',
                'subprocess shell=True warnings',
                'pickle deserialization risks',
                'hardcoded secrets detection'
            ]
        },
        'dependency_scan': {
            'tools': ['safety', 'pip-audit'],
            'databases': ['PyUp.io', 'OSV', 'CVE'],
            'checks': [
                'Known vulnerability detection',
                'License compliance analysis',
                'Outdated package identification'
            ]
        },
        'framework_specific': {
            'django': [
                'DEBUG=True in production',
                'SECRET_KEY exposure',
                'CSRF middleware configuration',
                'SQL injection via raw queries'
            ],
            'flask': [
                'Debug mode enabled',
                'Session security configuration',
                'Template injection via render_template_string',
                'Missing security headers'
            ]
        }
    }
    
    return security_checks
```

#### JavaScript/Node.js Security
```javascript
function scanJavaScriptSecurity() {
    const securityAnalysis = {
        staticAnalysis: {
            tools: ['eslint-plugin-security', 'semgrep'],
            vulnerabilities: [
                'eval() and new Function() usage',
                'Prototype pollution patterns',
                'Regular expression denial of service (ReDoS)',
                'Insecure randomness (Math.random())'
            ]
        },
        dependencyAudit: {
            tools: ['npm audit', 'yarn audit', 'snyk'],
            checks: [
                'Known CVE detection',
                'Malicious package identification',
                'License compatibility analysis',
                'Supply chain attack vectors'
            ]
        },
        frameworkChecks: {
            express: [
                'Missing helmet middleware',
                'CORS wildcard origins',
                'Insecure session configuration',
                'Missing rate limiting'
            ],
            react: [
                'dangerouslySetInnerHTML usage',
                'XSS in JSX expressions',
                'Insecure third-party components',
                'State injection vulnerabilities'
            ]
        }
    };
    
    return securityAnalysis;
}
```

#### Container Security Analysis
```yaml
# Container Security Assessment
container_security:
  base_image_analysis:
    - Vulnerability scanning with Trivy/Grype
    - Base image update recommendations
    - Known malware detection
    - Supply chain verification

  dockerfile_review:
    security_issues:
      - Running as root user
      - Copying sensitive files (.env, keys)
      - Using ADD instead of COPY
      - Missing health checks
      - Excessive privileges

  runtime_security:
    - Capability analysis
    - Seccomp profile validation
    - AppArmor/SELinux configuration
    - Resource limit enforcement

  secrets_management:
    - Environment variable exposure
    - Build-time secret leakage
    - Multi-stage build optimization
    - Secret mount best practices
```

### 3. Comprehensive Vulnerability Detection

#### Automated Scanning Engine
```python
class SecurityScanner:
    def __init__(self, project_path):
        self.project_path = project_path
        self.findings = []
        self.risk_score = 0
        
    def perform_comprehensive_scan(self):
        """Execute all security scans and compile results"""
        
        scan_results = {
            'secret_detection': self.scan_for_secrets(),
            'dependency_vulnerabilities': self.scan_dependencies(),
            'code_vulnerabilities': self.scan_code_patterns(),
            'configuration_issues': self.scan_configurations(),
            'container_security': self.scan_containers(),
            'api_security': self.scan_api_endpoints(),
            'authentication_issues': self.scan_auth_mechanisms()
        }
        
        self.generate_risk_assessment(scan_results)
        self.create_remediation_plan(scan_results)
        
        return scan_results
    
    def scan_for_secrets(self):
        """Multi-tool secret detection"""
        secret_patterns = {
            'api_keys': r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\'][^"\']{20,}["\']',
            'aws_credentials': r'AKIA[0-9A-Z]{16}',
            'jwt_tokens': r'eyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]+',
            'private_keys': r'-----BEGIN (RSA |EC )?PRIVATE KEY-----',
            'database_urls': r'(postgresql|mysql|mongodb)://[^:]+:[^@]+@[^/]+',
            'github_tokens': r'ghp_[0-9a-zA-Z]{36}',
            'slack_webhooks': r'https://hooks\.slack\.com/services/[A-Z0-9]{9}/[A-Z0-9]{9}/[a-zA-Z0-9]{24}'
        }
        
        findings = []
        for secret_type, pattern in secret_patterns.items():
            matches = self.scan_files_for_pattern(pattern)
            for match in matches:
                findings.append({
                    'type': secret_type,
                    'severity': 'CRITICAL',
                    'file': match['file'],
                    'line': match['line'],
                    'recommendation': f'Remove {secret_type} and use environment variables'
                })
        
        return findings
    
    def scan_dependencies(self):
        """Multi-ecosystem dependency vulnerability scanning"""
        vulnerabilities = []
        
        # Python dependencies
        if self.has_python_project():
            vulnerabilities.extend(self.scan_python_dependencies())
        
        # Node.js dependencies  
        if self.has_nodejs_project():
            vulnerabilities.extend(self.scan_nodejs_dependencies())
        
        # Container dependencies
        if self.has_dockerfile():
            vulnerabilities.extend(self.scan_container_dependencies())
        
        return vulnerabilities
    
    def generate_risk_assessment(self, scan_results):
        """Calculate overall security risk score"""
        severity_weights = {
            'CRITICAL': 10,
            'HIGH': 7,
            'MEDIUM': 4,
            'LOW': 1
        }
        
        total_score = 0
        for category, findings in scan_results.items():
            for finding in findings:
                severity = finding.get('severity', 'MEDIUM')
                total_score += severity_weights.get(severity, 1)
        
        # Normalize to 0-100 scale
        self.risk_score = min(100, (total_score / 50) * 100)
        
        return {
            'overall_risk': self.get_risk_level(self.risk_score),
            'score': self.risk_score,
            'total_findings': sum(len(findings) for findings in scan_results.values()),
            'critical_issues': sum(1 for findings in scan_results.values() 
                                 for finding in findings if finding.get('severity') == 'CRITICAL')
        }
    
    def create_remediation_plan(self, scan_results):
        """Generate prioritized remediation roadmap"""
        remediation_plan = {
            'immediate_actions': [],
            'short_term_fixes': [],
            'long_term_improvements': [],
            'automated_fixes': []
        }
        
        # Prioritize critical and high severity issues
        all_findings = []
        for category, findings in scan_results.items():
            all_findings.extend(findings)
        
        # Sort by severity
        critical_high = [f for f in all_findings if f.get('severity') in ['CRITICAL', 'HIGH']]
        medium_low = [f for f in all_findings if f.get('severity') in ['MEDIUM', 'LOW']]
        
        # Immediate actions for critical issues
        for finding in critical_high:
            if 'secret' in finding.get('type', '').lower():
                remediation_plan['immediate_actions'].append({
                    'action': f"Remove exposed {finding.get('type')} from {finding.get('file')}",
                    'priority': 'CRITICAL',
                    'effort': 'Low',
                    'impact': 'High'
                })
        
        return remediation_plan
```

### 4. Framework-Specific Security Patterns

#### API Security Assessment
```python
def assess_api_security():
    """Comprehensive API security evaluation"""
    
    api_security_checks = {
        'authentication': {
            'jwt_security': [
                'Weak signing secrets',
                'Missing token expiration', 
                'Algorithm confusion attacks',
                'Token storage in localStorage'
            ],
            'oauth_issues': [
                'Insufficient scope validation',
                'Missing PKCE implementation',
                'Redirect URI validation bypass',
                'State parameter vulnerabilities'
            ]
        },
        'authorization': {
            'access_control': [
                'Missing role-based checks',
                'Insecure direct object references',
                'Privilege escalation paths',
                'Resource-level permissions'
            ]
        },
        'input_validation': {
            'injection_risks': [
                'SQL injection vectors',
                'NoSQL injection patterns', 
                'Command injection points',
                'LDAP injection possibilities'
            ],
            'data_validation': [
                'Missing input sanitization',
                'Insufficient length limits',
                'File upload restrictions',
                'Content-type validation'
            ]
        },
        'rate_limiting': {
            'protection_levels': [
                'Global rate limits',
                'User-specific limits',
                'Endpoint-specific limits',
                'IP-based restrictions'
            ]
        }
    }
    
    return api_security_checks
```

#### Infrastructure Security
```yaml
# Infrastructure as Code Security
infrastructure_security:
  terraform_analysis:
    security_misconfigurations:
      - Unencrypted storage buckets
      - Overly permissive security groups
      - Missing encryption at rest
      - Weak password policies
      - Public database access
      
  kubernetes_security:
    pod_security:
      - Running as privileged
      - Missing security contexts
      - Excessive capabilities
      - Host network access
      
    rbac_analysis:
      - Overly broad permissions
      - Missing role bindings
      - Service account issues
      - Cluster admin usage
      
  cloud_configuration:
    aws_security:
      - S3 bucket public access
      - IAM policy violations
      - VPC security group rules
      - CloudTrail configuration
```

### 5. Advanced Threat Detection

#### Supply Chain Security
```python
def analyze_supply_chain_security():
    """Detect supply chain attacks and risks"""
    
    supply_chain_risks = {
        'dependency_confusion': {
            'detection': [
                'Internal package name conflicts',
                'Typosquatting package names',
                'Suspicious package maintainers',
                'Recent package ownership changes'
            ]
        },
        'malicious_packages': {
            'indicators': [
                'Unusual network connections',
                'File system modifications',
                'Cryptocurrency mining code',
                'Data exfiltration patterns'
            ]
        },
        'license_compliance': {
            'problematic_licenses': [
                'GPL in commercial projects',
                'AGPL restrictions',
                'Custom restrictive licenses',
                'Missing license information'
            ]
        }
    }
    
    return supply_chain_risks
```

### 6. Automated Remediation

#### Smart Fix Generation
```python
class SecurityRemediationEngine:
    def __init__(self):
        self.fix_templates = {
            'sql_injection': {
                'python': 'Use parameterized queries: cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))',
                'javascript': 'Use prepared statements: db.query("SELECT * FROM users WHERE id = ?", [userId])',
                'java': 'Use PreparedStatement: "SELECT * FROM users WHERE id = ?"'
            },
            'hardcoded_secrets': {
                'fix': 'Move to environment variables: os.environ.get("API_KEY")',
                'security_note': 'Rotate the exposed credential immediately'
            },
            'weak_hashing': {
                'python': 'Use bcrypt: bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())',
                'javascript': 'Use bcrypt: await bcrypt.hash(password, 12)',
                'java': 'Use BCryptPasswordEncoder from Spring Security'
            }
        }
    
    def generate_fix_recommendations(self, vulnerability):
        """Generate specific fix recommendations"""
        vuln_type = vulnerability.get('type')
        language = vulnerability.get('language', 'generic')
        
        if vuln_type in self.fix_templates:
            template = self.fix_templates[vuln_type]
            if language in template:
                return template[language]
            elif 'fix' in template:
                return template['fix']
        
        return "Manual review and remediation required"
    
    def create_security_headers_config(self, framework):
        """Generate security headers configuration"""
        
        configs = {
            'express': '''
// Express.js Security Headers
const helmet = require('helmet');

app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'"],
            styleSrc: ["'self'", "'unsafe-inline'"],
            imgSrc: ["'self'", "data:", "https:"],
            connectSrc: ["'self'"],
            fontSrc: ["'self'"],
            objectSrc: ["'none'"],
            mediaSrc: ["'self'"],
            frameSrc: ["'none'"]
        }
    },
    hsts: {
        maxAge: 31536000,
        includeSubDomains: true,
        preload: true
    }
}));
            ''',
            'flask': '''
# Flask Security Headers
from flask_talisman import Talisman

csp = {
    'default-src': "'self'",
    'script-src': "'self'",
    'style-src': "'self' 'unsafe-inline'",
    'img-src': "'self' data: https:",
    'connect-src': "'self'",
    'font-src': "'self'",
    'object-src': "'none'",
    'media-src': "'self'",
    'frame-src': "'none'"
}

Talisman(app, content_security_policy=csp)
            ''',
            'django': '''
# Django Security Settings
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# CSP Configuration
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_CONNECT_SRC = ("'self'",)
CSP_FONT_SRC = ("'self'",)
CSP_OBJECT_SRC = ("'none'",)
CSP_MEDIA_SRC = ("'self'",)
CSP_FRAME_SRC = ("'none'",)
            '''
        }
        
        return configs.get(framework, "Security headers configuration needed")
```

### 7. Security Monitoring Integration

#### Continuous Security Monitoring
```python
def setup_security_monitoring():
    """Configure ongoing security monitoring"""
    
    monitoring_config = {
        'dependency_monitoring': {
            'tools': ['Dependabot', 'Snyk', 'WhiteSource'],
            'frequency': 'Daily',
            'actions': [
                'Automated PR creation for updates',
                'Vulnerability notifications',
                'License compliance alerts'
            ]
        },
        'code_analysis': {
            'tools': ['SonarQube', 'CodeQL', 'Semgrep'],
            'triggers': ['Push to main', 'Pull requests'],
            'quality_gates': [
                'No critical vulnerabilities',
                'Security rating A or B',
                'Coverage > 80%'
            ]
        },
        'runtime_monitoring': {
            'security_events': [
                'Authentication failures',
                'Authorization violations', 
                'Unusual API usage patterns',
                'Failed security header checks'
            ],
            'alerting': [
                'Real-time SIEM integration',
                'Slack/Teams notifications',
                'Email alerts for critical issues'
            ]
        }
    }
    
    return monitoring_config
```

### 8. Compliance and Standards

#### Security Standards Compliance
```yaml
# Security Compliance Framework
compliance_standards:
  owasp_asvs:
    level_1: # Basic security requirements
      - V1: Architecture, Design and Threat Modeling
      - V2: Authentication
      - V3: Session Management
      - V4: Access Control
      - V5: Validation, Sanitization and Encoding
      
  iso_27001:
    security_controls:
      - Information security policies
      - Organization of information security  
      - Human resource security
      - Asset management
      - Access control
      - Cryptography
      
  nist_cybersecurity:
    framework_functions:
      - Identify: Asset management, risk assessment
      - Protect: Access control, data security
      - Detect: Security monitoring, detection processes
      - Respond: Incident response planning
      - Recover: Recovery planning, improvements
      
  pci_dss: # For payment processing
    requirements:
      - Install and maintain firewall configuration
      - Do not use vendor-supplied defaults
      - Protect stored cardholder data
      - Encrypt transmission of cardholder data
      - Use and regularly update anti-virus software
```

### 9. OpenCode Integration Features

#### Direct Conversation Security Analysis
- **Context-Aware Scanning**: Automatically detects project type and applies relevant security checks
- **Progressive Security Enhancement**: Starts with critical issues and progressively adds security layers
- **Framework-Specific Guidance**: Provides tailored security recommendations based on detected frameworks
- **Real-Time Risk Assessment**: Calculates and updates security risk scores as issues are found

#### Integration with Development Workflow
```python
def opencode_security_workflow():
    """Security integration patterns for OpenCode"""
    
    workflow_stages = {
        'development': {
            'pre_commit_hooks': [
                'Secret scanning with git hooks',
                'Linting with security rules',
                'Dependency vulnerability checks'
            ],
            'ide_integration': [
                'Real-time security hints',
                'Vulnerability highlighting',
                'Fix suggestions in context'
            ]
        },
        'testing': {
            'security_tests': [
                'Automated penetration testing',
                'API security testing',
                'Authentication flow testing'
            ]
        },
        'deployment': {
            'security_gates': [
                'Container image scanning', 
                'Infrastructure security validation',
                'Runtime security configuration'
            ]
        }
    }
    
    return workflow_stages
```

This OpenCode-adapted security scanner provides comprehensive vulnerability assessment while working within OpenCode's single-agent architecture, offering intelligent scanning, automated remediation suggestions, and progressive security enhancement through direct conversation.