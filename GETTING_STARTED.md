# Getting Started

A quick start guide to begin learning from this curriculum.

---

## 🚀 5-Minute Quick Start

### 1. **Understand the Structure**
- **7 Courses**: From engineering fundamentals to advanced system design
- **20+ Case Studies**: Real production architectures
- **8 Labs**: Hands-on projects with starter code and solutions
- **1 Capstone**: Build a complete production system

### 2. **Choose Your Path**

**Just starting out?**
→ Begin with [Course 01: Engineering Foundations](course-01-engineering-foundations/syllabus.md)

**Already have distributed systems background?**
→ Jump to [Course 02: Distributed Systems](course-02-distributed-systems/syllabus.md)

**Preparing for interviews?**
→ Study [System Design Exercises](course-07-advanced-system-design/exercises/system-design-exercises.md)

**Interested in a specific domain?**
→ Browse [all case studies](case-studies/) by category (messaging, search, streaming, ML, etc.)

### 3. **Access Key Resources**
- [README.md](README.md) — Overview and quick links
- [Curriculum Roadmap](curriculum-roadmap.md) — Detailed course descriptions
- [Glossary](GLOSSARY.md) — Look up technical terms
- [Resources](RESOURCES.md) — Recommended books, papers, tools

---

## 📖 Individual Course Structure

Each course follows this pattern:

```
course-NN-name/
├── syllabus.md              ← Read this first for course goals
├── lectures/                ← Theoretical foundations (where provided)
│   └── lecture-*.md
├── case-studies/            ← Real production examples
├── labs/                    ← Hands-on exercises
│   └── lab-name/
│       ├── README.md        ← Lab instructions
│       ├── starter-code/    ← Write your solution here
│       └── solution/        ← Reference solution
```

### How to Complete a Course

1. **Read the Syllabus** (15 min)
   - Understand learning objectives
   - Check prerequisites
   - Estimate time commitment

2. **Study Lectures** (where available) (2-3 hours)
   - Take notes on key concepts
   - Look up unfamiliar terms in [Glossary](GLOSSARY.md)
   - Pause and reflect on each topic

3. **Read Case Studies** (2-3 hours)
   - See real-world application of concepts
   - Note architectural decisions and trade-offs
   - Compare different approaches across case studies

4. **Complete Labs** (4-8 hours)
   - Read the lab README for context
   - Examine `starter-code/` and identify TODOs
   - Implement your solution **without peeking** at solution/
   - Compare with `solution/` and understand differences
   - (Optional) Extend solution with additional features

5. **Review & Reflect** (1 hour)
   - Summarize key learnings
   - Write 1-2 paragraph summary
   - Consider how concepts apply to your work

---

## 🔧 Lab Setup Guide

### Prerequisites
- **Programming**: Python 3.8+, basic Go or Java (depending on labs)
- **Tools**: Docker, Docker Compose, Git
- **Time**: 6-8 hours total per course

### Setup Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/modern-systems-engineering.git
cd modern-systems-engineering

# 2. Choose a course
cd course-02-distributed-systems/labs/chat-system

# 3. Install dependencies
pip install -r starter-code/requirements.txt

# 4. Start with starter code
cd starter-code
# Read the README and start implementing TODOs

# 5. Test your solution
# Run tests if available, or manually verify behavior

# 6. Compare with solution
cd ../solution
# Study how it's done and note differences
```

### Common Lab Commands

```bash
# View lab instructions
cat README.md

# See what you need to implement
grep -r "TODO" starter-code/

# Install Python dependencies
pip install -r requirements.txt

# Run Docker containers
docker compose up

# Build Docker image
docker build -t my-app:latest .

# Deploy to Kubernetes (some labs)
kubectl apply -f k8s/

# Test gRPC services
grpcurl -plaintext localhost:50051 ChatService.GetMessages
```

---

## 💡 Tips for Success

### 1. **Don't Skip the Fundamentals**
Even if you have experience, Course 01 and 02 provide essential context. Skip only if you're very confident.

### 2. **Complete Labs Yourself First**
Looking at solutions immediately defeats the purpose. Try for at least 30 minutes before peeking.

### 3. **Take Notes**
Write summaries of key concepts. This reinforces learning better than just reading.

### 4. **Discuss & Debate**
Find study partners or communities. Explaining concepts to others solidifies understanding.

### 5. **Connect to Your Work**
Relate curriculum concepts to systems you work on or use daily.

### 6. **Extend the Labs**
Don't stop at the provided solution. Add features, optimize, or adapt to different scenarios.

### 7. **Build the Capstone**
Don't skip this. The capstone integrates everything and creates a portfolio project.

---

## 📚 Recommended Reading Order

### Path 1: Complete & Structured (Best for Beginners)
```
Course 01 (4 weeks)
  ↓
Course 02 (5 weeks)
  ↓
Choose one of: Course 03, 04, 05, or 06 (3-4 weeks)
  ↓
Course 07 (4 weeks)
  ↓
