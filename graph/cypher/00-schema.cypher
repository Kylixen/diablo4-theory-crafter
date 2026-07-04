// Ontology v0.1 — constraints. See ../ontology.md
CREATE CONSTRAINT class_sno IF NOT EXISTS
FOR (c:Class) REQUIRE c.snoId IS UNIQUE;

CREATE CONSTRAINT skill_sno IF NOT EXISTS
FOR (s:Skill) REQUIRE s.snoId IS UNIQUE;

CREATE CONSTRAINT skill_category_name IF NOT EXISTS
FOR (sc:SkillCategory) REQUIRE sc.name IS UNIQUE;

CREATE CONSTRAINT tag_name IF NOT EXISTS
FOR (t:Tag) REQUIRE t.name IS UNIQUE;
