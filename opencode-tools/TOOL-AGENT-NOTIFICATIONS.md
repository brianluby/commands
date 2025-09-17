# 🔔 OpenCode Tool & Agent Notifications

## Current State: Transparent Operations

**OpenCode currently operates transparently** - it doesn't explicitly notify users when it's engaging specific tools or agents. This differs from Claude Code's explicit slash command system.

## Understanding OpenCode's Architecture

### **Does OpenCode Differentiate Between Commands and Agents?**

**Short Answer**: OpenCode operates as a **unified conversational assistant** rather than having explicit commands or separate agents.

**Detailed Explanation**:

```
Claude Code Architecture:
├── Commands (/api-scaffold, /security-scan)
├── Workflows (multi-agent orchestration)  
├── Subagents (backend-architect, security-expert)
└── Task tool for delegation

OpenCode Architecture:
├── Single conversational assistant
├── Tool capabilities (file operations, code analysis, execution)
├── Context-aware responses
└── No explicit agent delegation (tested - subagent calls don't create separate agents)
```

## How OpenCode Could Implement Tool Notifications

### **Option 1: Explicit Tool Engagement Notifications**

```markdown
You: "I need to secure my API before deployment"

OpenCode: "🛡️ **Engaging Security Auditor**
I'll analyze your FastAPI application for security vulnerabilities. Let me scan your codebase for:
- Authentication issues
- SQL injection risks  
- Dependency vulnerabilities
- Missing security headers

*[Security Auditor Active]*"
```

### **Option 2: Capability Indication**

```markdown
You: "Add user management to my app"

OpenCode: "🔧 **API Generator Mode**
I'll help you build user management features. Based on your FastAPI setup, I can create:
- User models and schemas
- Authentication endpoints
- Database migrations
- Security best practices

*[Using API development capabilities]*"
```

### **Option 3: Tool Switching Notifications**

```markdown
You: "Create user registration endpoint"
OpenCode: "🔧 *[API Generator]* Creating registration endpoint..."

You: "Make sure it's secure"  
OpenCode: "🛡️ *[Security Auditor]* Reviewing security implementation..."

You: "Add tests for this"
OpenCode: "🧪 *[Test Builder]* Generating comprehensive tests..."
```

## Proposed Implementation Patterns

### **1. Contextual Tool Headers**

```markdown
# For each response, OpenCode could include:
🔧 **API Generator** | Building user authentication system
🛡️ **Security Auditor** | Analyzing FastAPI application security  
🐳 **Container Optimizer** | Optimizing Docker configuration
☸️ **K8s Assistant** | Planning Kubernetes deployment
🧪 **Test Builder** | Creating comprehensive test suite
```

### **2. Capability Indicators**

```python
# OpenCode could indicate active capabilities:
class OpenCodeResponse:
    def __init__(self, user_request, context):
        self.active_tools = self.determine_tools(user_request, context)
        self.capabilities = self.get_capabilities()
        
    def format_response(self):
        header = f"🔧 {', '.join(self.active_tools)}"
        return f"{header}\n\n{self.response_content}"

# Example output:
# 🔧 API Generator, Security Auditor
# I'll create secure user management endpoints...
```

### **3. Tool Transition Notifications**

```markdown
You: "I need comprehensive security for my app"

OpenCode: 
**🛡️ Security Auditor Engaged**
Starting comprehensive security analysis...

*Transitioning to 🔧 API Generator*
Found authentication gaps - implementing secure auth system...

*Engaging 🐳 Container Optimizer*  
Detected Docker setup - reviewing container security...

**Summary**: Used Security Auditor → API Generator → Container Optimizer
```

## Benefits of Tool Notifications

### **✅ User Advantages**
- **Transparency**: Understand what capabilities are being used
- **Learning**: Discover tool capabilities through usage
- **Control**: Request specific tools or approaches  
- **Trust**: See the reasoning behind responses

### **✅ Development Advantages**
- **Debugging**: Understand which tools were engaged
- **Optimization**: See tool usage patterns
- **Training**: Learn how tools work together
- **Feedback**: Provide input on tool selection

## Implementation Approaches

### **Approach 1: Always Visible Notifications**
```markdown
🔧 **[API Generator]** 
I'll create a FastAPI user management system...

🛡️ **[Security Auditor]**
Reviewing the implementation for security issues...
```

**Pros**: Full transparency, educational
**Cons**: Potentially verbose, might interrupt flow

### **Approach 2: Optional Notifications**
```markdown
# User can toggle notifications
OpenCode Settings:
- Show tool notifications: ON/OFF
- Notification style: Headers/Badges/Minimal
- Tool transition alerts: ON/OFF
```

**Pros**: User control, customizable experience
**Cons**: Requires settings management

### **Approach 3: Context-Sensitive Notifications**
```markdown
# Show notifications only when:
- Multiple tools are used
- User asks "what are you doing?"
- Complex operations are performed
- User is learning/exploring
```

**Pros**: Clean experience, relevant notifications
**Cons**: Might miss important tool usage

## Current OpenCode Behavior Analysis

Based on testing and observation:

### **What OpenCode Currently Does**
```
✅ Responds conversationally without explicit tool mentions
✅ Uses available tools (file operations, code analysis, execution) transparently  
✅ Maintains conversation context across interactions
✅ Adapts responses based on detected project context
❌ Does not announce tool engagement
❌ Does not differentiate between different types of capabilities
❌ No explicit agent delegation (confirmed through testing)
```

### **How Tool Selection Currently Works**
```python
# Implicit tool selection based on:
user_intent = analyze_request("I need secure authentication")
project_context = detect_framework_and_setup()
capabilities_needed = match_intent_to_capabilities(user_intent)

# Results in contextual response without explicit tool announcement
response = generate_contextual_response(
    intent=user_intent,
    context=project_context,
    capabilities=capabilities_needed
)
```

## Recommendations for Enhanced Tool Awareness

### **1. Subtle Tool Indicators**
```markdown
🔧 I'll help you build secure user authentication for your FastAPI application...
```

### **2. Capability Breadcrumbs**
```markdown
*Building API endpoints → Adding security measures → Creating tests*
```

### **3. Summary Tool Usage**
```markdown
**Tools Used**: API Generator, Security Auditor, Test Builder
**Outcome**: Secure authentication system with comprehensive testing
```

### **4. On-Demand Tool Visibility**
```markdown
You: "What tools are you using?"
OpenCode: "I'm currently using:
- 🔧 API Generator for endpoint creation
- 🛡️ Security Auditor for vulnerability assessment  
- 🧪 Test Builder for comprehensive testing"
```

## Future Possibilities

### **Enhanced Tool Orchestration**
```markdown
You: "Make my app production-ready"

OpenCode: "I'll coordinate multiple tools for production readiness:

🛡️ Security Auditor: Vulnerability scan
🐳 Container Optimizer: Docker optimization  
☸️ K8s Assistant: Deployment configuration
📊 Monitor Setup: Observability stack

Would you like me to proceed with all tools or focus on specific areas?"
```

### **Tool Recommendation Engine**
```markdown
OpenCode: "Based on your request, I recommend:
- 🔧 API Generator (primary) - for building endpoints
- 🛡️ Security Auditor (supporting) - for security validation
- 🧪 Test Builder (optional) - for quality assurance

Proceed with recommended tools?"
```

This enhanced tool awareness would bridge the gap between OpenCode's transparent operation and users' desire to understand what capabilities are being engaged during their development conversations.