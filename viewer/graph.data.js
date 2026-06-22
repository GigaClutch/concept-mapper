window.GRAPH = {
 "meta": {
  "version": "0.1.0",
  "built": "2026-06-11",
  "description": "Phase 1 hand-built Kant cluster + Phase 3 backbone (bb-v1) over the full Ethics registry",
  "symmetric_types": [
   "CONTRASTS_WITH"
  ],
  "edge_families": {
   "hierarchical": [
    "IS_A",
    "PART_OF",
    "SUBCATEGORY_OF"
   ],
   "developmental": [
    "DEVELOPED_BY",
    "EXTENDED_BY",
    "DERIVED_FROM",
    "INFLUENCED_BY"
   ],
   "oppositional": [
    "CONTRASTS_WITH",
    "CRITIQUES",
    "RESPONDS_TO"
   ],
   "bibliographic": [
    "AUTHORED_BY",
    "INTRODUCED_IN"
   ]
  }
 },
 "nodes": [
  {
   "id": "categorical_imperative",
   "label": "Categorical Imperative",
   "type": "concept",
   "definition": "Kant's supreme principle of morality: act only according to that maxim whereby you can at the same time will that it should become a universal law. Unconditional, applying to all rational agents regardless of their desires.",
   "aliases": [
    "moral imperative",
    "CI"
   ],
   "domain": "Ethics",
   "tradition": "Kantian",
   "time_period": "18th century",
   "status": "curated",
   "metrics": {
    "degree": 8,
    "betweenness": 0.042647,
    "community": 2
   }
  },
  {
   "id": "hypothetical_imperative",
   "label": "Hypothetical Imperative",
   "type": "concept",
   "definition": "A command of reason that applies only conditionally, given some desired end: 'if you want X, do Y'. Contrasted by Kant with the unconditional categorical imperative.",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "Kantian",
   "time_period": "18th century",
   "status": "curated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.0,
    "community": 2
   }
  },
  {
   "id": "autonomy",
   "label": "Autonomy",
   "type": "concept",
   "definition": "Self-legislation of the rational will: the capacity to act according to laws one gives oneself, rather than from external causes or inclination. For Kant, the ground of human dignity.",
   "aliases": [
    "moral autonomy",
    "self-legislation"
   ],
   "domain": "Ethics",
   "tradition": "Kantian",
   "time_period": "18th century",
   "status": "curated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.000291,
    "community": 2
   }
  },
  {
   "id": "deontology",
   "label": "Deontology",
   "type": "concept",
   "definition": "A normative ethical theory that judges the morality of actions by their conformity to duties or rules, rather than by their consequences.",
   "aliases": [
    "duty-based ethics",
    "deontological ethics"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "18th century–present",
   "status": "curated",
   "metrics": {
    "degree": 8,
    "betweenness": 0.199379,
    "community": 2
   }
  },
  {
   "id": "consequentialism",
   "label": "Consequentialism",
   "type": "concept",
   "definition": "The family of normative ethical theories holding that the moral rightness of an act depends only on the value of its consequences.",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "19th century–present",
   "status": "curated",
   "metrics": {
    "degree": 6,
    "betweenness": 0.18227,
    "community": 8
   }
  },
  {
   "id": "utilitarianism",
   "label": "Utilitarianism",
   "type": "concept",
   "definition": "The consequentialist theory that the right action is the one that maximises overall well-being or utility, classically 'the greatest happiness of the greatest number'.",
   "aliases": [
    "utility principle"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "18th–19th century",
   "status": "curated",
   "metrics": {
    "degree": 13,
    "betweenness": 0.244687,
    "community": 0
   }
  },
  {
   "id": "virtue_ethics",
   "label": "Virtue Ethics",
   "type": "concept",
   "definition": "A normative approach centring on character and the virtues — stable excellences of the person — rather than on rules or consequences. Rooted in Aristotle's eudaimonism.",
   "aliases": [
    "aretaic ethics"
   ],
   "domain": "Ethics",
   "tradition": "Aristotelian",
   "time_period": "Ancient–present",
   "status": "curated",
   "metrics": {
    "degree": 12,
    "betweenness": 0.193561,
    "community": 3
   }
  },
  {
   "id": "normative_ethics",
   "label": "Normative Ethics",
   "type": "concept",
   "definition": "The branch of moral philosophy that studies what makes actions right or wrong and what we ought to do, comprising principally deontology, consequentialism, and virtue ethics.",
   "aliases": [
    "moral theory"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "Ancient–present",
   "status": "curated",
   "metrics": {
    "degree": 4,
    "betweenness": 0.092406,
    "community": 1
   }
  },
  {
   "id": "immanuel_kant",
   "label": "Immanuel Kant",
   "type": "person",
   "definition": "German philosopher (1724–1804), central figure of modern philosophy. Author of the three Critiques; founder of deontological ethics grounded in the categorical imperative and autonomy of the will.",
   "aliases": [
    "Kant"
   ],
   "domain": "Ethics",
   "tradition": "German Idealism",
   "time_period": "1724–1804",
   "status": "curated",
   "metrics": {
    "degree": 20,
    "betweenness": 0.361949,
    "community": 2
   }
  },
  {
   "id": "david_hume",
   "label": "David Hume",
   "type": "person",
   "definition": "Scottish empiricist philosopher (1711–1776). His scepticism about causation and reason famously woke Kant from his 'dogmatic slumber'.",
   "aliases": [
    "Hume"
   ],
   "domain": "Epistemology",
   "tradition": "Empiricism",
   "time_period": "1711–1776",
   "status": "curated",
   "metrics": {
    "degree": 9,
    "betweenness": 0.177833,
    "community": 4
   }
  },
  {
   "id": "jeremy_bentham",
   "label": "Jeremy Bentham",
   "type": "person",
   "definition": "English philosopher and reformer (1748–1832), founder of classical utilitarianism and the principle of utility.",
   "aliases": [
    "Bentham"
   ],
   "domain": "Ethics",
   "tradition": "Utilitarianism",
   "time_period": "1748–1832",
   "status": "curated",
   "metrics": {
    "degree": 4,
    "betweenness": 0.011416,
    "community": 0
   }
  },
  {
   "id": "john_stuart_mill",
   "label": "John Stuart Mill",
   "type": "person",
   "definition": "English philosopher (1806–1873) who refined utilitarianism with qualitative distinctions among pleasures, and defended liberty and representative government.",
   "aliases": [
    "Mill",
    "J.S. Mill"
   ],
   "domain": "Ethics",
   "tradition": "Utilitarianism",
   "time_period": "1806–1873",
   "status": "curated",
   "metrics": {
    "degree": 6,
    "betweenness": 0.116333,
    "community": 0
   }
  },
  {
   "id": "aristotle",
   "label": "Aristotle",
   "type": "person",
   "definition": "Greek philosopher (384–322 BC). His Nicomachean Ethics grounds virtue ethics in eudaimonia — flourishing achieved through excellent activity of the soul.",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "Peripatetic",
   "time_period": "384–322 BC",
   "status": "curated",
   "metrics": {
    "degree": 12,
    "betweenness": 0.115248,
    "community": 3
   }
  },
  {
   "id": "german_idealism",
   "label": "German Idealism",
   "type": "school",
   "definition": "The philosophical movement (c. 1781–1840) emerging from Kant's critical philosophy, developed by Fichte, Schelling, and Hegel.",
   "aliases": [],
   "domain": "Metaphysics",
   "tradition": "Continental",
   "time_period": "1781–1840",
   "status": "curated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 2
   }
  },
  {
   "id": "free_will",
   "label": "Free Will",
   "type": "concept",
   "definition": "ability of agents to be the ultimate source or originator of their choices, free from external determination",
   "aliases": [
    "freedom of the will"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q9476",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.013858,
    "community": 4
   }
  },
  {
   "id": "determinism",
   "label": "Determinism",
   "type": "concept",
   "definition": "philosophical belief that all events are determined completely by previously existing causes",
   "aliases": [
    "causal determinism"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q131133",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.027504,
    "community": 4
   }
  },
  {
   "id": "compatibilism",
   "label": "Compatibilism",
   "type": "concept",
   "definition": "belief that free will and determinism are mutually compatible to one another",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q1551125",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.055269,
    "community": 4
   }
  },
  {
   "id": "thomas_hobbes",
   "label": "Thomas Hobbes",
   "type": "person",
   "definition": "English philosopher (1588–1679)",
   "aliases": [
    "Hobbes",
    "Thomas Hobbsted",
    "Thomas Hobbes of Malflutry"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1588–1679",
   "wikidata_qid": "Q37621",
   "status": "generated",
   "metrics": {
    "degree": 4,
    "betweenness": 0.02147,
    "community": 7
   }
  },
  {
   "id": "moral_responsibility",
   "label": "Moral Responsibility",
   "type": "concept",
   "definition": "status of morally deserving praise, blame, reward, or punishment for an act or omission, in accordance with one's moral obligations",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q5190255",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 4
   }
  },
  {
   "id": "moral_luck",
   "label": "Moral Luck",
   "type": "concept",
   "definition": "philosophical concept",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q8095296",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.00499,
    "community": 0
   }
  },
  {
   "id": "bernard_williams",
   "label": "Bernard Williams",
   "type": "person",
   "definition": "English moral philosopher (1929–2003)",
   "aliases": [
    "Sir Bernard Arthur Owen Williams",
    "Bernard Arthur Owen Williams"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1929–2003",
   "wikidata_qid": "Q345641",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.002706,
    "community": 0
   }
  },
  {
   "id": "moral_status",
   "label": "Moral Status",
   "type": "concept",
   "definition": "description of intrinsic self-worth and dignity",
   "aliases": [
    "moral standing",
    "moral patient"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q58620410",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.013858,
    "community": 0
   }
  },
  {
   "id": "moral_agency",
   "label": "Moral Agency",
   "type": "concept",
   "definition": "ability to make ethical judgements",
   "aliases": [
    "moral agent"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q11883221",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 0
   }
  },
  {
   "id": "applied_ethics",
   "label": "Applied Ethics",
   "type": "concept",
   "definition": "branch of philosophy",
   "aliases": [
    "practical ethics",
    "conduct of life",
    "personal conduct"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q538733",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.027504,
    "community": 0
   }
  },
  {
   "id": "trolley_problem",
   "label": "Trolley Problem",
   "type": "concept",
   "definition": "thought experiment in ethics",
   "aliases": [
    "trolley dilemma"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q1753199",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.018892,
    "community": 6
   }
  },
  {
   "id": "moral_dilemma",
   "label": "Moral Dilemma",
   "type": "concept",
   "definition": "decision-making problem between two conflicting moral imperatives, neither of which is unambiguously acceptable or preferable",
   "aliases": [
    "ethical dilemma",
    "moral issue"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q192568",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 6
   }
  },
  {
   "id": "philippa_foot",
   "label": "Philippa Foot",
   "type": "person",
   "definition": "English philosopher (1920–2010)",
   "aliases": [
    "Philippa Ruth Bosanquet Foot",
    "Philippa Ruth Bosanquet",
    "Philippa Ruth Foot",
    "Philippa Bosanquet"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1920–2010",
   "wikidata_qid": "Q297493",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.046312,
    "community": 6
   }
  },
  {
   "id": "doctrine_of_double_effect",
   "label": "Doctrine of Double Effect",
   "type": "concept",
   "definition": "set of ethical criteria permitting certain actions when one's otherwise legitimate act may also cause harm",
   "aliases": [
    "double effect",
    "DDE",
    "rule of double effect",
    "double-effect reasoning",
    "PDE"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q1423147",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.003782,
    "community": 6
   }
  },
  {
   "id": "thomas_aquinas",
   "label": "Thomas Aquinas",
   "type": "person",
   "definition": "Italian Dominican friar, philosopher, Catholic priest, and Doctor of the Church (1225–1274)",
   "aliases": [
    "Aquinas",
    "St. Thomas Aquinas",
    "Saint Thomas Aquinas",
    "Saint Thomas",
    "Tommaso d'Aquino",
    "Thomas of Aquino",
    "St Thomas Aquinas",
    "Angelic Doctor"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1225–1274",
   "wikidata_qid": "Q9438",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.011853,
    "community": 6
   }
  },
  {
   "id": "natural_law",
   "label": "Natural Law",
   "type": "concept",
   "definition": "system of law that is purportedly determined by nature, and is thus universal",
   "aliases": [
    "natural law theory",
    "natural law ethics",
    "law of nature"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q29524",
   "status": "generated",
   "metrics": {
    "degree": 4,
    "betweenness": 0.010748,
    "community": 6
   }
  },
  {
   "id": "supererogation",
   "label": "Supererogation",
   "type": "concept",
   "definition": "acts which are good but not morally required to be done",
   "aliases": [
    "supererogatory acts",
    "supererogatory act",
    "works of supererogation",
    "supererogatory"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q2367476",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 2
   }
  },
  {
   "id": "duty",
   "label": "Duty",
   "type": "concept",
   "definition": "legal or moral requirement to take a certain course of action",
   "aliases": [
    "obligation",
    "binding",
    "requirement",
    "mandatory",
    "commitment"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q2648051",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.013858,
    "community": 2
   }
  },
  {
   "id": "practical_reason",
   "label": "Practical Reason",
   "type": "concept",
   "definition": "the use of reason to decide how to act",
   "aliases": [
    "practical rationality"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q3376512",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.054621,
    "community": 3
   }
  },
  {
   "id": "eudaimonia",
   "label": "Eudaimonia",
   "type": "concept",
   "definition": "Aristotelian term for happiness or welfare",
   "aliases": [
    "eudaemonia",
    "eudaimonism",
    "flourishing",
    "human flourishing",
    "eudaimonic life",
    "eu zên (\"living well\")",
    "eu zen (\"living well\")"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q1771260",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.013858,
    "community": 3
   }
  },
  {
   "id": "well_being",
   "label": "Well-Being",
   "type": "concept",
   "definition": "measure of how well life is to someone or a group with factors such as health, happiness and satisfaction",
   "aliases": [
    "wellbeing",
    "welfare",
    "human well-being",
    "human wellbeing"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q7981051",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 3
   }
  },
  {
   "id": "justice",
   "label": "Justice",
   "type": "concept",
   "definition": "broad idea of a situation where people receive that which they deserve",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q13189320",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 3
   }
  },
  {
   "id": "virtue",
   "label": "Virtue",
   "type": "concept",
   "definition": "morally positive trait or quality deemed to be morally good",
   "aliases": [
    "arete",
    "moral virtue",
    "moral value",
    "virtuousness"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q157811",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.013858,
    "community": 3
   }
  },
  {
   "id": "rights",
   "label": "Rights",
   "type": "concept",
   "definition": "fundamental legal, social, or ethical principles of freedom or entitlement according to some legal system, social convention, or ethical theory",
   "aliases": [
    "moral rights",
    "right"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q780687",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 2
   }
  },
  {
   "id": "peter_singer",
   "label": "Peter Singer",
   "type": "person",
   "definition": "Australian moral philosopher (born 1946)",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1946",
   "wikidata_qid": "Q211539",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.040939,
    "community": 0
   }
  },
  {
   "id": "psychological_egoism",
   "label": "Psychological Egoism",
   "type": "concept",
   "definition": "The view that true altruism in humans is impossible",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q1362786",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.013858,
    "community": 8
   }
  },
  {
   "id": "altruism",
   "label": "Altruism",
   "type": "concept",
   "definition": "principle or practice of concern for the welfare of others",
   "aliases": [
    "selflessness",
    "ministration"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q167323",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.0,
    "community": 8
   }
  },
  {
   "id": "socrates",
   "label": "Socrates",
   "type": "person",
   "definition": "5th-century BCE Greek philosopher",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "470 BCE–399 BCE",
   "wikidata_qid": "Q913",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.000106,
    "community": 3
   }
  },
  {
   "id": "akrasia",
   "label": "Akrasia",
   "type": "concept",
   "definition": "lack of self-control or state of acting against one's better judgment",
   "aliases": [
    "weakness of will",
    "incontinence",
    "acrasia"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q420749",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.006823,
    "community": 3
   }
  },
  {
   "id": "metaethics",
   "label": "Metaethics",
   "type": "concept",
   "definition": "branch of ethics seeking to understand ethical properties",
   "aliases": [
    "meta-ethics"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q56003",
   "status": "generated",
   "metrics": {
    "degree": 5,
    "betweenness": 0.089699,
    "community": 1
   }
  },
  {
   "id": "contractualism",
   "label": "Contractualism",
   "type": "concept",
   "definition": "moral theory",
   "aliases": [
    "social contract theory"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q3782613",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.031639,
    "community": 7
   }
  },
  {
   "id": "scholasticism",
   "label": "Scholasticism",
   "type": "school",
   "definition": "method of critical thought which dominated teaching by the academics (\"scholastics\", or \"schoolmen\") of medieval universities in Europe from about 1100 to 1700",
   "aliases": [
    "high scholasticism"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q41679",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.004678,
    "community": 6
   }
  },
  {
   "id": "hedonism",
   "label": "Hedonism",
   "type": "concept",
   "definition": "philosophy of pleasure as the highest value",
   "aliases": [
    "ethical hedonism"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q7064",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.054163,
    "community": 10
   }
  },
  {
   "id": "universalizability",
   "label": "Universalizability",
   "type": "concept",
   "definition": "concept in Kantian ethics",
   "aliases": [
    "universalisability"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q7894189",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.013052,
    "community": 1
   }
  },
  {
   "id": "prescriptivism",
   "label": "Prescriptivism",
   "type": "concept",
   "definition": "metaethical view that ethical sentences function similarly to imperatives which are universalizable—whoever makes a moral judgment is committed to the same judgment in any situation where the same relevant facts obtain",
   "aliases": [
    "universal prescriptivism"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q2980795",
   "status": "generated",
   "metrics": {
    "degree": 4,
    "betweenness": 0.035051,
    "community": 1
   }
  },
  {
   "id": "moral_realism",
   "label": "Moral Realism",
   "type": "concept",
   "definition": "philosophical position",
   "aliases": [
    "ethical realism"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q3100314",
   "status": "generated",
   "metrics": {
    "degree": 5,
    "betweenness": 0.045702,
    "community": 5
   }
  },
  {
   "id": "moral_anti_realism",
   "label": "Moral Anti-Realism",
   "type": "concept",
   "definition": "",
   "aliases": [
    "moral antirealism",
    "ethical anti-realism"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "",
   "status": "generated",
   "metrics": {
    "degree": 6,
    "betweenness": 0.077435,
    "community": 1
   }
  },
  {
   "id": "moral_cognitivism",
   "label": "Moral Cognitivism",
   "type": "concept",
   "definition": "the meta-ethical view that ethical sentences express propositions and can therefore be true or false",
   "aliases": [
    "cognitivism",
    "ethical cognitivism"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q15055389",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.002427,
    "community": 1
   }
  },
  {
   "id": "non_cognitivism",
   "label": "Non-Cognitivism",
   "type": "concept",
   "definition": "the meta-ethical view that ethical sentences do not express propositions and thus cannot be true or false",
   "aliases": [
    "noncognitivism"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q17156560",
   "status": "generated",
   "metrics": {
    "degree": 5,
    "betweenness": 0.040975,
    "community": 1
   }
  },
  {
   "id": "emotivism",
   "label": "Emotivism",
   "type": "concept",
   "definition": "metaethical view that moral statements are expressions of emotional attitudes rather than objective truths",
   "aliases": [
    "hurrah/boo theory"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q1058270",
   "status": "generated",
   "metrics": {
    "degree": 4,
    "betweenness": 0.032305,
    "community": 1
   }
  },
  {
   "id": "expressivism",
   "label": "Expressivism",
   "type": "concept",
   "definition": "metaethical theory that moral sentences are not descriptive, but express an evaluative attitude toward an object",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q5421730",
   "status": "generated",
   "metrics": {
    "degree": 4,
    "betweenness": 0.021943,
    "community": 5
   }
  },
  {
   "id": "a_j_ayer",
   "label": "A. J. Ayer",
   "type": "person",
   "definition": "English philosopher",
   "aliases": [
    "Alfred Jules Ayer",
    "Ayer",
    "Alfred J. Ayer",
    "Sir Alfred Jules Ayer",
    "Freddie"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1910–1989",
   "wikidata_qid": "Q243757",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.03472,
    "community": 1
   }
  },
  {
   "id": "charles_stevenson",
   "label": "Charles Stevenson",
   "type": "person",
   "definition": "American analytic philosopher (1908-1979)",
   "aliases": [
    "Charles Leslie Stevenson",
    "C. L. Stevenson"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1908–1979",
   "wikidata_qid": "Q264334",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 1
   }
  },
  {
   "id": "r_m_hare",
   "label": "R. M. Hare",
   "type": "person",
   "definition": "British moral philosopher (1919–2002)",
   "aliases": [
    "Richard Mervyn Hare",
    "Hare"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1919–2002",
   "wikidata_qid": "Q471923",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 1
   }
  },
  {
   "id": "simon_blackburn",
   "label": "Simon Blackburn",
   "type": "person",
   "definition": "English academic philosopher (born 1944)",
   "aliases": [
    "Blackburn",
    "Simon Walter Blackburn"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1944",
   "wikidata_qid": "Q287357",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.036706,
    "community": 5
   }
  },
  {
   "id": "allan_gibbard",
   "label": "Allan Gibbard",
   "type": "person",
   "definition": "American philosopher and social choice theorist",
   "aliases": [
    "Gibbard",
    "Allan F. Gibbard",
    "Allan Fletcher Gibbard"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1942",
   "wikidata_qid": "Q4730627",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 5
   }
  },
  {
   "id": "quasi_realism",
   "label": "Quasi-Realism",
   "type": "concept",
   "definition": "meta-ethical view",
   "aliases": [
    "quasirealism"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q7269470",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.015202,
    "community": 5
   }
  },
  {
   "id": "error_theory",
   "label": "Error Theory",
   "type": "concept",
   "definition": "",
   "aliases": [
    "moral error theory"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q10586383",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.027504,
    "community": 1
   }
  },
  {
   "id": "j_l_mackie",
   "label": "J. L. Mackie",
   "type": "person",
   "definition": "Australian philosopher (1917-1981)",
   "aliases": [
    "John Leslie Mackie",
    "Mackie",
    "John L. Mackie",
    "JL Mackie",
    "J.L. Mackie"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1917–1981",
   "wikidata_qid": "Q713642",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.0,
    "community": 1
   }
  },
  {
   "id": "ethics_inventing_right_and_wrong",
   "label": "Ethics: Inventing Right and Wrong",
   "type": "work",
   "definition": "work by John Mackie",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1977",
   "wikidata_qid": "Q31271796",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.0,
    "community": 1
   }
  },
  {
   "id": "moral_nihilism",
   "label": "Moral Nihilism",
   "type": "concept",
   "definition": "meta-ethical view that nothing is intrinsically moral or immoral",
   "aliases": [
    "ethical nihilism"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q12835757",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 1
   }
  },
  {
   "id": "moral_subjectivism",
   "label": "Moral Subjectivism",
   "type": "concept",
   "definition": "meta-ethical view",
   "aliases": [
    "ethical subjectivism"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q568188",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 1
   }
  },
  {
   "id": "moral_relativism",
   "label": "Moral Relativism",
   "type": "concept",
   "definition": "philosophical positions about the differences in moral judgments across peoples and cultures",
   "aliases": [
    "ethical relativism"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q1778848",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 1
   }
  },
  {
   "id": "moral_naturalism",
   "label": "Moral Naturalism",
   "type": "concept",
   "definition": "metaethical position",
   "aliases": [
    "ethical naturalism"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q3495350",
   "status": "generated",
   "metrics": {
    "degree": 4,
    "betweenness": 0.010402,
    "community": 5
   }
  },
  {
   "id": "moral_non_naturalism",
   "label": "Moral Non-Naturalism",
   "type": "concept",
   "definition": "meta-ethical view",
   "aliases": [
    "ethical non-naturalism"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q5403415",
   "status": "generated",
   "metrics": {
    "degree": 4,
    "betweenness": 0.027425,
    "community": 5
   }
  },
  {
   "id": "g_e_moore",
   "label": "G. E. Moore",
   "type": "person",
   "definition": "English philosopher (1873–1958)",
   "aliases": [
    "George Edward Moore",
    "Moore",
    "George Moore",
    "GE Moore"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1873–1958",
   "wikidata_qid": "Q295386",
   "status": "generated",
   "metrics": {
    "degree": 5,
    "betweenness": 0.052087,
    "community": 5
   }
  },
  {
   "id": "moral_intuitionism",
   "label": "Moral Intuitionism",
   "type": "concept",
   "definition": "family of views in moral epistemology",
   "aliases": [
    "ethical intuitionism",
    "intuitionism"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q2632427",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.012704,
    "community": 9
   }
  },
  {
   "id": "h_a_prichard",
   "label": "H. A. Prichard",
   "type": "person",
   "definition": "British philosopher (1871–1947)",
   "aliases": [
    "Harold Arthur Prichard",
    "Prichard",
    "Harold A. Prichard"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1871–1947",
   "wikidata_qid": "Q3498726",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.0,
    "community": 9
   }
  },
  {
   "id": "w_d_ross",
   "label": "W. D. Ross",
   "type": "person",
   "definition": "Scottish philosopher and translator (1877–1971)",
   "aliases": [
    "William David Ross",
    "David Ross",
    "Sir William David Ross",
    "William Ross",
    "Sir William Ross"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1877–1971",
   "wikidata_qid": "Q1364954",
   "status": "generated",
   "metrics": {
    "degree": 5,
    "betweenness": 0.065001,
    "community": 9
   }
  },
  {
   "id": "naturalistic_fallacy",
   "label": "Naturalistic Fallacy",
   "type": "concept",
   "definition": "ethical argument asserting that it is fallacious to explain something good reductively",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q376789",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.00226,
    "community": 5
   }
  },
  {
   "id": "open_question_argument",
   "label": "Open Question Argument",
   "type": "concept",
   "definition": "philosophical argument put forward by British philosopher G. E. Moore, to refute the equating of the property of goodness with some non-moral property, X, whether naturalistic (e.g. pleasure) or supernatural",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q7095717",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.00226,
    "community": 5
   }
  },
  {
   "id": "prima_facie_duty",
   "label": "Prima Facie Duty",
   "type": "concept",
   "definition": "",
   "aliases": [
    "pro tanto duty"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.013858,
    "community": 9
   }
  },
  {
   "id": "moral_sentimentalism",
   "label": "Moral Sentimentalism",
   "type": "concept",
   "definition": "",
   "aliases": [
    "sentimentalism",
    "moral sense school"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q677649",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.002283,
    "community": 4
   }
  },
  {
   "id": "francis_hutcheson",
   "label": "Francis Hutcheson",
   "type": "person",
   "definition": "Scottish philosopher (1694–1746)",
   "aliases": [
    "Hutcheson",
    "Franciscus Hutchinson",
    "Franciscus Hutcheson",
    "Frances Hutcheson",
    "Franciscus Hutchesonius",
    "Franz Hutcheson"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1694–1746",
   "wikidata_qid": "Q316367",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.0,
    "community": 4
   }
  },
  {
   "id": "rationalism",
   "label": "Rationalism",
   "type": "school",
   "definition": "philosophical view that reason should be the chief source of knowledge",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q483024",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.018879,
    "community": 4
   }
  },
  {
   "id": "is_ought_problem",
   "label": "Is-Ought Problem",
   "type": "concept",
   "definition": "philosophical problem articulated by David Hume in 1739 about how one can deduce prescriptive statements (what ought to be) from descriptive statements (what is)",
   "aliases": [
    "is-ought gap",
    "Hume's guillotine",
    "Hume's law",
    "fact–value gap",
    "is–ought distinction"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q1328762",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.0,
    "community": 4
   }
  },
  {
   "id": "moral_particularism",
   "label": "Moral Particularism",
   "type": "concept",
   "definition": "theory in meta-ethics",
   "aliases": [
    "particularism"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q3296948",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 9
   }
  },
  {
   "id": "act_utilitarianism",
   "label": "Act Utilitarianism",
   "type": "concept",
   "definition": "flavour of utilitarianism",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q3738092",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.0,
    "community": 0
   }
  },
  {
   "id": "rule_utilitarianism",
   "label": "Rule Utilitarianism",
   "type": "concept",
   "definition": "form of utilitarianism that says an action is right as it conforms to a rule that leads to the greatest good",
   "aliases": [
    "strong rule utilitarianism",
    "weak rule utilitarianism"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q651440",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.0,
    "community": 0
   }
  },
  {
   "id": "henry_sidgwick",
   "label": "Henry Sidgwick",
   "type": "person",
   "definition": "English philosopher (1838–1900)",
   "aliases": [
    "Sidgwick"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1838–1900",
   "wikidata_qid": "Q433076",
   "status": "generated",
   "metrics": {
    "degree": 6,
    "betweenness": 0.09968,
    "community": 0
   }
  },
  {
   "id": "greatest_happiness_principle",
   "label": "Greatest Happiness Principle",
   "type": "concept",
   "definition": "",
   "aliases": [
    "principle of utility"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q135402913",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.004214,
    "community": 0
   }
  },
  {
   "id": "heteronomy",
   "label": "Heteronomy",
   "type": "concept",
   "definition": "philosophical concept",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q1571420",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.0,
    "community": 2
   }
  },
  {
   "id": "good_will",
   "label": "Good Will",
   "type": "concept",
   "definition": "",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.0,
    "community": 2
   }
  },
  {
   "id": "maxim",
   "label": "Maxim",
   "type": "concept",
   "definition": "",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 2
   }
  },
  {
   "id": "kingdom_of_ends",
   "label": "Kingdom of Ends",
   "type": "concept",
   "definition": "Kant’s thought experiment about a world in which all humans are treated as ends, not as means",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q6412569",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.0,
    "community": 2
   }
  },
  {
   "id": "rosalind_hursthouse",
   "label": "Rosalind Hursthouse",
   "type": "person",
   "definition": "New Zealand philosopher",
   "aliases": [
    "Hursthouse",
    "Mary Rosalind Hursthouse"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1943",
   "wikidata_qid": "Q3480230",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.0,
    "community": 3
   }
  },
  {
   "id": "alasdair_macintyre",
   "label": "Alasdair MacIntyre",
   "type": "person",
   "definition": "Scottish-American philosopher (1929–2025)",
   "aliases": [
    "MacIntyre",
    "Alasdair Chalmers MacIntyre"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1929–2025",
   "wikidata_qid": "Q310178",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.0195,
    "community": 3
   }
  },
  {
   "id": "elizabeth_anscombe",
   "label": "Elizabeth Anscombe",
   "type": "person",
   "definition": "British analytic philosopher",
   "aliases": [
    "G. E. M. Anscombe",
    "Anscombe",
    "(Gertrude) Elizabeth (Margaret) Anscombe",
    "Elisabeth Anscombe"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1919–2001",
   "wikidata_qid": "Q229646",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.001515,
    "community": 8
   }
  },
  {
   "id": "golden_mean",
   "label": "Golden Mean",
   "type": "concept",
   "definition": "perfect moderation",
   "aliases": [
    "doctrine of the mean",
    "aura mediocritas"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q1054131",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.003473,
    "community": 3
   }
  },
  {
   "id": "practical_wisdom",
   "label": "Practical Wisdom",
   "type": "concept",
   "definition": "ancient Greek word for a type of wisdom or intelligence",
   "aliases": [
    "phronesis",
    "prudence"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q2316040",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.0,
    "community": 3
   }
  },
  {
   "id": "contractarianism",
   "label": "Contractarianism",
   "type": "concept",
   "definition": "",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.014085,
    "community": 7
   }
  },
  {
   "id": "social_contract",
   "label": "Social Contract",
   "type": "concept",
   "definition": "concept in political philosophy",
   "aliases": [
    "social contract theory",
    "political contract"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q1326430",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.009979,
    "community": 7
   }
  },
  {
   "id": "t_m_scanlon",
   "label": "T. M. Scanlon",
   "type": "person",
   "definition": "American philosopher",
   "aliases": [
    "Thomas Michael Scanlon",
    "Tim Scanlon",
    "Thomas M. Scanlon, Jr.",
    "TM Scanlon",
    "T M Scanlon",
    "Thomas M. Scanlon",
    "Thomas Michael"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1940",
   "wikidata_qid": "Q1773977",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.015332,
    "community": 7
   }
  },
  {
   "id": "john_rawls",
   "label": "John Rawls",
   "type": "person",
   "definition": "American political philosopher (1921–2002)",
   "aliases": [
    "Rawls"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1921–2002",
   "wikidata_qid": "Q172544",
   "status": "generated",
   "metrics": {
    "degree": 4,
    "betweenness": 0.041693,
    "community": 7
   }
  },
  {
   "id": "ethical_egoism",
   "label": "Ethical Egoism",
   "type": "concept",
   "definition": "ethical position that moral agents should act in their own self-interest",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q616772",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.040939,
    "community": 8
   }
  },
  {
   "id": "epicurus",
   "label": "Epicurus",
   "type": "person",
   "definition": "ancient Greek philosopher",
   "aliases": [
    "Epíkouros",
    "Epikouros"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "342 BCE–270 BCE",
   "wikidata_qid": "Q43216",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.040939,
    "community": 10
   }
  },
  {
   "id": "divine_command_theory",
   "label": "Divine Command Theory",
   "type": "concept",
   "definition": "theory that morality is commanded by, and originates only from, the divine",
   "aliases": [
    "theological voluntarism"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q430585",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.013008,
    "community": 6
   }
  },
  {
   "id": "care_ethics",
   "label": "Ethics of Care",
   "type": "concept",
   "definition": "Ethical theory",
   "aliases": [
    "care ethics",
    "EoC"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q1035845",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.000317,
    "community": 11
   }
  },
  {
   "id": "carol_gilligan",
   "label": "Carol Gilligan",
   "type": "person",
   "definition": "American feminist, ethicist, and psychologist",
   "aliases": [
    "Gilligan"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1936",
   "wikidata_qid": "Q284025",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 11
   }
  },
  {
   "id": "nel_noddings",
   "label": "Nel Noddings",
   "type": "person",
   "definition": "American philosopher (1929–2022)",
   "aliases": [
    "Noddings"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1929–2022",
   "wikidata_qid": "Q467525",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 11
   }
  },
  {
   "id": "feminist_ethics",
   "label": "Feminist Ethics",
   "type": "concept",
   "definition": "approach to ethics",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q10494601",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 11
   }
  },
  {
   "id": "arthur_schopenhauer",
   "label": "Arthur Schopenhauer",
   "type": "person",
   "definition": "German philosopher (1788-1860)",
   "aliases": [
    "Schopenhauer"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1788–1860",
   "wikidata_qid": "Q38193",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.014852,
    "community": 6
   }
  },
  {
   "id": "friedrich_nietzsche",
   "label": "Friedrich Nietzsche",
   "type": "person",
   "definition": "German philosopher (1844-1900)",
   "aliases": [
    "Nietzsche"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1844–1900",
   "wikidata_qid": "Q9358",
   "status": "generated",
   "metrics": {
    "degree": 4,
    "betweenness": 0.038401,
    "community": 6
   },
   "research": {
    "status": "researched",
    "date": "2026-06-22",
    "sources": [
     "nietzsche"
    ],
    "model": "claude-haiku-4-5"
   }
  },
  {
   "id": "derek_parfit",
   "label": "Derek Parfit",
   "type": "person",
   "definition": "British philosopher (1942–2017)",
   "aliases": [
    "Parfit"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1942–2017",
   "wikidata_qid": "Q962160",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.013858,
    "community": 0
   }
  },
  {
   "id": "plato",
   "label": "Plato",
   "type": "person",
   "definition": "4th-century BCE Greek philosopher",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "427 BCE–347 BCE",
   "wikidata_qid": "Q859",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 0.020681,
    "community": 3
   }
  },
  {
   "id": "christine_korsgaard",
   "label": "Christine Korsgaard",
   "type": "person",
   "definition": "American philosopher",
   "aliases": [
    "Korsgaard",
    "Christine Marion Korsgaard",
    "Christine M. Korsgaard",
    "C. M. Korsgaard",
    "C.M. Korsgaard",
    "C M Korsgaard",
    "Christine M Korsgaard"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1952",
   "wikidata_qid": "Q467518",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 2
   }
  },
  {
   "id": "stoicism",
   "label": "Stoicism",
   "type": "school",
   "definition": "school of Hellenistic philosophy who held that the practice of virtue suffices to attain eudaimonia",
   "aliases": [
    "Stoic philosophy",
    "the porch",
    "stoics",
    "Stoa"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q48235",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.013858,
    "community": 10
   }
  },
  {
   "id": "zeno_of_citium",
   "label": "Zeno of Citium",
   "type": "person",
   "definition": "Greek philosopher, founder of Stoicism",
   "aliases": [
    "Zenon of Citium",
    "Zeno",
    "Zeno the Stoic",
    "Zeno of Kition"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "334 BCE–263 BCE",
   "wikidata_qid": "Q171303",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 10
   }
  },
  {
   "id": "epicureanism",
   "label": "Epicureanism",
   "type": "school",
   "definition": "philosophical movement developed by Epicurus",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q179541",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.027504,
    "community": 10
   }
  },
  {
   "id": "empiricism",
   "label": "Empiricism",
   "type": "school",
   "definition": "theory that states that knowledge comes only or primarily from sensory experience",
   "aliases": [
    "British Empiricism"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "Q83368",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 4
   }
  },
  {
   "id": "joseph_butler",
   "label": "Joseph Butler",
   "type": "person",
   "definition": "English bishop and philosopher (1692–1752)",
   "aliases": [
    "Bishop Butler",
    "A Gentleman in Gloucestershire"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1692–1752",
   "wikidata_qid": "Q218322",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 8
   }
  },
  {
   "id": "groundwork_metaphysics_of_morals",
   "label": "Groundwork of the Metaphysics of Morals",
   "type": "work",
   "definition": "Translation of Kant's Groundwork published in 1997",
   "aliases": [
    "Groundwork",
    "Grundlegung zur Metaphysik der Sitten"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1997",
   "wikidata_qid": "Q113015922",
   "status": "generated",
   "metrics": {
    "degree": 4,
    "betweenness": 0.000344,
    "community": 2
   }
  },
  {
   "id": "critique_of_practical_reason",
   "label": "Critique of Practical Reason",
   "type": "work",
   "definition": "1788 work by Immanuel Kant",
   "aliases": [
    "second Critique"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1788",
   "wikidata_qid": "Q870851",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 2
   }
  },
  {
   "id": "critique_of_pure_reason",
   "label": "Critique of Pure Reason",
   "type": "work",
   "definition": "1781 philosophical work by Immanuel Kant",
   "aliases": [
    "first Critique"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1781",
   "wikidata_qid": "Q220002",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 2
   }
  },
  {
   "id": "metaphysics_of_morals",
   "label": "The Metaphysics of Morals",
   "type": "work",
   "definition": "work of political and moral philosophy by Immanuel Kant",
   "aliases": [
    "Metaphysik der Sitten"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1797",
   "wikidata_qid": "Q1214817",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 2
   }
  },
  {
   "id": "nicomachean_ethics",
   "label": "Nicomachean Ethics",
   "type": "work",
   "definition": "literary work by Aristotle",
   "aliases": [
    "Nichomachean Ethics",
    "Aristot. Nic. Eth.",
    "Ethica Nicomachea"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "340 BCE",
   "wikidata_qid": "Q474537",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.0,
    "community": 3
   }
  },
  {
   "id": "republic_plato",
   "label": "Republic",
   "type": "work",
   "definition": "philosophical work written by Plato",
   "aliases": [
    "The Republic",
    "Politeia",
    "Plato's Republic",
    "Plat. Rep."
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1963",
   "wikidata_qid": "Q123397",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 3
   }
  },
  {
   "id": "leviathan",
   "label": "Leviathan",
   "type": "work",
   "definition": "book by Thomas Hobbes",
   "aliases": [
    "Leviathan or The Matter, Forme and Power of a Commonwealth Ecclesiasticall and Civil"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1651",
   "wikidata_qid": "Q193034",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 7
   }
  },
  {
   "id": "treatise_of_human_nature",
   "label": "A Treatise of Human Nature",
   "type": "work",
   "definition": "work by David Hume",
   "aliases": [
    "Treatise"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1739",
   "wikidata_qid": "Q2451675",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.0,
    "community": 4
   }
  },
  {
   "id": "enquiry_principles_of_morals",
   "label": "An Enquiry Concerning the Principles of Morals",
   "type": "work",
   "definition": "philosophical book by David Hume",
   "aliases": [
    "second Enquiry"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1751",
   "wikidata_qid": "Q1306663",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 4
   }
  },
  {
   "id": "principles_of_morals_and_legislation",
   "label": "An Introduction to the Principles of Morals and Legislation",
   "type": "work",
   "definition": "intro to the Principles of Morals and Legislation",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1789",
   "wikidata_qid": "Q19041209",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.0,
    "community": 0
   }
  },
  {
   "id": "utilitarianism_mill",
   "label": "Utilitarianism",
   "type": "work",
   "definition": "1861 essay by John Stuart Mill",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1861",
   "wikidata_qid": "Q1197767",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 0
   }
  },
  {
   "id": "on_liberty",
   "label": "On Liberty",
   "type": "work",
   "definition": "non-fiction work by John Stuart Mill",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1859",
   "wikidata_qid": "Q1055881",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 0
   }
  },
  {
   "id": "methods_of_ethics",
   "label": "The Methods of Ethics",
   "type": "work",
   "definition": "book by Henry Sidgwick",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1874",
   "wikidata_qid": "Q7751187",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 0
   }
  },
  {
   "id": "principia_ethica",
   "label": "Principia Ethica",
   "type": "work",
   "definition": "philosophical book",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1903",
   "wikidata_qid": "Q2344885",
   "status": "generated",
   "metrics": {
    "degree": 3,
    "betweenness": 3.5e-05,
    "community": 5
   }
  },
  {
   "id": "language_truth_and_logic",
   "label": "Language, Truth and Logic",
   "type": "work",
   "definition": "philosophical book by A. J. Ayer",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1936",
   "wikidata_qid": "Q1431691",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 1
   }
  },
  {
   "id": "the_right_and_the_good",
   "label": "The Right and the Good",
   "type": "work",
   "definition": "1930 book by the Scottish philosopher David Ross",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1930",
   "wikidata_qid": "Q105061759",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.0,
    "community": 9
   }
  },
  {
   "id": "a_theory_of_justice",
   "label": "A Theory of Justice",
   "type": "work",
   "definition": "work of political philosophy and ethics by John Rawls",
   "aliases": [
    "Theory of Justice",
    "Rawlsian Justice",
    "A theory of social justice"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1971",
   "wikidata_qid": "Q300588",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.00402,
    "community": 7
   }
  },
  {
   "id": "after_virtue",
   "label": "After Virtue",
   "type": "work",
   "definition": "book by Alasdair MacIntyre",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1981",
   "wikidata_qid": "Q4690583",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.012151,
    "community": 3
   }
  },
  {
   "id": "reasons_and_persons",
   "label": "Reasons and Persons",
   "type": "work",
   "definition": "book by Derek Parfit",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1984",
   "wikidata_qid": "Q7301514",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 0
   }
  },
  {
   "id": "what_we_owe_to_each_other",
   "label": "What We Owe to Each Other",
   "type": "work",
   "definition": "book by T.M. Scanlon",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1999",
   "wikidata_qid": "Q107191343",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 7
   }
  },
  {
   "id": "on_the_genealogy_of_morality",
   "label": "On the Genealogy of Morality",
   "type": "work",
   "definition": "essay by Friedrich Nietzsche",
   "aliases": [
    "On the Genealogy of Morals",
    "Zur Genealogie der Moral",
    "Genealogy of Morality",
    "Genealogy of Morals"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1887",
   "wikidata_qid": "Q230302",
   "status": "generated",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 6
   }
  },
  {
   "id": "modern_moral_philosophy",
   "label": "Modern Moral Philosophy",
   "type": "work",
   "definition": "article",
   "aliases": [],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "1958",
   "wikidata_qid": "Q3859951",
   "status": "generated",
   "metrics": {
    "degree": 2,
    "betweenness": 0.002019,
    "community": 8
   }
  },
  {
   "id": "slave_revolt_in_morality",
   "label": "slave_revolt_in_morality",
   "type": "concept",
   "definition": "Nietzsche's historical thesis that modern morality originated when the powerless oppressed developed a resentful hatred of their masters and inverted values, labeling the masters' traits (strength, domination) as evil an",
   "aliases": [
    "slave morality",
    "the revaluation of values"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "",
   "status": "provisional",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 12
   }
  },
  {
   "id": "master_morality",
   "label": "master_morality",
   "type": "concept",
   "definition": "The original form of moral evaluation based on the good/bad distinction, arising from the self-affirmation and sense of superiority of the strong and noble. Values strength, courage, excellence, and integrity over univer",
   "aliases": [
    "noble morality",
    "aristocratic morality"
   ],
   "domain": "Ethics",
   "tradition": "",
   "time_period": "",
   "wikidata_qid": "",
   "status": "provisional",
   "metrics": {
    "degree": 1,
    "betweenness": 0.0,
    "community": 12
   }
  }
 ],
 "edges": [
  {
   "source": "categorical_imperative",
   "target": "immanuel_kant",
   "type": "DEVELOPED_BY",
   "weight": 0.875,
   "origin": "backbone",
   "evidence": [
    {
     "article_id": "kant-moral",
     "quote": "Immanuel Kant (1724–1804) argued that the supreme principle of morality is a principle of rationality that he dubbed the “Categorical Imperative” (CI)."
    },
    {
     "article_id": "kant-hume-morality",
     "quote": "Kant believes that our moral concerns are dominated by the question of what duties are imposed on us by a law that commands with a uniquely moral necessity."
    }
   ],
   "status": "confirmed"
  },
  {
   "source": "autonomy",
   "target": "immanuel_kant",
   "type": "DEVELOPED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "evidence": [
    {
     "article_id": "kant-moral",
     "quote": "At the heart of Kant’s moral theory is the idea of autonomy."
    }
   ],
   "status": "confirmed"
  },
  {
   "source": "categorical_imperative",
   "target": "deontology",
   "type": "PART_OF",
   "weight": 0.5,
   "origin": "backbone",
   "evidence": [],
   "status": "confirmed"
  },
  {
   "source": "autonomy",
   "target": "categorical_imperative",
   "type": "PART_OF",
   "weight": 0.5,
   "origin": "backbone",
   "evidence": [],
   "status": "confirmed"
  },
  {
   "source": "hypothetical_imperative",
   "target": "categorical_imperative",
   "type": "CONTRASTS_WITH",
   "weight": 0.75,
   "origin": "backbone",
   "evidence": [
    {
     "article_id": "kant-moral",
     "quote": "A hypothetical imperative is a command that also applies to us in virtue of our having a rational will, but not simply in virtue of this. It requires us to exercise our wills in a certain way given we have antecedently willed an end. A hypothetical imperative is thus a command in a conditional form."
    }
   ],
   "status": "confirmed"
  },
  {
   "source": "deontology",
   "target": "normative_ethics",
   "type": "SUBCATEGORY_OF",
   "weight": 0.9375,
   "origin": "backbone",
   "evidence": [
    {
     "article_id": "ethics-deontological",
     "quote": "deontology is one of those kinds of normative theories regarding which choices are morally required, forbidden, or permitted"
    },
    {
     "article_id": "ethics-virtue",
     "quote": "Virtue ethics is currently one of three major approaches in normative ethics."
    },
    {
     "article_id": "kant-moral",
     "quote": "Although Kant gives several examples in the Groundwork that illustrate the CI, he goes on to describe in later writings, especially in The Metaphysics of Morals, a complicated normative ethical theory for interpreting and applying the CI to human persons in ordinary contexts."
    }
   ],
   "status": "confirmed"
  },
  {
   "source": "consequentialism",
   "target": "normative_ethics",
   "type": "SUBCATEGORY_OF",
   "weight": 0.984375,
   "origin": "backbone",
   "evidence": [
    {
     "article_id": "consequentialism",
     "quote": "Consequentialism, as its name suggests, is simply the view that normative properties depend only on consequences."
    },
    {
     "article_id": "ethics-deontological",
     "quote": "within the domain of moral theories that assess our choices, deontologists—those who subscribe to deontological theories of morality—stand in opposition to consequentialists"
    },
    {
     "article_id": "ethics-virtue",
     "quote": "Virtue ethics is currently one of three major approaches in normative ethics."
    },
    {
     "article_id": "mill-moral-political",
     "quote": "Utilitarianism assesses actions and institutions in terms of their effects on human happiness and enjoins us to perform actions and design institutions so that they promote—in one formulation, maximize—human happiness."
    },
    {
     "article_id": "utilitarianism-history",
     "quote": "The approach is a species of consequentialism, which holds that the moral quality of an action or policy is entirely a function of its consequences, or the value produced by the action or policy."
    }
   ],
   "status": "confirmed"
  },
  {
   "source": "virtue_ethics",
   "target": "normative_ethics",
   "type": "SUBCATEGORY_OF",
   "weight": 0.75,
   "origin": "backbone",
   "evidence": [
    {
     "article_id": "ethics-virtue",
     "quote": "Virtue ethics is currently one of three major approaches in normative ethics."
    }
   ],
   "status": "confirmed"
  },
  {
   "source": "deontology",
   "target": "consequentialism",
   "type": "CONTRASTS_WITH",
   "weight": 0.875,
   "origin": "backbone",
   "evidence": [
    {
     "article_id": "ethics-deontological",
     "quote": "within the domain of moral theories that assess our choices, deontologists—those who subscribe to deontological theories of morality—stand in opposition to consequentialists"
    },
    {
     "article_id": "ethics-virtue",
     "quote": "the one that emphasizes the virtues, or moral character, in contrast to the approach that emphasizes duties or rules (deontology) or that emphasizes the consequences of actions (consequentialism)."
    }
   ],
   "status": "confirmed"
  },
  {
   "source": "utilitarianism",
   "target": "consequentialism",
   "type": "SUBCATEGORY_OF",
   "weight": 0.96875,
   "origin": "backbone",
   "evidence": [
    {
     "article_id": "consequentialism",
     "quote": "The paradigm case of consequentialism is utilitarianism"
    },
    {
     "article_id": "ethics-deontological",
     "quote": "Utilitarians, for example, identify the Good with pleasure, happiness, desire satisfaction, or “welfare” in some other sense"
    },
    {
     "article_id": "ethics-virtue",
     "quote": "A utilitarian will point to the fact that the consequences of doing so will maximize well-being"
    },
    {
     "article_id": "utilitarianism-history",
     "quote": "What distinguishes utilitarianism from other forms of consequentialism are specific commitments regarding the nature of the value to be produced as well as the approach to that value."
    }
   ],
   "status": "confirmed"
  },
  {
   "source": "utilitarianism",
   "target": "jeremy_bentham",
   "type": "DEVELOPED_BY",
   "weight": 0.984375,
   "origin": "backbone",
   "evidence": [
    {
     "article_id": "bentham",
     "quote": "it was Bentham who rendered the theory in its recognisably secular and systematic form"
    },
    {
     "article_id": "consequentialism",
     "quote": "The paradigm case of consequentialism is utilitarianism, whose classic proponents were Jeremy Bentham (1789), John Stuart Mill (1861), and Henry Sidgwick (1907)."
    },
    {
     "article_id": "hedonism",
     "quote": "Jeremy Bentham asserted both psychological and ethical hedonism with the first two sentences of his book An Introduction to the Principles of Morals and Legislation"
    },
    {
     "article_id": "mill-moral-political",
     "quote": "Mill was raised in the tradition of Philosophical Radicalism, made famous by Jeremy Bentham (1748–1832)"
    },
    {
     "article_id": "utilitarianism-history",
     "quote": "Though the first systematic account of utilitarianism was developed by Jeremy Bentham (1748–1832), the core insight motivating the theory occurred much earlier."
    }
   ],
   "status": "confirmed"
  },
  {
   "source": "utilitarianism",
   "target": "john_stuart_mill",
   "type": "EXTENDED_BY",
   "weight": 0.984375,
   "origin": "backbone",
   "evidence": [
    {
     "article_id": "bentham",
     "quote": "As is well known, while adhering to the basic Benthamic analysis of motives, in Utilitarianism (1861) J. S. Mill introduced the concept of“higher pleasures”"
    },
    {
     "article_id": "consequentialism",
     "quote": "The paradigm case of consequentialism is utilitarianism, whose classic proponents were Jeremy Bentham (1789), John Stuart Mill (1861), and Henry Sidgwick (1907)."
    },
    {
     "article_id": "hedonism",
     "quote": "J.S. Mill (ch. 2) developed an alternative approach according to which there is ‘higher’ and ‘lower’ pleasure, and its value is irreducibly a matter of its quality as well as its quantity."
    },
    {
     "article_id": "mill-moral-political",
     "quote": "Though Mill accepts the utilitarian legacy of the Radicals, he transforms that legacy in important ways."
    },
    {
     "article_id": "utilitarianism-history",
     "quote": "Because Bentham, quite famously, had an enormous impact on the development of John Stuart Mill’s thought, it seemed natural to view the development of Classical Utilitarianism as proceeding from Bentham through Mill."
    }
   ],
   "status": "confirmed"
  },
  {
   "source": "virtue_ethics",
   "target": "aristotle",
   "type": "DEVELOPED_BY",
   "weight": 0.875,
   "origin": "backbone",
   "evidence": [
    {
     "article_id": "aristotle-ethics",
     "quote": "Aristotle follows Socrates and Plato in taking the virtues to be central to a well-lived life."
    },
    {
     "article_id": "ethics-virtue",
     "quote": "In the West, virtue ethics’ founding fathers are Plato and Aristotle"
    }
   ],
   "status": "confirmed"
  },
  {
   "source": "immanuel_kant",
   "target": "david_hume",
   "type": "INFLUENCED_BY",
   "weight": 0.875,
   "origin": "backbone",
   "evidence": [
    {
     "article_id": "kant-hume-morality",
     "quote": "Kant credited Hume with waking him from his “dogmatic slumber”, and he describes the Critique of Pure Reason, arguably the most important work of modern philosophy, as the solution to the “Humean problem in its greatest possible amplification”"
    },
    {
     "article_id": "kant-moral",
     "quote": "Thus, at the heart of Kant’s moral philosophy is a conception of reason whose reach in practical affairs goes well beyond that of a Humean ‘slave’ to the passions."
    }
   ],
   "status": "confirmed"
  },
  {
   "source": "john_stuart_mill",
   "target": "jeremy_bentham",
   "type": "INFLUENCED_BY",
   "weight": 0.9375,
   "origin": "backbone",
   "evidence": [
    {
     "article_id": "bentham",
     "quote": "It was in the flush of his early commitment to utilitarianism that Mill edited the five volumes of Bentham’s writings on evidence"
    },
    {
     "article_id": "consequentialism",
     "quote": "The paradigm case of consequentialism is utilitarianism, whose classic proponents were Jeremy Bentham (1789), John Stuart Mill (1861), and Henry Sidgwick (1907)."
    },
    {
     "article_id": "utilitarianism-history",
     "quote": "John Stuart Mill (1806–1873) was a follower of Bentham, and, through most of his life, greatly admired Bentham’s work even though he disagreed with some of Bentham’s claims"
    }
   ],
   "status": "confirmed"
  },
  {
   "source": "german_idealism",
   "target": "immanuel_kant",
   "type": "DERIVED_FROM",
   "weight": 0.5,
   "origin": "backbone",
   "evidence": [],
   "status": "confirmed"
  },
  {
   "source": "john_stuart_mill",
   "target": "immanuel_kant",
   "type": "CRITIQUES",
   "weight": 0.5,
   "origin": "backbone",
   "evidence": [],
   "status": "confirmed"
  },
  {
   "source": "free_will",
   "target": "determinism",
   "type": "CONTRASTS_WITH",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "compatibilism",
   "target": "determinism",
   "type": "RESPONDS_TO",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-responsibility",
     "quote": "Compatibilists maintain that free will and moral responsibility are compatible with determinism."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "compatibilism",
   "target": "thomas_hobbes",
   "type": "DEVELOPED_BY",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "kant-hume-morality",
     "quote": "Kant sides with Hume and Hutcheson against the psychological egoism associated with Pufendorf, Hobbes, Locke, and Mandeville"
    },
    {
     "article_id": "moral-responsibility",
     "quote": "philosophers in the Modern period (such as Hobbes and Hume) distinguished the general way in which our actions are necessitated if determinism is true from the specific instances of necessity sometimes imposed on us by everyday constraints on behavior"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "compatibilism",
   "target": "david_hume",
   "type": "EXTENDED_BY",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "kant-hume-morality",
     "quote": "Kant was directly influenced by the sentimentalist tradition to which Hume belongs (especially Francis Hutcheson’s version)."
    },
    {
     "article_id": "moral-responsibility",
     "quote": "This compatibilist tradition was carried into the 20th century by logical positivists such as Ayer (1954) and Schlick ([1930]1966). Here is how Schlick expressed a central compatibilist insight in 1930 (drawing, in particular, on Hume)"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "free_will",
   "target": "moral_responsibility",
   "type": "PART_OF",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "moral_luck",
   "target": "bernard_williams",
   "type": "DEVELOPED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-luck",
     "quote": "Bernard Williams writes, “when I first introduced the expression moral luck, I expected to suggest an oxymoron”"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "moral_luck",
   "target": "immanuel_kant",
   "type": "CRITIQUES",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "moral_status",
   "target": "moral_agency",
   "type": "CONTRASTS_WITH",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "moral_status",
   "target": "applied_ethics",
   "type": "PART_OF",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "trolley_problem",
   "target": "moral_dilemma",
   "type": "IS_A",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "trolley_problem",
   "target": "philippa_foot",
   "type": "DEVELOPED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "trolley_problem",
   "target": "doctrine_of_double_effect",
   "type": "RESPONDS_TO",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "doctrine_of_double_effect",
   "target": "thomas_aquinas",
   "type": "DEVELOPED_BY",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "double-effect",
     "quote": "Thomas Aquinas is credited with introducing the principle of double effect in his discussion of the permissibility of self-defense in the Summa Theologica (II-II, Qu. 64, Art.7)."
    },
    {
     "article_id": "ethics-deontological",
     "quote": "Deontologists of this stripe are committed to something like the doctrine of double effect, a long-established doctrine of Catholic theology (Woodward 2001)"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "doctrine_of_double_effect",
   "target": "natural_law",
   "type": "PART_OF",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "supererogation",
   "target": "duty",
   "type": "CONTRASTS_WITH",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-deontological",
     "quote": "deontological morality, in contrast to consequentialism, leaves space for agents to give special concern to their families, friends, and projects"
    },
    {
     "article_id": "supererogation",
     "quote": "supererogation, the category of actions that are praiseworthy (either in creating good states of affairs or in reflecting a particularly virtuous trait of character) yet at the same time not obligatory"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "practical_reason",
   "target": "aristotle",
   "type": "DEVELOPED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "practical_reason",
   "target": "immanuel_kant",
   "type": "DEVELOPED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "eudaimonia",
   "target": "well_being",
   "type": "IS_A",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "justice",
   "target": "virtue",
   "type": "IS_A",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-virtue",
     "quote": "justice, charity, courage, and generosity are virtues"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "rights",
   "target": "deontology",
   "type": "PART_OF",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-deontological",
     "quote": "Such norms are to be simply obeyed by each moral agent; such norm-keepings are not to be maximized by each agent. In this sense, for such deontologists, the Right is said to have priority over the Good"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "applied_ethics",
   "target": "peter_singer",
   "type": "DEVELOPED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "psychological_egoism",
   "target": "altruism",
   "type": "CONTRASTS_WITH",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "socrates",
   "target": "akrasia",
   "type": "CRITIQUES",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "metaethics",
   "target": "normative_ethics",
   "type": "CONTRASTS_WITH",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-anti-realism",
     "quote": "All three terms are to be defined in opposition to realism, but since there is no consensus on how “realism” is to be understood, “anti-realism” fares no better."
    },
    {
     "article_id": "moral-relativism",
     "quote": "Metaethical moral relativist positions are typically contrasted with moral objectivism."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "contractualism",
   "target": "utilitarianism",
   "type": "CONTRASTS_WITH",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "natural_law",
   "target": "scholasticism",
   "type": "PART_OF",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "hedonism",
   "target": "utilitarianism",
   "type": "PART_OF",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "universalizability",
   "target": "prescriptivism",
   "type": "PART_OF",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "moral_realism",
   "target": "metaethics",
   "type": "SUBCATEGORY_OF",
   "weight": 0.984375,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "metaethics",
     "quote": "non-naturalist views that see morality as presupposing, or being committed to, properties over and above those that would be countenanced by natural science"
    },
    {
     "article_id": "moral-anti-realism",
     "quote": "Traditionally, to hold a realist position with respect to X is to hold that X exists objectively."
    },
    {
     "article_id": "moral-non-naturalism",
     "quote": "non-naturalism is a form of moral realism"
    },
    {
     "article_id": "moral-realism",
     "quote": "Moral realism is not a particular substantive moral view nor does it carry a distinctive metaphysical commitment over and above the commitment that comes with thinking moral claims can be true or false and some are true."
    },
    {
     "article_id": "moral-relativism",
     "quote": "Other views—variously called moral non-cognitivism, expressivism, anti-realism, nihilism, etc."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "moral_anti_realism",
   "target": "metaethics",
   "type": "SUBCATEGORY_OF",
   "weight": 0.9375,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "metaethics",
     "quote": "non-naturalist views that see morality as presupposing, or being committed to, properties over and above those that would be countenanced by natural science"
    },
    {
     "article_id": "moral-anti-realism",
     "quote": "So understood, moral anti-realism is the disjunction of three theses: moral noncognitivism moral error theory moral non-objectivism"
    },
    {
     "article_id": "moral-relativism",
     "quote": "Other views—variously called moral non-cognitivism, expressivism, anti-realism, nihilism, etc."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "moral_realism",
   "target": "moral_anti_realism",
   "type": "CONTRASTS_WITH",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-anti-realism",
     "quote": "moral anti-realism is the denial of the thesis that moral properties—or facts, objects, relations, events, etc. (whatever categories one is willing to countenance)—exist objectively."
    },
    {
     "article_id": "moral-relativism",
     "quote": "Metaethical moral relativist positions are typically contrasted with moral objectivism."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "moral_cognitivism",
   "target": "metaethics",
   "type": "SUBCATEGORY_OF",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "metaethics",
     "quote": "These are all examples of naturalist accounts of morality that identify various moral properties with non-problematic natural features of the world."
    },
    {
     "article_id": "moral-realism",
     "quote": "Moral realists are those who think that, in these respects, things should be taken at face value—moral claims do purport to report facts and are true if they get the facts right."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "moral_cognitivism",
   "target": "non_cognitivism",
   "type": "CONTRASTS_WITH",
   "weight": 0.9375,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "metaethics",
     "quote": "non-cognitivists argue that Moore’s mistake was in thinking that moral claims attribute any sort of property to things, and so he was also wrong in thinking that moral claims have propositional content and express genuine beliefs"
    },
    {
     "article_id": "moral-anti-realism",
     "quote": "Moral noncognitivism holds that our moral judgments are not in the business of aiming at truth."
    },
    {
     "article_id": "moral-relativism",
     "quote": "Other views—variously called moral non-cognitivism, expressivism, anti-realism, nihilism, etc.—contend that moral judgments lack truth-value"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "non_cognitivism",
   "target": "moral_anti_realism",
   "type": "SUBCATEGORY_OF",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-anti-realism",
     "quote": "There are broadly two ways of endorsing (1): moral noncognitivism and moral error theory."
    },
    {
     "article_id": "moral-realism",
     "quote": "those who reject moral realism are usefully divided into (i) those who think moral claims do not purport to report facts in light of which they are true or false (noncognitivists)"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "emotivism",
   "target": "non_cognitivism",
   "type": "SUBCATEGORY_OF",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-cognitivism",
     "quote": "Emotivists think moral terms in grammatically assertive utterances function primarily to express emotion and perhaps also to elicit similar emotions in others"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "prescriptivism",
   "target": "non_cognitivism",
   "type": "SUBCATEGORY_OF",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "expressivism",
   "target": "non_cognitivism",
   "type": "SUBCATEGORY_OF",
   "weight": 0.9375,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "metaethics",
     "quote": "recent versions of expressivism, flying the banner of “quasi-realism”, have taken as a central project explaining, on non-cognitivist foundations, how and why moral language has all the trappings of being cognitivist and realist"
    },
    {
     "article_id": "moral-anti-realism",
     "quote": "Another influential kind of noncognitivism called “prescriptivism” claims that moral judgments are really veiled commands"
    },
    {
     "article_id": "moral-realism",
     "quote": "Noncognitivists often appeal to this apparent contrast to argue that moral claims have this necessary connection to motivation precisely because they do not express beliefs (that might be true or false) but instead express motivational states of desire, approval, or commitment"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "emotivism",
   "target": "a_j_ayer",
   "type": "DEVELOPED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-cognitivism",
     "quote": "Emotivists think moral terms in grammatically assertive utterances function primarily to express emotion and perhaps also to elicit similar emotions in others (Barnes 1933; Stevenson 1946; Ayer 1952, Chapter 6)."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "emotivism",
   "target": "charles_stevenson",
   "type": "EXTENDED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-cognitivism",
     "quote": "Some theorists who view themselves as emotivists suggest that even the most general terms of moral evaluation have a descriptive meaning rather than just an emotive or non-cognitive meaning (Stevenson 1944, 22; Hare 1952, suggests the same sort of idea within a prescriptivist theory at 118)."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "prescriptivism",
   "target": "r_m_hare",
   "type": "DEVELOPED_BY",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-anti-realism",
     "quote": "R.M. Hare (1952, 1963) restricted this to commands that one is willing to universalize."
    },
    {
     "article_id": "moral-cognitivism",
     "quote": "By contrast current versions of prescriptivism, most developed in the works of R. M. Hare, have attempted to vindicate moral thinking as a rational enterprise."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "expressivism",
   "target": "simon_blackburn",
   "type": "DEVELOPED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-cognitivism",
     "quote": "Simon Blackburn, whose quasi-realist project was briefly described above, has contributed various ideas not only for the states expressed by indicative sentences but also for complex embeddings of moral claims."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "expressivism",
   "target": "allan_gibbard",
   "type": "EXTENDED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-cognitivism",
     "quote": "But the proponent who has developed the program in the most systematic way is Allan Gibbard."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "quasi_realism",
   "target": "simon_blackburn",
   "type": "DEVELOPED_BY",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-anti-realism",
     "quote": "Simon Blackburn, for example, has pursued what he calls a “quasi-realist” program (Blackburn 1984, 1993, 1998)."
    },
    {
     "article_id": "moral-cognitivism",
     "quote": "‘Quasi-Realism’ is Simon Blackburn’s name for this sort of non-cognitivism, and especially his own version of expressivism."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "quasi_realism",
   "target": "expressivism",
   "type": "DERIVED_FROM",
   "weight": 0.9375,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "metaethics",
     "quote": "recent versions of expressivism, flying the banner of “quasi-realism”, have taken as a central project explaining, on non-cognitivist foundations, how and why moral language has all the trappings of being cognitivist and realist"
    },
    {
     "article_id": "moral-anti-realism",
     "quote": "The quasi-realist is someone who endorses an anti-realist metaphysical stance but who seeks, through philosophical maneuvering, to earn the right for moral discourse to enjoy all the trappings of realist talk."
    },
    {
     "article_id": "moral-cognitivism",
     "quote": "What especially distinguishes the quasi-realist project is an emphasis on explaining why we are entitled to act as if moral judgments are genuinely truth-apt even while strictly speaking they are neither true nor false in any robust sense."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "quasi_realism",
   "target": "moral_realism",
   "type": "RESPONDS_TO",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "error_theory",
   "target": "j_l_mackie",
   "type": "DEVELOPED_BY",
   "weight": 0.9375,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-anti-realism",
     "quote": "Defenders of moral error theory include Mackie 1977, Hinckfuss 1987, Joyce 2001, and Olson 2014."
    },
    {
     "article_id": "moral-non-naturalism",
     "quote": "John Mackie (see Mackie 1977 and Joyce 2001)"
    },
    {
     "article_id": "moral-realism",
     "quote": "Some error theorists do argue that combining cognitivism with motivational internalism results in an untenable position (Mackie 1977)."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "error_theory",
   "target": "ethics_inventing_right_and_wrong",
   "type": "INTRODUCED_IN",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-anti-realism",
     "quote": "John Mackie (who coined the term “error theory” in 1977) argues that when we participate in moral discourse we commit ourselves to the existence of objective values and objective prescriptions"
    },
    {
     "article_id": "moral-realism",
     "quote": "Mackie, J. L., 1977. Ethics: Inventing Right and Wrong, London: Penguin Books."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "error_theory",
   "target": "moral_anti_realism",
   "type": "SUBCATEGORY_OF",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "moral_nihilism",
   "target": "moral_anti_realism",
   "type": "SUBCATEGORY_OF",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "moral_subjectivism",
   "target": "moral_anti_realism",
   "type": "SUBCATEGORY_OF",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "moral_relativism",
   "target": "metaethics",
   "type": "SUBCATEGORY_OF",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "moral_naturalism",
   "target": "moral_realism",
   "type": "SUBCATEGORY_OF",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "moral_non_naturalism",
   "target": "moral_realism",
   "type": "SUBCATEGORY_OF",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-non-naturalism",
     "quote": "non-naturalism is a form of moral realism and is opposed to non-cognitivist positions"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "moral_naturalism",
   "target": "moral_non_naturalism",
   "type": "CONTRASTS_WITH",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "moral_non_naturalism",
   "target": "g_e_moore",
   "type": "DEVELOPED_BY",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-non-naturalism",
     "quote": "there is widespread agreement that G.E. Moore’s account of goodness in Principia Ethica is a paradigmatically non-naturalist account"
    },
    {
     "article_id": "moral-realism",
     "quote": "This standard view can be traced to a powerful and influential argument offered by G.E. Moore (1903)."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "moral_intuitionism",
   "target": "moral_non_naturalism",
   "type": "SUBCATEGORY_OF",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "moral_intuitionism",
   "target": "h_a_prichard",
   "type": "DEVELOPED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "intuitionism-ethics",
     "quote": "W. D. Ross, for example, uses the notion of apprehension, but he tends to base his moral theory largely on our considered moral convictions."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "moral_intuitionism",
   "target": "w_d_ross",
   "type": "EXTENDED_BY",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "intuitionism-ethics",
     "quote": "Ross is arguably an exception"
    },
    {
     "article_id": "moral-non-naturalism",
     "quote": "Moore held that it was true by definition that right actions maximize goodness, though he later came to the conclusion that this definition of rightness was also vulnerable to an Open Question Argument"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "naturalistic_fallacy",
   "target": "g_e_moore",
   "type": "DEVELOPED_BY",
   "weight": 0.9375,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "metaethics",
     "quote": "Moore offered a simple test. Take whichever account you will—say, one according to which to be good is to be pleasant—and then consider whether a person who understands the terms involved might nonetheless intelligibly ask whether something she acknowledges to be pleasant is good."
    },
    {
     "article_id": "moral-non-naturalism",
     "quote": "Moore famously claimed that naturalists were guilty of what he called the “naturalistic fallacy.”"
    },
    {
     "article_id": "moral-realism",
     "quote": "This standard view can be traced to a powerful and influential argument offered by G.E. Moore (1903)."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "naturalistic_fallacy",
   "target": "moral_naturalism",
   "type": "CRITIQUES",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "metaethics",
     "quote": "no naturalist account of morality could do justice to what we are actually thinking and claiming when we make moral judgments"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "open_question_argument",
   "target": "g_e_moore",
   "type": "DEVELOPED_BY",
   "weight": 0.96875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "intuitionism-ethics",
     "quote": "Moore’s open question argument can be regarded as giving form to this intuition."
    },
    {
     "article_id": "metaethics",
     "quote": "Moore offered a simple test. Take whichever account you will—say, one according to which to be good is to be pleasant—and then consider whether a person who understands the terms involved might nonetheless intelligibly ask whether something she acknowledges to be pleasant is good."
    },
    {
     "article_id": "moral-non-naturalism",
     "quote": "Moore’s “Open Question Argument” for the conclusion that goodness is a non-natural property"
    },
    {
     "article_id": "naturalism-moral",
     "quote": "Moore’s Open Question Argument"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "open_question_argument",
   "target": "moral_naturalism",
   "type": "CRITIQUES",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "intuitionism-ethics",
     "quote": "Moore’s argument can be captured as follows: If some property F could be defined in terms of some other property G, then the question “is something which is G, F?” would be closed."
    },
    {
     "article_id": "metaethics",
     "quote": "no naturalist account of morality could do justice to what we are actually thinking and claiming when we make moral judgments"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "prima_facie_duty",
   "target": "w_d_ross",
   "type": "DEVELOPED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "intuitionism-ethics",
     "quote": "Ross writes, a self-evident proposition is “evident without any need of proof, or of evidence beyond itself” (1930/2002, 29)"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "moral_sentimentalism",
   "target": "francis_hutcheson",
   "type": "DEVELOPED_BY",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "kant-hume-morality",
     "quote": "Hume locates the foundation of morality in human nature, primarily in our emotional responses to the behavior of our fellow human beings."
    },
    {
     "article_id": "moral-sentimentalism",
     "quote": "the roots of the modern sentimentalist tradition in ethics go back to early 18th century debates in Britain. Anthony Ashley Cooper, better known by his title as the Earl of Shaftesbury, introduced the notion of a moral sense"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "moral_sentimentalism",
   "target": "david_hume",
   "type": "DEVELOPED_BY",
   "weight": 0.9375,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "hume-moral",
     "quote": "Hume sides with the moral sense theorists: we gain awareness of moral good and evil by experiencing the pleasure of approval and the uneasiness of disapproval when we contemplate a character trait or action from an imaginatively sensitive and unbiased point of view."
    },
    {
     "article_id": "kant-hume-morality",
     "quote": "Kant was directly influenced by the sentimentalist tradition to which Hume belongs (especially Francis Hutcheson’s version)."
    },
    {
     "article_id": "moral-sentimentalism",
     "quote": "Following Hutcheson, Hume rejects reason or reasoning as the source of moral distinctions"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "moral_sentimentalism",
   "target": "rationalism",
   "type": "CONTRASTS_WITH",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "is_ought_problem",
   "target": "david_hume",
   "type": "DEVELOPED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "moral_particularism",
   "target": "prima_facie_duty",
   "type": "RESPONDS_TO",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "virtue_ethics",
   "target": "deontology",
   "type": "CONTRASTS_WITH",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-virtue",
     "quote": "in contrast to the approach that emphasizes duties or rules (deontology) or that emphasizes the consequences of actions (consequentialism)."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "virtue_ethics",
   "target": "consequentialism",
   "type": "CONTRASTS_WITH",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-virtue",
     "quote": "in contrast to the approach that emphasizes duties or rules (deontology) or that emphasizes the consequences of actions (consequentialism)."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "act_utilitarianism",
   "target": "utilitarianism",
   "type": "SUBCATEGORY_OF",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "consequentialism",
     "quote": "Act consequentialism is the claim that an act is morally right if and only if that act maximizes the good"
    },
    {
     "article_id": "mill-moral-political",
     "quote": "Act Utilitarianism: An act is right insofar as its consequences for the general happiness are at least as good as any alternative available to the agent."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "rule_utilitarianism",
   "target": "utilitarianism",
   "type": "SUBCATEGORY_OF",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "mill-moral-political",
     "quote": "Rule Utilitarianism: An act is right insofar as it conforms to a rule whose acceptance value for the general happiness is at least as great as any alternative rule available to the agent."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "act_utilitarianism",
   "target": "rule_utilitarianism",
   "type": "CONTRASTS_WITH",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "utilitarianism",
   "target": "henry_sidgwick",
   "type": "EXTENDED_BY",
   "weight": 0.96875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "consequentialism",
     "quote": "The paradigm case of consequentialism is utilitarianism, whose classic proponents were Jeremy Bentham (1789), John Stuart Mill (1861), and Henry Sidgwick (1907)."
    },
    {
     "article_id": "egoism",
     "quote": "Sidgwick usually does"
    },
    {
     "article_id": "hedonism",
     "quote": "Other key contributors to debate over hedonism include Plato, Aristotle, Epicurus, Aquinas, Butler, Hume, Mill, Nietzsche, Brentano, Sidgwick, Moore, Ross, Broad, Ryle and Chisholm."
    },
    {
     "article_id": "utilitarianism-history",
     "quote": "Sidgwick was also a British philosopher, and his views developed out of and in response to those of Bentham and Mill."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "utilitarianism",
   "target": "peter_singer",
   "type": "EXTENDED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "consequentialism",
     "quote": "Advocates of these theories often call them consequentialism rather than utilitarianism so that their theories will not be subject to refutation by association with the classic utilitarian theory."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "greatest_happiness_principle",
   "target": "jeremy_bentham",
   "type": "DEVELOPED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "bentham",
     "quote": "In the Fragment Bentham stated the “fundamental axiom” that “it is the greatest happiness of the greatest number that is the measure of right and wrong”"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "greatest_happiness_principle",
   "target": "utilitarianism",
   "type": "PART_OF",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "utilitarianism-history",
     "quote": "Classical Utilitarianism emerged in the nineteenth-century and is distinguished from earlier forms of utilitarianism by it’s clear structure and committment to hedonism as a theory of value."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "deontology",
   "target": "immanuel_kant",
   "type": "DEVELOPED_BY",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-deontological",
     "quote": "If any philosopher is regarded as central to deontological moral theories, it is surely Immanuel Kant"
    },
    {
     "article_id": "kant-moral",
     "quote": "At the heart of Kant’s moral theory is the idea of autonomy. Understanding the idea of autonomy was, in Kant’s view, key to understanding and justifying the authority that moral requirements have over us."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "deontology",
   "target": "w_d_ross",
   "type": "EXTENDED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "duty",
   "target": "deontology",
   "type": "PART_OF",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "hypothetical_imperative",
   "target": "immanuel_kant",
   "type": "DEVELOPED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "kant-moral",
     "quote": "Kant holds that the fundamental principle of our moral duties is a categorical imperative."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "autonomy",
   "target": "heteronomy",
   "type": "CONTRASTS_WITH",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "heteronomy",
   "target": "immanuel_kant",
   "type": "DEVELOPED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "good_will",
   "target": "immanuel_kant",
   "type": "DEVELOPED_BY",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-deontological",
     "quote": "For Kant, the only thing unqualifiedly good is a good will (Kant 1785)"
    },
    {
     "article_id": "kant-moral",
     "quote": "Kant’s analysis of commonsense ideas begins with the thought that the only thing good without qualification is a “good will”."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "maxim",
   "target": "categorical_imperative",
   "type": "PART_OF",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "kingdom_of_ends",
   "target": "immanuel_kant",
   "type": "DEVELOPED_BY",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "kant-hume-morality",
     "quote": "Kant’s notion of autonomy is one of the more central, distinctive, and influential aspects of his ethics."
    },
    {
     "article_id": "kant-moral",
     "quote": "Kant states that the above concept of every rational will as a will that must regard itself as enacting laws binding all rational wills is closely connected to another concept, that of a “systematic union of different rational beings under common laws”, or a “Kingdom of Ends” (G 4:433)."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "kingdom_of_ends",
   "target": "categorical_imperative",
   "type": "PART_OF",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "universalizability",
   "target": "categorical_imperative",
   "type": "PART_OF",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "virtue_ethics",
   "target": "rosalind_hursthouse",
   "type": "EXTENDED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-virtue",
     "quote": "It was heralded by Anscombe’s famous article “Modern Moral Philosophy”"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "virtue_ethics",
   "target": "philippa_foot",
   "type": "EXTENDED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "virtue_ethics",
   "target": "alasdair_macintyre",
   "type": "EXTENDED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "virtue_ethics",
   "target": "elizabeth_anscombe",
   "type": "EXTENDED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-virtue",
     "quote": "It was heralded by Anscombe’s famous article “Modern Moral Philosophy” (Anscombe 1958)"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "virtue",
   "target": "virtue_ethics",
   "type": "PART_OF",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-virtue",
     "quote": "We begin by discussing two concepts that are central to all forms of virtue ethics, namely, virtue and practical wisdom."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "eudaimonia",
   "target": "aristotle",
   "type": "DEVELOPED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-virtue",
     "quote": "These are arête (excellence or virtue), phronesis (practical or moral wisdom) and eudaimonia"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "eudaimonia",
   "target": "virtue_ethics",
   "type": "PART_OF",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-virtue",
     "quote": "These are arête (excellence or virtue), phronesis (practical or moral wisdom) and eudaimonia (usually translated as happiness or flourishing)."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "golden_mean",
   "target": "aristotle",
   "type": "DEVELOPED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "aristotle-ethics",
     "quote": "every ethical virtue is a condition intermediate (a “golden mean” as it is popularly known) between two other states, one involving excess, and the other deficiency"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "golden_mean",
   "target": "virtue_ethics",
   "type": "PART_OF",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "practical_wisdom",
   "target": "aristotle",
   "type": "DEVELOPED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-virtue",
     "quote": "Following (and adapting) Aristotle, virtue ethicists draw a distinction between full or perfect virtue and “continence”"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "practical_wisdom",
   "target": "virtue_ethics",
   "type": "PART_OF",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-virtue",
     "quote": "Another way in which one can easily fall short of full virtue is through lacking phronesis—moral or practical wisdom."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "akrasia",
   "target": "aristotle",
   "type": "DEVELOPED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "aristotle-ethics",
     "quote": "In VII.1–10 Aristotle investigates character traits—continence and incontinence—that are not as blameworthy as the vices but not as praiseworthy as the virtues."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "contractarianism",
   "target": "thomas_hobbes",
   "type": "DEVELOPED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "contractarianism",
     "quote": "Contractarianism, which stems from the Hobbesian line of social contract thought, holds that persons are primarily self-interested"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "contractarianism",
   "target": "social_contract",
   "type": "DERIVED_FROM",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "contractualism",
   "target": "t_m_scanlon",
   "type": "DEVELOPED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "contractarianism",
     "quote": "Contractualism, which stems from the Kantian line of social contract thought, holds that rationality requires that we respect persons"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "contractualism",
   "target": "contractarianism",
   "type": "CONTRASTS_WITH",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "contractarianism",
     "quote": "It has been more recently recognized that there are two distinct strains of social contract thought, which now typically go by the names contractarianism and contractualism."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "social_contract",
   "target": "thomas_hobbes",
   "type": "DEVELOPED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "social_contract",
   "target": "john_rawls",
   "type": "EXTENDED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "ethical_egoism",
   "target": "consequentialism",
   "type": "SUBCATEGORY_OF",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "ethical_egoism",
   "target": "altruism",
   "type": "CONTRASTS_WITH",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "psychological_egoism",
   "target": "ethical_egoism",
   "type": "CONTRASTS_WITH",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "hedonism",
   "target": "epicurus",
   "type": "DEVELOPED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "hedonism",
     "quote": "Other key contributors to debate over hedonism include Plato, Aristotle, Epicurus, Aquinas, Butler, Hume, Mill, Nietzsche, Brentano, Sidgwick, Moore, Ross, Broad, Ryle and Chisholm."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "divine_command_theory",
   "target": "natural_law",
   "type": "CONTRASTS_WITH",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "natural_law",
   "target": "thomas_aquinas",
   "type": "DEVELOPED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "natural-law-ethics",
     "quote": "Aquinas says that the fundamental principle of the natural law is that good is to be done and evil avoided (ST IaIIae 94, 2)."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "care_ethics",
   "target": "carol_gilligan",
   "type": "DEVELOPED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "feminism-ethics",
     "quote": "Psychologist Carol Gilligan’s landmark work, In a Different Voice: Psychological Theory and Women’s Development (1982), disputes accounts of moral development that do not take into account girls’ moral experiences"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "care_ethics",
   "target": "nel_noddings",
   "type": "EXTENDED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "feminism-ethics",
     "quote": "Nel Noddings’s influential work, Caring: A Feminine Approach to Ethics and Moral Education (1984), argues for the moral preferability of a care perspective"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "care_ethics",
   "target": "feminist_ethics",
   "type": "SUBCATEGORY_OF",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "feminism-ethics",
     "quote": "The ethic of care has its roots in projects that aim to correct for the exclusion of women from traditional theorizations of moral reasoning."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "immanuel_kant",
   "target": "rationalism",
   "type": "INFLUENCED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "arthur_schopenhauer",
   "target": "immanuel_kant",
   "type": "INFLUENCED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "friedrich_nietzsche",
   "target": "arthur_schopenhauer",
   "type": "INFLUENCED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "nietzsche",
     "quote": "he was already interested in philosophy, particularly the work of Arthur Schopenhauer and Friedrich Albert Lange"
    }
   ],
   "status": "unverified"
  },
  {
   "source": "henry_sidgwick",
   "target": "john_stuart_mill",
   "type": "INFLUENCED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "utilitarianism-history",
     "quote": "Sidgwick was also a British philosopher, and his views developed out of and in response to those of Bentham and Mill."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "peter_singer",
   "target": "henry_sidgwick",
   "type": "INFLUENCED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "derek_parfit",
   "target": "henry_sidgwick",
   "type": "INFLUENCED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "g_e_moore",
   "target": "henry_sidgwick",
   "type": "INFLUENCED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "w_d_ross",
   "target": "h_a_prichard",
   "type": "INFLUENCED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "plato",
   "target": "socrates",
   "type": "INFLUENCED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "aristotle",
   "target": "plato",
   "type": "INFLUENCED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-virtue",
     "quote": "In the West, virtue ethics’ founding fathers are Plato and Aristotle"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "thomas_aquinas",
   "target": "aristotle",
   "type": "INFLUENCED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "natural-law-ethics",
     "quote": "These writers, not surprisingly, trace their views to Aquinas as the major influence, though they do not claim to reproduce his views in detail. (See, for example, Grisez 1983, Finnis 1980, MacIntyre 1999, and Murphy 2001.)"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "david_hume",
   "target": "francis_hutcheson",
   "type": "INFLUENCED_BY",
   "weight": 0.96875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-virtue",
     "quote": "It has also generated virtue ethical readings of philosophers other than Plato and Aristotle, such as Martineau, Hume and Nietzsche"
    },
    {
     "article_id": "hume-moral",
     "quote": "Hume roundly criticizes Hobbes for his insistence on psychological egoism or something close to it"
    },
    {
     "article_id": "kant-hume-morality",
     "quote": "Kant was directly influenced by the sentimentalist tradition to which Hume belongs (especially Francis Hutcheson’s version)."
    },
    {
     "article_id": "utilitarianism-history",
     "quote": "Hume was heavily influenced by Hutcheson, who was one of his teachers."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "a_j_ayer",
   "target": "david_hume",
   "type": "INFLUENCED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "simon_blackburn",
   "target": "david_hume",
   "type": "INFLUENCED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "christine_korsgaard",
   "target": "immanuel_kant",
   "type": "INFLUENCED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "john_rawls",
   "target": "immanuel_kant",
   "type": "INFLUENCED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-virtue",
     "quote": "Theorists have turned to philosophers like Hutcheson, Hume, Nietzsche, Martineau, and Heidegger for resources"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "t_m_scanlon",
   "target": "john_rawls",
   "type": "INFLUENCED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "alasdair_macintyre",
   "target": "aristotle",
   "type": "INFLUENCED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-virtue",
     "quote": "modern virtue ethics does not have to take a “neo-Aristotelian” or eudaimonist form"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "rosalind_hursthouse",
   "target": "aristotle",
   "type": "INFLUENCED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-virtue",
     "quote": "It has also generated virtue ethical readings of philosophers other than Plato and Aristotle, such as Martineau, Hume and Nietzsche, and thereby different forms of virtue ethics have developed"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "stoicism",
   "target": "zeno_of_citium",
   "type": "DEVELOPED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "epicureanism",
   "target": "epicurus",
   "type": "DEVELOPED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "stoicism",
   "target": "epicureanism",
   "type": "CONTRASTS_WITH",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "empiricism",
   "target": "rationalism",
   "type": "CONTRASTS_WITH",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "scholasticism",
   "target": "aristotle",
   "type": "DERIVED_FROM",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "bernard_williams",
   "target": "utilitarianism",
   "type": "CRITIQUES",
   "weight": 0.9375,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "metaethics",
     "quote": "Glaucon follows up, in Book II, with an alternative, and less cynical, proposal. While he too sees morality as a human creation"
    },
    {
     "article_id": "practical-reason",
     "quote": "Such views ascribe to us very demanding requirements of impartial benevolence, which leave little scope for the independent significance of the agent’s own projects and interests (Williams 1973)."
    },
    {
     "article_id": "utilitarianism-history",
     "quote": "In The Methods Sidgwick is concerned with developing an account of “…the different methods of Ethics that I find implicit in our common moral reasoning…” These methods are egoism, intuition based morality, and utilitarianism."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "joseph_butler",
   "target": "psychological_egoism",
   "type": "CRITIQUES",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "egoism",
     "quote": "A common objection to psychological egoism, made famously by Joseph Butler, is that I must desire things other than my own welfare in order to get welfare."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "philippa_foot",
   "target": "prescriptivism",
   "type": "CRITIQUES",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "groundwork_metaphysics_of_morals",
   "target": "immanuel_kant",
   "type": "AUTHORED_BY",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-deontological",
     "quote": "For Kant, the only thing unqualifiedly good is a good will (Kant 1785)"
    },
    {
     "article_id": "moral-luck",
     "quote": "Kant: A good will is not good because of what it effects or accomplishes, because of its fitness to attain some proposed end, but only because of its volition, that is, it is good in itself"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "critique_of_practical_reason",
   "target": "immanuel_kant",
   "type": "AUTHORED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "critique_of_pure_reason",
   "target": "immanuel_kant",
   "type": "AUTHORED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "kant-hume-morality",
     "quote": "Kant reports that his “labor” in the Critique of Pure Reason was fundamentally a response to “that Humean skeptical teaching” (CPrR 5:32)."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "metaphysics_of_morals",
   "target": "immanuel_kant",
   "type": "AUTHORED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "kant-hume-morality",
     "quote": "In the Metaphysics of Morals, Kant argues that additional feelings also play a role in motivating virtuous conduct."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "nicomachean_ethics",
   "target": "aristotle",
   "type": "AUTHORED_BY",
   "weight": 0.9375,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "aristotle-ethics",
     "quote": "Aristotle wrote two ethical treatises: the Nicomachean Ethics and the Eudemian Ethics."
    },
    {
     "article_id": "moral-responsibility",
     "quote": "A picture along these lines can be found in Aristotle’s suggestion (in Book III of the Nicomachean Ethics) that one can be responsible for being a careless person"
    },
    {
     "article_id": "natural-law-ethics",
     "quote": "Aristotle, Nicomachean Ethics, Cited by book and chapter number."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "republic_plato",
   "target": "plato",
   "type": "AUTHORED_BY",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "leviathan",
   "target": "thomas_hobbes",
   "type": "AUTHORED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "natural-law-ethics",
     "quote": "He held that the laws of nature are divine law (Leviathan, xv, ¶41), that all humans are bound by them (Leviathan, xv, ¶¶36), and that it is easy to know at least the basics of the natural law (Leviathan, xv, ¶35)."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "treatise_of_human_nature",
   "target": "david_hume",
   "type": "AUTHORED_BY",
   "weight": 0.9375,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "hume-moral",
     "quote": "Hume’s main ethical writings are Book 3 of his Treatise of Human Nature, “Of Morals” (which builds on Book 2, “Of the Passions”)"
    },
    {
     "article_id": "moral-sentimentalism",
     "quote": "See David Hume’s Treatise of Human Nature (T), 456"
    },
    {
     "article_id": "utilitarianism-history",
     "quote": "Hume, David, 1738. A Treatise of Human Nature, edited by L. A. Selby-Bigge, Oxford: Oxford University Press, 1978."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "enquiry_principles_of_morals",
   "target": "david_hume",
   "type": "AUTHORED_BY",
   "weight": 0.9375,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "hume-moral",
     "quote": "Hume’s main ethical writings are Book 3 of his Treatise of Human Nature, “Of Morals” (which builds on Book 2, “Of the Passions”), his Enquiry concerning the Principles of Morals"
    },
    {
     "article_id": "moral-relativism",
     "quote": "There were certainly occasional discussions of moral disagreement—for example in Michel de Montaigne’s Essays or in the dialogue David Hume attached to An Enquiry Concerning the Principles of Morals."
    },
    {
     "article_id": "moral-sentimentalism",
     "quote": "An Enquiry Concerning the Principles of Morals. Ed. J. B. Schneewind. Indianapolis, Hackett, 1983"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "principles_of_morals_and_legislation",
   "target": "jeremy_bentham",
   "type": "AUTHORED_BY",
   "weight": 0.96875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "bentham",
     "quote": "In An Introduction to the Principles of Morals and Legislation (printed 1780, published with additions 1789), as a preliminary to developing a theory of penal law he detailed the basic elements of classical utilitarian theory."
    },
    {
     "article_id": "consequentialism",
     "quote": "Bentham wrote, “It is not to be expected that this process [his hedonic calculus] should be strictly pursued previously to every moral judgment.” (1789, Chap. IV, Sec. VI)"
    },
    {
     "article_id": "hedonism",
     "quote": "Jeremy Bentham asserted both psychological and ethical hedonism with the first two sentences of his book An Introduction to the Principles of Morals and Legislation: “Nature has placed mankind under the governance of two sovereign masters, pain, and pleasure."
    },
    {
     "article_id": "utilitarianism-history",
     "quote": "Bentham, Jeremy, 1789 [PML]. An Introduction to the Principles of Morals and Legislation, Oxford: Clarendon Press, 1907."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "utilitarianism_mill",
   "target": "john_stuart_mill",
   "type": "AUTHORED_BY",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "hedonism",
     "quote": "J.S. Mill (ch. 2) developed an alternative approach according to which there is ‘higher’ and ‘lower’ pleasure"
    },
    {
     "article_id": "mill-moral-political",
     "quote": "Utilitarianism (1861, cited as U)"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "on_liberty",
   "target": "john_stuart_mill",
   "type": "AUTHORED_BY",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "mill-moral-political",
     "quote": "On Liberty (1859, cited as OL)"
    },
    {
     "article_id": "utilitarianism-history",
     "quote": "–––, 1859. On Liberty, London: Longman, Roberts & Green."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "methods_of_ethics",
   "target": "henry_sidgwick",
   "type": "AUTHORED_BY",
   "weight": 0.998046875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "bentham",
     "quote": "James Fitzjames Stephen, Henry Sidgwick, and A.V. Dicey all advocated versions of utilitarian individualism, although Sidgwick occasionally gave voice to “socialist” sentiments in developing his intuitional utilitarian theory in The Methods of Ethics (1874)."
    },
    {
     "article_id": "consequentialism",
     "quote": "Sidgwick added, “It is not necessary that the end which gives the criterion of rightness should always be the end at which we consciously aim.” (1907, 413)"
    },
    {
     "article_id": "egoism",
     "quote": "Sidgwick usually does"
    },
    {
     "article_id": "intuitionism-ethics",
     "quote": "Sidgwick thought that good could be analysed as what ought to be desired"
    },
    {
     "article_id": "mill-moral-political",
     "quote": "Henry Sidgwick (1838–1900), for one, read Mill as a psychological egoist (The Methods of Ethics 42–44)."
    },
    {
     "article_id": "moral-non-naturalism",
     "quote": "A very similar argument was used by Sidgwick to establish that certain moral notions are irreducible (see Sidgwick 1907: Book I, Chapter 3)"
    },
    {
     "article_id": "practical-reason",
     "quote": "Sidgwick, Henry, 1907, The Methods of Ethics, New York: Macmillan, 7th edition."
    },
    {
     "article_id": "utilitarianism-history",
     "quote": "Henry Sidgwick’s (1838–1900) The Methods of Ethics (1874) is one of the most well known works in utilitarian moral philosophy, and deservedly so."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "principia_ethica",
   "target": "g_e_moore",
   "type": "AUTHORED_BY",
   "weight": 0.998046875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "egoism",
     "quote": "G. E. Moore argued that ethical egoism is self-contradictory."
    },
    {
     "article_id": "intuitionism-ethics",
     "quote": "Moore is the intuitionist who laid most stress on the non-natural nature of moral properties, though his focus was on goodness rather than rightness. In Principia Ethica"
    },
    {
     "article_id": "mill-moral-political",
     "quote": "Bernard Williams (1973) has argued that the demandingness of utilitarianism threatens the sort of personal projects and partial relationships that help give our lives meaning."
    },
    {
     "article_id": "moral-non-naturalism",
     "quote": "Moore’s account in Principia is important"
    },
    {
     "article_id": "moral-realism",
     "quote": "Moore, G. E., 1903. Principia Ethica, Cambridge: Cambridge University Press."
    },
    {
     "article_id": "naturalism-moral",
     "quote": "Moore’s Principia Ethica"
    },
    {
     "article_id": "practical-reason",
     "quote": "Moore, George E., 1903, Principia Ethica, Mineola, NY: Dover; reprinted in 2004."
    },
    {
     "article_id": "utilitarianism-history",
     "quote": "Moore, G. E., 1903 [PE]. Principia Ethica, Amherst, New York: Prometheus Books, 1988."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "language_truth_and_logic",
   "target": "a_j_ayer",
   "type": "AUTHORED_BY",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-cognitivism",
     "quote": "Early prescriptivists thought that this had radical implications for moral reasoning and argument. Carnap suggested that moral judgments are equivalent to relatively simple imperatives."
    },
    {
     "article_id": "moral-non-naturalism",
     "quote": "Ayer 1952"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "ethics_inventing_right_and_wrong",
   "target": "j_l_mackie",
   "type": "AUTHORED_BY",
   "weight": 0.9375,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-anti-realism",
     "quote": "Mackie, J.L., 1977. Ethics: Inventing Right and Wrong, Harmondsworth: Penguin."
    },
    {
     "article_id": "moral-non-naturalism",
     "quote": "Mackie, J.L., 1977. Ethics: Inventing Right and Wrong"
    },
    {
     "article_id": "moral-realism",
     "quote": "Mackie, J. L., 1977. Ethics: Inventing Right and Wrong, London: Penguin Books."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "the_right_and_the_good",
   "target": "w_d_ross",
   "type": "AUTHORED_BY",
   "weight": 0.9375,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "intuitionism-ethics",
     "quote": "Ross writes, a self-evident proposition is “evident without any need of proof, or of evidence beyond itself” (1930/2002, 29), and Broad describes"
    },
    {
     "article_id": "metaethics",
     "quote": "Socrates, in contrast, rejects the idea that justice is a human invention and argues instead that justice provides independent and eternal standards"
    },
    {
     "article_id": "moral-non-naturalism",
     "quote": "Ross, W.D., 1930. The Right and The Good"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "a_theory_of_justice",
   "target": "john_rawls",
   "type": "AUTHORED_BY",
   "weight": 0.984375,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "consequentialism",
     "quote": "Rawls 1971"
    },
    {
     "article_id": "contractualism",
     "quote": "Derek Parfit argues that, despite their differences, contractualism does coincide with the best interpretation of Kant’s moral theory."
    },
    {
     "article_id": "mill-moral-political",
     "quote": "Rawls (1971) has argued that the sort of interpersonal sacrifice that utilitarianism requires violates the strains of commitment in a well-ordered society."
    },
    {
     "article_id": "moral-anti-realism",
     "quote": "Rawls, J., 1971. A Theory of Justice, Cambridge, MA.: Belknap Press."
    },
    {
     "article_id": "moral-luck",
     "quote": "Rawls writes that The existing distribution of income and wealth, say, is the cumulative effect of prior distributions of natural assets—that is, natural talents and abilities"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "after_virtue",
   "target": "alasdair_macintyre",
   "type": "AUTHORED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-anti-realism",
     "quote": "MacIntyre, A., 1984. After Virtue, Indiana: University of Notre Dame Press."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "reasons_and_persons",
   "target": "derek_parfit",
   "type": "AUTHORED_BY",
   "weight": 0.9375,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "consequentialism",
     "quote": "Parfit 1984"
    },
    {
     "article_id": "egoism",
     "quote": "Parfit 1984 pts. II-III"
    },
    {
     "article_id": "practical-reason",
     "quote": "Parfit, Derek, 1984, Reasons and Persons, Oxford: Clarendon Press."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "what_we_owe_to_each_other",
   "target": "t_m_scanlon",
   "type": "AUTHORED_BY",
   "weight": 0.96875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "contractualism",
     "quote": "Scanlon introduces contractualism as a distinctive account of moral reasoning."
    },
    {
     "article_id": "intuitionism-ethics",
     "quote": "T. M. Scanlon has argued that goodness is to be understood as something’s having properties that give us reason to have a pro-attitude towards it (1998, 95)"
    },
    {
     "article_id": "moral-responsibility",
     "quote": "Scanlon (1998, 2008)"
    },
    {
     "article_id": "practical-reason",
     "quote": "Scanlon, Thomas M., 1998, What We Owe to Each Other, Cambridge, Mass.: Harvard University Press."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "on_the_genealogy_of_morality",
   "target": "friedrich_nietzsche",
   "type": "AUTHORED_BY",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-virtue",
     "quote": "On the Genealogy of Morality"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "modern_moral_philosophy",
   "target": "elizabeth_anscombe",
   "type": "AUTHORED_BY",
   "weight": 0.9375,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-virtue",
     "quote": "It was heralded by Anscombe’s famous article “Modern Moral Philosophy” (Anscombe 1958)"
    },
    {
     "article_id": "moral-anti-realism",
     "quote": "Anscombe, G.E.M., 1958. “Modern moral philosophy,” Philosophy, 33: 1–19."
    },
    {
     "article_id": "natural-law-ethics",
     "quote": "Anscombe, G. E. M., 1958, “Modern Moral Philosophy,” Philosophy, 33: 1–19."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "categorical_imperative",
   "target": "groundwork_metaphysics_of_morals",
   "type": "INTRODUCED_IN",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "good_will",
   "target": "groundwork_metaphysics_of_morals",
   "type": "INTRODUCED_IN",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-luck",
     "quote": "Inspired by the work of John Rawls, some egalitarians have invoked the idea that our constitution and circumstances are out of our control"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "kingdom_of_ends",
   "target": "groundwork_metaphysics_of_morals",
   "type": "INTRODUCED_IN",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "greatest_happiness_principle",
   "target": "principles_of_morals_and_legislation",
   "type": "INTRODUCED_IN",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "bentham",
     "quote": "In the Fragment Bentham stated the “fundamental axiom” that “it is the greatest happiness of the greatest number that is the measure of right and wrong”, and “the obligation to minister to general happiness, was an obligation paramount to and inclusive of every other” (1776 [1977, 393, 440n])."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "golden_mean",
   "target": "nicomachean_ethics",
   "type": "INTRODUCED_IN",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "open_question_argument",
   "target": "principia_ethica",
   "type": "INTRODUCED_IN",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "moral-cognitivism",
     "quote": "At the beginning of the 20th Century, G. E. Moore’s open question argument convinced many philosophers that moral statements were not equivalent to statements made using non-moral or descriptive terms."
    },
    {
     "article_id": "naturalism-moral",
     "quote": "with G.E. Moore’s Principia Ethica"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "naturalistic_fallacy",
   "target": "principia_ethica",
   "type": "INTRODUCED_IN",
   "weight": 0.984375,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "intuitionism-ethics",
     "quote": "Moore is the intuitionist who laid most stress on the non-natural nature of moral properties, though his focus was on goodness rather than rightness. In Principia Ethica Moore defines a natural property"
    },
    {
     "article_id": "moral-cognitivism",
     "quote": "At the beginning of the 20th Century, G. E. Moore’s open question argument convinced many philosophers that moral statements were not equivalent to statements made using non-moral or descriptive terms."
    },
    {
     "article_id": "moral-non-naturalism",
     "quote": "Moore famously claimed that naturalists were guilty of what he called the “naturalistic fallacy.”"
    },
    {
     "article_id": "naturalism-moral",
     "quote": "with G.E. Moore’s Principia Ethica"
    },
    {
     "article_id": "utilitarianism-history",
     "quote": "G. E. Moore (1873–1958) criticized this as fallacious. He argued that it rested on an obvious ambiguity: Mill has made as naïve and artless a use of the naturalistic fallacy as anybody could desire."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "is_ought_problem",
   "target": "treatise_of_human_nature",
   "type": "INTRODUCED_IN",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "prima_facie_duty",
   "target": "the_right_and_the_good",
   "type": "INTRODUCED_IN",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "intuitionism-ethics",
     "quote": "“[T]he moral convictions of thoughtful and well-educated people are the data of ethics, just as sense-perceptions are the data of natural science” (1930/2002, 41)"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "consequentialism",
   "target": "modern_moral_philosophy",
   "type": "INTRODUCED_IN",
   "weight": 0.75,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "ethics-virtue",
     "quote": "It was heralded by Anscombe’s famous article “Modern Moral Philosophy” (Anscombe 1958) which crystallized an increasing dissatisfaction with the forms of deontology and utilitarianism then prevailing."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "after_virtue",
   "target": "emotivism",
   "type": "CRITIQUES",
   "weight": 0.5,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [],
   "status": "unverified"
  },
  {
   "source": "modern_moral_philosophy",
   "target": "consequentialism",
   "type": "CRITIQUES",
   "weight": 0.9375,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "consequentialism",
     "quote": "Mill 1861"
    },
    {
     "article_id": "ethics-deontological",
     "quote": "consequentialists generally agree that the Good is “agent-neutral” (Parfit 1984; Nagel 1986)"
    },
    {
     "article_id": "ethics-virtue",
     "quote": "It was heralded by Anscombe’s famous article “Modern Moral Philosophy” (Anscombe 1958) which crystallized an increasing dissatisfaction with the forms of deontology and utilitarianism then prevailing."
    }
   ],
   "status": "grounded"
  },
  {
   "source": "a_theory_of_justice",
   "target": "utilitarianism",
   "type": "RESPONDS_TO",
   "weight": 0.875,
   "origin": "backbone",
   "extractor": {
    "model": "claude-fable-5",
    "prompt_version": "bb-v1",
    "date": "2026-06-11"
   },
   "evidence": [
    {
     "article_id": "consequentialism",
     "quote": "Sidgwick 1907"
    },
    {
     "article_id": "ethics-deontological",
     "quote": "Rawls 1971"
    }
   ],
   "status": "grounded"
  },
  {
   "source": "friedrich_nietzsche",
   "target": "utilitarianism",
   "type": "CRITIQUES",
   "weight": 0.5,
   "origin": "research",
   "extractor": {
    "model": "claude-haiku-4-5",
    "prompt_version": "rs-v1",
    "date": "2026-06-22"
   },
   "evidence": [
    {
     "article_id": "nietzsche",
     "quote": "He is famous for uncompromising criticisms of traditional European morality and religion, as well as of conventional philosophical ideas and social and political pieties associated with modernity"
    }
   ],
   "status": "unverified"
  },
  {
   "source": "friedrich_nietzsche",
   "target": "divine_command_theory",
   "type": "CRITIQUES",
   "weight": 0.5,
   "origin": "research",
   "extractor": {
    "model": "claude-haiku-4-5",
    "prompt_version": "rs-v1",
    "date": "2026-06-22"
   },
   "evidence": [
    {
     "article_id": "nietzsche",
     "quote": "famous for uncompromising criticisms of traditional European morality and religion, as well as of conventional philosophical ideas"
    }
   ],
   "status": "unverified"
  },
  {
   "source": "master_morality",
   "target": "slave_revolt_in_morality",
   "type": "CONTRASTS_WITH",
   "weight": 0.5,
   "origin": "research",
   "extractor": {
    "model": "claude-haiku-4-5",
    "prompt_version": "rs-v1",
    "date": "2026-06-22"
   },
   "evidence": [
    {
     "article_id": "nietzsche",
     "quote": "The contrast, together with the prior dominance of good/bad structured moralities, raises a straightforward historical question: what happened? How did we get from the widespread acceptance of good/bad valuation to the near universal dominance of good/evil thinking?"
    }
   ],
   "status": "unverified"
  }
 ],
 "articles": [
  {
   "id": "aristotle-ethics",
   "title": "ethics",
   "url": "https://plato.stanford.edu/entries/aristotle-ethics/",
   "retrieved": "2026-06-12",
   "grounded_edges": 4,
   "proposed_edges": 1
  },
  {
   "id": "bentham",
   "title": "Bentham, Jeremy",
   "url": "https://plato.stanford.edu/entries/bentham/",
   "retrieved": "2026-06-12",
   "grounded_edges": 7,
   "proposed_edges": 1
  },
  {
   "id": "consequentialism",
   "title": "consequentialism",
   "url": "https://plato.stanford.edu/entries/consequentialism/",
   "retrieved": "2026-06-12",
   "grounded_edges": 14,
   "proposed_edges": 0
  },
  {
   "id": "contractarianism",
   "title": "contractarianism",
   "url": "https://plato.stanford.edu/entries/contractarianism/",
   "retrieved": "2026-06-12",
   "grounded_edges": 3,
   "proposed_edges": 3
  },
  {
   "id": "contractualism",
   "title": "contractualism",
   "url": "https://plato.stanford.edu/entries/contractualism/",
   "retrieved": "2026-06-12",
   "grounded_edges": 2,
   "proposed_edges": 1
  },
  {
   "id": "double-effect",
   "title": "double effect, doctrine of",
   "url": "https://plato.stanford.edu/entries/double-effect/",
   "retrieved": "2026-06-12",
   "grounded_edges": 1,
   "proposed_edges": 4
  },
  {
   "id": "egoism",
   "title": "egoism",
   "url": "https://plato.stanford.edu/entries/egoism/",
   "retrieved": "2026-06-12",
   "grounded_edges": 5,
   "proposed_edges": 1
  },
  {
   "id": "ethics-deontological",
   "title": "ethics: deontological",
   "url": "https://plato.stanford.edu/entries/ethics-deontological/",
   "retrieved": "2026-06-12",
   "grounded_edges": 12,
   "proposed_edges": 2
  },
  {
   "id": "ethics-virtue",
   "title": "virtue",
   "url": "https://plato.stanford.edu/entries/ethics-virtue/",
   "retrieved": "2026-06-12",
   "grounded_edges": 25,
   "proposed_edges": 1
  },
  {
   "id": "feminism-ethics",
   "title": "feminist philosophy, interventions: ethics",
   "url": "https://plato.stanford.edu/entries/feminism-ethics/",
   "retrieved": "2026-06-12",
   "grounded_edges": 3,
   "proposed_edges": 0
  },
  {
   "id": "hedonism",
   "title": "hedonism",
   "url": "https://plato.stanford.edu/entries/hedonism/",
   "retrieved": "2026-06-12",
   "grounded_edges": 6,
   "proposed_edges": 3
  },
  {
   "id": "hume-moral",
   "title": "moral philosophy",
   "url": "https://plato.stanford.edu/entries/hume-moral/",
   "retrieved": "2026-06-12",
   "grounded_edges": 4,
   "proposed_edges": 1
  },
  {
   "id": "intuitionism-ethics",
   "title": "moral intuitionism",
   "url": "https://plato.stanford.edu/entries/intuitionism-ethics/",
   "retrieved": "2026-06-12",
   "grounded_edges": 11,
   "proposed_edges": 1
  },
  {
   "id": "kant-hume-morality",
   "title": "Kant, Immanuel: and Hume on morality",
   "url": "https://plato.stanford.edu/entries/kant-hume-morality/",
   "retrieved": "2026-06-12",
   "grounded_edges": 10,
   "proposed_edges": 4
  },
  {
   "id": "kant-moral",
   "title": "moral philosophy",
   "url": "https://plato.stanford.edu/entries/kant-moral/",
   "retrieved": "2026-06-12",
   "grounded_edges": 8,
   "proposed_edges": 2
  },
  {
   "id": "metaethics",
   "title": "metaethics",
   "url": "https://plato.stanford.edu/entries/metaethics/",
   "retrieved": "2026-06-12",
   "grounded_edges": 12,
   "proposed_edges": 2
  },
  {
   "id": "mill-moral-political",
   "title": "moral and political philosophy",
   "url": "https://plato.stanford.edu/entries/mill-moral-political/",
   "retrieved": "2026-06-12",
   "grounded_edges": 10,
   "proposed_edges": 0
  },
  {
   "id": "moral-anti-realism",
   "title": "moral anti-realism",
   "url": "https://plato.stanford.edu/entries/moral-anti-realism/",
   "retrieved": "2026-06-12",
   "grounded_edges": 16,
   "proposed_edges": 3
  },
  {
   "id": "moral-cognitivism",
   "title": "cognitivism vs. non-cognitivism, moral",
   "url": "https://plato.stanford.edu/entries/moral-cognitivism/",
   "retrieved": "2026-06-12",
   "grounded_edges": 11,
   "proposed_edges": 2
  },
  {
   "id": "moral-luck",
   "title": "moral",
   "url": "https://plato.stanford.edu/entries/moral-luck/",
   "retrieved": "2026-06-12",
   "grounded_edges": 4,
   "proposed_edges": 1
  },
  {
   "id": "moral-non-naturalism",
   "title": "moral non-naturalism",
   "url": "https://plato.stanford.edu/entries/moral-non-naturalism/",
   "retrieved": "2026-06-12",
   "grounded_edges": 13,
   "proposed_edges": 1
  },
  {
   "id": "moral-realism",
   "title": "moral realism",
   "url": "https://plato.stanford.edu/entries/moral-realism/",
   "retrieved": "2026-06-12",
   "grounded_edges": 10,
   "proposed_edges": 3
  },
  {
   "id": "moral-relativism",
   "title": "moral relativism",
   "url": "https://plato.stanford.edu/entries/moral-relativism/",
   "retrieved": "2026-06-12",
   "grounded_edges": 6,
   "proposed_edges": 2
  },
  {
   "id": "moral-responsibility",
   "title": "moral responsibility",
   "url": "https://plato.stanford.edu/entries/moral-responsibility/",
   "retrieved": "2026-06-12",
   "grounded_edges": 5,
   "proposed_edges": 0
  },
  {
   "id": "moral-sentimentalism",
   "title": "moral sentimentalism",
   "url": "https://plato.stanford.edu/entries/moral-sentimentalism/",
   "retrieved": "2026-06-12",
   "grounded_edges": 4,
   "proposed_edges": 0
  },
  {
   "id": "natural-law-ethics",
   "title": "natural law tradition",
   "url": "https://plato.stanford.edu/entries/natural-law-ethics/",
   "retrieved": "2026-06-12",
   "grounded_edges": 5,
   "proposed_edges": 3
  },
  {
   "id": "naturalism-moral",
   "title": "naturalism: moral",
   "url": "https://plato.stanford.edu/entries/naturalism-moral/",
   "retrieved": "2026-06-12",
   "grounded_edges": 4,
   "proposed_edges": 1
  },
  {
   "id": "practical-reason",
   "title": "practical reason",
   "url": "https://plato.stanford.edu/entries/practical-reason/",
   "retrieved": "2026-06-12",
   "grounded_edges": 5,
   "proposed_edges": 0
  },
  {
   "id": "supererogation",
   "title": "supererogation",
   "url": "https://plato.stanford.edu/entries/supererogation/",
   "retrieved": "2026-06-12",
   "grounded_edges": 1,
   "proposed_edges": 0
  },
  {
   "id": "utilitarianism-history",
   "title": "history of",
   "url": "https://plato.stanford.edu/entries/utilitarianism-history/",
   "retrieved": "2026-06-12",
   "grounded_edges": 16,
   "proposed_edges": 1
  },
  {
   "id": "nietzsche",
   "title": "Nietzsche, Friedrich",
   "url": "https://plato.stanford.edu/entries/nietzsche/",
   "retrieved": "2026-06-22",
   "grounded_edges": 3,
   "proposed_edges": 0
  }
 ]
};