Capstone (4-6 weeks)

Total: ~8-9 months / 340-400 hours
```

### Path 2: Accelerated (For Experienced Engineers)
```
Skip Course 01
  ↓
Course 02 (focus on lectures + selected case studies) (2 weeks)
  ↓
Course 07 System Design Exercises (2 weeks)
  ↓
Deep-dive case studies in your domain (2 weeks)
  ↓
Capstone in domain of interest (4 weeks)

Total: ~2-3 months / 120-160 hours
```

### Path 3: Interview Focused
```
Course 02 Distributed Systems Fundamentals (read lectures) (1 week)
  ↓
Course 07 System Design Exercises (solve all 5) (2 weeks)
  ↓
Practice with peers/mock interviews (2 weeks)
  ↓
Deep study of case studies in target domain (2 weeks)

Total: ~3-4 weeks / 80-120 hours
```

### Path 4: Domain Specialist
**Choose your domain** and focus deeply:

**Real-Time Systems**
- Course 05 Realtime Systems + labs
- Case Studies: Discord, Figma, WhatsApp
- Capstone: Global Chat Platform

**Machine Learning Systems**
- Course 04 AI Systems + labs
- Case Studies: NVIDIA, OpenAI, Spotify
- Capstone: AI Knowledge Platform

**Financial Systems**
- Course 06 Financial Systems + labs
- Case Studies: Stripe, Shopify
- Capstone: Payment Processing or Trading System

**Cloud Infrastructure**
- Course 03 Cloud Infrastructure + labs
- Case Studies: AWS, Cloudflare
- Capstone: Multi-region deployment

---

## ❓ Frequently Asked Questions

### Q: Do I need to complete all courses?
**A**: No! Choose based on your interests and background. However, Course 02 (Distributed Systems) is foundational for all others.

### Q: Can I skip some labs?
**A**: Not recommended. Labs provide hands-on experience that reading alone doesn't. They're essential for retention.

### Q: How long does each course take?
**A**: 3-5 weeks per course depending on depth. Estimate: reading + labs + capstone = 20-30 hours per course + 40-60 for capstone.

### Q: Do I need Docker/Kubernetes installed?
**A**: For most labs, yes. Some labs can run locally with Python/Go directly.

### Q: Can I do this part-time?
**A**: Absolutely. Many people do 5-10 hours/week. It'll take 6-12 months, but that's fine.

### Q: What programming languages are used?
**A**: Primarily Python and Go, with some YAML (Kubernetes, Docker) and SQL. Labs are designed to be adaptable to your preferred language.

### Q: How do I get help?
**A**: Check [Resources](RESOURCES.md) for communities. Also, search company engineering blogs (Netflix, Uber, Discord) for solutions to similar problems.

### Q: Should I build a capstone?
**A**: Yes. Capstone projects become portfolio pieces demonstrating your systems engineering knowledge.

### Q: Can I share my capstone publicly?
**A**: Yes! GitHub portfolios with systems design projects are highly valued by employers.

---

## 🎯 Success Criteria

You've successfully completed the curriculum when you can:

- [ ] **Explain** key distributed systems concepts (CAP, consensus, replication)
- [ ] **Design** scalable systems from first principles
- [ ] **Analyze** trade-offs in architectural decisions
- [ ] **Implement** key components (caches, queues, databases)
- [ ] **Diagnose** performance and reliability issues
- [ ] **Deploy** systems using cloud platforms or Kubernetes
- [ ] **Interview** confidently on system design topics

---

## 📝 Template: Document Your Learning

For each course, create a learning journal:

```markdown
# [Course Name] - My Learning Journal

## Key Concepts Learned
- Concept 1: [explanation]
- Concept 2: [explanation]
- ...

## Case Study Insights
- [Company/System]: [key insight]
- ...

## Lab Completion
- Lab 1: ✓ Completed, [key learnings]
- Lab 2: ✓ Completed, [key learnings]

## Reflection
[250 words on how this course changed your thinking about systems]

## Applied to Work
[How are you applying these concepts in your current role?]
```

---

## 🚀 Next Steps

1. **Pick a course** based on your experience level
2. **Read the syllabus** for that course
3. **Schedule time** (recommend 6-8 hours/week)
4. **Start with lectures** if foundational, or case studies if experienced
5. **Complete labs** for hands-on practice
6. **Join communities** (Discord, communities, Reddit) for discussion
7. **Build capstone** to integrate and showcase learning

---

## 📞 Support & Community

- **Questions about content?** Check [Glossary](GLOSSARY.md) or [Resources](RESOURCES.md)
- **Stuck on a lab?** Review the solution and compare approaches
- **Want to discuss?** Find systems engineering communities (Reddit r/cscareerquestions, Discord servers, etc.)
- **Working on capstone?** Share progress and get feedback

---

**Ready to begin?** Start with [README.md](README.md) for course overview, then pick [Course 01](course-01-engineering-foundations/syllabus.md) or your domain of interest.

Good luck! 🚀
