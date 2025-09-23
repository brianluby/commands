# OpenCode vs Claude Code: Key Differentiators

## Core Architectural Differences

### 1. Execution Model
**Claude Code (Original)**
- Slash command system: `/api-scaffold user management API`
- `$ARGUMENTS` placeholder for user input
- Multi-subagent orchestration via Task tool
- Workflow-based approach with specialized subagents

**OpenCode (Adapted)**
- Direct conversational interface: "Create a FastAPI user management API"
- Context-aware parameter extraction from natural language
- Single-agent execution with progressive refinement
- Conversation-driven development with iterative enhancement

### 2. Command Structure
**Claude Code**
```markdown
# API Scaffold Generator
$ARGUMENTS

## Instructions
Use Task tool with subagent_type="backend-architect"...
```

**OpenCode**
```markdown
# API Scaffold Generator (OpenCode Version)
## Usage Pattern
Request through conversation: "Create a [framework] API for [description]"

## Direct Implementation
- Framework auto-detection from existing codebase
- Progressive conversation-based refinement
- Single-agent comprehensive implementation
```

### 3. User Interaction Paradigm
**Claude Code**: Command → Subagent → Result
**OpenCode**: Conversation → Context Analysis → Progressive Implementation

## Differentiation Strategy

### 1. Rename and Reorganize
```bash
# Current structure
tools/
├── api-scaffold.md              # Original Claude Code
├── api-scaffold-opencode.md     # OpenCode adaptation
├── security-scan.md             # Original Claude Code  
├── security-scan-opencode.md    # OpenCode adaptation

# Proposed structure
opencode-tools/
├── api-generator.md             # OpenCode native
├── security-auditor.md          # OpenCode native
├── container-optimizer.md       # OpenCode native
├── deployment-assistant.md      # OpenCode native
└── test-framework-builder.md    # OpenCode native

legacy-claude-tools/
├── api-scaffold.md              # Original preserved
├── security-scan.md             # Original preserved
└── ...                          # All originals preserved
```

### 2. Unique Value Propositions

#### OpenCode Advantages
**Interactive Development**
- Real-time conversation with context awareness
- Progressive feature building through dialogue
- Dynamic requirement refinement
- Immediate feedback and iteration

**Contextual Intelligence**
- Automatic framework detection from existing code
- Codebase-aware suggestions and implementations
- Integration with existing patterns and conventions
- Smart conflict resolution

**Simplified Workflow**
- No need to learn slash command syntax
- Natural language requirement specification
- Single conversation thread for complex implementations
- Reduced cognitive overhead

#### Example Differentiation
**Claude Code Approach:**
```bash
/api-scaffold "FastAPI user management with JWT auth"
# → Triggers backend-architect subagent
# → Generates complete implementation
# → Fixed template-based output
```

**OpenCode Approach:**
```
User: "I need a user management API for my FastAPI app"
OpenCode: "I see you have FastAPI already set up. Would you like me to add user registration, authentication, and profile management? I noticed you're using SQLAlchemy - should I integrate with your existing database setup?"
User: "Yes, and add password reset functionality"
OpenCode: "Perfect! I'll create the user management system with password reset. Since you mentioned JWT auth, I'll implement secure token-based authentication. Let me start with the models..."
```

### 3. Technical Differentiation

#### OpenCode-Specific Features
```python
# OpenCode: Context-aware framework detection
def detect_existing_stack():
    """Intelligently detect and integrate with existing codebase"""
    existing_config = analyze_project_structure()
    return {
        'framework': existing_config.framework,
        'database': existing_config.database,
        'auth_system': existing_config.auth_patterns,
        'testing_setup': existing_config.test_framework,
        'integration_points': existing_config.api_endpoints
    }

# OpenCode: Progressive conversation building
def progressive_feature_building(user_request, existing_code):
    """Build features incrementally through conversation"""
    return iterative_implementation(
        user_request, 
        context=existing_code,
        conversation_history=get_conversation_context()
    )
```

