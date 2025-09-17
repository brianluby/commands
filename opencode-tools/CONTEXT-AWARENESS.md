# 🤖 How OpenCode Automatically Selects Tools

## The Magic Behind Conversational Development

OpenCode doesn't require you to specify which tool to use. Instead, it **intelligently analyzes your request and context** to automatically engage the right development assistant.

## Context Analysis Flow

### 1. **Natural Language Processing**
```
Your Request: "I need to secure my API before deployment"

OpenCode Analysis:
├── Intent: Security-focused task
├── Context: Existing API/application  
├── Goal: Pre-deployment security review
└── Tool Selection: Security Auditor
```

### 2. **Codebase Context Detection**
```python
# OpenCode automatically scans:
project_context = {
    'framework': 'FastAPI',           # From main.py, requirements.txt
    'database': 'PostgreSQL',        # From database imports
    'auth_system': 'JWT',            # From auth middleware
    'testing': 'pytest',             # From test files
    'deployment': 'Docker',          # From Dockerfile
}

# Tool selection based on context:
if 'security' in user_request and project_context['framework']:
    engage_tool = SecurityAuditor(context=project_context)
```

### 3. **Smart Tool Routing**

| Your Request | Detected Intent | Auto-Selected Tool | Why |
|-------------|----------------|-------------------|-----|
| "I need user authentication" | API Development | 🔧 API Generator | Building new functionality |
| "Check for vulnerabilities" | Security Analysis | 🛡️ Security Auditor | Security assessment needed |
| "Optimize my containers" | DevOps/Performance | 🐳 Container Optimizer | Infrastructure improvement |
| "Deploy to Kubernetes" | Deployment | ☸️ K8s Assistant | Deployment task |
| "Add comprehensive tests" | Quality Assurance | 🧪 Test Builder | Testing requirements |

## Comparison: Explicit vs Automatic Tool Selection

### **Claude Code: Explicit Selection**
```bash
# You must know and specify the tool:
/api-scaffold "user management with JWT auth"
/security-scan "check for SQL injection vulnerabilities"  
/docker-optimize "multi-stage build for Node.js app"
/k8s-manifest "production deployment with monitoring"

# Pros:
✅ Precise control over which tool runs
✅ Predictable, templated outputs
✅ Works well for known workflows

# Cons:
❌ Must memorize 52+ command names
❌ Need to know which tool does what
❌ Can't blend multiple tools in one conversation
❌ Fixed templates don't adapt to your specific context
```

### **OpenCode: Automatic Selection**
```
# Just describe what you need:
"I need secure user management for my FastAPI app"

OpenCode automatically:
🤖 Detects: API development + security requirements
🔧 Engages: API Generator with security focus
🛡️ Includes: Security best practices from Security Auditor
🎯 Adapts: To your existing FastAPI + PostgreSQL setup

# Pros:
✅ No commands to memorize
✅ Context-aware tool blending
✅ Adapts to your specific tech stack
✅ Natural conversation flow
✅ Can switch tools mid-conversation

# Cons:
❌ Less predictable outputs (more personalized)
❌ Requires more conversation to clarify requirements
```

## Advanced Context Awareness Examples

### **Multi-Tool Conversations**
```
You: "I'm launching my app next week and want to make sure it's production-ready"

OpenCode Analysis:
├── Multiple concerns detected:
│   ├── Security (pre-launch audit)
│   ├── Performance (production readiness)  
│   ├── Deployment (infrastructure)
│   └── Monitoring (observability)
│
└── Automatic tool orchestration:
    ├── 🛡️ Security Auditor: "Let me scan for vulnerabilities first"
    ├── 🐳 Container Optimizer: "I'll check your Docker setup"
    ├── ☸️ K8s Assistant: "Review your deployment configuration"
    └── 📊 Monitor Setup: "Add health checks and metrics"
```

