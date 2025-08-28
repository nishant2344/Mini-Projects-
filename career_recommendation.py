import math
import json
from dataclasses import dataclass
from typing import Dict, List, Tuple

# ---------- Data Models ----------
TraitVec = Dict[str, float]

@dataclass
class Career:
    id: str
    title: str
    traits: TraitVec
    skills: List[str]
    education_path: str
    typical_salary_range: Tuple[int, int]
    work_modes: List[str]
    industries: List[str]

# ---------- Knowledge Base (15 careers) ----------
CAREERS: List[Career] = [
    Career("se", "Software Engineer",
           {"collaboration":0.6,"creativity":0.5,"analysis":0.8,"empathy":0.3,"tech":1.0,"variety":0.7,"risk":0.5,"physical":0.1,"leadership":0.4,"stability":0.6,"worklife":0.7},
           ["python","algorithms","git","databases","problem-solving","apis","testing"], "medium", (900000,3500000),
           ["remote","hybrid","on-site"], ["software","fintech","saas","technology"]),
    Career("ux", "UX Designer",
           {"collaboration":0.7,"creativity":0.8,"analysis":0.5,"empathy":0.8,"tech":0.5,"variety":0.7,"risk":0.3,"physical":0.1,"leadership":0.3,"stability":0.5,"worklife":0.7},
           ["wireframing","research","figma","usability testing","prototyping","information architecture"], "medium", (800000,2500000),
           ["hybrid","remote","on-site"], ["software","product","agency","design"]),
    Career("da", "Data Analyst",
           {"collaboration":0.6,"creativity":0.4,"analysis":0.8,"empathy":0.4,"tech":0.7,"variety":0.6,"risk":0.4,"physical":0.1,"leadership":0.3,"stability":0.7,"worklife":0.8},
           ["sql","excel","data visualization","python","statistics","dashboarding"], "short", (700000,2200000),
           ["hybrid","remote","on-site"], ["software","retail","operations","analytics"]),
    Career("pm", "Product Manager",
           {"collaboration":0.9,"creativity":0.6,"analysis":0.7,"empathy":0.7,"tech":0.6,"variety":0.8,"risk":0.6,"physical":0.1,"leadership":0.8,"stability":0.6,"worklife":0.6},
           ["roadmapping","research","analytics","communication","strategy","prioritization"], "medium", (1200000,4000000),
           ["hybrid","on-site","remote"], ["software","consumer","b2b","technology"]),
    Career("rn", "Registered Nurse",
           {"collaboration":0.8,"creativity":0.3,"analysis":0.6,"empathy":0.9,"tech":0.4,"variety":0.6,"risk":0.5,"physical":0.7,"leadership":0.4,"stability":0.8,"worklife":0.4},
           ["patient care","triage","documentation","medical knowledge","infection control"], "long", (500000,1500000),
           ["on-site"], ["healthcare"]),
    Career("coach", "Sports Coach",
           {"collaboration":0.8,"creativity":0.5,"analysis":0.5,"empathy":0.8,"tech":0.3,"variety":0.7,"risk":0.4,"physical":0.9,"leadership":0.7,"stability":0.5,"worklife":0.6},
           ["training","motivation","fitness","sports tactics","nutrition basics"], "medium", (400000,1200000),
           ["on-site"], ["sports","education"]),
    Career("army", "Army Officer",
           {"collaboration":0.9,"creativity":0.4,"analysis":0.6,"empathy":0.6,"tech":0.5,"variety":0.8,"risk":0.9,"physical":1.0,"leadership":0.9,"stability":0.7,"worklife":0.4},
           ["leadership","discipline","strategy","combat","operations"], "medium", (600000,1500000),
           ["on-site"], ["defense","security"]),
    Career("civil", "Civil Services Officer",
           {"collaboration":0.8,"creativity":0.5,"analysis":0.7,"empathy":0.8,"tech":0.4,"variety":0.7,"risk":0.6,"physical":0.4,"leadership":0.8,"stability":0.9,"worklife":0.5},
           ["policy","administration","decision-making","law","public speaking"], "long", (800000,2000000),
           ["on-site"], ["public sector","administration","governance"]),
    Career("teacher", "School Teacher",
           {"collaboration":0.8,"creativity":0.7,"analysis":0.6,"empathy":0.9,"tech":0.5,"variety":0.6,"risk":0.3,"physical":0.3,"leadership":0.5,"stability":0.8,"worklife":0.8},
           ["teaching","communication","curriculum planning","classroom management","assessment"], "medium", (300000,800000),
           ["on-site"], ["education"]),
    Career("doctor", "Doctor",
           {"collaboration":0.7,"creativity":0.4,"analysis":0.8,"empathy":0.9,"tech":0.6,"variety":0.7,"risk":0.6,"physical":0.6,"leadership":0.5,"stability":0.9,"worklife":0.4},
           ["diagnosis","patient care","medical research","clinical procedures"], "long", (1000000,4000000),
           ["on-site"], ["healthcare","research"]),
    Career("lawyer", "Lawyer",
           {"collaboration":0.7,"creativity":0.5,"analysis":0.8,"empathy":0.6,"tech":0.4,"variety":0.6,"risk":0.5,"physical":0.2,"leadership":0.7,"stability":0.8,"worklife":0.5},
           ["legal research","negotiation","drafting","advocacy","client counseling"], "long", (800000,3000000),
           ["on-site","hybrid"], ["law","corporate","litigation"]),
    Career("pilot", "Pilot",
           {"collaboration":0.8,"creativity":0.3,"analysis":0.7,"empathy":0.4,"tech":0.8,"variety":0.8,"risk":0.8,"physical":0.7,"leadership":0.6,"stability":0.6,"worklife":0.4},
           ["navigation","aerodynamics","communication","emergency handling","checklists"], "long", (1200000,5000000),
           ["on-site"], ["aviation","transportation"]),
    Career("artist", "Artist",
           {"collaboration":0.5,"creativity":1.0,"analysis":0.3,"empathy":0.6,"tech":0.3,"variety":0.9,"risk":0.6,"physical":0.4,"leadership":0.4,"stability":0.3,"worklife":0.7},
           ["painting","illustration","concept design","visual storytelling","portfolio"], "medium", (300000,1500000),
           ["remote","on-site","hybrid"], ["media","entertainment","art"]),
    Career("entrepreneur", "Entrepreneur",
           {"collaboration":0.9,"creativity":0.8,"analysis":0.7,"empathy":0.6,"tech":0.6,"variety":1.0,"risk":1.0,"physical":0.3,"leadership":1.0,"stability":0.3,"worklife":0.3},
           ["business strategy","fundraising","networking","product design","sales"], "medium", (0,10000000),
           ["hybrid","on-site"], ["startups","business","technology"]),
    Career("ds", "Data Scientist",
           {"collaboration":0.6,"creativity":0.6,"analysis":1.0,"empathy":0.4,"tech":0.9,"variety":0.7,"risk":0.5,"physical":0.1,"leadership":0.4,"stability":0.6,"worklife":0.7},
           ["python","machine learning","statistics","data wrangling","modeling","communication"], "long", (1200000,4500000),
           ["remote","hybrid","on-site"], ["software","analytics","technology","research"])
]