#### Claude Code Pattern (Original)
```python
# Claude Code: Fixed template execution
def execute_api_scaffold(arguments):
    """Execute predefined API scaffold with arguments"""
    task_delegation = Task(
        subagent_type="backend-architect",
        prompt=f"Create API with requirements: {arguments}"
    )
    return task_delegation.execute()
```

### 4. File Naming and Organization Strategy

#### New OpenCode Native Tools
```
opencode-tools/
├── api-generator.md             # vs api-scaffold.md
├── security-auditor.md          # vs security-scan.md  
├── container-optimizer.md       # vs docker-optimize.md
├── k8s-deployment-assistant.md  # vs k8s-manifest.md
├── test-framework-builder.md    # vs test-harness.md
├── database-migrator.md         # vs db-migrate.md
├── code-quality-analyzer.md     # vs refactor-clean.md
├── performance-optimizer.md     # vs performance-optimization.md
└── devops-assistant.md          # vs monitor-setup.md
```

#### Distinct Branding Elements
```markdown
# Each OpenCode tool includes:
🔧 **OpenCode Native Tool**
📝 **Conversational Interface**
🤖 **Context-Aware Implementation**
🔄 **Progressive Development**

## OpenCode Advantages
- Natural language interaction
- Existing codebase integration
- Real-time refinement
- Context-aware suggestions
```

### 5. Documentation Differentiation

#### OpenCode Documentation Style
```markdown
# API Generator (OpenCode)

## How to Use
Simply describe what you need:
- "Create a REST API for user management"
- "Add authentication to my existing FastAPI app"
- "Build a GraphQL API with TypeScript"

## Conversation Examples
**User**: "I need an API for my e-commerce app"
**OpenCode**: "I see you're using Express.js. Should I add product management, user accounts, and order processing? I can integrate with your existing Mongoose setup."

**User**: "Yes, and add payment integration"  
**OpenCode**: "Great! I'll add Stripe integration. Would you prefer checkout sessions or payment intents? I'll also add webhook handling for order status updates."
```

#### Claude Code Documentation Style (Original)
```markdown
# API Scaffold Generator

## Requirements
$ARGUMENTS

## Instructions
1. Analyze requirements
2. Use Task tool with subagent_type="backend-architect"
3. Generate complete API implementation
4. Provide deployment configuration
```

### 6. Implementation Strategy

#### Phase 1: Core Differentiation
1. **Rename all adapted tools** with OpenCode-specific names
2. **Create opencode-tools/ directory** for new implementations
3. **Preserve original tools** in legacy-claude-tools/ directory
4. **Add clear branding** to distinguish approaches

#### Phase 2: Enhanced Functionality
1. **Implement conversation-based interfaces**
2. **Add context-awareness features**
3. **Create progressive development workflows** 
4. **Build integration detection systems**

#### Phase 3: Documentation and Positioning
1. **Create comparison documentation**
2. **Highlight unique value propositions**
3. **Provide migration guides** from Claude Code to OpenCode approach
4. **Establish clear use case scenarios**

### 7. Positioning Statement

**Claude Code Commands**: "Production-ready slash commands for Claude Code with multi-subagent orchestration"

**OpenCode Tools**: "Conversational development assistants that integrate with your existing codebase through natural language interaction"

### 8. Marketing Differentiation

#### Claude Code (Original)
- **Target**: Claude Code users familiar with slash commands
- **Value**: Rapid template-based generation with specialist subagents
- **Use Case**: Starting new projects from scratch

#### OpenCode Tools (Adapted)
- **Target**: Developers using OpenCode/general AI assistants
- **Value**: Intelligent integration with existing codebases
- **Use Case**: Enhancing and extending existing projects

This differentiation strategy ensures OpenCode tools provide unique value while respecting the original Claude Code command patterns.