### **Context-Driven Specialization**
```
Same Request, Different Contexts:

Request: "Add authentication to my app"

Context A - New Project:
🔧 API Generator: "I'll create a complete auth system with registration, login, and JWT tokens"

Context B - Existing Django App:
🔧 API Generator: "I see you have Django. I'll add DRF authentication that integrates with your existing User model"

Context C - Microservices:
🔧 API Generator: "I'll create an auth service that works with your existing microservices architecture"
```

### **Intelligent Tool Switching**
```
You: "Add user registration to my API"
🔧 API Generator: *Creates registration endpoint*

You: "Make sure this is secure"  
🛡️ Security Auditor: *Automatically takes over to review the auth implementation*

You: "Now help me deploy this"
☸️ K8s Assistant: *Seamlessly transitions to deployment planning*
```

## The Intelligence Behind Tool Selection

### **Pattern Recognition**
```python
class ContextAnalyzer:
    def analyze_request(self, user_input, project_context):
        # Intent detection
        intents = {
            'security': ['secure', 'vulnerability', 'audit', 'hack', 'protect'],
            'api_development': ['API', 'endpoint', 'authentication', 'CRUD'],
            'deployment': ['deploy', 'kubernetes', 'docker', 'production'],
            'testing': ['test', 'coverage', 'validation', 'QA'],
            'performance': ['optimize', 'speed', 'performance', 'scale']
        }
        
        # Context awareness
        if 'FastAPI' in project_context and 'API' in user_input:
            return ApiGenerator(framework='fastapi')
        elif 'security' in user_input.lower():
            return SecurityAuditor(context=project_context)
        elif 'docker' in project_context and 'optimize' in user_input:
            return ContainerOptimizer(existing_setup=project_context)
```

### **Dynamic Tool Blending**
```python
# OpenCode can blend multiple tools:
response = ToolOrchestrator.blend([
    ApiGenerator.create_auth_system(),
    SecurityAuditor.validate_implementation(),
    TestBuilder.generate_auth_tests()
])
```

## Benefits of Automatic Tool Selection

### **1. Reduced Cognitive Load**
- **No memorization**: Don't need to know 52+ command names
- **Natural language**: Describe what you need, not how to do it
- **Context retention**: OpenCode remembers your project setup

### **2. Intelligent Adaptation**
- **Tech stack aware**: Automatically uses your frameworks and patterns
- **Progressive enhancement**: Builds on existing code rather than replacing
- **Smart defaults**: Chooses secure, performant implementations

### **3. Seamless Workflow**
- **Tool transitions**: Smoothly move between development concerns
- **Conversational flow**: Natural back-and-forth refinement
- **Multi-domain support**: Handle complex requirements spanning multiple areas

### **4. Discovery and Learning**
- **Capability discovery**: Learn about tools through natural exploration
- **Best practices**: Automatic inclusion of security and performance considerations
- **Explanation on demand**: Ask "why" at any point to understand decisions

## When Automatic Selection Shines

### **✅ Perfect For:**
- **Exploratory development**: "I want to add social login"
- **Cross-cutting concerns**: "Make my app production-ready"
- **Learning new technologies**: "Help me add GraphQL to my REST API"
- **Complex requirements**: "Build a secure, scalable user system"

### **⚠️ Consider Explicit Tools When:**
- **Precise workflow control**: You know exactly which tool and template you need
- **Repeatable processes**: Running the same command across multiple projects
- **Team standardization**: Everyone needs identical outputs
- **Learning tool capabilities**: Understanding what each specific tool does

## The Future of Development Assistance

OpenCode's automatic tool selection represents a shift from **command-driven** to **conversation-driven** development:

```
Traditional: Human → Command → Tool → Output
OpenCode:    Human → Conversation → Context Analysis → Intelligent Tool Orchestration → Collaborative Building
```

This creates a more **intuitive, adaptive, and powerful** development experience where tools work together seamlessly based on your actual needs rather than rigid command structures.