# ---------- Career Guides (start -> intermediate -> expert) ----------
CAREER_GUIDES = {
    "se": {
        "start": [
            "Learn programming basics (Python/Java/C++).",
            "Study algorithms & data structures.",
            "Build small scripts and practice on LeetCode/HackerRank."
        ],
        "intermediate": [
            "Create 2–3 projects (APIs, web apps).",
            "Learn Git, SQL/NoSQL, testing and CI.",
            "Contribute to open source; prep system design fundamentals."
        ],
        "expert": [
            "Specialize (cloud, backend, mobile, AI).",
            "Lead projects or mentor others.",
            "Architect scalable systems and performance tune."
        ]
    },
    "ux": {
        "start": [
            "Study UX principles, HCI basics.",
            "Learn Figma; redesign an app as practice.",
            "Run simple user interviews with friends/peers."
        ],
        "intermediate": [
            "Build a portfolio (3–5 case studies).",
            "Master usability testing and IA.",
            "Collaborate with devs to ship a feature."
        ],
        "expert": [
            "Specialize (research, design systems).",
            "Lead UX strategy or manage a design team.",
            "Drive metrics with A/B experiments."
        ]
    },
    "da": {
        "start": [
            "Learn Excel, SQL and basic charts.",
            "Take an intro statistics course.",
            "Recreate dashboards from public datasets."
        ],
        "intermediate": [
            "Automate with Python (pandas) and build dashboards.",
            "Model with A/B testing, cohort, funnel analysis.",
            "Create a portfolio site with 3 business case studies."
        ],
        "expert": [
            "Own company metrics and stakeholder reporting.",
            "Optimize pipelines; introduce experimentation platforms.",
            "Mentor analysts; align with business strategy."
        ]
    },
    "pm": {
        "start": [
            "Learn product discovery and user stories.",
            "Shadow engineers/designers; study agile basics.",
            "Practice writing PRDs for mock products."
        ],
        "intermediate": [
            "Ship features end-to-end; track metrics.",
            "Run discovery interviews and prioritize roadmap.",
            "Collaborate cross-functionally (design, eng, marketing)."
        ],
        "expert": [
            "Lead multi-team programs or platform areas.",
            "Own P&L; drive north-star metrics.",
            "Coach PMs; influence org strategy."
        ]
    },
    "rn": {
        "start": [
            "Study biology & first-aid; volunteer at clinics.",
            "Understand basic patient care & hygiene protocols.",
            "Research nursing programs and licensure."
        ],
        "intermediate": [
            "Complete BSc Nursing or equivalent.",
            "Intern in hospital departments; practice documentation.",
            "Earn specialty certifications (ICU, ER)."
        ],
        "expert": [
            "Become Nurse Practitioner or Nurse Educator.",
            "Lead units; develop protocols and training.",
            "Contribute to research or policy."
        ]
    },
    "coach": {
        "start": [
            "Learn training principles and sports rules.",
            "Get basic fitness & first-aid certifications.",
            "Assist a local team or academy."
        ],
        "intermediate": [
            "Design training plans; track athlete progress.",
            "Study nutrition and sports psychology.",
            "Earn sport-specific coaching credentials."
        ],
        "expert": [
            "Coach at state/national level.",
            "Specialize in youth, performance, or rehab.",
            "Run your own academy/program."
        ]
    },
    "army": {
        "start": [
            "Focus on fitness, discipline, and leadership.",
            "Prepare for entrance exams & SSB interviews.",
            "Learn basics of navigation and field craft."
        ],
        "intermediate": [
            "Complete academy training; master tactics.",
            "Lead squads; learn operations planning.",
            "Cross-train in logistics/engineering/signals as relevant."
        ],
        "expert": [
            "Command larger units and specialized ops.",
            "Pursue staff college & advanced leadership.",
            "Move into strategy, training, or diplomacy roles."
        ]
    },
    "civil": {
        "start": [
            "Study polity, economy, history, geography basics.",
            "Build reading & writing practice for essays.",
            "Mock tests for prelims & mains."
        ],
        "intermediate": [
            "Clear exam; join service training.",
            "Learn administration, law, budgeting on the job.",
            "Drive local development and governance projects."
        ],
        "expert": [
            "Lead departments/districts; policy formulation.",
            "Central postings and inter-ministerial coordination.",
            "Pursue fellowships or international assignments."
        ]
    },
    "teacher": {
        "start": [
            "Pick a subject and strengthen fundamentals.",
            "Practice lesson planning and classroom delivery.",
            "Volunteer/tutor to gain experience."
        ],
        "intermediate": [
            "Get B.Ed or relevant credential.",
            "Develop assessments; manage classrooms.",
            "Integrate tech: LMS, digital content."
        ],
        "expert": [
            "Head of department or academic coordinator.",
            "Design curricula or ed-tech content.",
            "Mentor teachers; education leadership."
        ]
    },
    "doctor": {
        "start": [
            "Focus on biology & chemistry; shadow clinicians.",
            "Volunteer at hospitals/health camps.",
            "Prepare for medical entrance exams."
        ],
        "intermediate": [
            "Complete MBBS and internship.",
            "Choose specialization; begin residency.",
            "Publish case reports or research."
        ],
        "expert": [
            "Pursue MD/MS or super-specialization.",
            "Lead departments or run a clinic.",
            "Advance research; teach in academia."
        ]
    },
    "lawyer": {
        "start": [
            "Develop strong reading, writing, public speaking.",
            "Study basic law (contracts, torts, crim).",
            "Join moot courts or legal aid clinics."
        ],
        "intermediate": [
            "Earn LLB/JD; intern with firms/courts.",
            "Draft contracts; assist in filings & research.",
            "Pick a track (corp, litigation, IP)."
        ],
        "expert": [
            "Lead cases; become senior counsel/partner.",
            "Specialize (M&A, arbitration, constitutional).",
            "Build a practice or teach law."
        ]
    },
    "pilot": {
        "start": [
            "Understand aviation basics and safety culture.",
            "Begin ground school; prepare for aptitude tests.",
            "Maintain fitness and medical standards."
        ],
        "intermediate": [
            "Obtain PPL then CPL; accumulate flight hours.",
            "Type rating and simulator training.",
            "Build radio/ATC communication skills."
        ],
        "expert": [
            "First Officer → Captain progression.",
            "Instructor or examiner credentials.",
            "Move to wide-body/international operations."
        ]
    },
    "artist": {
        "start": [
            "Practice drawing/painting daily; learn fundamentals.",
            "Study composition, color, perspective.",
            "Start a portfolio on Behance/ArtStation."
        ],
        "intermediate": [
            "Pick a niche (illustration, concept, 3D).",
            "Take commissions; collaborate with studios.",
            "Learn digital tools (Photoshop/Procreate/3D)."
        ],
        "expert": [
            "Exhibit work; license art.",
            "Lead art direction or run a studio.",
            "Teach workshops or publish tutorials."
        ]
    },
    "entrepreneur": {
        "start": [
            "Identify problems; validate with interviews.",
            "Build MVPs quickly; learn basic finance.",
            "Join a startup community/accelerator."
        ],
        "intermediate": [
            "Find product-market fit; iterate from feedback.",
            "Fundraising or bootstrapping; hire first team.",
            "Establish sales/marketing channels."
        ],
        "expert": [
            "Scale operations; OKRs and dashboards.",
            "Expand to new markets or products.",
            "Mentor founders; consider angel investing."
        ]
    },
    "ds": {
        "start": [
            "Master Python, statistics, and linear algebra.",
            "Recreate classic analyses on public datasets.",
            "Learn pandas, matplotlib, and scikit-learn."
        ],
        "intermediate": [
            "Ship ML projects end-to-end.",
            "Learn model evaluation, feature engineering, MLOps basics.",
            "Publish notebooks/portfolios with real impact."
        ],
        "expert": [
            "Deploy large-scale ML; optimize cost/latency.",
            "Research or specialize (NLP, CV, RecSys).",
            "Lead data teams; set modeling standards."
        ]
    }
}

