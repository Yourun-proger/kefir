from kefir import Kefir, Repr


class TestKefirRepr:
    def test_repr(self):
        class A:
            def __init__(self, some_attr):
                self.attr = some_attr

        class B:
            def __init__(self, some_id, some_attr, some_a_object, unused=None):
                self.id = some_id
                self.attr = some_attr
                self.a_object = some_a_object
                self.unused = unused

        class BRepr(Repr):
            ignore = ["unused"]
            names_map = {"a_object": "a_obj"}
            look = ["a_obj"]
            validate = ["attr"]

            def look_a_obj(a_obj):
                return {
                    "first": a_obj["attr"].partition(" ")[0],
                    "second": a_obj["attr"].partition(" ")[2],
                }

            def validate_attr(attr):
                assert "kef" in attr, "WHY?"

        kef = Kefir(represents={B: BRepr})

        a_object = A("kefir project")
        b_object = B(42, "ke", a_object)
        # due to the fact that the pytest conjures with everything the assertion that it sees,
        # I had to add one stupid thing to the assertion below.
        assert kef.dump(b_object) == {
            "id": 42,
            "attr": "WHY?\nassert 'kef' in 'ke'",
            "a_obj": {"first": "kefir", "second": "project"},
        }
