"""Historical Generic Space Memory v0.9: source-grounding and no-proof checks."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
MEMORY=ROOT/"graph"/"generic_space_memory_v0_9.json"

class GenericMemoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.memory=json.loads(MEMORY.read_text(encoding="utf-8"))
        cls.entries=cls.memory["entries"]
        cls.catalog={x["id"]:x for x in json.loads((ROOT/"data"/"propositions.json").read_text(encoding="utf-8"))}

    def test_grounded_source_file_and_source_identity(self):
        for entry in self.entries:
            p=entry["provenance"]
            path=ROOT.parent/p["file"].replace("NMerovingio/","NMerovingio/")
            self.assertTrue(path.is_file(),entry["id"])
            self.assertIn(p["file"],[s["path"] for s in self.memory["sources"]])
            if entry["kind"]=="workspace_abstraction":
                raw=json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(p["workspace_id"],raw["workspace"]["id"])
                ids={node["id"] for node in raw["nodes"]}
                self.assertTrue(p["node_ids"])
                self.assertTrue(set(p["node_ids"])<=ids,entry["id"])
                for role in entry["abstract_roles"]:
                    self.assertTrue(set(role["source_objects"])<=ids,entry["id"])
            else:
                self.assertEqual(p["workspace_id"],None)
                prop=self.catalog[p["proposition_id"]]
                self.assertEqual(entry["abstract_roles"][0]["source_objects"],prop["preconditions"])
                self.assertEqual(entry["abstract_roles"][1]["source_objects"],prop["effect"])

    def test_counts_and_nondestructive_genealogies(self):
        self.assertEqual(len(self.entries),10)
        self.assertEqual(sum(x["kind"]=="workspace_abstraction" for x in self.entries),5)
        self.assertEqual(sum(x["kind"]=="proposition_catalog_pattern" for x in self.entries),5)
        self.assertEqual(len({x["id"] for x in self.entries}),len(self.entries))
        self.assertTrue(all(x["conservation"] for x in self.entries))
        self.assertTrue(all(x["interpretation"] for x in self.entries))
        sources={x["provenance"]["file"] for x in self.entries}
        self.assertEqual(len(sources),5)

    def test_not_claiming_proofs(self):
        for e in self.entries:
            self.assertNotEqual(e["metric_status"],"proven")
            self.assertNotEqual(e["interpretation"],"verified_theorem")
            self.assertEqual(e["memory_status"],"retrievable_template")
            if e["kind"]=="proposition_catalog_pattern":
                self.assertEqual(e["provenance"]["status"],"catalogued_rule_only_not_workspace_proof")
                self.assertIn("requires_independent_proof",e["metric_status"])
            if e["kind"]=="workspace_abstraction":
                self.assertEqual(e["provenance"]["status"],"source_observed_structural_pattern")

    def test_negative_workspace_has_no_fabricated_node_ids(self):
        all_source_nodes=set()
        for s in self.memory["sources"]:
            if s["source_kind"]=="workspace_example":
                raw=json.loads((ROOT.parent/s["path"]).read_text(encoding="utf-8"))
                all_source_nodes.update(x["id"] for x in raw["nodes"])
        for e in self.entries:
            if e["kind"]=="workspace_abstraction":
                self.assertTrue(set(e["provenance"]["node_ids"])<=all_source_nodes)
        self.assertFalse(any(e["provenance"]["proposition_id"]=="I.10" for e in self.entries))

    def test_workspace_signatures_without_duplicates(self):
        signature_pairs=[(x["provenance"]["file"],tuple(sorted(x["tags"]))) for x in self.entries]
        self.assertEqual(len(signature_pairs),len(set(signature_pairs)))
        self.assertTrue(any("multi_role_carrier" in x["tags"] for x in self.entries))
        self.assertTrue(any("different_genealogy" in x["tags"] for x in self.entries))

if __name__=="__main__":
    unittest.main()