# ---------- Questionnaire ----------
QUESTIONS = [
    ("Preferred work style", {"solo":{"collaboration":0.3},"team":{"collaboration":0.8},"mixed":{"collaboration":0.6}}),
    ("Problem types you enjoy", {"people":{"empathy":0.8},"numbers":{"analysis":0.8},"creative":{"creativity":0.8},"hands-on":{"physical":0.6},"systems":{"analysis":0.7,"tech":0.7}}),
    ("Risk appetite", {"low":{"risk":0.3},"medium":{"risk":0.5},"high":{"risk":0.8}}),
    ("Variety vs routine", {"routine":{"variety":0.3},"balanced":{"variety":0.5},"variety":{"variety":0.8}}),
    ("Communication comfort", {"writing":{"empathy":0.5},"speaking":{"collaboration":0.7},"visual":{"creativity":0.6},"minimal":{}}),
    ("Analytical depth you enjoy", {"light":{"analysis":0.4},"moderate":{"analysis":0.6},"deep":{"analysis":0.85}}),
    ("Tech comfort", {"low":{"tech":0.3},"medium":{"tech":0.6},"high":{"tech":0.9}}),
    ("Empathy-heavy work interest", {"low":{"empathy":0.3},"medium":{"empathy":0.6},"high":{"empathy":0.85}}),
    ("Creativity emphasis", {"low":{"creativity":0.3},"medium":{"creativity":0.6},"high":{"creativity":0.85}}),
    ("Work-life balance importance", {"low":{"worklife":0.3},"medium":{"worklife":0.6},"high":{"worklife":0.9}}),
    ("Leadership preference", {"individual":{"leadership":0.3},"some":{"leadership":0.6},"high":{"leadership":0.9}}),
    ("Stability vs growth", {"stability":{"stability":0.9},"balanced":{"stability":0.6},"growth":{"stability":0.3}})
]

INDUSTRY_OPTIONS = [
    "software","finance","design","education","healthcare","public sector","retail",
    "manufacturing","consumer","b2b","operations","fintech","saas","product",
    "sports","defense","security","administration","aviation","transportation",
    "law","media","art","startups","technology","analytics","research","governance"
]
EDU_ORDER = {"short":0,"medium":1,"long":2}

# ---------- Helpers ----------
def cosine(a: TraitVec, b: TraitVec) -> float:
    keys = set(a) | set(b)
    num = sum(a.get(k,0.0)*b.get(k,0.0) for k in keys)
    da = math.sqrt(sum(a.get(k,0.0)**2 for k in keys))
    db = math.sqrt(sum(b.get(k,0.0)**2 for k in keys))
    return 0.0 if da==0 or db==0 else num/(da*db)

def jaccard(A: List[str], B: List[str]) -> float:
    sa, sb = set(map(str.lower, A)), set(map(str.lower, B))
    return 0.0 if not (sa or sb) else (len(sa & sb) / len(sa | sb))

def top_trait_alignments(user_traits: TraitVec, ctraits: TraitVec, k: int = 3) -> List[Tuple[str, float]]:
    # Score contribution by product of user and career trait weights
    keys = set(user_traits) | set(ctraits)
    pairs = [(t, user_traits.get(t,0.0) * ctraits.get(t,0.0)) for t in keys]
    pairs.sort(key=lambda x: x[1], reverse=True)
    return [(t, round(v,3)) for t, v in pairs[:k] if v > 0]

def score_career(user_traits: TraitVec, interests: List[str], user_skills: List[str], constraints: dict, c: Career):
    base = cosine(user_traits, c.traits)                 # traits similarity
    interest = 0.05 * jaccard(interests, c.industries)   # industry alignment
    skill_score = 0.15 * jaccard(user_skills, c.skills)  # skill alignment (strong)
    mode_bonus = 0.05 if constraints.get("remote") in c.work_modes else 0.0

    umin, umax = constraints.get("salary_min", 0), constraints.get("salary_max", 10**9)
    cmin, cmax = c.typical_salary_range
    overlap = max(0, min(umax, cmax) - max(umin, cmin))
    salary_fit = 0.05 if overlap > 0 else (-0.05 if cmax < umin else 0.0)

    edu_user = EDU_ORDER[constraints.get("education_horizon", "medium")]
    edu_career = EDU_ORDER[c.education_path]
    education_fit = 0.03 if edu_career <= edu_user else -0.03

    total = base + interest + skill_score + mode_bonus + salary_fit + education_fit
    breakdown = {
        "traits": round(base, 3),
        "skills": round(skill_score, 3),
        "interests": round(interest, 3),
        "mode": mode_bonus,
        "salary": salary_fit,
        "education": education_fit
    }
    why_traits = top_trait_alignments(user_traits, c.traits, 3)
    overlapping_skills = sorted(set(s for s in user_skills if s.lower() in [x.lower() for x in c.skills]))
    return total, breakdown, why_traits, overlapping_skills

def ask(options: List[str]) -> str:
    opts = [o.lower() for o in options]
    while True:
        ans = input(f"Choose {options}: ").strip().lower()
        if ans in opts:
            return ans
        print("Invalid choice. Try again.")

# ---------- CLI ----------
def run_cli():
    print("\n=== Career Recommender ===\n")
    user_traits = {k:0.0 for k in ["collaboration","creativity","analysis","empathy","tech","variety","risk","physical","leadership","stability","worklife"]}

    for q, mapping in QUESTIONS:
        print(f"{q} -> {list(mapping.keys())}")
        ans = ask(list(mapping.keys()))
        for k, v in mapping[ans].items():
            user_traits[k] = max(user_traits.get(k, 0.0), v)

    print("\nEnter up to 3 industries of interest (comma-separated). Options:")
    print(", ".join(INDUSTRY_OPTIONS))
    interests = [s.strip() for s in input("Your choices: ").strip().lower().split(",") if s.strip()][:3]

    print("\nEnter your top 5 skills (comma-separated):")
    user_skills = [s.strip().lower() for s in input("Skills: ").strip().split(",") if s.strip()][:5]

    print("\nEducation horizon options: short, medium, long")
    education_horizon = ask(["short","medium","long"])

    print("Preferred work mode: on-site / hybrid / remote")
    remote = ask(["on-site","hybrid","remote"])

    print("Desired salary range (annual, in ₹). Example: 800000-2000000")
    try:
        s = input("Range: ").strip()
        salary_min, salary_max = [int(x) for x in s.split("-")]
    except Exception:
        salary_min, salary_max = 0, 10**9

    constraints = {
        "education_horizon": education_horizon,
        "remote": remote,
        "salary_min": salary_min,
        "salary_max": salary_max
    }

    # Score all careers
    results = []
    for c in CAREERS:
        total, breakdown, why_traits, overlap_skills = score_career(user_traits, interests, user_skills, constraints, c)
        results.append((total, c, breakdown, why_traits, overlap_skills))

    results.sort(key=lambda t: t[0], reverse=True)

    # Show Top 5 summary
    print("\nTop Matches:\n")
    for rank, (total, c, br, _, _) in enumerate(results[:5], start=1):
        print(f"{rank}. {c.title} — score {total:.3f}")
        print(f"   Breakdown: traits={br['traits']}, skills={br['skills']}, interests={br['interests']}, mode={br['mode']}, salary={br['salary']}, education={br['education']}")
        print(f"   Skills needed: {', '.join(c.skills)}")
        print(f"   Work modes: {', '.join(c.work_modes)} | Education: {c.education_path} | Industries: {', '.join(c.industries)}\n")

    # Detailed Guides for Top 3
    print("=== Deep Dive: Your Top 3 Career Guides ===\n")
    for total, c, br, why_traits, overlap_skills in results[:3]:
        print(f">>> {c.title} (score {total:.3f})")
        # Why fit
        top_traits_str = ", ".join([f"{t}({v})" for t, v in why_traits]) or "—"
        overlap_skills_str = ", ".join(overlap_skills) or "—"
        print(f"Why you fit: top aligned traits → {top_traits_str}; overlapping skills → {overlap_skills_str}")
        # Guide
        guide = CAREER_GUIDES.get(c.id, None)
        if guide:
            print("How to start:")
            for step in guide["start"]: print(f"  - {step}")
            print("Grow to intermediate:")
            for step in guide["intermediate"]: print(f"  - {step}")
            print("Reach expert level:")
            for step in guide["expert"]: print(f"  - {step}")
        else:
            print("Guide not available yet. (We’ll add it soon.)")
        # Practical snapshot
        cmin, cmax = c.typical_salary_range
        print(f"Snapshot: education={c.education_path} | salary≈₹{cmin:,}–₹{cmax:,} | modes={', '.join(c.work_modes)}\n")

    # Optional: Save results
    save = input("Save top 5 results to file? (y/n): ").strip().lower()
    if save == "y":
        payload = []
        for total, c, br, why_traits, overlap_skills in results[:5]:
            payload.append({
                "career": c.title,
                "score": round(total,3),
                "breakdown": br,
                "top_traits": why_traits,
                "overlapping_skills": overlap_skills
            })
        with open("career_results.json","w") as f:
            json.dump(payload, f, indent=2)
        print("Results saved to career_results.json")

if __name__ == "__main__":
    run_cli()
